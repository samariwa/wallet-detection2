import { useState } from "react";
import "./App.css";

function App() {
  const [address, setAddress] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeAddress = async () => {
    if (!address.trim()) {
      setError("Please enter an Ethereum address");
      return;
    }

    if (!address.startsWith("0x") || address.length !== 42) {
      setError("Invalid Ethereum address format");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://localhost:5001/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ address: address.trim() }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || "Failed to analyze address");
      }
    } catch (err) {
      setError(
        "Failed to connect to API. Make sure the backend is running on port 5001."
      );
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (verdict) => {
    switch (verdict) {
      case "flagged":
        return "#ff4444";
      case "not flagged":
        return "#44ff44";
      default:
        return "#ffaa44";
    }
  };

  const getRiskLevel = (verdict, confidence) => {
    if (verdict === "flagged") {
      return confidence > 0.8 ? "High Risk" : "Medium Risk";
    } else if (verdict === "not flagged") {
      return confidence > 0.8 ? "Low Risk" : "Medium Risk";
    }
    return "Unknown";
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Blockchain Fraud Detective</h1>
        <p>Analyze Ethereum addresses for fraudulent activity using AI</p>
      </header>

      <main className="main-content">
        <div className="input-section">
          <div className="input-group">
            <label htmlFor="address">Ethereum Address:</label>
            <input
              id="address"
              type="text"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              placeholder="0x1234567890abcdef..."
              className="address-input"
              disabled={loading}
            />
            <button
              onClick={analyzeAddress}
              disabled={loading || !address.trim()}
              className="analyze-btn"
            >
              {loading ? "Analyzing..." : "Analyze Address"}
            </button>
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        {result && (
          <div className="results-section">
            <div className="result-header">
              <h2>Analysis Results</h2>
              <div className="address-info">
                <strong>Address:</strong> {result.address}
              </div>
            </div>

            <div className="risk-assessment">
              <div
                className="risk-badge"
                style={{ backgroundColor: getRiskColor(result.verdict) }}
              >
                {result.verdict === "flagged" ? "FLAGGED" : "NOT FLAGGED"}
              </div>
              <div className="risk-details">
                <div className="risk-level">
                  Risk Level:{" "}
                  <strong>
                    {getRiskLevel(result.verdict, result.confidence)}
                  </strong>
                </div>
                <div className="confidence">
                  Confidence:{" "}
                  <strong>{(result.confidence * 100).toFixed(1)}%</strong>
                </div>
              </div>
            </div>

            <div className="transaction-info">
              <h3>Transaction Summary</h3>
              <div className="stats-grid">
                <div className="stat-item">
                  <span className="stat-label">Total Transactions:</span>
                  <span className="stat-value">{result.transaction_count}</span>
                </div>
                {result.features && (
                  <>
                    <div className="stat-item">
                      <span className="stat-label">Sent Transactions:</span>
                      <span className="stat-value">
                        {result.features["Sent tnx"]}
                      </span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Received Transactions:</span>
                      <span className="stat-value">
                        {result.features["Received Tnx"]}
                      </span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Total ETH Sent:</span>
                      <span className="stat-value">
                        {result.features["total Ether sent"]?.toFixed(4)} ETH
                      </span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Total ETH Received:</span>
                      <span className="stat-value">
                        {result.features["total ether received"]?.toFixed(4)}{" "}
                        ETH
                      </span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">ETH Balance:</span>
                      <span className="stat-value">
                        {result.features["total ether balance"]?.toFixed(4)} ETH
                      </span>
                    </div>
                  </>
                )}
              </div>
            </div>

            {result.explanations && result.explanations.length > 0 && (
              <div className="explanations">
                <h3> AI Explanation</h3>
                <p>
                  The model flagged this address based on these top factors:
                </p>
                <ul className="explanation-list">
                  {result.explanations.map(([feature, impact], index) => (
                    <li key={index} className="explanation-item">
                      <strong>{feature}:</strong> Impact score{" "}
                      {impact.toFixed(4)}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
