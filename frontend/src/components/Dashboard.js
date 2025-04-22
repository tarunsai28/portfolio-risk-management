//Dashboard.js
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Investors from "./Investors";
import Portfolios from "./Portfolios";
import Assets from "./Assets";
import PortfolioChart, { AssetPieChart } from "./charts"; // Import Charts
import { fetchPortfolioData, predictRisk } from "../services/api"; // Import ML API

const Dashboard = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState("");
  const [selectedInvestor, setSelectedInvestor] = useState(null);
  const [selectedPortfolio, setSelectedPortfolio] = useState(null);
  const [portfolioData, setPortfolioData] = useState(null);
  const [riskLevel, setRiskLevel] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      console.log("🔒 No token found! Redirecting to login...");
      navigate("/");
      return;
    }

    // Fetch protected data
    fetch("http://127.0.0.1:5000/api/protected", {
      method: "GET",
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("✅ Protected route response:", data);
        setMessage(data.message);
      })
      .catch((error) => console.error("❌ Error fetching protected data:", error));

    // Fetch Portfolio Data
    fetchPortfolioData()
      .then((data) => {
        console.log("📊 Portfolio Data:", data);
        setPortfolioData(data);

        // Call ML API for risk prediction based on portfolio data
        if (data.portfolio_volatility && data.portfolio_return) {
          predictRisk(data.portfolio_volatility, data.portfolio_return).then(
            (riskResult) => {
              setRiskLevel(riskResult.risk_level);
            }
          );
        }
      })
      .catch((error) => console.error("❌ Error fetching portfolio data:", error));
  }, [navigate]);

  return (
    <div className="container mt-4">
      <h2 className="text-center">📊 Investor Dashboard</h2>
      <p>{message ? message : "Fetching protected data..."}</p>

      {portfolioData && (
        <>
          <h3>Total Portfolio Value: ${portfolioData.total_value}</h3>
          <h4>Risk Level: {riskLevel ? riskLevel : "Calculating..."}</h4>

          {/* Portfolio Performance Chart */}
          <PortfolioChart data={portfolioData.performance} />

          {/* Asset Allocation Pie Chart */}
          <AssetPieChart assets={portfolioData.assets} />
        </>
      )}

      {/* Investors Component */}
      <Investors onSelectInvestor={(id) => setSelectedInvestor(id)} />

      {/* Portfolios Component - Only show when an investor is selected */}
      {selectedInvestor && (
        <Portfolios
          investorId={selectedInvestor}
          onSelectPortfolio={(id) => setSelectedPortfolio(id)}
        />
      )}

      {/* Assets Component - Only show when a portfolio is selected */}
      {selectedPortfolio && <Assets portfolioId={selectedPortfolio} />}
    </div>
  );
};

export default Dashboard;
