# ml_model.py
import os
import numpy as np
import pandas as pd
import yfinance as yf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.losses import MeanSquaredError

# Ensure models directory exists
os.makedirs("backend/models", exist_ok=True)

def get_stock_prices(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="2y")['Close']
    return hist

def prepare_data(prices, time_steps=50):
    data = prices.pct_change().dropna().values.reshape(-1, 1)
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i + time_steps])
        y.append(data[i + time_steps])
    return np.array(X), np.array(y)

def train_lstm(ticker):
    print(f"Fetching stock prices for {ticker}...")
    prices = get_stock_prices(ticker)

    print("Preparing data...")
    X, y = prepare_data(prices)

    print("Training LSTM model...")
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)),
        LSTM(50),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss=MeanSquaredError())  # Fix: Explicitly use MeanSquaredError
    model.fit(X, y, epochs=10, batch_size=16)

    model_path = "backend/models/lstm_model.h5"
    model.save(model_path)
    print(f"✅ Model saved at {model_path}")

def predict_risk(ticker):
    """Predict risk score using the trained LSTM model"""
    try:
        model_path = "backend/models/lstm_model.h5"

        # Ensure the model exists before loading
        if not os.path.exists(model_path):
            return "Error: Model file not found. Train the model first."

        # Register custom loss function when loading the model
        custom_objects = {"mse": MeanSquaredError()}
        model = load_model(model_path, custom_objects=custom_objects)

        # Fetch latest stock prices
        prices = get_stock_prices(ticker)

        # Ensure we have enough data points
        if len(prices) < 50:
            return "Error: Not enough data points for prediction."

        last_prices = np.array(prices[-50:]).reshape(1, 50, 1)

        # Make prediction
        prediction = model.predict(last_prices)

        return float(prediction[0][0])
    
    except Exception as e:
        return f"Error in prediction: {str(e)}"

if __name__ == '__main__':
    train_lstm("AAPL")
