/* A static, low-fidelity graph backdrop so the panel feels in-context.
   Not a real D3 sim — a hand-laid arrangement of nodes + edges. */

function GraphBackdrop({ width, height, focusedId, variant }) {
  // Seeded pseudo-random
  const rng = (seed) => {
    let s = seed;
    return () => {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
  };

  const nodes = React.useMemo(() => {
    const r = rng(variant === "search" ? 7 : variant === "topic" ? 3 : variant === "standard" ? 5 : variant === "page" ? 2 : 11);
    const list = [];
    // Topic group anchor nodes
    const groups = ["compliance", "security", "data", "platform", "ml"];
    groups.forEach((g, i) => {
      const angle = (i / groups.length) * Math.PI * 2 + 0.4;
      const cx = width / 2 + Math.cos(angle) * (width * 0.28);
      const cy = height / 2 + Math.sin(angle) * (height * 0.32);
      list.push({ id: `g-${g}`, type: "group", x: cx, y: cy, r: 9 });
    });
    // Page nodes scattered
    for (let i = 0; i < 38; i++) {
      list.push({
        id: `p-${i}`,
        type: r() > 0.78 ? "substantive" : "page",
        x: r() * width,
        y: r() * height,
        r: 3.2 + r() * 1.6,
      });
    }
    // Standards (small dots)
    for (let i = 0; i < 60; i++) {
      list.push({
        id: `s-${i}`,
        type: "standard",
        x: r() * width,
        y: r() * height,
        r: 1.6 + r() * 0.6,
      });
    }
    return list;
  }, [width, height, variant]);

  const edges = React.useMemo(() => {
    const r = rng(variant === "search" ? 17 : variant === "topic" ? 13 : variant === "standard" ? 19 : variant === "page" ? 23 : 29);
    const e = [];
    for (let i = 0; i < nodes.length; i++) {
      const a = nodes[i];
      // each node connects to 1-2 nearby
      for (let k = 0; k < 2; k++) {
        const j = Math.floor(r() * nodes.length);
        if (j === i) continue;
        const b = nodes[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        if (Math.hypot(dx, dy) < width * 0.22) {
          e.push([a, b]);
        }
      }
    }
    return e;
  }, [nodes, variant]);

  const focused = nodes.find(n => n.id === focusedId) || nodes[Math.floor(nodes.length / 3)];

  const colorFor = (n) => {
    if (n.id === focused.id) return "#0E0E0E";
    if (n.type === "substantive") return "#D97A3C";
    if (n.type === "group") return "#0E0E0E";
    return "#3C3C3C";
  };
  const opacityFor = (n) => {
    if (n.id === focused.id) return 1;
    if (n.type === "standard") return 0.35;
    if (n.type === "substantive") return 0.7;
    if (n.type === "group") return 0.85;
    return 0.55;
  };

  return (
    <svg width={width} height={height} style={{ display: "block" }}>
      {/* Soft halo around focused */}
      {focused && variant !== "empty" && variant !== "search" && (
        <circle cx={focused.x} cy={focused.y} r={28} fill="rgba(14,14,14,0.05)" />
      )}
      {edges.map(([a, b], i) => (
        <line
          key={i}
          x1={a.x} y1={a.y} x2={b.x} y2={b.y}
          stroke="#0E0E0E"
          strokeOpacity={(a.id === focused.id || b.id === focused.id) ? 0.35 : 0.08}
          strokeWidth={1}
        />
      ))}
      {nodes.map((n) => (
        <circle
          key={n.id}
          cx={n.x} cy={n.y} r={n.id === focused.id ? n.r + 2 : n.r}
          fill={colorFor(n)}
          opacity={opacityFor(n)}
        />
      ))}
      {focused && variant !== "empty" && variant !== "search" && (
        <circle cx={focused.x} cy={focused.y} r={focused.r + 5}
                fill="none" stroke="#0E0E0E" strokeWidth={1} strokeOpacity={0.35} />
      )}
    </svg>
  );
}

/* The full graph + panel composition wrapper. */
function GraphFrame({ width, height, variant, children, mobile }) {
  return (
    <div style={{
      width, height,
      background: "#FAFAF7",
      position: "relative",
      overflow: "hidden",
      fontFamily: '"IBM Plex Serif", Georgia, serif',
      color: "#0E0E0E",
    }}>
      {/* Graph area */}
      <div style={{
        position: "absolute",
        inset: 0,
        right: mobile ? 0 : 400,
      }}>
        <GraphBackdrop
          width={mobile ? width : width - 400}
          height={height}
          variant={variant}
        />
        {/* Tiny chrome label top-left */}
        <div style={{
          position: "absolute",
          top: 22, left: 28,
          fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
          fontSize: 11,
          letterSpacing: "0.16em",
          textTransform: "uppercase",
          color: "#6B6B6B",
          fontWeight: 500,
        }}>
          ascendion.engineering · knowledge graph
        </div>
        {/* Stat ticker bottom-left */}
        <div style={{
          position: "absolute",
          bottom: 22, left: 28,
          fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
          fontSize: 11,
          color: "#6B6B6B",
          letterSpacing: "0.04em",
          fontVariantNumeric: "tabular-nums",
        }}>
          73 pages · 224 standards · 18 groups
        </div>
      </div>
      {children}
    </div>
  );
}

Object.assign(window, { GraphBackdrop, GraphFrame });
