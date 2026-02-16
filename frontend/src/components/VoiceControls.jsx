function VoiceControls({ recording, onStart, onStop }) {
  return (
    <div className="card">
      {!recording ? (
        <button onClick={onStart}>🎤 Record</button>
      ) : (
        <button onClick={onStop}>⏹ Stop</button>
      )}
    </div>
  );
}

export default VoiceControls;
