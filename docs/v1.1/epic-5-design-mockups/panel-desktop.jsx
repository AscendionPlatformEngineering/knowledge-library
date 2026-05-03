/* Desktop panel — applying Laws of UX:
   - Fixed header w/ breadcrumb + close (Serial Position: primacy & corner reachability)
   - Fixed footer CTA (Serial Position: recency, peak-end)
   - Group containers (Common Region) for Related / Standards / etc.
   - Miller's Law: lists capped at 5–7 visible w/ Show More
   - Goal-Gradient: counts shown on every section
   - Collapse rail variant
*/

function DesktopPanel({ children, footer, onCollapse, collapsed }) {
  if (collapsed) return <CollapsedRail onExpand={onCollapse} />;
  return (
    <aside style={{
      position: "absolute",
      top: 0, right: 0, bottom: 0,
      width: 400,
      background: "#FAFAF7",
      borderLeft: "1px solid rgba(14,14,14,0.12)",
      display: "flex",
      flexDirection: "column",
      fontFamily: '"IBM Plex Serif", Georgia, serif',
    }}>
      {onCollapse && <CollapseButton collapsed={false} onClick={onCollapse} />}
      <div style={{ flex: 1, overflow: "auto", display: "flex", flexDirection: "column" }}>
        {children}
      </div>
      {footer && (
        <div style={{
          borderTop: "1px solid rgba(14,14,14,0.12)",
          padding: "14px 20px 16px 20px",
          background: "#FAFAF7",
        }}>{footer}</div>
      )}
    </aside>
  );
}

/* Collapsed rail — 56px wide, vertical mini-summary so users don't lose context */
function CollapsedRail({ onExpand }) {
  return (
    <aside style={{
      position: "absolute",
      top: 0, right: 0, bottom: 0,
      width: 56,
      background: "#FAFAF7",
      borderLeft: "1px solid rgba(14,14,14,0.12)",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      paddingTop: 22,
      gap: 18,
    }}>
      <button
        onClick={onExpand}
        aria-label="Expand panel"
        title="Expand panel ( [ )"
        style={{
          width: 36, height: 36,
          background: "transparent",
          border: "1px solid rgba(14,14,14,0.12)",
          borderRadius: 4,
          cursor: "pointer",
          fontSize: 14, color: "#3C3C3C",
        }}
      >‹</button>
      <div style={{ width: 1, height: 24, background: "rgba(14,14,14,0.12)" }}></div>
      {/* Vertical title */}
      <div style={{
        writingMode: "vertical-rl",
        transform: "rotate(180deg)",
        fontFamily: '"IBM Plex Serif", Georgia, serif',
        fontSize: 14,
        color: "#0E0E0E",
        letterSpacing: "0.02em",
        marginTop: 6,
      }}>PCI DSS</div>
      <span style={{ width: 7, height: 7, borderRadius: "50%", background: "#D97A3C" }}></span>
      <div style={{
        flex: 1,
      }}></div>
      <div style={{
        marginBottom: 18,
        writingMode: "vertical-rl",
        transform: "rotate(180deg)",
        fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
        fontSize: 9.5,
        letterSpacing: "0.16em",
        textTransform: "uppercase",
        color: "#9A9A9A",
      }}>panel collapsed</div>
    </aside>
  );
}

/* Header pattern reused across non-empty states */
const PanelHeader = ({ children, onClose, sticky }) => (
  <div style={{
    position: sticky ? "sticky" : "static",
    top: 0,
    background: "#FAFAF7",
    padding: "20px 28px 14px 28px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: 12,
    zIndex: 2,
  }}>
    <div style={{ minWidth: 0, flex: 1, paddingTop: 6 }}>{children}</div>
    <CloseButton onClick={onClose} />
  </div>
);

