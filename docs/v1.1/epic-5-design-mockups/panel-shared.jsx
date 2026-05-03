/* Shared bits for KG panels — applying Laws of UX:
   - Fitts's Law: 32–44px hit targets, close icon corner-positioned
   - Jakob's Law: familiar conventions (⌘K, breadcrumbs, drawer handle)
   - Law of Proximity / Common Region: subtle grouping bands
   - Miller's Law: chunked lists capped to ~7 with "Show more"
   - Goal-Gradient: visible counts on every list
   - Von Restorff: single orange accent, used only on substantive things
   - Doherty Threshold: 160ms transitions everywhere
*/

const EASE = "cubic-bezier(0.2, 0.8, 0.2, 1)";

const Hairline = ({ style }) => (
  <div style={{ height: 1, background: "rgba(14,14,14,0.10)", ...(style || {}) }}></div>
);

const MetaLabel = ({ children, style }) => (
  <div style={{
    fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
    fontSize: 10.5,
    letterSpacing: "0.12em",
    textTransform: "uppercase",
    color: "#6B6B6B",
    fontWeight: 500,
    ...(style || {})
  }}>{children}</div>
);

const Breadcrumb = ({ section, page }) => (
  <nav aria-label="Breadcrumb" style={{
    fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
    fontSize: 11,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    color: "#6B6B6B",
    fontWeight: 500,
    display: "flex",
    alignItems: "center",
    gap: 0,
  }}>
    <a href="#" style={{
      color: "#6B6B6B",
      textDecoration: "none",
      padding: "4px 0",
    }}>{section}</a>
    <span style={{ margin: "0 8px", opacity: 0.5 }}>/</span>
    <span style={{ color: "#3C3C3C" }}>{page}</span>
  </nav>
);

const LensBadge = ({ label }) => (
  <span style={{
    display: "inline-flex",
    alignItems: "center",
    gap: 6,
    fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
    fontSize: 10.5,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    color: "#A85420",
    border: "1px solid rgba(168,84,32,0.35)",
    background: "rgba(217,122,60,0.08)",
    padding: "3px 9px 3px 8px",
    borderRadius: 999,
    fontWeight: 500,
  }}>
    <span style={{
      width: 5, height: 5, borderRadius: "50%",
      background: "#D97A3C", display: "inline-block"
    }}></span>
    {label}
  </span>
);

/* Fitts-friendly list row: 44px+ tap target, hover affordance, arrow on hover */
const ListRow = ({ title, sub, kind, onClick, dense }) => {
  const [hover, setHover] = React.useState(false);
  const dot = kind === "substantive" ? "#D97A3C"
            : kind === "group" ? "#0E0E0E"
            : kind === "standard" ? "#9A9A9A"
            : "#3C3C3C";
  const dotSize = kind === "group" ? 7
                : kind === "substantive" ? 6
                : kind === "standard" ? 4
                : 5;
  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "flex",
        width: "100%",
        alignItems: "center",
        gap: 12,
        minHeight: dense ? 40 : 48,
        padding: dense ? "8px 10px" : "10px 10px",
        margin: "0 -10px",
        background: hover ? "rgba(14,14,14,0.04)" : "transparent",
        border: "none",
        textAlign: "left",
        cursor: "pointer",
        fontFamily: '"IBM Plex Serif", Georgia, serif',
        transition: `background 160ms ${EASE}`,
      }}
    >
      {kind && (
        <span style={{
          width: dotSize, height: dotSize, borderRadius: "50%",
          background: dot, flexShrink: 0,
        }}></span>
      )}
      <div style={{ minWidth: 0, flex: 1 }}>
        <div style={{
          fontSize: 14.5,
          color: "#0E0E0E",
          fontWeight: 400,
          lineHeight: 1.3,
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
        }}>{title}</div>
        {sub && (
          <div style={{
            fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
            fontSize: 11.5,
            color: "#6B6B6B",
            marginTop: 3,
            letterSpacing: "0.01em",
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
          }}>{sub}</div>
        )}
      </div>
      <span style={{
        fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
        fontSize: 13,
        color: "#0E0E0E",
        opacity: hover ? 1 : 0,
        transform: hover ? "translateX(0)" : "translateX(-4px)",
        transition: `all 160ms ${EASE}`,
        flexShrink: 0,
      }}>→</span>
    </button>
  );
};

/* Common Region: a card-like grouping container w/ a heading.
   Uses a subtle background tint instead of hard borders. */
const Group = ({ heading, count, children, action, style }) => (
  <section style={{
    background: "rgba(14,14,14,0.025)",
    padding: "14px 14px 8px 14px",
    marginBottom: 16,
    ...(style || {}),
  }}>
    <header style={{
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between",
      marginBottom: 6,
      paddingBottom: 6,
    }}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 8 }}>
        <MetaLabel>{heading}</MetaLabel>
        {typeof count === "number" && (
          <span style={{
            fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
            fontSize: 10.5,
            color: "#9A9A9A",
            fontVariantNumeric: "tabular-nums",
          }}>{count}</span>
        )}
      </div>
      {action}
    </header>
    {children}
  </section>
);

const SectionHeading = ({ children, count }) => (
  <div style={{
    display: "flex",
    alignItems: "baseline",
    justifyContent: "space-between",
    marginBottom: 4,
  }}>
    <MetaLabel>{children}</MetaLabel>
    {typeof count === "number" && (
      <div style={{
        fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
        fontSize: 10.5,
        color: "#9A9A9A",
        fontVariantNumeric: "tabular-nums",
      }}>{count}</div>
    )}
  </div>
);

