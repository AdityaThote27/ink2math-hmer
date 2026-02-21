import { useState } from "react";

function ImageUploadPanel({ solveFromImage, loading }) {
  const [file, setFile] = useState(null);

  const handleUpload = () => {
    if (!file) return;
    solveFromImage(file);
  };

  return (
    <div className="card">
      <h2>Upload Image</h2>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "🖼 Solve from Image"}
      </button>
    </div>
  );
}

export default ImageUploadPanel;
