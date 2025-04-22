import React from "react";

const MarketData = ({ movingAvg20, movingAvg50, rsi, news }) => {
    return (
        <div className="market-data">
            <h3>📊 Market Indicators</h3>
            <p>📈 20-day Moving Avg: {movingAvg20 ? movingAvg20.toFixed(2) : "N/A"}</p>
            <p>📉 50-day Moving Avg: {movingAvg50 ? movingAvg50.toFixed(2) : "N/A"}</p>
            <p>📊 RSI (Relative Strength Index): {rsi ? rsi.toFixed(2) : "N/A"}</p>

            <h3>📰 Latest News</h3>
            {news.length > 0 ? (
                <ul>
                    {news.map((item, index) => (
                        <li key={index}>
                            <a href={item.url} target="_blank" rel="noopener noreferrer">{item.title}</a>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No recent news available.</p>
            )}
        </div>
    );
};

export default MarketData;
