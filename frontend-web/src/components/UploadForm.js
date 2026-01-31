import React, { useState } from "react";

const UploadForm = ({ onUpload, loading }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      onUpload(file);
      setFile(null);
      e.target.reset();
    }
  };

  return (
    <form className="upload-form" onSubmit={handleSubmit}>
      <h3>📤 Upload CSV File</h3>
      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        required
        className="file-input"
      />
      <button type="submit" className="upload-btn" disabled={!file || loading}>
        {loading ? "📤 Uploading..." : "🚀 Upload & Analyze"}
      </button>
    </form>
  );
};

export default UploadForm;
