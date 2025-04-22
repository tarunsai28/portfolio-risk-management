//api.js
import axios from "axios";

const API_URL = "http://127.0.0.1:5000/api";

// INVESTORS
export const getInvestors = async () => {
  const response = await axios.get(`${API_URL}/investors`);
  return response.data;
};

export const addInvestor = async (investor) => {
  const response = await axios.post(`${API_URL}/investor`, investor);
  return response.data;
};

export const deleteInvestor = async (investorId) => {
  await axios.delete(`${API_URL}/investor/${investorId}`);
};

// PORTFOLIOS
export const getInvestorPortfolios = async (investorId) => {
  const response = await axios.get(`${API_URL}/investor/${investorId}/portfolios`);
  return response.data;
};

export const addPortfolio = async (portfolio) => {
  const response = await axios.post(`${API_URL}/portfolio`, portfolio);
  return response.data;
};

export const deletePortfolio = async (portfolioId) => {
  await axios.delete(`${API_URL}/portfolio/${portfolioId}`);
};

// ASSETS
export const getPortfolioAssets = async (portfolioId) => {
  const response = await axios.get(`${API_URL}/portfolio/${portfolioId}/assets`);
  return response.data;
};

export const addAsset = async (asset) => {
  const response = await axios.post(`${API_URL}/asset`, asset);
  return response.data;
};

export const deleteAsset = async (assetId) => {
  await axios.delete(`${API_URL}/asset/${assetId}`);
};

export const registerUser = async (userData) => {
    return axios.post(`${API_URL}/register`, userData);
};

export const loginUser = async (userData) => {
    return axios.post(`${API_URL}/login`, userData);
};

export const getProtectedData = async (token) => {
    return axios.get(`${API_URL}/protected`, {
        headers: { Authorization: `Bearer ${token}` }
    });
};

// src/services/api.js
export const fetchPortfolioData = async () => {
    const token = localStorage.getItem("token"); // Get JWT token
    const response = await fetch("http://127.0.0.1:5000/api/portfolio_summary", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
  
    if (!response.ok) throw new Error("Failed to fetch portfolio data");
  
    return response.json();
  };
  


//Test ML API

export const predictRisk = async (volatility, expectedReturn) => {
  const response = await fetch("http://127.0.0.1:5000/predict_risk", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ volatility, expected_return: expectedReturn }),
  });

  return response.json();
};

