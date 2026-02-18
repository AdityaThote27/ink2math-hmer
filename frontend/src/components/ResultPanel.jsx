import { BlockMath } from "react-katex";

function ResultPanel({ result }) {
  if (!result) return null;

  return (
    <div className="card">
      {/* Equation Type */}
      {result.type && (
        <>
          <h2>Equation Type</h2>
          <p>{result.type}</p>
        </>
      )}

      {/* Original Equation */}
      {result.display_latex && (
        <>
          <h2>Given Equation</h2>
          <BlockMath math={result.display_latex} />
        </>
      )}

      {/* Final Solution */}
      {result.solution_latex && (
        <>
          <h2>Solution</h2>
          <BlockMath math={`x = ${result.solution_latex}`} />
        </>
      )}

      {/* Steps */}
      {Array.isArray(result.steps) && result.steps.length > 0 && (
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
