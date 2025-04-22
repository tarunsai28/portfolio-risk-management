import React from "react";

const MonteCarlo = ({ data }) => {
    return (
        <div className="monte-carlo">
            <h3>📈 Monte Carlo Simulation Results</h3>
            <p>🔮 **Expected Price in 30 Days:** <b>${data["Expected Price"]}</b></p>
            <p>🎯 **95% Confidence Interval:** <b>${data["95% Confidence Interval"][0]} - ${data["95% Confidence Interval"][1]}</b></p>
            <img src={data["Monte Carlo Plot"]} alt="Monte Carlo Simulation Plot" style={{ width: "100%", borderRadius: "10px" }} />
        </div>
    );
};

export default MonteCarlo;
