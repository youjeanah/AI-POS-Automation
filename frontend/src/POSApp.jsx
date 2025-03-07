import React, { useState, useEffect } from "react";
import "./POSApp.css"; // 스타일 적용

const POSApp = () => {
  const [menuItems, setMenuItems] = useState([
    { name: "Big Mac", category: "burger" },
    { name: "Quarter Pounder", category: "burger" },
    { name: "McNuggets", category: "chicken" },
    { name: "French Fries", category: "sides" },
    { name: "Coke", category: "drinks" },
    { name: "Sprite", category: "drinks" },
  ]);

  const [selectedItems, setSelectedItems] = useState([]);
  const [highlightedItems, setHighlightedItems] = useState([]);
  const [loading, setLoading] = useState(false);

  // 음성 인식 후 주문된 메뉴 반영
  const handleVoiceOrder = () => {
    setLoading(true);

    fetch("http://127.0.0.1:5000/get-menu")
      .then((res) => res.json())
      .then((data) => {
        setHighlightedItems(data.menu);
        setSelectedItems((prev) => [...prev, ...data.menu]);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching menu:", error);
        setLoading(false);
      });
  };

  // 파일 업로드 처리
  const handleFileUpload = (event) => {
    setLoading(true);
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:5000/upload-audio", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        setHighlightedItems(data.menu);
        setSelectedItems((prev) => [...prev, ...data.menu]);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        setLoading(false);
      });
  };

  return (
    <div className="pos-container">
      {/* 좌측 POS 버튼 패널 */}
      <div className="menu-panel">
        <h2>🍔 McDonald's POS</h2>

        {/* 메뉴 버튼 */}
        <div className="menu-grid">
          {/* First row: Number buttons 0-9 */}
          {Array.from({ length: 10 }, (_, index) => (
            <button key={`num-${index}`} className="menu-button num-button">
              {index}
            </button>
          ))}

          {/* Second row: Size buttons */}
          <div className="size-row">
            {["S", "M", "L", "XL"].map((size, index) => (
              <button key={`size-${index}`} className="menu-button size-button">
                {size}
              </button>
            ))}
          </div>

          {/* Third row onward: Menu items */}
          {menuItems.map((item, index) => (
            <button
              key={`menu-${index}`}
              className={`menu-button ${
                highlightedItems.includes(item.name) ? "highlight" : ""
              }`}
            >
              {item.name}
            </button>
          ))}
        </div>

        {/* 컨트롤 버튼 */}
        <div className="controls">
          <button onClick={handleVoiceOrder} className="voice-btn">
            🎙 Start Voice Order
          </button>
          <input
            type="file"
            onChange={handleFileUpload}
            className="file-input"
          />
        </div>
      </div>
      
      {/* 우측 주문 내역 패널 */}
      <div className="order-panel">
        <h2>📝 Order Summary</h2>
        {selectedItems.length > 0 ? (
          selectedItems.map((item, index) => (
            <p key={index} className="order-item">
              {item}
            </p>
          ))
        ) : (
          <p>No items ordered yet.</p>
        )}
      </div>
    </div>
  );
};

export default POSApp;
