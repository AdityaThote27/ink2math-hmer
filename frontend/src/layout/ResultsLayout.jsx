function ResultsLayout({ result, ResultPanel }) {
  if (!result) return null;

  return (
    <section className="card">
      <ResultPanel result={result} />
    </section>
  );
}

export default ResultsLayout;
