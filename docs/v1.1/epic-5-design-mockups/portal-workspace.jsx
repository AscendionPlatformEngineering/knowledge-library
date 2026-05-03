/* Standalone, header-less workspace.
   Goals:
   - Maximum viewport given to graph + panel
   - Striking, technical-but-editorial meta-layer
   - All controls reachable per Fitts; choices grouped per Hick
   - Familiar conventions where it counts (⌘K, Esc, segmented controls)
*/

const TOPBAR_H = 52;
const STATUSBAR_H = 32;

/* Top utility bar — workspace identity, layout mode, density,
   inline ⌘K search, view toggles. Sits flush at top. */
function StandaloneTopbar({ width }) {
  return (
    <div style={{
      width, height: TOPBAR_H,
      background: "#FAFAF7",
      borderBottom: "1px solid rgba(14,14,14,0.10)",
      display: "flex", alignItems: "center", justifyContent: "space-between",
      padding: "0 22px",
      fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
      flexShrink: 0, position: "relative", zIndex: 10,
    }}>
      {/* Left: workspace mark + title */}
      <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
        <div style={{
          width: 26, height: 26,
          background: "#0E0E0E", color: "#FAFAF7",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontFamily: '"IBM Plex Serif", Georgia, serif', fontSize: 13,
        }}>◐</div>
        <div style={{ display: "flex", flexDirection: "column", lineHeight: 1.1 }}>
          <span style={{
            fontFamily: '"IBM Plex Serif", Georgia, serif',
            fontSize: 14, color: "#0E0E0E",
          }}>Knowledge Graph</span>
          <span style={{
            fontSize: 9.5, color: "#9A9A9A",
            letterSpacing: "0.14em", textTransform: "uppercase",
            fontFamily: '"IBM Plex Mono", "IBM Plex Sans", monospace',
          }}>workspace · v1.1</span>
        </div>
        <span style={{ width: 1, height: 22, background: "rgba(14,14,14,0.12)", margin: "0 4px" }}></span>
        <ToolbarSegment items={["Force", "Radial", "Tree", "Matrix"]} active="Force" />
      </div>

      {/* Center: ⌘K search */}
      <div style={{
        position: "absolute", left: "50%", transform: "translateX(-50%)",
        display: "flex", alignItems: "center", gap: 10,
        background: "rgba(14,14,14,0.04)",
        padding: "7px 14px", borderRadius: 4,
        minWidth: 360,
      }}>
        <span style={{ fontSize: 12, color: "#6B6B6B" }}>⌕</span>
        <span style={{
          fontSize: 12.5, color: "#9A9A9A",
          fontFamily: '"IBM Plex Serif", Georgia, serif',
          fontStyle: "italic", flex: 1,
        }}>Search 73 pages, 224 standards, 18 groups…</span>
        <kbd style={{
          fontSize: 9.5, padding: "2px 5px",
          border: "1px solid rgba(14,14,14,0.18)",
          borderRadius: 2, color: "#6B6B6B",
          background: "#FAFAF7", letterSpacing: "0.02em", fontWeight: 500,
        }}>⌘ K</kbd>
      </div>

      {/* Right: lens, density, share, help */}
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <LensControl />
        <span style={{ width: 1, height: 22, background: "rgba(14,14,14,0.12)" }}></span>
        <DensityToggle />
        <span style={{ width: 1, height: 22, background: "rgba(14,14,14,0.12)" }}></span>
        <IconBtn title="Share view (⌘ ⇧ S)">↗</IconBtn>
        <IconBtn title="Keyboard (?)">?</IconBtn>
      </div>
    </div>
  );
}

const ToolbarSegment = ({ items, active }) => (
  <div style={{
    display: "flex",
    border: "1px solid rgba(14,14,14,0.14)",
    borderRadius: 4,
    overflow: "hidden",
  }}>
    {items.map((it, i) => (
      <button key={i} style={{
        background: it === active ? "#0E0E0E" : "transparent",
        color: it === active ? "#FAFAF7" : "#3C3C3C",
        border: "none",
        padding: "5px 11px",
        fontSize: 11,
        fontWeight: 500,
        letterSpacing: "0.02em",
        cursor: "pointer",
        fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
      }}>{it}</button>
    ))}
  </div>
);

