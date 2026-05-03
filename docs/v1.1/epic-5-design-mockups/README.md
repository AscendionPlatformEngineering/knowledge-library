# EPIC-5 Design Mockups — v1.1 North Star

These mockups were produced via Claude Design (claude.ai/design) on
May 3 2026 as the visual reference for EPIC-5 through EPIC-10 of v1.1.

The full design includes features that are deferred beyond EPIC-5:
- Layout selector toolbar (Force/Radial/Tree/Matrix) — out of v1.1 scope
- Minimap (upper-right corner) — defer to EPIC-10 polish
- Neighborhood subtitle — defer to EPIC-6 or follow-up
- Sparse/Dense view toggle — defer or cut
- Debt Ledger lens chip in toolbar — defer to EPIC-6 (lens UI)
- Workspace v1.1 branding — defer or cut

EPIC-5 (T5.1) implements only:
- Panel shell with 70/30 grid layout
- 5 panel states (empty, page, standard, topic group, search placeholder)
- Collapsed rail (6th state)
- Mobile drawer with three states (peek/open/full)

Subsequent EPICs reference these mockups for their respective
feature implementations.

## Files

- `KG Panel States - standalone.html` — self-contained renderable mockup
- `KG Panel States.html` + `.jsx` files — modular React source
- `KG Panel States.bundle-src.html` — original prompts/exports
- `wireframe-layout.jsx` — annotated wireframe view
- `uploads/` — reference images

## How to view

```bash
explorer.exe "$(wslpath -w "$(pwd)/KG Panel States - standalone.html")"
```

Opens the standalone HTML in your default Windows browser.
