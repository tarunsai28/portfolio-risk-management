import React, { useEffect, useState } from "react";
import { getInvestors, addInvestor, deleteInvestor } from "../services/api";

const Investors = ({ onSelectInvestor }) => {
  const [investors, setInvestors] = useState([]);
  const [investorData, setInvestorData] = useState({ name: "", email: "" });

  useEffect(() => {
    const fetchInvestors = async () => {
      const data = await getInvestors();
      setInvestors(data);
    };
    fetchInvestors();
  }, []);

  const handleAddInvestor = async () => {
    if (investorData.name && investorData.email) {
      await addInvestor(investorData);
      setInvestorData({ name: "", email: "" });
      const updatedInvestors = await getInvestors();
      setInvestors(updatedInvestors);
    }
  };

  const handleDeleteInvestor = async (investorId) => {
    await deleteInvestor(investorId);
    const updatedInvestors = await getInvestors();
    setInvestors(updatedInvestors);
  };

  return (
    <div className="container mt-4">
      <h2 className="text-center">Investors</h2>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Name"
          value={investorData.name}
          onChange={(e) => setInvestorData({ ...investorData, name: e.target.value })}
        />
        <input
          type="email"
          className="form-control"
          placeholder="Email"
          value={investorData.email}
          onChange={(e) => setInvestorData({ ...investorData, email: e.target.value })}
        />
        <button className="btn btn-primary" onClick={handleAddInvestor}>
          Add Investor
        </button>
      </div>

      <ul className="list-group">
        {investors.map((investor) => (
          <li key={investor.id} className="list-group-item d-flex justify-content-between align-items-center">
            <span onClick={() => onSelectInvestor(investor.id)} style={{ cursor: "pointer" }}>
              {investor.name} ({investor.email})
            </span>
            <button
              className="btn btn-danger btn-sm"
              onClick={() => handleDeleteInvestor(investor.id)}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Investors;
