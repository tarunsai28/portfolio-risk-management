# 📈 Portfolio Risk Management

A predictive analytics dashboard for assessing portfolio risk using real-time stock data, technical indicators, and machine learning. This platform helps investors and analysts evaluate potential financial risks, visualize trends, and make informed decisions.

---

## 🚀 Features

- 🔍 Real-time stock data integration via Yahoo Finance
- 🤖 LSTM-based ML model for risk score prediction
- 📉 Value at Risk (VaR) & Conditional VaR (CVaR) calculation
- 📊 Monte Carlo simulation for future stock forecasting
- 📰 Live financial news for each stock
- 💡 Interactive React.js dashboard with risk trends, RSI, and moving averages

---

## 🧠 Tech Stack

- **Backend:** Python, Flask, TensorFlow, yFinance, NewsAPI
- **Frontend:** React.js, Axios, Recharts, Bootstrap
- **Database:** MySQL
- **Machine Learning:** LSTM (Keras)
- **Simulation:** Monte Carlo, VaR, CVaR

---

## 🛠️ Getting Started

### 🔧 Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # On Windows
# source venv/bin/activate   # On macOS/Linux
pip install -r requirements.txt
python app.py
💻 Frontend Setup
bash
Copy
Edit
cd frontend
npm install
npm start
📡 API Endpoints

Endpoint	Method	Description
/predict-risk	POST	Predicts risk score for a stock
/monte-carlo	POST	Returns price simulation
/calculate-var	POST	Computes Value at Risk
/calculate-cvar	POST	Computes Conditional VaR
/portfolio	POST	Add a stock to portfolio
/portfolio/<user_id>	GET	Fetch user portfolio
🧪 Sample Prediction Output
json
Copy
Edit
{
  "Stock Price": 193.16,
  "Risk Score": -0.15208,
  "Moving Avg (20-day)": 204.94,
  "Moving Avg (50-day)": 221.01,
  "RSI": 37.40,
  "News": [
    { "title": "Apple hits record high", "url": "https://example.com" }
  ]
}
📷 Screenshots
Add screenshots of your React dashboard UI here to visually impress visitors

📘 License
Licensed under the MIT License.