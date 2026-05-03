/* Portal chrome — recreates the ascendion.engineering header & footer.
   Original implementation; spacing, type, and layout inferred from the user's
   reference screenshots. NOT a copy of any third-party asset. */

const PortalHeader = ({ width }) => (
  <header style={{
    width,
    height: 56,
    background: "#0E0E0E",
    color: "#FAFAF7",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 28px",
    fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
    flexShrink: 0,
    position: "relative",
    zIndex: 20,
  }}>
    {/* Wordmark */}
    <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 11 }}>
        <div style={{
          width: 26, height: 26,
          border: "1px solid rgba(250,250,247,0.5)",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontFamily: '"IBM Plex Serif", Georgia, serif',
          fontSize: 15,
          fontWeight: 500,
        }}>A</div>
        <div style={{
          fontSize: 12,
          letterSpacing: "0.18em",
          fontWeight: 500,
        }}>ASCENDION&nbsp;&nbsp;ENGINEERING</div>
      </div>
      <div style={{ width: 1, height: 18, background: "rgba(250,250,247,0.2)" }}></div>
      <nav style={{ display: "flex", gap: 22, fontSize: 12 }}>
        {["Principles", "Patterns", "System Design", "Technology", "Security", "AI-Native", "Governance"].map((n) => (
          <a key={n} href="#" style={{
            color: "rgba(250,250,247,0.7)",
            textDecoration: "none",
            padding: "4px 0",
            letterSpacing: "0.01em",
          }}>{n}</a>
        ))}
      </nav>
    </div>
    <div style={{ display: "flex", gap: 10 }}>
      <button style={{
        background: "#FAFAF7", color: "#0E0E0E",
        border: "none", borderRadius: 999,
        padding: "7px 14px",
        fontSize: 11.5, fontWeight: 600, letterSpacing: "0.02em",
        cursor: "pointer",
      }}>Knowledge Graph</button>
      <button style={{
        background: "transparent", color: "#FAFAF7",
        border: "1px solid rgba(250,250,247,0.5)", borderRadius: 999,
        padding: "7px 14px",
        fontSize: 11.5, fontWeight: 500, letterSpacing: "0.02em",
        cursor: "pointer",
      }}>All Topics</button>
    </div>
  </header>
);

const PortalFooter = ({ width }) => (
  <footer style={{
    width,
    height: 84,
    background: "#0E0E0E",
    color: "rgba(250,250,247,0.7)",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 36px",
    fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
    flexShrink: 0,
    position: "relative",
    zIndex: 20,
  }}>
    <div style={{
      fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
      fontSize: 18,
      fontWeight: 700,
      letterSpacing: "0.08em",
      fontStyle: "italic",
      color: "#FAFAF7",
    }}>ASCENDION</div>
    <div style={{ fontSize: 12, letterSpacing: "0.02em" }}>
      © 2025 Ascendion Solutions Architecture Practice
    </div>
  </footer>
);

Object.assign(window, { PortalHeader, PortalFooter });
