import React, { useState } from "react";
import axios from "axios";
import StockInput from "./components/StockInput";
import RiskDisplay from "./components/RiskDisplay";
import MarketData from "./components/MarketData";
import RiskChart from "./components/RiskChart";
import MonteCarlo from "./components/MonteCarlo";
import RiskMetrics from "./components/RiskMetrics"; // Import RiskMetrics component

const App = () => {
    const [riskScore, setRiskScore] = useState(null);
    const [stockPrice, setStockPrice] = useState(null);
    const [movingAvg20, setMovingAvg20] = useState(null);
    const [movingAvg50, setMovingAvg50] = useState(null);
    const [rsi, setRsi] = useState(null);
    const [news, setNews] = useState([]);
    const [riskHistory, setRiskHistory] = useState([]);
    const [monteCarloData, setMonteCarloData] = useState(null);
    const [varData, setVarData] = useState(null);
    const [cvarData, setCvarData] = useState(null);

    const fetchRisk = async (ticker) => {
        try {
            const response = await axios.post("http://127.0.0.1:5000/predict-risk", {
                ticker: ticker
            });

            const {
                "Risk Score": risk,
                "Stock Price": price,
                "Moving Avg (20-day)": ma20,
                "Moving Avg (50-day)": ma50,
                "RSI": rsiValue,
                "News": newsData
            } = response.data;

            setRiskScore(risk);
            setStockPrice(price);
            setMovingAvg20(ma20);
            setMovingAvg50(ma50);
            setRsi(rsiValue);
            setNews(newsData);
            if (typeof risk === "number" && !isNaN(risk)) {
                setRiskHistory((prev) => [...prev, risk]);
              } 
            else {
                console.warn("Invalid risk score:", risk);
            }
            

            // Fetch additional risk metrics
            fetchMonteCarlo(ticker);
            fetchVarMetrics(ticker);

        } catch (error) {
            console.error("Error fetching risk score:", error);
            setRiskScore(null);
            setStockPrice(null);
            setMovingAvg20(null);
            setMovingAvg50(null);
            setRsi(null);
            setNews([]);
            setMonteCarloData(null);
            setVarData(null);
            setCvarData(null);
        }
    };

    const fetchMonteCarlo = async (ticker) => {
        try {
            const response = await axios.post("http://127.0.0.1:5000/monte-carlo", {
                ticker: ticker,
                days: 30  // Default prediction for 30 days
            });

            setMonteCarloData(response.data);
        } catch (error) {
            console.error("Error fetching Monte Carlo data:", error);
            setMonteCarloData(null);
        }
    };

    const fetchVarMetrics = async (ticker) => {
        try {
            const varResponse = await axios.post("http://127.0.0.1:5000/calculate-var", {
                ticker: ticker,
                confidence: 0.95
            });

            const cvarResponse = await axios.post("http://127.0.0.1:5000/calculate-cvar", {
                ticker: ticker,
                confidence: 0.95
            });

            setVarData(varResponse.data);
            setCvarData(cvarResponse.data);
        } catch (error) {
            console.error("Error fetching VaR & CVaR data:", error);
            setVarData(null);
            setCvarData(null);
        }
    };

    return (
        <div className="app-container">
          {/* Title */}
          <h1>Portfolio Risk Management</h1>
      
          {/* 🔷 Container 1: Search Input */}
          <div className="search-container">
            <StockInput onFetchRisk={fetchRisk} />
          </div>
      
          {/* 🔶 Container 2: Result Display */}
          <div className="results-container">
            <RiskDisplay riskScore={riskScore} stockPrice={stockPrice} />
          </div>
      
          {/* Keep the rest as-is */}
          <MarketData movingAvg20={movingAvg20} movingAvg50={movingAvg50} rsi={rsi} news={news} />
          <RiskChart riskHistory={riskHistory} />
          {monteCarloData && <MonteCarlo data={monteCarloData} />}
          {varData && cvarData && <RiskMetrics varData={varData} cvarData={cvarData} />}
        </div>
    );
};
export default App;
