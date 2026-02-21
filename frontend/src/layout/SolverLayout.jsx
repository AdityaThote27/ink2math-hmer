function SolverLayout({
  activeTab,
  setActiveTab,
  equation,
  setEquation,
  solveEquation,
  recording,
  startRecording,
  stopRecording,
  solveFromImage,
  solveFromDrawing,
  loading,
  InputPanel,
  VoiceControls,
  ImageUploadPanel,
  DrawCanvasPanel,
}) {
  return (
    <section id="solver" className="solver-section card">
      <div className="tabs">
        <button
          className={`tab ${activeTab === "text" ? "active" : ""}`}
          onClick={() => setActiveTab("text")}
        >
          Text
        </button>
        <button
          className={`tab ${activeTab === "image" ? "active" : ""}`}
          onClick={() => setActiveTab("image")}
        >
          Image
        </button>
        <button
          className={`tab ${activeTab === "voice" ? "active" : ""}`}
          onClick={() => setActiveTab("voice")}
        >
          Voice
        </button>
        <button
          className={`tab ${activeTab === "draw" ? "active" : ""}`}
          onClick={() => setActiveTab("draw")}
        >
          Draw
        </button>
      </div>

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
        <ImageUploadPanel
          solveFromImage={solveFromImage}
          loading={loading}
        />
      )}



      {activeTab === "draw" && (
        <DrawCanvasPanel
          onSolveDraw={solveFromDrawing}
          loading={loading}
        />

      )}



      {loading && <div className="loading">Processing...</div>}
    </section>
  );
}

export default SolverLayout;

