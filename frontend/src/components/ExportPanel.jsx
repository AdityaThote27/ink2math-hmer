import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

function ExportPanel({ result }) {
  if (!result) return null;

  const downloadFile = async (endpoint, filename) => {
    try {
      // 🔥 FIX: handle all modes
      const expression =
        result.input ||
        result.recognized_text_cleaned ||
        result.recognized_text_raw;

      if (!expression) {
        alert("No equation available to export.");
        return;
      }

      const response = await axios.post(
        `${BASE_URL}${endpoint}`,
        { expression },  // ✅ always valid now
        { responseType: "blob" }
      );

      const blob = new Blob([response.data]);
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();

      link.remove();
      window.URL.revokeObjectURL(url);

    } catch (error) {
      alert("Export failed.");
      console.error(error.response?.data || error);
    }
  };

  return (
    <div className="card">
      <h2>Export</h2>

      <button onClick={() => downloadFile("/export/pdf", "solution.pdf")}>
        📄 Export PDF
      </button>

      <button onClick={() => downloadFile("/export/docx", "solution.docx")}>
        📄 Export DOCX
      </button>

      <button onClick={() => downloadFile("/export/braille", "solution_braille.txt")}>
        ♿ Export Braille
      </button>
    </div>
  );
}

export default ExportPanel;
