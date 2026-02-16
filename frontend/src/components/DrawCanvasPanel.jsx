import { useRef, useState } from "react";
import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

function DrawCanvasPanel({ setResult, setLoading }) {
  const canvasRef = useRef(null);
  const [drawing, setDrawing] = useState(false);

  const startDrawing = () => setDrawing(true);
  const stopDrawing = () => setDrawing(false);

  const draw = (e) => {
    if (!drawing) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    ctx.lineWidth = 3;
    ctx.lineCap = "round";
    ctx.strokeStyle = "black";

    const rect = canvas.getBoundingClientRect();

    ctx.lineTo(
      e.clientX - rect.left,
      e.clientY - rect.top
    );
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(
      e.clientX - rect.left,
      e.clientY - rect.top
    );
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  };

  const submitDrawing = async () => {
    const canvas = canvasRef.current;
    const dataURL = canvas.toDataURL("image/png");

    const blob = await (await fetch(dataURL)).blob();

    const formData = new FormData();
    formData.append("file", blob);

    try {
      setLoading(true);

      const response = await axios.post(
        `${BASE_URL}/solve/draw`,  // ⚠ adjust if needed
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      setResult(response.data);
    } catch (error) {
      alert("Draw solve failed.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Draw Equation</h2>

      <canvas
        ref={canvasRef}
        width={500}
        height={200}
        style={{ border: "1px solid #ccc" }}
        onMouseDown={startDrawing}
        onMouseUp={stopDrawing}
        onMouseMove={draw}
      />

      <div style={{ marginTop: "10px" }}>
        <button onClick={clearCanvas}>Clear</button>
        <button onClick={submitDrawing}>
          ✍ Solve Drawing
        </button>
      </div>
    </div>
  );
}

export default DrawCanvasPanel;
