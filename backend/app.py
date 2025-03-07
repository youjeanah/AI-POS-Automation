from flask import Flask, jsonify, request
from flask_cors import CORS
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time
import os

app = Flask(__name__)
CORS(app)

# Whisper 모델 로드
model = whisper.load_model("small")

# 메뉴 리스트
MENU_ITEMS = {
    "Big Mac": ["big mac combo", "medium big mac"],
    "Medium" : ["medium", "Medium"],
    "Small" : ["small", "Small"],
    "Large" : ["large", "Large"],
    "Chicken McNuggets Combo": ["chicken mcnuggets", "nuggets", "nugget"],
    "Dr. Pepper": ["dr. pepper"],
    "Sprite": ["sprite"],
    "Honey Mustard": ["honey mustard"]
}

# 최종 주문 저장
final_order = {"menu": []}

SAMPLE_RATE = 16000  # 샘플 레이트
THRESHOLD = 0.02  # 음성 감지 임계값 (작은 값일수록 작은 소리도 감지)
SILENCE_DURATION = 2.0  # 조용한 상태가 지속되면 녹음 종료 (초 단위)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 업로드 폴더 자동 생성


def detect_voice():
    """실시간 음성 감지 후 녹음 시작 & 종료"""
    print("🎙 음성을 감지하는 중... (말하면 녹음 시작)")

    recording = []
    silent_time = 0
    recording_started = False

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype=np.float32) as stream:
        start_time = time.time()

        while True:
            audio_chunk, _ = stream.read(int(SAMPLE_RATE * 0.1))  # 0.1초 단위로 샘플 읽기
            volume = np.max(np.abs(audio_chunk))  # 음성의 최대 볼륨 값 계산

            if volume > THRESHOLD:  # 소리가 일정 크기 이상이면 녹음 시작
                recording.append(audio_chunk)
                silent_time = 0
                if not recording_started:
                    print("🔴 녹음 시작!")
                    recording_started = True
            else:
                if recording_started:
                    silent_time += 0.1  # 0.1초 단위로 증가

            if recording_started and silent_time > SILENCE_DURATION:
                print("✅ 녹음 종료! (조용한 상태가 지속됨)")
                break

    # 녹음된 데이터 합치기
    recorded_audio = np.concatenate(recording, axis=0)

    # WAV 파일로 저장
    wav_file = "recorded_audio.wav"
    wav.write(wav_file, SAMPLE_RATE, (recorded_audio * 32767).astype(np.int16))  # 16-bit PCM 변환
    return wav_file


def extract_order(text):
    """음성 인식 결과에서 메뉴 추출"""
    order = {"menu": []}
    for menu, keywords in MENU_ITEMS.items():
        if any(keyword in text.lower() for keyword in keywords):
            order["menu"].append(menu)
    return order


@app.route("/get-menu", methods=["GET"])
def get_menu():
    """음성 인식 후 감지된 메뉴 반환"""
    audio_path = detect_voice()
    result = model.transcribe(audio_path, language="en")
    extracted_menu = extract_order(result["text"])

    # 하이라이트 & 주문 내역을 위해 메뉴 리스트 반환
    return jsonify({"menu": extracted_menu["menu"]})


@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    """사용자가 업로드한 오디오 파일을 분석하여 메뉴 반환"""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # 파일 저장
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Whisper로 변환
    result = model.transcribe(file_path, language="en")
    extracted_menu = extract_order(result["text"])

    return jsonify({"menu": extracted_menu["menu"]})


if __name__ == "__main__":
    app.run(debug=True)