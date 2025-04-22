import matplotlib
matplotlib.use('Agg') 
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def calculate_var(prices, confidence_level=0.95):
    returns = prices.pct_change().dropna()
    var = np.percentile(returns, (1 - confidence_level) * 100)
    return var

def calculate_sharpe_ratio(prices, risk_free_rate=0.02):
    returns = prices.pct_change().dropna()
    excess_returns = returns - risk_free_rate / 252
    sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns)
    return sharpe_ratio

def calculate_beta(stock_ticker, market_ticker):
    stock = yf.Ticker(stock_ticker).history(period="1y")['Close']
    market = yf.Ticker(market_ticker).history(period="1y")['Close']
    stock_returns = stock.pct_change().dropna()
    market_returns = market.pct_change().dropna()
    covariance = np.cov(stock_returns, market_returns)[0, 1]
    market_variance = np.var(market_returns)
    beta = covariance / market_variance
    return beta
def monte_carlo_simulation(ticker, days=30, num_simulations=1000):
    """Perform Monte Carlo Simulation for stock price prediction."""
    try:
        # Fetch historical stock data
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2y")["Close"]

        if len(hist) < 50:
            return {"error": "Not enough historical data for Monte Carlo simulation"}

        # Calculate daily returns
        log_returns = np.log(hist / hist.shift(1)).dropna()
        mean_return = log_returns.mean()
        std_dev = log_returns.std()

        # Monte Carlo Simulation: Predict future prices
        simulated_prices = np.zeros((num_simulations, days))
        last_price = hist.iloc[-1]

        for i in range(num_simulations):
            future_prices = [last_price]
            for _ in range(days):
                random_return = np.random.normal(mean_return, std_dev)
                future_prices.append(future_prices[-1] * np.exp(random_return))
            simulated_prices[i, :] = future_prices[1:]

        # Calculate expected price range
        expected_price = np.mean(simulated_prices[:, -1])
        confidence_interval = np.percentile(simulated_prices[:, -1], [5, 95])

        # Generate Monte Carlo plot
        plt.figure(figsize=(10, 5))  # Avoid using plt.show()
        plt.plot(simulated_prices.T, color="lightgray", alpha=0.3)
        plt.title(f"Monte Carlo Simulation - {ticker} (Next {days} Days)")
        plt.xlabel("Days")
        plt.ylabel("Stock Price")

        # Save plot as Base64 string
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        plt.close()  # Close figure to prevent memory issues

        return {
            "Expected Price": round(expected_price, 2),
            "95% Confidence Interval": [round(confidence_interval[0], 2), round(confidence_interval[1], 2)],
            "Monte Carlo Plot": f"data:image/png;base64,{image_base64}"
        }

    except Exception as e:
        return {"error": str(e)}

import numpy as np
import yfinance as yf

def calculate_var(ticker, confidence_level=0.95):
    """Calculate Value at Risk (VaR) using historical stock data"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2y")["Close"]

        if len(hist) < 50:
            return {"error": "Not enough historical data for VaR calculation"}

        # Calculate daily returns
        returns = np.log(hist / hist.shift(1)).dropna()

        # Compute VaR at given confidence level
        var_value = np.percentile(returns, (1 - confidence_level) * 100)

        return {
            "VaR": round(var_value, 4),  # Format to 4 decimal places
            "Confidence Level": confidence_level
        }

    except Exception as e:
        return {"error": str(e)}

def calculate_cvar(ticker, confidence_level=0.95):
    """Calculate Conditional Value at Risk (CVaR)"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2y")["Close"]

        if len(hist) < 50:
            return {"error": "Not enough historical data for CVaR calculation"}

        # Calculate daily returns
        returns = np.log(hist / hist.shift(1)).dropna()

        # Compute VaR
        var_value = np.percentile(returns, (1 - confidence_level) * 100)

        # Compute CVaR (average loss beyond VaR threshold)
        cvar_value = np.mean(returns[returns < var_value])

        return {
            "CVaR": round(cvar_value, 4),
            "Confidence Level": confidence_level
        }

    except Exception as e:
        return {"error": str(e)}

    