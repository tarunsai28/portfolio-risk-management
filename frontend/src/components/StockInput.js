import React, { useState } from "react";
import "./StockInput.css"; // optional external styling

const StockInput = ({ onFetchRisk }) => {
  const [ticker, setTicker] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (ticker.trim() === "") return;
    onFetchRisk(ticker.toUpperCase());
  };

  return (
    <div className="input-container">
      <form onSubmit={handleSubmit} className="stock-form">
        <input
          type="text"
          placeholder="Enter Stock Ticker (e.g., AAPL)"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
        />
        <button type="submit">Get Risk Score</button>
      </form>
    </div>
  );
};

export default StockInput;
