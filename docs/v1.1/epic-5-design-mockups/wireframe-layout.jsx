/* Wireframe layout — gray placeholders for everything except the panel.
   The panel is the ONLY designed element; everything else is labeled
   gray block to show context and proportional position. */

function PlaceholderBlock({ label, height, sub, style }) {
  return (
    <div style={{
      width: "100%",
      height,
      background: "repeating-linear-gradient(135deg, rgba(14,14,14,0.04) 0 8px, rgba(14,14,14,0.06) 8px 16px)",
      border: "1px dashed rgba(14,14,14,0.22)",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      gap: 4,
      fontFamily: '"IBM Plex Mono", "IBM Plex Sans", monospace',
      color: "#6B6B6B",
      ...(style || {}),
    }}>
      <span style={{
        fontSize: 11,
        letterSpacing: "0.14em",
        textTransform: "uppercase",
        fontWeight: 500,
      }}>{label}</span>
      {sub && (
        <span style={{
          fontSize: 10,
          color: "#9A9A9A",
          letterSpacing: "0.06em",
        }}>{sub}</span>
      )}
    </div>
  );
}

/* The complete wireframe page with the panel docked beside the graph canvas. */
function WireframeLayout({ width, height, panelState = "page" }) {
  const navH = 48;
  const heroH = 140;
  const footerH = 64;
  const canvasH = height - navH - heroH - footerH - 24; // 24 = vertical gaps
  const panelW = 400;
  const canvasW = width - panelW - 32 - 32 - 1; // page padding + gap

  let panelChildren;
  if (panelState === "empty") panelChildren = <PanelEmpty />;
  else if (panelState === "page") panelChildren = <PanelPage />;
  else if (panelState === "standard") panelChildren = <PanelStandard />;
  else if (panelState === "topic") panelChildren = <PanelTopic />;
  else if (panelState === "search") panelChildren = <PanelSearch />;

  return (
    <div style={{
      width, height,
      background: "#FAFAF7",
      padding: 32,
      boxSizing: "border-box",
      display: "flex",
      flexDirection: "column",
      gap: 8,
      fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
    }}>
      <PlaceholderBlock
        height={navH}
        label="site nav"
        sub="already exists, do not design"
      />
      <PlaceholderBlock
        height={heroH}
        label="knowledge graph hero with stats"
        sub="already exists"
      />
      <div style={{
        display: "flex",
        gap: 0,
        height: canvasH,
      }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          <PlaceholderBlock
            height={canvasH}
            label="graph canvas"
            sub="D3, existing"
            style={{ height: "100%" }}
          />
        </div>
        <div style={{
          width: panelW,
          flexShrink: 0,
          height: canvasH,
          position: "relative",
          marginLeft: -1,
          background: "#FAFAF7",
          border: "1px solid rgba(14,14,14,0.12)",
          overflow: "hidden",
        }}>
          {panelChildren}
        </div>
      </div>
      <PlaceholderBlock
        height={footerH}
        label="footer"
        sub="already exists, do not design"
      />
    </div>
  );
}

Object.assign(window, { PlaceholderBlock, WireframeLayout });
