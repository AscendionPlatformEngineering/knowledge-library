/* Mobile drawer — Laws of UX:
   - Fitts: 44px+ row targets, 56×56 close hit area, fat drawer handle
   - Jakob: standard bottom-sheet pattern w/ peek/half/full
   - Doherty: 160ms transitions
   - Common Region: grouped sections w/ tinted bands
   - Aesthetic-Usability: editorial calm preserved on small screens
*/

const PHONE_W = 390;
const PHONE_H = 760;
const STATUS_BAR_H = 40;

function PhoneFrame({ children, dim }) {
  return (
    <div style={{
      width: PHONE_W,
      height: PHONE_H,
      background: "#FAFAF7",
      position: "relative",
      overflow: "hidden",
      fontFamily: '"IBM Plex Serif", Georgia, serif',
      borderLeft: "1px solid rgba(14,14,14,0.08)",
      borderRight: "1px solid rgba(14,14,14,0.08)",
    }}>
      <div style={{
        height: STATUS_BAR_H,
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "0 22px 0 26px",
        fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
        fontSize: 13, color: "#0E0E0E", fontWeight: 600,
        fontVariantNumeric: "tabular-nums",
        position: "relative", zIndex: 5,
      }}>
        <span>9:41</span>
        <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
          <span style={{ width: 16, height: 9, border: "1px solid #0E0E0E", borderRadius: 2, position: "relative" }}>
            <span style={{ position: "absolute", inset: 1, right: 4, background: "#0E0E0E" }}></span>
          </span>
        </div>
      </div>

      <div style={{
        height: 44,
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "0 14px",
        borderBottom: "1px solid rgba(14,14,14,0.08)",
        fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
        fontSize: 11, letterSpacing: "0.14em", textTransform: "uppercase",
        color: "#6B6B6B", fontWeight: 500,
        position: "relative", zIndex: 5,
      }}>
        <button style={{
          minWidth: 44, height: 36, background: "transparent", border: "none",
          color: "#3C3C3C", fontSize: 13, letterSpacing: "0.04em",
          textTransform: "none", fontWeight: 500, cursor: "pointer",
          textAlign: "left", padding: "0 6px",
        }}>← Graph</button>
        <span style={{ color: "#0E0E0E" }}>knowledge</span>
        <button style={{
          width: 44, height: 36, background: "transparent", border: "none",
          color: "#3C3C3C", fontSize: 16, cursor: "pointer",
        }}>⌕</button>
      </div>

      <div style={{
        position: "absolute",
        top: STATUS_BAR_H + 44, left: 0, right: 0, bottom: 0,
      }}>
        <GraphBackdrop width={PHONE_W} height={PHONE_H - STATUS_BAR_H - 44} variant="page" />
        {dim && (
          <div style={{
            position: "absolute", inset: 0,
            background: "rgba(14,14,14,0.36)",
            transition: `opacity 160ms ${EASE}`,
          }}></div>
        )}
      </div>

      {children}
    </div>
  );
}

/* Drawer handle: 56px tall hit area for Fitts (visual grip is small but
   tappable area extends across the full top of the drawer) */
const DrawerHandle = ({ label }) => (
  <div style={{
    width: "100%",
    minHeight: 28,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    paddingTop: 8,
    paddingBottom: 6,
    cursor: "grab",
    touchAction: "none",
  }}>
    <div style={{
      width: 44, height: 4,
      borderRadius: 4,
      background: "rgba(14,14,14,0.22)",
    }}></div>
    {label && (
      <div style={{
        fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
        fontSize: 9.5, letterSpacing: "0.14em",
        textTransform: "uppercase", color: "#9A9A9A",
        marginTop: 6,
      }}>{label}</div>
    )}
  </div>
);

function Drawer({ height, children, peek }) {
  return (
    <div style={{
      position: "absolute",
      left: 0, right: 0, bottom: 0,
      height,
      background: "#FAFAF7",
      borderTop: "1px solid rgba(14,14,14,0.12)",
      display: "flex",
      flexDirection: "column",
      boxShadow: peek ? "0 -2px 12px rgba(14,14,14,0.04)" : "0 -8px 32px rgba(14,14,14,0.08)",
      zIndex: 10,
      transition: `height 200ms ${EASE}`,
    }}>
      <DrawerHandle label={peek ? "swipe up" : null} />
      {children}
    </div>
  );
}

