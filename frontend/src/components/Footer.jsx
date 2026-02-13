function Footer() {
  return (
    <footer style={footer}>
      <div style={container}>
        <p style={text}>
          RealityCheck © 2026 — AI content verification system
        </p>
      </div>
    </footer>
  );
}

const footer = {
  marginTop: 60,
  borderTop: "1px solid #e5e7eb",
  background: "#f9fafb",
};

const container = {
  maxWidth: 1100,
  margin: "0 auto",
  padding: "20px",
  textAlign: "center",
};

const text = {
  fontSize: 14,
  color: "#6b7280",
};

export default Footer;
