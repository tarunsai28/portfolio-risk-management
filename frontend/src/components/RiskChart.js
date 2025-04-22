import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const RiskChart = ({ riskHistory }) => {
  if (!riskHistory || riskHistory.length === 0) {
    return (
      <div>
        <h3>📉 No Risk Prediction Data</h3>
        <p>Enter a stock ticker to generate predictions and see the graph.</p>
      </div>
    );
  }

  // Format data
  const chartData = riskHistory.map((score, index) => ({
    name: `Run ${index + 1}`,
    risk: typeof score === "string" ? parseFloat(score) : score,
  }));

  return (
    <div>
      <h3>📊 Risk Score History</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis domain={[0, 1]} /> {/* Clamp values between 0 and 1 */}
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="risk" stroke="#8884d8" strokeWidth={2} activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RiskChart;
