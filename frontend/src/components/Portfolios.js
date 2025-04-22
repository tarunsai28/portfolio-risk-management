import React, { useEffect, useState, useCallback } from "react";
import { getInvestorPortfolios, addPortfolio, deletePortfolio } from "../services/api";

const Portfolios = ({ investorId, onSelectPortfolio }) => {
  const [portfolios, setPortfolios] = useState([]);
  const [portfolioName, setPortfolioName] = useState("");

  const fetchPortfolios = useCallback(async () => {
    const data = await getInvestorPortfolios(investorId);
    setPortfolios(data);
  }, [investorId]);

  useEffect(() => {
    fetchPortfolios();
  }, [fetchPortfolios]);

  const handleAddPortfolio = async () => {
    if (portfolioName) {
      await addPortfolio({ name: portfolioName, investor_id: investorId });
      setPortfolioName("");
      fetchPortfolios();
    }
  };

  const handleDeletePortfolio = async (portfolioId) => {
    await deletePortfolio(portfolioId);
    fetchPortfolios();
  };

  return (
    <div className="container mt-4">
      <h2 className="text-center">Portfolios</h2>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Portfolio Name"
          value={portfolioName}
          onChange={(e) => setPortfolioName(e.target.value)}
        />
        <button className="btn btn-primary" onClick={handleAddPortfolio}>
          Add Portfolio
        </button>
      </div>

      <div className="row">
        {portfolios.map((portfolio) => (
          <div key={portfolio.id} className="col-md-4">
            <div className="card mb-3 shadow-sm">
              <div className="card-body">
                <h5 className="card-title">{portfolio.name}</h5>
                <button
                  className="btn btn-outline-secondary btn-sm mt-2 me-2"
                  onClick={() => onSelectPortfolio(portfolio.id)}
                >
                  View Assets
                </button>
                <button
                  className="btn btn-danger btn-sm mt-2"
                  onClick={() => handleDeletePortfolio(portfolio.id)}
                >
                  Delete Portfolio
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Portfolios;