/* ---------- State 1: Empty ---------- */
function PanelEmpty({ onCollapse }) {
  return (
    <DesktopPanel onCollapse={onCollapse}>
      <div style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: "26px 28px 24px 28px",
      }}>
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}>
          <MetaLabel>panel</MetaLabel>
          <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
            <KeyHint>Esc</KeyHint>
            <span style={{ fontSize: 11, color: "#9A9A9A", fontFamily: '"IBM Plex Sans", system-ui, sans-serif' }}>to clear</span>
          </div>
        </div>

        <div style={{ paddingRight: 12 }}>
          <div style={{ display: "flex", gap: 14, marginBottom: 28, opacity: 0.7 }}>
            <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#0E0E0E" }}></span>
            <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#D97A3C", marginTop: 1 }}></span>
            <span style={{ width: 5, height: 5, borderRadius: "50%", background: "#3C3C3C", marginTop: 2 }}></span>
          </div>
          <p style={{
            fontFamily: '"IBM Plex Serif", Georgia, serif',
            fontStyle: "italic",
            fontSize: 19,
            lineHeight: 1.5,
            color: "#3C3C3C",
            margin: 0,
            textWrap: "pretty",
          }}>
            Click any node to open it here. Pages, standards, and topic groups —
            explore relationships without losing your place.
          </p>
        </div>

        <div>
          <Hairline style={{ marginBottom: 16 }} />
          <MetaLabel style={{ marginBottom: 12 }}>legend</MetaLabel>
          <div style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "10px 14px",
            fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
            marginBottom: 18,
          }}>
            <LegendRow color="#0E0E0E" label="Topic group" size={9} />
            <LegendRow color="#D97A3C" label="Substantive page" size={6} />
            <LegendRow color="#3C3C3C" label="Page" size={5} opacity={0.55} />
            <LegendRow color="#9A9A9A" label="Standard" size={3} opacity={0.7} />
          </div>
          <Hairline style={{ marginBottom: 14 }} />
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <KeyboardRow keys={["⌘", "K"]} label="Search" />
            <KeyboardRow keys={["Esc"]} label="Close panel" />
            <KeyboardRow keys={["["]} label="Collapse panel" />
          </div>
        </div>
      </div>
    </DesktopPanel>
  );
}

const LegendRow = ({ color, label, size, opacity }) => (
  <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
    <span style={{
      width: size, height: size, borderRadius: "50%",
      background: color, opacity: opacity || 1,
      flexShrink: 0,
    }}></span>
    <span style={{ fontSize: 11.5, color: "#6B6B6B", letterSpacing: "0.02em" }}>{label}</span>
  </div>
);

const KeyboardRow = ({ keys, label }) => (
  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
    <span style={{
      fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
      fontSize: 11.5, color: "#6B6B6B", letterSpacing: "0.02em",
    }}>{label}</span>
    <span style={{ display: "flex", gap: 4 }}>
      {keys.map((k, i) => <KeyHint key={i}>{k}</KeyHint>)}
    </span>
  </div>
);