const IconBtn = ({ children, title }) => (
  <button title={title} style={{
    width: 30, height: 30,
    background: "transparent",
    border: "1px solid rgba(14,14,14,0.14)",
    borderRadius: 4, cursor: "pointer",
    color: "#3C3C3C", fontSize: 12,
    display: "flex", alignItems: "center", justifyContent: "center",
    transition: `all 160ms ${EASE}`,
  }}>{children}</button>
);

const LensControl = () => (
  <div style={{
    display: "inline-flex", alignItems: "center", gap: 8,
    padding: "5px 10px",
    border: "1px solid rgba(168,84,32,0.35)",
    background: "rgba(217,122,60,0.06)",
    borderRadius: 4, cursor: "pointer",
  }}>
    <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#D97A3C" }}></span>
    <span style={{
      fontSize: 11, color: "#A85420",
      letterSpacing: "0.04em", fontWeight: 500,
    }}>Debt Ledger</span>
    <span style={{ fontSize: 10, color: "#A85420", opacity: 0.6 }}>▾</span>
  </div>
);

const DensityToggle = () => (
  <div style={{
    display: "flex",
    border: "1px solid rgba(14,14,14,0.14)",
    borderRadius: 4, overflow: "hidden",
  }}>
    {[
      { l: "Sparse", a: false },
      { l: "Dense", a: true },
    ].map((d, i) => (
      <button key={i} style={{
        background: d.a ? "#0E0E0E" : "transparent",
        color: d.a ? "#FAFAF7" : "#3C3C3C",
        border: "none",
        padding: "5px 10px",
        fontSize: 11, fontWeight: 500,
        cursor: "pointer",
        fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
      }}>{d.l}</button>
    ))}
  </div>
);

/* Bottom status bar — counts, zoom, coordinates, perf indicator.
   Reads like a precision instrument readout. */
function StatusBar({ width }) {
  return (
    <div style={{
      width, height: STATUSBAR_H,
      background: "#FAFAF7",
      borderTop: "1px solid rgba(14,14,14,0.10)",
      display: "flex", alignItems: "center", justifyContent: "space-between",
      padding: "0 22px",
      fontFamily: '"IBM Plex Mono", "IBM Plex Sans", monospace',
      fontSize: 10.5, color: "#6B6B6B",
      letterSpacing: "0.06em", textTransform: "uppercase",
      fontVariantNumeric: "tabular-nums",
      flexShrink: 0, zIndex: 10,
    }}>
      <div style={{ display: "flex", gap: 18, alignItems: "center" }}>
        <span style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <span style={{
            width: 6, height: 6, borderRadius: "50%",
            background: "#5A8A5A",
            boxShadow: "0 0 0 3px rgba(90,138,90,0.15)",
          }}></span>
          <span>simulation idle</span>
        </span>
        <Stat l="nodes" v="73" />
        <Stat l="standards" v="224" />
        <Stat l="groups" v="18" />
        <Stat l="edges" v="1,412" />
        <Stat l="visible" v="73 / 73" />
      </div>
      <div style={{ display: "flex", gap: 18 }}>
        <Stat l="zoom" v="100%" />
        <Stat l="x" v="0" />
        <Stat l="y" v="0" />
        <span style={{
          color: "#0E0E0E",
          fontFamily: '"IBM Plex Serif", Georgia, serif',
          textTransform: "none", letterSpacing: 0,
          fontStyle: "italic",
          fontSize: 11,
        }}>focus: PCI DSS</span>
      </div>
    </div>
  );
}

const Stat = ({ l, v }) => (
  <span><span style={{ color: "#0E0E0E" }}>{v}</span><span style={{ marginLeft: 5, opacity: 0.7 }}>{l}</span></span>
);

/* The graph zone — adds dot-grid backdrop, neighborhood label,
   minimap, zoom dock, focused-node callout. */