/* ---- Mobile state 1: empty (no drawer, hint pill) ---- */
function MobileEmpty() {
  return (
    <PhoneFrame>
      <div style={{
        position: "absolute", left: 0, right: 0, bottom: 28,
        display: "flex", justifyContent: "center", zIndex: 8,
      }}>
        <div style={{
          background: "#FAFAF7",
          border: "1px solid rgba(14,14,14,0.18)",
          padding: "12px 18px",
          fontFamily: '"IBM Plex Serif", Georgia, serif',
          fontStyle: "italic", fontSize: 13.5, color: "#3C3C3C",
          maxWidth: 320, textAlign: "center", lineHeight: 1.4,
        }}>
          Tap any node to open it. Drag to pan, pinch to zoom.
        </div>
      </div>
    </PhoneFrame>
  );
}

/* ---- Mobile state 2: page peek (60px) ---- */
function MobilePagePeek() {
  return (
    <PhoneFrame>
      <Drawer height={66} peek>
        <div style={{
          padding: "0 18px",
          minHeight: 38,
          display: "flex", alignItems: "center", justifyContent: "space-between",
          gap: 12,
        }}>
          <div style={{ minWidth: 0, flex: 1 }}>
            <div style={{
              fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
              fontSize: 9.5, letterSpacing: "0.12em",
              textTransform: "uppercase", color: "#6B6B6B",
              marginBottom: 2,
            }}>Compliance · page</div>
            <div style={{
              fontFamily: '"IBM Plex Serif", Georgia, serif',
              fontSize: 17, color: "#0E0E0E",
              whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
            }}>PCI DSS</div>
          </div>
          <span style={{
            width: 8, height: 8, borderRadius: "50%",
            background: "#D97A3C", flexShrink: 0,
          }}></span>
        </div>
      </Drawer>
    </PhoneFrame>
  );
}

