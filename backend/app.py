from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
from newsapi import NewsApiClient
from risk_calculations import calculate_var, calculate_sharpe_ratio, calculate_beta
from ml_model import predict_risk
from database import create_tables, add_portfolio, get_portfolio
import sys
import os
from risk_calculations import monte_carlo_simulation
from risk_calculations import calculate_var, calculate_cvar
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)
CORS(app)

# Replace with your NewsAPI Key
NEWS_API_KEY = "b1b4f8833cbf4ae9a21828d67ac2a007"
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def get_stock_news(ticker):
    """Fetch latest news for a stock ticker"""
    try:
        articles = newsapi.get_everything(q=ticker, language="en", sort_by="publishedAt")["articles"]
        top_articles = [{"title": a["title"], "url": a["url"]} for a in articles[:3]]  # Get top 3 news
        return top_articles
    except Exception as e:
        return f"Error fetching news: {str(e)}"

def get_technical_indicators(ticker):
    """Fetch stock price and technical indicators"""
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")["Close"]

    if len(hist) < 20:
        return {"Error": "Not enough historical data for indicators"}

    # Calculate Moving Averages
    moving_avg_20 = hist.rolling(window=20).mean().iloc[-1]
    moving_avg_50 = hist.rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else None

    # Calculate RSI (Relative Strength Index)
    delta = hist.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs)).iloc[-1]

    return {
        "Stock Price": hist.iloc[-1],
        "20-day Moving Avg": moving_avg_20,
        "50-day Moving Avg": moving_avg_50,
        "RSI": rsi
    }

@app.route("/predict-risk", methods=["POST"])
def get_risk():
    try:
        data = request.get_json()
        ticker = data.get("ticker", "").upper()

        # Get stock indicators
        indicators = get_technical_indicators(ticker)

        if "Error" in indicators:
            return jsonify({"error": indicators["Error"]}), 400

        # Get risk score from ML model
        risk_score = predict_risk(ticker)

        # Get financial news
        news = get_stock_news(ticker)

        return jsonify({
            "Stock Price": indicators["Stock Price"],
            "Risk Score": risk_score,
            "Moving Avg (20-day)": indicators["20-day Moving Avg"],
            "Moving Avg (50-day)": indicators["50-day Moving Avg"],
            "RSI": indicators["RSI"],
            "News": news
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/stock/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    return jsonify(hist['Close'].to_dict())

@app.route('/var/<ticker>', methods=['GET'])
def get_var(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")['Close']
    var = calculate_var(hist)
    return jsonify({"VaR": var})

@app.route('/sharpe/<ticker>', methods=['GET'])
def get_sharpe(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")['Close']
    sharpe = calculate_sharpe_ratio(hist)
    return jsonify({"Sharpe Ratio": sharpe})

@app.route('/beta', methods=['POST'])
def get_beta():
    data = request.json
    stock_ticker = data['stock']
    market_ticker = data['market']
    beta = calculate_beta(stock_ticker, market_ticker)
    return jsonify({"Beta": beta})

@app.route('/portfolio', methods=['POST'])
def add_to_portfolio():
    """API to add a stock to the user's portfolio"""
    data = request.json
    add_portfolio(data['user_id'], data['ticker'], data['quantity'])
    return jsonify({"message": "Portfolio updated successfully"})

@app.route('/portfolio/<user_id>', methods=['GET'])
def get_user_portfolio(user_id):
    """API to fetch the user's portfolio"""
    portfolio = get_portfolio(user_id)
    return jsonify({"portfolio": portfolio})

@app.route('/monte-carlo', methods=['POST'])
def get_monte_carlo():
    """API endpoint to run Monte Carlo Simulation for stock price prediction."""
    try:
        data = request.get_json()
        ticker = data.get("ticker", "").upper()
        days = data.get("days", 30)  # Default to 30 days

        result = monte_carlo_simulation(ticker, days)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 

@app.route('/calculate-var', methods=['POST'])
def calculate_var_route():
    """API endpoint to calculate Value at Risk (VaR)"""
    try:
        data = request.get_json()
        ticker = data.get("ticker", "").upper()
        confidence = data.get("confidence", 0.95)

        result = calculate_var(ticker, confidence)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/calculate-cvar', methods=['POST'])
def calculate_cvar_route():
    """API endpoint to calculate Conditional Value at Risk (CVaR)"""
    try:
        data = request.get_json()
        ticker = data.get("ticker", "").upper()
        confidence = data.get("confidence", 0.95)

        result = calculate_cvar(ticker, confidence)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
