import { useState, useRef } from "react";
import axios from "axios";

import InputPanel from "./components/InputPanel";
import VoiceControls from "./components/VoiceControls";
import ImageUploadPanel from "./components/ImageUploadPanel";
import DrawCanvasPanel from "./components/DrawCanvasPanel";
import ResultPanel from "./components/ResultPanel";
import ExportPanel from "./components/ExportPanel";

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

  // ========================= SOLVE TEXT =========================
  const solveEquation = async (customExpression = null) => {
    const expressionToSolve = customExpression ?? equation;
    if (!expressionToSolve) return null;

    try {
      setLoading(true);

      const response = await axios.post(`${BASE_URL}/solve`, {
        expression: expressionToSolve,
      });

      setResult(response.data);

      document
        .getElementById("results")
        ?.scrollIntoView({ behavior: "smooth" });

      return response.data; // 🔥 Needed for MiniAssistant

    } catch (error) {
      console.error(error);
      alert("Text solve failed.");
      return null;
    } finally {
      setLoading(false);
    }
  };

  // ========================= TAB CHANGE =========================
  const handleTabChange = (tab) => {
    setActiveTab(tab);
    document
      .getElementById("solver")
      ?.scrollIntoView({ behavior: "smooth" });
  };

  // ========================= VOICE RECORD =========================
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

        document
          .getElementById("results")
          ?.scrollIntoView({ behavior: "smooth" });

      } catch (error) {
        console.error(error);
        alert("Voice solve failed.");
      } finally {
        setLoading(false);
      }
    };

    mediaRecorder.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  };

  // ========================= IMAGE SOLVE =========================
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

      document
        .getElementById("results")
        ?.scrollIntoView({ behavior: "smooth" });

    } catch (error) {
      console.error(error);
      alert("Image solve failed.");
    } finally {
      setLoading(false);
    }
  };

  // ========================= DRAW SOLVE =========================
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

      document
        .getElementById("results")
        ?.scrollIntoView({ behavior: "smooth" });

    } catch (error) {
      console.error(error);
      alert("Draw solve failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-wrapper">

      {/* ================= HERO (Mini inside Hero) ================= */}
      <HeroSection
        setActiveTab={handleTabChange}
        solveEquation={solveEquation}
        setEquation={setEquation}
      />

      {/* ================= SOLVER ================= */}
      <div id="solver">
        <SolverLayout
          activeTab={activeTab}
          setActiveTab={handleTabChange}
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
      </div>

      {/* ================= RESULTS ================= */}
      <div id="results">
        <ResultsLayout
          result={result}
          ResultPanel={ResultPanel}
        />
      </div>

      {/* ================= EXPORT ================= */}
      <ExportLayout
        result={result}
        ExportPanel={ExportPanel}
      />

      <Footer />
    </div>
  );
}

export default App;