/* ---- Mobile state 3: page open (~60% viewport) ---- */
function MobilePageOpen() {
  const drawerH = Math.round(PHONE_H * 0.62);
  return (
    <PhoneFrame dim>
      <Drawer height={drawerH}>
        <div style={{
          padding: "4px 18px 0 18px",
          flex: 1, minHeight: 0,
          display: "flex", flexDirection: "column",
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
            <Breadcrumb section="Compliance" page="PCI DSS" />
            <CloseButton />
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
            <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#D97A3C" }}></span>
            <MetaLabel style={{ color: "#A85420" }}>substantive page</MetaLabel>
          </div>
          <h2 style={{
            fontFamily: '"IBM Plex Serif", Georgia, serif',
            fontSize: 26, fontWeight: 400,
            margin: "6px 0 12px 0",
            letterSpacing: "-0.01em",
          }}>PCI DSS</h2>

          <div style={{ marginBottom: 12 }}><LensBadge label="Debt Ledger" /></div>

          <p style={{
            fontFamily: '"IBM Plex Serif", Georgia, serif',
            fontSize: 13.5, lineHeight: 1.5, color: "#3C3C3C",
            margin: "0 0 14px 0",
          }}>
            Reconciles v3.2.1 control families with v4.0 customized approaches
            and notes where our internal posture has accrued debt.
          </p>

          <div style={{ flex: 1, overflow: "auto", margin: "0 -4px", padding: "0 4px" }}>
            <Group heading="Related" count={5}>
              {["Tokenization patterns",
                "Audit trail retention",
                "SAQ-D vs SAQ-A scoping",
                "Network segmentation reference"].map((t, i) =>
                <ListRow key={i} title={t} kind={i === 0 ? "substantive" : "page"} dense />
              )}
              <ShowMore remaining={1} />
            </Group>
          </div>
        </div>
        <div style={{
          padding: "10px 16px 16px 16px",
          borderTop: "1px solid rgba(14,14,14,0.08)",
          background: "#FAFAF7",
        }}>
          <PrimaryCTA shortcut="↵">Open page</PrimaryCTA>
        </div>
      </Drawer>
    </PhoneFrame>
  );
}

/* ---- Mobile state 4: standard (open) ---- */
function MobileStandard() {
  const drawerH = Math.round(PHONE_H * 0.62);
  return (
    <PhoneFrame dim>
      <Drawer height={drawerH}>
        <div style={{ padding: "4px 18px 18px 18px", flex: 1, minHeight: 0, overflow: "auto" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 10 }}>
            <MetaLabel>standard</MetaLabel>
            <CloseButton />
          </div>
          <h2 style={{
            fontFamily: '"IBM Plex Serif", Georgia, serif',
            fontSize: 22, fontWeight: 400, margin: "0 0 14px 0",
          }}>PCI DSS v4.0</h2>

          <dl style={{
            margin: "0 0 14px 0",
            fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
            fontSize: 11.5,
            display: "grid", gridTemplateColumns: "100px 1fr",
            rowGap: 6, columnGap: 12,
          }}>
            <dt style={{ color: "#6B6B6B" }}>Organization</dt>
            <dd style={{ margin: 0 }}>PCI Security Standards Council</dd>
            <dt style={{ color: "#6B6B6B" }}>License</dt>
            <dd style={{ margin: 0 }}>Public reference</dd>
            <dt style={{ color: "#6B6B6B" }}>Last verified</dt>
            <dd style={{ margin: 0, fontVariantNumeric: "tabular-nums" }}>May 2026</dd>
          </dl>
          <p style={{
            fontFamily: '"IBM Plex Serif", Georgia, serif',
            fontSize: 13, lineHeight: 1.5, color: "#3C3C3C",
            margin: "0 0 14px 0",
          }}>
            Released March 2022. Introduces customized validation and shifts
            requirements toward outcome-based objectives.
          </p>
          <div style={{ marginBottom: 18 }}>
            <SecondaryButton icon={<span style={{ fontSize: 12 }}>↗</span>}>Open source</SecondaryButton>
          </div>

          <Group heading="Pages aligning" count={4}>
            {[
              { t: "PCI DSS", k: "substantive" },
              { t: "Cardholder data tokenization", k: "substantive" },
              { t: "Network segmentation reference", k: "page" },
              { t: "SAQ-D vs SAQ-A scoping", k: "page" },
            ].map((p, i) => <ListRow key={i} title={p.t} kind={p.k} dense />)}
          </Group>
        </div>
      </Drawer>
    </PhoneFrame>
  );
}

/* ---- Mobile state 5: topic group (full ~92%) ---- */
function MobileTopicFull() {
  const drawerH = Math.round(PHONE_H * 0.92);
  return (
    <PhoneFrame dim>
      <Drawer height={drawerH}>
        <div style={{ padding: "4px 18px 18px 18px", flex: 1, minHeight: 0, overflow: "auto" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 10 }}>
            <MetaLabel>topic group · 7 pages</MetaLabel>
            <CloseButton />
          </div>
          <h2 style={{
            fontFamily: '"IBM Plex Serif", Georgia, serif',
            fontSize: 26, fontWeight: 400, lineHeight: 1.12,
            margin: "0 0 14px 0", letterSpacing: "-0.01em",
            textWrap: "balance",
          }}>Compliance & Regulatory Frameworks</h2>
          <p style={{
            fontFamily: '"IBM Plex Serif", Georgia, serif',
            fontSize: 13.5, lineHeight: 1.5, color: "#3C3C3C",
            margin: "0 0 18px 0",
          }}>
            Pages that reconcile external regulatory regimes with our internal
            engineering posture.
          </p>

          <Group heading="Member pages" count={7}>
            {[
              { t: "PCI DSS", d: "Cardholder data storage & transit.", k: "substantive" },
              { t: "HIPAA & PHI handling", d: "PHI across our stack.", k: "page" },
              { t: "SOC 2 readiness", d: "Trust services, evidence cadence.", k: "substantive" },
              { t: "GDPR data subject requests", d: "DSAR intake, SLAs.", k: "page" },
              { t: "FedRAMP moderate baseline", d: "Control inheritance.", k: "page" },
              { t: "Export controls (EAR/ITAR)", d: "When to consult counsel.", k: "page" },
              { t: "State privacy patchwork", d: "CCPA, VCDPA, CTDPA overlaps.", k: "page" },
            ].map((m, i) => <ListRow key={i} title={m.t} sub={m.d} kind={m.k} />)}
          </Group>
        </div>
      </Drawer>
    </PhoneFrame>
  );
}

/* ---- Mobile state 6: search (full) ---- */
function MobileSearchFull() {
  const drawerH = Math.round(PHONE_H * 0.92);
  return (
    <PhoneFrame dim>
      <Drawer height={drawerH}>
        <div style={{ padding: "4px 18px 18px 18px", flex: 1, minHeight: 0, overflow: "auto" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
            <MetaLabel>search · placeholder</MetaLabel>
            <CloseButton />
          </div>

          <div style={{ position: "relative", marginBottom: 12 }}>
            <span style={{
              position: "absolute", left: 0, top: 9,
              fontSize: 14, color: "#6B6B6B",
            }}>⌕</span>
            <input
              defaultValue="cardholder"
              style={{
                width: "100%", boxSizing: "border-box",
                background: "transparent", border: "none",
                borderBottom: "1.5px solid #0E0E0E",
                padding: "8px 8px 8px 22px",
                fontFamily: '"IBM Plex Serif", Georgia, serif',
                fontSize: 18, color: "#0E0E0E", outline: "none",
                fontStyle: "italic",
              }}
            />
          </div>

          <div style={{ display: "flex", gap: 6, marginBottom: 10, flexWrap: "wrap" }}>
            {[
              { l: "All", n: 12, a: true },
              { l: "Pages", n: 5 },
              { l: "Standards", n: 4 },
              { l: "Groups", n: 3 },
            ].map((f, i) => (
              <Chip key={i} active={f.a}>{f.l} <span style={{ opacity: 0.6, marginLeft: 3 }}>{f.n}</span></Chip>
            ))}
          </div>

          <div style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: 10,
            paddingTop: 4,
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span style={{
                fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
                fontSize: 10.5, color: "#6B6B6B",
                letterSpacing: "0.08em", textTransform: "uppercase",
              }}>Sort</span>
              <SortMenu value="Relevance" onChange={() => {}} />
            </div>
            <span style={{
              fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
              fontSize: 10.5, color: "#9A9A9A",
              letterSpacing: "0.06em", textTransform: "uppercase",
              fontVariantNumeric: "tabular-nums",
            }}>5 results</span>
          </div>

          {[
            { t: "PCI DSS", k: "substantive", type: "Page", date: "2026-04",
              s: "…cardholder data must be stored, processed, and <mark>transmitted</mark> per v4.0…" },
            { t: "Network segmentation", k: "page", type: "Page", date: "2026-03",
              s: "…<mark>cardholder</mark> data environment isolated from corporate network…" },
            { t: "Tokenization patterns", k: "substantive", type: "Page", date: "2025-11",
              s: "…surrogate values replace <mark>cardholder</mark> PAN; vault-only reversibility…" },
            { t: "Audit trail retention", k: "page", type: "Page", date: "2026-02",
              s: "…minimum one year, three months immediately available, including <mark>cardholder</mark> access…" },
            { t: "PCI DSS v4.0", k: "standard", type: "Standard", date: "2026-05",
              s: "…requirements for protecting <mark>cardholder</mark> data; customized validation…" },
          ].map((r, i) => <SearchResultRow key={i} title={r.t} snippet={r.s} kind={r.k} type={r.type} date={r.date} />)}
        </div>
      </Drawer>
    </PhoneFrame>
  );
}

Object.assign(window, {
  PhoneFrame, Drawer, DrawerHandle,
  MobileEmpty, MobilePagePeek, MobilePageOpen,
  MobileStandard, MobileTopicFull, MobileSearchFull,
  PHONE_W, PHONE_H,
});
