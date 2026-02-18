function Footer({
  brandName = "Ink2Math",
  tagline = "Making mathematics accessible for everyone",
  links,
}) {
  return (
    <footer className="app-footer">
      <div className="footer-container">
        <p className="footer-text">
          <strong>{brandName}</strong> — {tagline}
        </p>

        {links && links.length > 0 && (
          <nav className="footer-links">
            {links.map(({ label, href }) => (
              <a key={label} href={href} className="footer-link">
                {label}
              </a>
            ))}
          </nav>
        )}
      </div>
    </footer>
  );
}

export default Footer;