function StandaloneGraphZone({ width, height }) {
  return (
    <div style={{
      position: "relative",
      width, height,
      background: "#FAFAF7",
      overflow: "hidden",
    }}>
      {/* Dot grid */}
      <svg width={width} height={height} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <pattern id="sa-grid" width="80" height="80" patternUnits="userSpaceOnUse">
            <circle cx="0" cy="0" r="0.6" fill="rgba(14,14,14,0.18)" />
          </pattern>
        </defs>
        <rect width={width} height={height} fill="url(#sa-grid)" />
      </svg>

      <GraphBackdrop width={width} height={height} variant="page" />

      {/* Neighborhood label top-left */}
      <div style={{
        position: "absolute", top: 18, left: 22,
        display: "flex", flexDirection: "column", gap: 4,
      }}>
        <div style={{
          fontSize: 9.5, letterSpacing: "0.16em",
          textTransform: "uppercase", color: "#9A9A9A",
          fontFamily: '"IBM Plex Mono", "IBM Plex Sans", monospace',
        }}>neighborhood</div>
        <div style={{
          fontFamily: '"IBM Plex Serif", Georgia, serif',
          fontSize: 18, color: "#0E0E0E",
          fontStyle: "italic",
        }}>Compliance & Regulatory</div>
      </div>

      {/* Filter chips top-center */}
      <div style={{
        position: "absolute", top: 20, left: "50%",
        transform: "translateX(-50%)",
        display: "flex", gap: 6,
      }}>
        {[
          { l: "All", n: 73, a: true },
          { l: "Substantive", n: 8 },
          { l: "Standards", n: 224 },
          { l: "Groups", n: 18 },
        ].map((f, i) => (
          <button key={i} style={{
            fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
            fontSize: 11, padding: "5px 11px",
            background: f.a ? "#0E0E0E" : "rgba(250,250,247,0.8)",
            color: f.a ? "#FAFAF7" : "#3C3C3C",
            border: f.a ? "1px solid #0E0E0E" : "1px solid rgba(14,14,14,0.14)",
            borderRadius: 999, cursor: "pointer", fontWeight: 500,
            backdropFilter: "blur(4px)",
          }}>{f.l} <span style={{ opacity: 0.6, marginLeft: 3 }}>{f.n}</span></button>
        ))}
      </div>

      {/* Minimap top-right */}
      <div style={{
        position: "absolute", top: 18, right: 22,
        width: 110, height: 72,
        border: "1px solid rgba(14,14,14,0.14)",
        background: "rgba(250,250,247,0.85)",
        padding: 4,
        backdropFilter: "blur(4px)",
      }}>
        <div style={{
          fontSize: 9, color: "#9A9A9A",
          letterSpacing: "0.12em", textTransform: "uppercase",
          fontFamily: '"IBM Plex Mono", "IBM Plex Sans", monospace',
          marginBottom: 2,
        }}>map</div>
        <svg width="100" height="52">
          {Array.from({ length: 36 }).map((_, i) => {
            const x = ((i * 31) % 100);
            const y = ((i * 17) % 52);
            return <circle key={i} cx={x} cy={y} r="1" fill="rgba(14,14,14,0.4)" />;
          })}
          <rect x="28" y="14" width="36" height="22" fill="none" stroke="#D97A3C" strokeWidth="1" />
        </svg>
      </div>

      {/* Focused-node callout */}
      <FocusedCallout x={width * 0.42} y={height * 0.48} />

      {/* Zoom dock bottom-right */}
      <div style={{
        position: "absolute", bottom: 18, right: 22,
        display: "flex", flexDirection: "column",
        border: "1px solid rgba(14,14,14,0.14)",
        background: "rgba(250,250,247,0.95)",
      }}>
        <ZBtn>+</ZBtn>
        <Divider h />
        <ZBtn>−</ZBtn>
        <Divider h />
        <ZBtn title="Recenter (Z)">⊕</ZBtn>
        <Divider h />
        <ZBtn title="Fullscreen">⛶</ZBtn>
      </div>

      {/* Legend bottom-left */}
      <div style={{
        position: "absolute", bottom: 18, left: 22,
        display: "flex", gap: 14,
        background: "rgba(250,250,247,0.85)",
        padding: "8px 12px",
        border: "1px solid rgba(14,14,14,0.10)",
        backdropFilter: "blur(4px)",
        fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
        fontSize: 11, color: "#6B6B6B",
      }}>
        <LegendDot color="#0E0E0E" size={8} label="Group" />
        <LegendDot color="#D97A3C" size={6} label="Substantive" />
        <LegendDot color="#3C3C3C" size={5} opacity={0.55} label="Page" />
        <LegendDot color="#9A9A9A" size={3} label="Standard" />
      </div>
    </div>
  );
}

