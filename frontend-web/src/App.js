import React, { useState, useEffect } from "react";
import axios from "axios";
import DataTable from "./components/DataTable";
import Charts from "./components/Charts";
import UploadForm from "./components/UploadForm";
import HistoryPanel from "./components/HistoryPanel";
import "./App.css";

function App() {
  const [currentDataset, setCurrentDataset] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: "", type: "" });

  // Configure axios with basic auth
  axios.defaults.auth = {
    username: "admin",
    password: "password123",
  };

  // Set base URL
  axios.defaults.baseURL = "http://localhost:8000";

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get("/api/history/");
      setHistory(response.data);
    } catch (error) {
      showMessage(
        "Failed to load history. Make sure backend is running.",
        "error",
      );
      console.error("Error fetching history:", error);
    }
  };

  const showMessage = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: "", type: "" }), 5000);
  };

  const handleUpload = async (file) => {
    setLoading(true);
    setMessage({ text: "", type: "" });
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("/api/datasets/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setCurrentDataset(response.data);
      fetchHistory();
      showMessage("File uploaded and analyzed successfully!", "success");
    } catch (error) {
      const errorMsg = error.response?.data?.error || error.message;
      showMessage(`Upload failed: ${errorMsg}`, "error");
      console.error("Error uploading file:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDatasetSelect = (dataset) => {
    setCurrentDataset(dataset);
    showMessage(`Loaded dataset: ${dataset.name}`, "success");
  };

  const handleGenerateReport = async (datasetId) => {
    try {
      const response = await axios.get(
        `/api/datasets/${datasetId}/generate_report/`,
        { responseType: "blob" },
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        `equipment_report_${datasetId.slice(0, 8)}.pdf`,
      );
      document.body.appendChild(link);
      link.click();
      link.remove();

      showMessage("PDF report generated successfully!", "success");
    } catch (error) {
      showMessage("Failed to generate PDF report", "error");
      console.error("Error generating report:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🧪 Chemical Equipment Parameter Visualizer</h1>
        <p>Hybrid Web + Desktop Application for Equipment Analysis</p>
      </header>

      {message.text && (
        <div className={`status-message status-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="main-container">
        <div className="left-panel">
          <UploadForm onUpload={handleUpload} loading={loading} />
          <HistoryPanel
            history={history}
            onSelectDataset={handleDatasetSelect}
            onGenerateReport={handleGenerateReport}
          />
        </div>

        <div className="content">
          {currentDataset ? (
            <>
              <div className="summary-section">
                <h2>📊 Analysis Results</h2>
                <div className="summary-cards">
                  <div className="card">
                    <h3>Total Equipment</h3>
                    <p>{currentDataset.summary_data.total_count}</p>
                  </div>
                  <div className="card">
                    <h3>Equipment Types</h3>
                    <p>
                      {
                        Object.keys(currentDataset.summary_data.equipment_types)
                          .length
                      }
                    </p>
                  </div>
                  <div className="card">
                    <h3>Avg Flowrate</h3>
                    <p>
                      {currentDataset.summary_data.averages.flowrate.toFixed(2)}
                    </p>
                  </div>
                  <div className="card">
                    <h3>Avg Pressure</h3>
                    <p>
                      {currentDataset.summary_data.averages.pressure.toFixed(2)}
                    </p>
                  </div>
                  <div className="card">
                    <h3>Avg Temperature</h3>
                    <p>
                      {currentDataset.summary_data.averages.temperature.toFixed(
                        2,
                      )}
                    </p>
                  </div>
                </div>
              </div>

              <Charts dataset={currentDataset} />
              <DataTable data={currentDataset.records} />
            </>
          ) : (
            <div className="welcome-message">
              <h2>Welcome to Chemical Equipment Visualizer 🧪</h2>
              <p>
                Upload a CSV file to begin equipment analysis and visualization
              </p>
              <div
                style={{
                  textAlign: "left",
                  background: "#f8f9ff",
                  padding: "20px",
                  borderRadius: "10px",
                  maxWidth: "600px",
                  margin: "30px auto",
                  border: "1px solid #e0e0e0",
                }}
              >
                <h3 style={{ marginTop: "0" }}>📝 Sample CSV Format:</h3>
                <pre
                  style={{
                    background: "white",
                    padding: "15px",
                    borderRadius: "8px",
                    overflowX: "auto",
                    fontSize: "14px",
                  }}
                >
                  Equipment Name,Equipment Type,Flowrate,Pressure,Temperature
                  Reactor-001,Reactor,150.5,10.2,85.0
                  Mixer-001,Mixer,200.0,5.5,65.0
                  Separator-001,Separator,120.3,8.7,75.5
                  Reactor-002,Reactor,180.7,12.1,90.0
                  Pump-001,Pump,300.2,15.3,40.0
                </pre>
                <p
                  style={{ fontSize: "14px", color: "#666", marginTop: "10px" }}
                >
                  <strong>Note:</strong> Make sure your CSV has these exact
                  column headers
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
