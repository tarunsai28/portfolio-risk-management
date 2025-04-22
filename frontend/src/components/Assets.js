import React, { useEffect, useState, useCallback } from "react";
import { getPortfolioAssets, addAsset } from "../services/api";

const Assets = ({ portfolioId }) => {
  const [assets, setAssets] = useState([]);
  const [assetData, setAssetData] = useState({ name: "", type: "", value: "" });

  const fetchAssets = useCallback(async () => {
    const data = await getPortfolioAssets(portfolioId);
    setAssets(data);
  }, [portfolioId]);

  useEffect(() => {
    fetchAssets();
  }, [fetchAssets]);

  const handleAddAsset = async () => {
    if (assetData.name && assetData.type && assetData.value) {
      await addAsset({
        name: assetData.name,
        type: assetData.type,
        value: parseFloat(assetData.value),
        portfolio_id: portfolioId,
      });
      setAssetData({ name: "", type: "", value: "" });
      fetchAssets();
    }
  };

  return (
    <div className="container mt-4">
      <h2 className="text-center">Assets</h2>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Asset Name"
          value={assetData.name}
          onChange={(e) => setAssetData({ ...assetData, name: e.target.value })}
        />
        <input
          type="text"
          className="form-control"
          placeholder="Asset Type"
          value={assetData.type}
          onChange={(e) => setAssetData({ ...assetData, type: e.target.value })}
        />
        <input
          type="number"
          className="form-control"
          placeholder="Asset Value"
          value={assetData.value}
          onChange={(e) =>
            setAssetData({ ...assetData, value: e.target.value })
          }
        />
        <button className="btn btn-success" onClick={handleAddAsset}>
          Add Asset
        </button>
      </div>

      <div className="row">
        {assets.map((asset) => (
          <div key={asset.id} className="col-md-4">
            <div className="card mb-3 shadow-sm">
              <div className="card-body">
                <h5 className="card-title">{asset.name}</h5>
                <p className="card-text">
                  Type: {asset.type} <br />
                  Value: ${asset.value}
                </p>
                <button className="btn btn-danger btn-sm">
                  Delete Asset
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Assets;