/* ---------- State 2: Page ---------- */
function PanelPage({ onCollapse }) {
  const related = [
    { t: "Tokenization patterns for cardholder data", k: "substantive" },
    { t: "Audit trail retention", k: "page" },
    { t: "SAQ-D vs SAQ-A scoping", k: "page" },
    { t: "Network segmentation reference", k: "page" },
    { t: "Vendor risk assessment workflow", k: "page" },
  ];
  const standards = [
    { t: "PCI DSS v4.0", o: "PCI Council · Public reference" },
    { t: "PCI DSS v3.2.1", o: "PCI Council · Public reference" },
    { t: "NIST SP 800-53 r5", o: "NIST · Public domain" },
    { t: "ISO/IEC 27001:2022", o: "ISO · Licensed excerpt" },
    { t: "SOC 2 Trust Services", o: "AICPA · Licensed excerpt" },
  ];

  return (
    <DesktopPanel
      onCollapse={onCollapse}
      footer={<PrimaryCTA shortcut="↵">Open page</PrimaryCTA>}
    >
      <PanelHeader sticky>
        <Breadcrumb section="Compliance" page="PCI DSS" />
      </PanelHeader>

      <div style={{ padding: "0 28px 24px 28px", flex: 1 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
          <span style={{ width: 9, height: 9, borderRadius: "50%", background: "#D97A3C" }}></span>
          <MetaLabel style={{ color: "#A85420" }}>substantive page</MetaLabel>
        </div>

        <h1 style={{
          fontFamily: '"IBM Plex Serif", Georgia, serif',
          fontWeight: 400,
          fontSize: 32,
          lineHeight: 1.1,
          letterSpacing: "-0.01em",
          margin: "4px 0 14px 0",
          color: "#0E0E0E",
          textWrap: "balance",
        }}>PCI DSS</h1>

        <div style={{ marginBottom: 14 }}>
          <LensBadge label="Debt Ledger" />
        </div>

        <p style={{
          fontFamily: '"IBM Plex Serif", Georgia, serif',
          fontSize: 14.5,
          lineHeight: 1.55,
          color: "#3C3C3C",
          margin: "0 0 22px 0",
          textWrap: "pretty",
        }}>
          The Payment Card Industry Data Security Standard governs how
          cardholder data must be stored, processed, and transmitted. This
          page reconciles v3.2.1 control families with v4.0 customized
          approaches.
        </p>

        <Group heading="Related pages" count={5}>
          {related.map((r, i) => (
            <ListRow key={i} title={r.t} kind={r.k} dense />
          ))}
        </Group>

        <Group
          heading="Aligned standards"
          count={7}
          action={<span style={{ fontSize: 10.5, color: "#9A9A9A", letterSpacing: "0.06em", fontFamily: '"IBM Plex Sans", system-ui, sans-serif', textTransform: "uppercase" }}>5 of 7</span>}
        >
          {standards.map((s, i) => (
            <ListRow key={i} title={s.t} sub={s.o} kind="standard" dense />
          ))}
          <ShowMore remaining={2} />
        </Group>
      </div>
    </DesktopPanel>
  );
}

/* ---------- State 3: Standard ---------- */
function PanelStandard({ onCollapse }) {
  const pages = [
    { t: "PCI DSS", k: "substantive" },
    { t: "Cardholder data tokenization", k: "substantive" },
    { t: "Network segmentation reference", k: "page" },
    { t: "SAQ-D vs SAQ-A scoping", k: "page" },
    { t: "Audit trail retention", k: "page" },
    { t: "Encryption-at-rest patterns", k: "page" },
  ];
  return (
    <DesktopPanel onCollapse={onCollapse}>
      <PanelHeader sticky>
        <MetaLabel>standard</MetaLabel>
      </PanelHeader>

      <div style={{ padding: "0 28px 28px 28px", flex: 1 }}>
        <h1 style={{
          fontFamily: '"IBM Plex Serif", Georgia, serif',
          fontWeight: 400,
          fontSize: 26,
          lineHeight: 1.15,
          letterSpacing: "-0.005em",
          margin: "0 0 18px 0",
        }}>PCI DSS v4.0</h1>

        <dl style={{
          margin: "0 0 18px 0",
          fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
          fontSize: 12.5,
          display: "grid",
          gridTemplateColumns: "120px 1fr",
          rowGap: 8,
          columnGap: 14,
        }}>
          <dt style={{ color: "#6B6B6B", letterSpacing: "0.04em" }}>Organization</dt>
          <dd style={{ margin: 0, color: "#0E0E0E" }}>PCI Security Standards Council</dd>

          <dt style={{ color: "#6B6B6B", letterSpacing: "0.04em" }}>License</dt>
          <dd style={{ margin: 0, color: "#0E0E0E" }}>Public reference</dd>

          <dt style={{ color: "#6B6B6B", letterSpacing: "0.04em" }}>Last verified</dt>
          <dd style={{ margin: 0, color: "#0E0E0E", fontVariantNumeric: "tabular-nums" }}>May 2026</dd>
        </dl>

        <p style={{
          fontFamily: '"IBM Plex Serif", Georgia, serif',
          fontSize: 14.5,
          lineHeight: 1.55,
          color: "#3C3C3C",
          margin: "0 0 18px 0",
          textWrap: "pretty",
        }}>
          Released March 2022 with a transition deadline of 31 March 2024,
          v4.0 introduces customized validation and shifts several requirements
          from prescriptive controls to outcome-based objectives.
        </p>

        <div style={{ marginBottom: 22 }}>
          <SecondaryButton icon={<span style={{ fontSize: 12 }}>↗</span>}>
            Open source
          </SecondaryButton>
        </div>

        <Group heading="Pages aligning with this standard" count={6}>
          {pages.map((p, i) => (
            <ListRow key={i} title={p.t} kind={p.k} dense />
          ))}
        </Group>
      </div>
    </DesktopPanel>
  );
}

/* ---------- State 4: Topic group ---------- */
function PanelTopic({ onCollapse }) {
  const members = [
    { t: "PCI DSS", d: "Cardholder data storage, processing, transmission.", k: "substantive" },
    { t: "HIPAA & PHI handling", d: "Protected health information across our stack.", k: "page" },
    { t: "SOC 2 readiness", d: "Trust services criteria, evidence cadence, gaps.", k: "substantive" },
    { t: "GDPR data subject requests", d: "DSAR intake, fulfillment SLAs, audit.", k: "page" },
    { t: "FedRAMP moderate baseline", d: "Control inheritance from cloud provider.", k: "page" },
    { t: "Export controls (EAR/ITAR)", d: "Where engineering must consult counsel.", k: "page" },
    { t: "State privacy patchwork", d: "CCPA, VCDPA, CTDPA — what overlaps.", k: "page" },
  ];
  return (
    <DesktopPanel onCollapse={onCollapse}>
      <PanelHeader sticky>
        <MetaLabel>topic group · 7 pages</MetaLabel>
      </PanelHeader>

      <div style={{ padding: "0 28px 28px 28px", flex: 1 }}>
        <h1 style={{
          fontFamily: '"IBM Plex Serif", Georgia, serif',
          fontWeight: 400,
          fontSize: 28,
          lineHeight: 1.12,
          letterSpacing: "-0.01em",
          margin: "0 0 14px 0",
          textWrap: "balance",
        }}>Compliance & Regulatory Frameworks</h1>

        <p style={{
          fontFamily: '"IBM Plex Serif", Georgia, serif',
          fontSize: 14.5,
          lineHeight: 1.55,
          color: "#3C3C3C",
          margin: "0 0 22px 0",
          textWrap: "pretty",
        }}>
          Pages that reconcile external regulatory regimes with our internal
          engineering posture — what we owe, what we've shipped, and where
          the two diverge.
        </p>

        <Group heading="Member pages" count={members.length}>
          {members.map((m, i) => (
            <ListRow key={i} title={m.t} sub={m.d} kind={m.k} />
          ))}
        </Group>
      </div>
    </DesktopPanel>
  );
}

/* ---------- State 5: Search (with sort) ---------- */
function PanelSearch({ onCollapse }) {
  const [filter, setFilter] = React.useState("All");
  const [sort, setSort] = React.useState("Relevance");
  const [query, setQuery] = React.useState("cardholder");

  const allResults = [
    { t: "PCI DSS", k: "substantive", type: "Page", date: "2026-04", score: 0.98,
      s: "…cardholder data must be stored, processed, and <mark>transmitted</mark> per v4.0 customized approaches…" },
    { t: "Network segmentation reference", k: "page", type: "Page", date: "2026-03", score: 0.91,
      s: "…<mark>cardholder</mark> data environment isolated from corporate network via stateful inspection…" },
    { t: "Tokenization patterns", k: "substantive", type: "Page", date: "2025-11", score: 0.87,
      s: "…surrogate values replace <mark>cardholder</mark> PAN; reversibility scoped to vault service only…" },
    { t: "Audit trail retention", k: "page", type: "Page", date: "2026-02", score: 0.74,
      s: "…minimum one year, three months immediately available, including <mark>cardholder</mark> environment access…" },
    { t: "PCI DSS v4.0", k: "standard", type: "Standard", date: "2026-05", score: 0.69,
      s: "…requirements for protecting <mark>cardholder</mark> data; customized validation pathway…" },
  ];

  const sorted = React.useMemo(() => {
    const copy = [...allResults];
    if (sort === "A–Z") copy.sort((a, b) => a.t.localeCompare(b.t));
    else if (sort === "Recent") copy.sort((a, b) => b.date.localeCompare(a.date));
    else if (sort === "Type") copy.sort((a, b) => a.type.localeCompare(b.type));
    return copy;
  }, [sort]);

  return (
    <DesktopPanel onCollapse={onCollapse}>
      <div style={{
        padding: "20px 28px 14px 28px",
        position: "sticky", top: 0, background: "#FAFAF7", zIndex: 3,
        borderBottom: "1px solid rgba(14,14,14,0.08)",
      }}>
        <div style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          marginBottom: 10,
        }}>
          <MetaLabel>search</MetaLabel>
          <CloseButton />
        </div>

        <div style={{ position: "relative", marginBottom: 14 }}>
          <span style={{
            position: "absolute", left: 0, top: 12,
            fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
            fontSize: 16, color: "#6B6B6B",
          }}>⌕</span>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search the graph"
            style={{
              width: "100%",
              boxSizing: "border-box",
              background: "transparent",
              border: "none",
              borderBottom: "1.5px solid #0E0E0E",
              padding: "8px 60px 8px 26px",
              fontFamily: '"IBM Plex Serif", Georgia, serif',
              fontSize: 22,
              color: "#0E0E0E",
              outline: "none",
              fontStyle: query ? "italic" : "normal",
            }}
          />
          <span style={{
            position: "absolute", right: 0, top: 12,
            display: "flex", alignItems: "center", gap: 6,
          }}>
            <KeyHint>⌘K</KeyHint>
          </span>
        </div>

        {/* Filter chips (Hick's Law: 4 grouped buckets) */}
        <div style={{ display: "flex", gap: 6, marginBottom: 10, flexWrap: "wrap" }}>
          {[
            { l: "All", n: 12 },
            { l: "Pages", n: 5 },
            { l: "Standards", n: 4 },
            { l: "Groups", n: 3 },
          ].map((f) => (
            <Chip key={f.l}
              active={filter === f.l}
              onClick={() => setFilter(f.l)}
            >{f.l} <span style={{ opacity: 0.6, marginLeft: 3 }}>{f.n}</span></Chip>
          ))}
        </div>

        {/* Sort row */}
        <div style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          paddingTop: 4,
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <span style={{
              fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
              fontSize: 10.5, color: "#6B6B6B",
              letterSpacing: "0.08em", textTransform: "uppercase",
            }}>Sort</span>
            <SortMenu value={sort} onChange={setSort} />
          </div>
          <span style={{
            fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
            fontSize: 10.5, color: "#9A9A9A",
            letterSpacing: "0.06em", textTransform: "uppercase",
            fontVariantNumeric: "tabular-nums",
          }}>{sorted.length} results · 0.04s</span>
        </div>
      </div>

      <div style={{ padding: "10px 28px 24px 28px", flex: 1 }}>
        {sorted.map((r, i) => (
          <SearchResultRow key={i} title={r.t} snippet={r.s} kind={r.k} type={r.type} date={r.date} />
        ))}
      </div>
    </DesktopPanel>
  );
}

