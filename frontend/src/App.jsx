import { useState, useRef } from "react";
import axios from "axios";

import InputPanel from "./components/InputPanel";
import VoiceControls from "./components/VoiceControls";
import ImageUploadPanel from "./components/ImageUploadPanel";
import DrawCanvasPanel from "./components/DrawCanvasPanel";
import ResultPanel from "./components/ResultPanel";
import ExportPanel from "./components/ExportPanel";
import MiniAssistant from "./components/MiniAssistant";


import HeroSection from "./layout/HeroSection";
import SolverLayout from "./layout/SolverLayout";
import ResultsLayout from "./layout/ResultsLayout";
import ExportLayout from "./layout/ExportLayout";
import Footer from "./layout/Footer";

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

  const solveEquation = async () => {
    if (!equation) return;

    try {
      setLoading(true);
      const response = await axios.post(`${BASE_URL}/solve`, {
        expression: equation,
      });
      setResult(response.data);
    } catch {
      alert("Text solve failed.");
    } finally {
      setLoading(false);
    }
  };

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
    <div className="app-wrapper">
      <HeroSection />

      <MiniAssistant
        setActiveTab={setActiveTab}
        solveEquation={solveEquation}
        result={result}
      />


      <SolverLayout
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        equation={equation}
        setEquation={setEquation}
        solveEquation={solveEquation}
        recording={recording}
        startRecording={startRecording}
        stopRecording={stopRecording}
        solveFromImage={solveFromImage}
        solveFromDrawing={solveFromDrawing}
        loading={loading}
        InputPanel={InputPanel}
        VoiceControls={VoiceControls}
        ImageUploadPanel={ImageUploadPanel}
        DrawCanvasPanel={DrawCanvasPanel}
      />

      <ResultsLayout result={result} ResultPanel={ResultPanel} />
      <ExportLayout result={result} ExportPanel={ExportPanel} />

      <MiniAssistant
        setActiveTab={setActiveTab}
        onSolve={solveEquation}
        result={result}
      />



      <Footer />
    </div>
  );
}

export default App;