const ZBtn = ({ children, title }) => (
  <button title={title} style={{
    width: 30, height: 30,
    background: "transparent", border: "none",
    color: "#3C3C3C", fontSize: 13, cursor: "pointer",
    fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
  }}>{children}</button>
);
const Divider = ({ h }) => (
  <span style={{
    [h ? "borderTop" : "borderLeft"]: "1px solid rgba(14,14,14,0.10)",
    height: h ? 1 : "auto",
    width: h ? "100%" : 1,
  }}></span>
);

const LegendDot = ({ color, size, opacity, label }) => (
  <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
    <span style={{
      width: size, height: size, borderRadius: "50%",
      background: color, opacity: opacity || 1,
    }}></span>{label}
  </span>
);

/* Focused-node bracketed callout */
function FocusedCallout({ x, y }) {
  return (
    <svg
      style={{ position: "absolute", inset: 0, pointerEvents: "none" }}
      width="100%" height="100%"
    >
      <line x1={x} y1={y} x2={x + 100} y2={y - 70}
        stroke="#0E0E0E" strokeWidth="1" strokeOpacity="0.4" />
      <circle cx={x} cy={y} r="14" fill="none"
        stroke="#0E0E0E" strokeWidth="1" strokeOpacity="0.5" />
      <circle cx={x} cy={y} r="22" fill="none"
        stroke="#0E0E0E" strokeWidth="1" strokeOpacity="0.18" strokeDasharray="2 3" />
      <g transform={`translate(${x + 102}, ${y - 92})`}>
        <text x="0" y="0" fontFamily='"IBM Plex Mono", monospace' fontSize="9.5"
          fill="#9A9A9A" letterSpacing="0.1em">[ NODE · 042 ]</text>
        <text x="0" y="16" fontFamily='"IBM Plex Serif", Georgia, serif' fontSize="14"
          fill="#0E0E0E">PCI DSS</text>
        <text x="0" y="32" fontFamily='"IBM Plex Sans", system-ui, sans-serif' fontSize="10"
          fill="#6B6B6B" letterSpacing="0.04em">deg 12 · substantive · debt</text>
      </g>
    </svg>
  );
}

/* The complete page (no header/footer). */
function StandaloneWorkspace({ width, height, panelState = "page", collapsed }) {
  const isCollapsed = collapsed || panelState === "collapsed";
  const panelW = isCollapsed ? 56 : 400;
  const workH = height - TOPBAR_H - STATUSBAR_H;

  let panelChildren;
  if (panelState === "empty") panelChildren = <PanelEmpty />;
  else if (panelState === "page") panelChildren = <PanelPage />;
  else if (panelState === "standard") panelChildren = <PanelStandard />;
  else if (panelState === "topic") panelChildren = <PanelTopic />;
  else if (panelState === "search") panelChildren = <PanelSearch />;
  else if (panelState === "collapsed") panelChildren = <CollapsedRail />;

  return (
    <div style={{
      width, height,
      display: "flex", flexDirection: "column",
      background: "#FAFAF7",
      fontFamily: '"IBM Plex Serif", Georgia, serif',
      overflow: "hidden",
    }}>
      <StandaloneTopbar width={width} />
      <div style={{ display: "flex", flex: 1, minHeight: 0 }}>
        <StandaloneGraphZone width={width - panelW} height={workH} />
        <div style={{ position: "relative", width: panelW, height: workH, flexShrink: 0 }}>
          {panelChildren}
        </div>
      </div>
      <StatusBar width={width} />
    </div>
  );
}

Object.assign(window, {
  StandaloneTopbar, StatusBar, StandaloneGraphZone, StandaloneWorkspace,
  TOPBAR_H, STATUSBAR_H,
});
