function InputPanel({ equation, setEquation, onSolve }) {
  return (
    <div className="card">
      <input
        type="text"
        placeholder="Enter equation (e.g., 2x + 3 = 7)"
        value={equation}
        onChange={(e) => setEquation(e.target.value)}
      />
      <button onClick={() => onSolve()}>Solve</button>
    </div>
  );
}

export default InputPanel;
