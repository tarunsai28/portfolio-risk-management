import React from "react";

const RiskMetrics = ({ varData, cvarData }) => {
    return (
        <div className="risk-metrics">
            <h3>📊 Advanced Risk Metrics</h3>
            <p>⚠️ <b>Value at Risk (VaR 95% Confidence Level):</b> {varData.VaR * 100}%</p>
            <p>🔥 <b>Conditional VaR (CVaR 95% Confidence Level):</b> {cvarData.CVaR * 100}%</p>
        </div>
    );
};

export default RiskMetrics;
