import React from "react";

const RiskDisplay = ({ riskScore, stockPrice }) => {
    return (
        <div className="risk-display">
            {typeof stockPrice === "number" ? (
                <h2>💰 Stock Price: ${stockPrice.toFixed(2)}</h2>
            ) : (
                <h2>💰 Stock Price: N/A</h2>
            )}

            {typeof riskScore === "number" ? (
                <h2>✅ Predicted Risk Score: {riskScore.toFixed(5)}</h2>
            ) : (
                <h2>❗ Enter a stock ticker to get risk prediction.</h2>
            )}
        </div>
    );
};

export default RiskDisplay;