const Chip = ({ children, active, onClick }) => (
  <button onClick={onClick} style={{
    fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
    fontSize: 11,
    letterSpacing: "0.04em",
    minHeight: 28,
    padding: "5px 11px",
    background: active ? "#0E0E0E" : "transparent",
    color: active ? "#FAFAF7" : "#3C3C3C",
    border: active ? "1px solid #0E0E0E" : "1px solid rgba(14,14,14,0.18)",
    borderRadius: 999,
    cursor: "pointer",
    transition: `all 160ms ${EASE}`,
    fontWeight: 500,
  }}>{children}</button>
);

/* Native-styled sort menu — Jakob's Law (familiar select pattern) */
function SortMenu({ value, onChange }) {
  return (
    <div style={{ position: "relative", display: "inline-block" }}>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{
          appearance: "none",
          WebkitAppearance: "none",
          background: "transparent",
          border: "1px solid rgba(14,14,14,0.18)",
          borderRadius: 4,
          fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
          fontSize: 11.5,
          color: "#0E0E0E",
          padding: "5px 24px 5px 10px",
          letterSpacing: "0.02em",
          cursor: "pointer",
          minHeight: 28,
          fontWeight: 500,
        }}
      >
        <option>Relevance</option>
        <option>Recent</option>
        <option>A–Z</option>
        <option>Type</option>
      </select>
      <span style={{
        position: "absolute", right: 8, top: 7,
        fontSize: 10, color: "#6B6B6B", pointerEvents: "none",
      }}>▾</span>
    </div>
  );
}

