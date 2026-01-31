import React from 'react';

const HistoryPanel = ({ history, onSelectDataset, onGenerateReport }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="history-panel">
      <h3>📜 Recent Datasets</h3>
      <div className="history-list">
        {history.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#666' }}>No datasets uploaded yet</p>
        ) : (
          history.map((dataset) => (
            <div key={dataset.id} className="history-item">
              <div onClick={() => onSelectDataset(dataset)}>
                <strong>📁 {dataset.name}</strong>
                <p>📅 {formatDate(dataset.upload_date)}</p>
                <p>🔢 Records: {dataset.summary_data.total_count}</p>
                <p>📊 Types: {Object.keys(dataset.summary_data.equipment_types).length}</p>
              </div>
              <button 
                className="report-btn"
                onClick={() => onGenerateReport(dataset.id)}
              >
                📄 Generate PDF
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default HistoryPanel;