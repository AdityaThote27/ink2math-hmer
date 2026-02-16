import axios from "axios";
import { useState } from "react";

const BASE_URL = "http://127.0.0.1:8000";

function ImageUploadPanel({ setResult, setLoading }) {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const response = await axios.post(
        `${BASE_URL}/solve/image`,  // ⚠ adjust if needed
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      setResult(response.data);
    } catch (error) {
      alert("Image solve failed.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Upload Image</h2>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={handleUpload}>
        🖼 Solve from Image
      </button>
    </div>
  );
}

export default ImageUploadPanel;