function SearchResultRow({ title, snippet, kind, type, date }) {
  const [hover, setHover] = React.useState(false);
  const dot = kind === "substantive" ? "#D97A3C"
            : kind === "standard" ? "#9A9A9A"
            : "#3C3C3C";
  return (
    <button
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "flex",
        width: "100%",
        alignItems: "flex-start",
        gap: 12,
        padding: "12px 10px",
        margin: "0 -10px",
        background: hover ? "rgba(14,14,14,0.04)" : "transparent",
        border: "none",
        textAlign: "left",
        cursor: "pointer",
        fontFamily: '"IBM Plex Serif", Georgia, serif',
        transition: `background 160ms ${EASE}`,
      }}
    >
      <span style={{
        width: 6, height: 6, borderRadius: "50%",
        background: dot, flexShrink: 0, marginTop: 8,
      }}></span>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          display: "flex", alignItems: "baseline", gap: 8,
          justifyContent: "space-between",
          marginBottom: 3,
        }}>
          <span style={{ fontSize: 14.5, color: "#0E0E0E", fontWeight: 400 }}>{title}</span>
          <span style={{
            fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
            fontSize: 10, color: "#9A9A9A",
            letterSpacing: "0.06em", textTransform: "uppercase",
            flexShrink: 0,
          }}>{type} · {date}</span>
        </div>
        <div
          style={{
            fontFamily: '"IBM Plex Serif", Georgia, serif',
            fontStyle: "italic",
            fontSize: 13,
            color: "#6B6B6B",
            lineHeight: 1.45,
          }}
          dangerouslySetInnerHTML={{ __html: snippet.replace(/<mark>/g, '<mark style="background:rgba(217,122,60,0.22);color:#A85420;font-style:normal;padding:0 2px;">') }}
        ></div>
      </div>
      <span style={{
        fontSize: 14, color: "#0E0E0E",
        opacity: hover ? 1 : 0,
        transform: hover ? "translateX(0)" : "translateX(-4px)",
        transition: `all 160ms ${EASE}`,
        marginTop: 4,
      }}>→</span>
    </button>
  );
}

Object.assign(window, {
  DesktopPanel, CollapsedRail,
  PanelEmpty, PanelPage, PanelStandard, PanelTopic, PanelSearch,
  SearchResultRow, SortMenu, Chip,
});
