import { BlockMath } from "react-katex";

function ResultPanel({ result }) {
  if (!result) return null;

  return (
    <div className="card">

      {/* 🔥 SHOW BACKEND ERRORS + DEBUG INFO */}
      {result.error && (
        <>
          <h2 style={{ color: "red" }}>Error</h2>
          <p style={{ color: "red" }}>{result.error}</p>

          {result.recognized_text_raw && (
            <>
              <h3>Recognized Raw Text</h3>
              <p>{result.recognized_text_raw}</p>
            </>
          )}

          {result.recognized_text_cleaned && (
            <>
              <h3>Recognized Cleaned Text</h3>
              <p>{result.recognized_text_cleaned}</p>
            </>
          )}
        </>
      )}

      {/* Equation Type */}
      {!result.error && result.type && (
        <>
          <h2>Equation Type</h2>
          <p>{result.type}</p>
        </>
      )}

      {/* Original Equation */}
      {!result.error && result.display_latex && (
        <>
          <h2>Given Equation</h2>
          <BlockMath math={result.display_latex} />
        </>
      )}

      {/* Final Solution */}
      {!result.error && result.solution_latex && (
        <>
          <h2>Solution</h2>
          <BlockMath math={`x = ${result.solution_latex}`} />
        </>
      )}

      {/* Steps */}
      {!result.error &&
        Array.isArray(result.steps) &&
        result.steps.length > 0 && (
          <>
            <h2>Step-by-Step Explanation</h2>
            {result.steps.map((step, index) => (
              <div key={index} className="step">
                <strong>
                  Step {step.step}: {step.title}
                </strong>
                <p>{step.description}</p>
              </div>
            ))}
          </>
        )}
    </div>
  );
}

export default ResultPanel;
