function Header() {
  return (
    <header style={header}>
      <div style={container}>
        <div style={logo}>🕵️ RealityCheck</div>

        <nav style={nav}>
          <a href="#image" style={link}>Image</a>
          <a href="#video" style={link}>Video</a>
        </nav>
      </div>
    </header>
  );
}

const header = {
  position: "sticky",
  top: 0,
  zIndex: 100,
  background: "#ffffff",
  borderBottom: "1px solid #e5e7eb",
};

const container = {
  maxWidth: 1100,
  margin: "0 auto",
  padding: "12px 20px",
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
};

const logo = {
  fontSize: 20,
  fontWeight: 600,
};

const nav = {
  display: "flex",
  gap: 20,
};

const link = {
  textDecoration: "none",
  color: "#374151",
  fontWeight: 500,
};

export default Header;
