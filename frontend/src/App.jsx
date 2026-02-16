import { useState, useRef } from "react";
import axios from "axios";

import InputPanel from "./components/InputPanel";
import VoiceControls from "./components/VoiceControls";
import ImageUploadPanel from "./components/ImageUploadPanel";
import DrawCanvasPanel from "./components/DrawCanvasPanel";
import ResultPanel from "./components/ResultPanel";
import ExportPanel from "./components/ExportPanel";

import "./styles.css";

const BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [activeTab, setActiveTab] = useState("text");
  const [equation, setEquation] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);

  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  // =============================
  // TEXT SOLVE
  // =============================
  const solveEquation = async () => {
    if (!equation) return;

    try {
      setLoading(true);
      const response = await axios.post(`${BASE_URL}/solve`, {
        expression: equation,
      });
      setResult(response.data);
    } catch (error) {
      alert("Text solve failed.");
    } finally {
      setLoading(false);
    }
  };

  // =============================
  // VOICE SOLVE
  // =============================
  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);

    mediaRecorderRef.current = mediaRecorder;
    chunksRef.current = [];

    mediaRecorder.ondataavailable = (e) => {
      chunksRef.current.push(e.data);
    };

    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunksRef.current, { type: "audio/webm" });

      const formData = new FormData();
      formData.append("file", blob);

      try {
        setLoading(true);
        const response = await axios.post(
          `${BASE_URL}/solve/voice`,
          formData,
          { headers: { "Content-Type": "multipart/form-data" } }
        );
        setResult(response.data);
      } catch {
        alert("Voice solve failed.");
      } finally {
        setLoading(false);
      }
    };

    mediaRecorder.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  // =============================
  // IMAGE SOLVE
  // =============================
  const solveFromImage = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const response = await axios.post(
        `${BASE_URL}/solve/image`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setResult(response.data);
    } catch {
      alert("Image solve failed.");
    } finally {
      setLoading(false);
    }
  };

  // =============================
  // DRAW SOLVE
  // =============================
  const solveFromDrawing = async (blob) => {
    const formData = new FormData();
    formData.append("file", blob);

    try {
      setLoading(true);
      const response = await axios.post(
        `${BASE_URL}/solve/draw`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setResult(response.data);
    } catch {
      alert("Draw solve failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Ink2Math AI Assistant</h1>

      {/* TABS */}
      <div className="tabs">
        <button
          className={activeTab === "text" ? "active" : ""}
          onClick={() => setActiveTab("text")}
        >
          Text
        </button>

        <button
          className={activeTab === "voice" ? "active" : ""}
          onClick={() => setActiveTab("voice")}
        >
          Voice
        </button>

        <button
          className={activeTab === "image" ? "active" : ""}
          onClick={() => setActiveTab("image")}
        >
          Image
        </button>

        <button
          className={activeTab === "draw" ? "active" : ""}
          onClick={() => setActiveTab("draw")}
        >
          Draw
        </button>
      </div>

      {/* TAB CONTENT */}
      {activeTab === "text" && (
        <InputPanel
          equation={equation}
          setEquation={setEquation}
          onSolve={solveEquation}
        />
      )}

      {activeTab === "voice" && (
        <VoiceControls
          recording={recording}
          onStart={startRecording}
          onStop={stopRecording}
        />
      )}

      {activeTab === "image" && (
        <ImageUploadPanel onSolveImage={solveFromImage} />
      )}

      {activeTab === "draw" && (
        <DrawCanvasPanel onSolveDraw={solveFromDrawing} />
      )}

      {loading && <p className="loading">Processing...</p>}

      <ResultPanel result={result} />
      <ExportPanel result={result} />
    </div>
  );
}

export default App;
