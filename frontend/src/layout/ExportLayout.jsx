function ExportLayout({ result, ExportPanel }) {
  if (!result) return null;

  return (
    <section className="card">
      <ExportPanel result={result} />
    </section>
  );
}

export default ExportLayout;
