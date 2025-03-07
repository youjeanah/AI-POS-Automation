# 🍔 AI-POS-Automation (AI 기반 맥도날드 POS 시스템)
이 프로젝트는 **음성 인식 기반의 AI-POS 시스템**으로,  
**OpenAI Whisper**를 활용하여 고객의 음성을 텍스트로 변환하고,  
React 기반의 UI를 통해 주문을 관리할 수 있도록 설계되었습니다.

🎤 사용 방법  
	1.	“Start Voice Order” 버튼을 클릭한 후, 주문을 음성으로 말하세요. 실시간 음성 감지 후 녹음이 시작되고, 2초간 조용한 상태가 지속되면 자동으로 녹음 종료됩니다.  
	2.	또는, 녹음된 음성 파일을 업로드하여 주문을 입력할 수도 있습니다. (샘플 오디오 파일: sample-audio/trimmed_sample_audio.wav)  
	3.	AI가 인식한 메뉴 항목이 강조 표시되고 주문 목록에 자동 추가됩니다.  


---

## 🚀 **프로젝트 실행 방법**
이 프로젝트는 **백엔드(Flask)** 와 **프론트엔드(Vite)** 로 구성되어 있습니다.  
아래 단계를 따라 백엔드와 프론트엔드를 실행하세요.

---

## **🔹 1️⃣ 프로젝트 다운로드 (Git Clone)**
먼저 GitHub에서 프로젝트를 클론합니다.
```sh
git clone git@github.com:youjeanah/AI-POS-Automation.git
cd AI-POS-Automation
```

    
## **🔹 2️⃣ 백엔드(Flask) 실행 방법**

백엔드는 Flask와 OpenAI Whisper를 사용하며, Python 가상환경에서 실행됩니다.

📌 1. 백엔드 폴더로 이동하고 가상환경 생성
```sh
cd backend
python3 -m venv venv
source venv/bin/activate  # (Mac/Linux)
```  
📌 2. 필요한 패키지 설치 (requirements.txt 사용)
```sh
pip install -r requirements.txt
```

📌 3. 백엔드 서버 실행
```sh
python app.py
```
✅ 백엔드 서버가 실행되면 http://127.0.0.1:5000/에서 확인할 수 있습니다.

  
## 🔹 3️⃣ 프론트엔드(Vite) 실행 방법

Vite 기반의 React 프론트엔드를 실행합니다.

📌 1. 프론트엔드 폴더로 이동
```sh
cd frontend
```

📌 2. 필요한 패키지 설치 (package.json 사용)
```sh
npm install
```

📌 3. 프론트엔드 서버 실행
```sh
npm run dev
```

✅ 프론트엔드는 http://localhost:5173/에서 실행됩니다.
브라우저에서 해당 주소를 열어 UI를 확인하세요.

 