/* Show more / collapse — Miller's Law */
const ShowMore = ({ remaining, onClick }) => (
  <button onClick={onClick} style={{
    width: "100%",
    fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
    fontSize: 11.5,
    letterSpacing: "0.06em",
    textTransform: "uppercase",
    color: "#3C3C3C",
    background: "transparent",
    border: "none",
    padding: "10px 0 4px 0",
    cursor: "pointer",
    textAlign: "left",
    fontWeight: 500,
  }}>
    Show {remaining} more <span style={{ opacity: 0.5 }}>↓</span>
  </button>
);

/* Primary CTA — Fitts-friendly: full width, 48px tall, pinned in footer */
const PrimaryCTA = ({ children, onClick, shortcut }) => (
  <button
    onClick={onClick}
    style={{
      width: "100%",
      minHeight: 48,
      fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
      fontSize: 13.5,
      letterSpacing: "0.04em",
      color: "#FAFAF7",
      background: "#0E0E0E",
      border: "none",
      padding: "13px 18px",
      cursor: "pointer",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      fontWeight: 500,
      transition: `background 160ms ${EASE}`,
    }}
    onMouseEnter={(e) => e.currentTarget.style.background = "#2A2A2A"}
    onMouseLeave={(e) => e.currentTarget.style.background = "#0E0E0E"}
  >
    <span>{children}</span>
    <span style={{ display: "flex", alignItems: "center", gap: 10 }}>
      {shortcut && (
        <kbd style={{
          fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
          fontSize: 10,
          padding: "2px 6px",
          border: "1px solid rgba(250,250,247,0.35)",
          borderRadius: 3,
          color: "rgba(250,250,247,0.75)",
          letterSpacing: "0.02em",
          fontWeight: 500,
        }}>{shortcut}</kbd>
      )}
      <span style={{ fontSize: 14 }}>→</span>
    </span>
  </button>
);

const SecondaryButton = ({ children, onClick, icon }) => (
  <button onClick={onClick} style={{
    minHeight: 36,
    fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
    fontSize: 12,
    letterSpacing: "0.04em",
    color: "#0E0E0E",
    background: "transparent",
    border: "1px solid rgba(14,14,14,0.2)",
    padding: "8px 14px",
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    gap: 8,
    fontWeight: 500,
    transition: `all 160ms ${EASE}`,
  }}>
    {icon}{children}
  </button>
);

const GhostLink = ({ children, href }) => (
  <a href={href || "#"} target="_blank" rel="noreferrer" style={{
    fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
    fontSize: 12.5,
    color: "#0E0E0E",
    textDecoration: "none",
    borderBottom: "1px solid rgba(14,14,14,0.4)",
    paddingBottom: 1,
    display: "inline-flex",
    alignItems: "center",
    gap: 6,
  }}>{children}</a>
);

/* Fitts-friendly close button — 36×36, top-right corner (Fitts: corners are infinite-target zones) */
const CloseButton = ({ onClick, label = "Close" }) => (
  <button
    onClick={onClick}
    aria-label={label}
    title={`${label} (Esc)`}
    style={{
      width: 36, height: 36,
      background: "transparent",
      border: "none",
      cursor: "pointer",
      color: "#3C3C3C",
      display: "flex", alignItems: "center", justifyContent: "center",
      fontSize: 20,
      padding: 0,
      fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
      transition: `background 160ms ${EASE}`,
      borderRadius: 4,
    }}
    onMouseEnter={(e) => e.currentTarget.style.background = "rgba(14,14,14,0.06)"}
    onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}
  >×</button>
);

/* Collapse-panel toggle — sits on the LEFT edge of the panel so it's always
   reachable. 44×44 for Fitts. Distinct icon for collapse vs expand. */
const CollapseButton = ({ collapsed, onClick, position = "outside" }) => (
  <button
    onClick={onClick}
    aria-label={collapsed ? "Expand panel" : "Collapse panel"}
    title={`${collapsed ? "Expand" : "Collapse"} panel ( [ )`}
    style={{
      position: "absolute",
      top: 22,
      left: position === "outside" ? -18 : 8,
      width: 36, height: 36,
      background: "#FAFAF7",
      border: "1px solid rgba(14,14,14,0.12)",
      borderRadius: 4,
      cursor: "pointer",
      color: "#3C3C3C",
      display: "flex", alignItems: "center", justifyContent: "center",
      padding: 0,
      zIndex: 5,
      transition: `all 160ms ${EASE}`,
      fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
    }}
    onMouseEnter={(e) => {
      e.currentTarget.style.background = "#0E0E0E";
      e.currentTarget.style.color = "#FAFAF7";
    }}
    onMouseLeave={(e) => {
      e.currentTarget.style.background = "#FAFAF7";
      e.currentTarget.style.color = "#3C3C3C";
    }}
  >
    <span style={{ fontSize: 14, lineHeight: 1, transform: collapsed ? "rotate(180deg)" : "none" }}>›</span>
  </button>
);

/* Keyboard hint pill */
const KeyHint = ({ children }) => (
  <kbd style={{
    fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
    fontSize: 10,
    padding: "2px 6px",
    border: "1px solid rgba(14,14,14,0.18)",
    borderRadius: 3,
    color: "#6B6B6B",
    background: "rgba(14,14,14,0.02)",
    letterSpacing: "0.02em",
    fontWeight: 500,
  }}>{children}</kbd>
);

Object.assign(window, {
  Hairline, MetaLabel, Breadcrumb, LensBadge, ListRow,
  Group, SectionHeading, ShowMore,
  PrimaryCTA, SecondaryButton, GhostLink,
  CloseButton, CollapseButton, KeyHint,
  EASE,
});
