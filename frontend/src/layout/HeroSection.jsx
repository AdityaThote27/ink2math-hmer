import MiniAssistant from "../components/MiniAssistant";

function HeroSection({
  badge = "AI-Powered Math Assistant",
  title = "Ink2Math",
  subtitle = "Smart Math Solver",
  description = "Solve equations from text, voice, images, and handwriting with full accessibility support.",
  ctaLabel = "Start Solving Now",
  stats = [
    { label: "Input Methods", value: "4+" },
    { label: "Accessibility", value: "100%" },
  ],
  setActiveTab,
  solveEquation,   // ✅ renamed properly
  setEquation,
}) {

  const handleCTA = () => {
    document.getElementById("solver")?.scrollIntoView({
      behavior: "smooth",
    });
  };

  return (
    <header className="hero-section">
      <div className="hero-container">

        {/* LEFT SIDE */}
        <div className="hero-left">
          <div className="badge">{badge}</div>

          <div className="hero-title-group">
            <h1 className="hero-title">{title}</h1>
            <h2 className="hero-subtitle">{subtitle}</h2>
          </div>

          <p className="hero-description">{description}</p>

          <button className="primary-btn" onClick={handleCTA}>
            {ctaLabel} →
          </button>

          <div className="hero-stats">
            {stats.map((stat) => (
              <div key={stat.label} className="stat-item">
                <p className="stat-label">{stat.label}</p>
                <p className="stat-value">{stat.value}</p>
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT SIDE */}
        <div className="hero-right">
          <div className="hero-card">
            <div className="hero-illustration">
              <div className="hero-symbol">∑</div>
              <p className="hero-illustration-label">
                Advanced AI Recognition
              </p>
            </div>

            <p className="hero-card-text">
              Advanced AI recognizes handwritten equations, typed problems,
              and voice commands — delivering step-by-step solutions.
            </p>
          </div>
        </div>

      </div>

      {/* 🤖 MINI ASSISTANT (floating) */}
      <MiniAssistant
        setActiveTab={setActiveTab}
        solveEquation={solveEquation}   
        setEquation={setEquation}
      />
    </header>
  );
}

export default HeroSection;
