# Contributing to ascendion.engineering

This site is a curated, practitioner-grade architecture knowledge base maintained by Ascendion's Solutions Architecture practice. It is built from Markdown content and Mermaid diagrams using a small static-site generator.

This guide explains how to contribute.

---

## How the site is built

```
content/<section>/<subsection>/README.md     ← topic content (Markdown)
content/<section>/<subsection>/diagram.mmd   ← optional Mermaid diagram
                                ↓
                  python tools/generate.py
                                ↓
            dist/<section>/<subsection>/index.html
                                ↓
              GitHub Actions → S3 → CloudFront → live site
```

- **One folder per topic.** Each subsection is `content/<section>/<subsection>/` with a `README.md` (and optionally a `diagram.mmd`).
- **Title comes from the first `# ` line.** Description is the first non-heading line that follows.
- **Tags come from the `**Alignment:**` line** (e.g. `**Alignment:** TOGAF | NIST CSF | ISO 27001`).
- **The generator owns the chrome** (header, footer, navigation, breadcrumbs, styling). Authors only write the body.
- **Section index pages and the home page are auto-generated.** Adding or removing a subsection updates the parent index automatically.

---

## How to add or improve a page

### 1. Find the right location

The taxonomy is organised by 29 sections (see `content/`). Find or create the right subsection folder.

### 2. Edit the README.md

Open `content/<section>/<subsection>/README.md` in your editor.

**Structure expected by the generator:**

```markdown
# Page Title

A one-line description that becomes the page subtitle.

**Section:** `<section>/` | **Subsection:** `<subsection>/`
**Alignment:** TOGAF ADM | NIST CSF | ISO 27001

---

## First Heading

Your content here. Standard Markdown is supported including:
- bullet lists
- numbered lists
- `inline code`
- **bold**, *italic*
- code fences (```)
- tables
- blockquotes (> ...)
- links

## Second Heading

More content.
```

### 3. Add or update the diagram

Diagrams are [Mermaid](https://mermaid.js.org/) source files. Save them as `content/<section>/<subsection>/diagram.mmd`.

A good diagram is **topic-specific** — it should explain something about *this* topic that prose cannot show as efficiently. A generic governance flowchart copied across pages does not earn its space on the page.

Examples:
- For a **patterns** page: show the structural relationship the pattern creates.
- For an **architecture** page: show the architectural layers and their boundaries.
- For a **lifecycle** page: show the stages and transitions.
- For a **data** page: show data flow or schema relationships.

If a diagram is not yet ready, leave the existing stub `diagram.mmd` and mark a TODO in the README — but `diagram.mmd` files that are obviously generic placeholders should be replaced or removed before the page is considered complete.

### 4. Preview locally

You need Python 3.10+ and one dependency:

```bash
pip install markdown
python3 tools/generate.py
```

This builds `dist/` from `content/`. Open `dist/<section>/<subsection>/index.html` in your browser to preview, or run a local web server for navigable preview:

```bash
cd dist && python3 -m http.server 8000
# then open http://localhost:8000/ in your browser
```

To rebuild from scratch (recommended after taxonomy changes):

```bash
python3 tools/generate.py --clean
```

> **Note:** if `python` works on your system, you can use it instead of `python3`. On Ubuntu/WSL you may need to install `python-is-python3` (`sudo apt install python-is-python3`) to make `python` available as an alias.

### 5. Commit and open a PR

```bash
git checkout -b improve/<section>-<subsection>
git add content/<section>/<subsection>/
git commit -m "Improve <section>/<subsection>: <what changed>"
git push origin improve/<section>-<subsection>
```

Then open a Pull Request. CI will not block on content quality, but reviewers will look for:

- **Specificity.** The content distinguishes this topic from neighbouring ones.
- **Defensibility.** A senior architect could stand behind every claim.
- **Sourced.** Standards, frameworks, and external claims are linked.
- **Diagram earns its space.** It explains something prose cannot.
- **Practitioner voice.** Written for engineers who know the area, not for first-time learners.

---

## Quality bar — what good content looks like

The reference page is [`principles/ai-native/`](https://ascendion.engineering/principles/ai-native/) (and its source `content/principles/ai-native/README.md`). Use it as the model when enriching other pages.

A page is "complete" when it satisfies the following:

| Criterion | Why |
|---|---|
| Distinguishes the topic from adjacent topics | Clarity for the reader, prevents content overlap |
| Has a stable point of view (POV) | The site exists to take positions, not to be a Wikipedia mirror |
| Includes a topic-relevant diagram | Visual reasoning is part of architectural thinking |
| Cites standards or sources where claims are made | Defensibility and signal of rigour |
| Includes pitfalls or anti-patterns where relevant | Real practitioner experience, not just abstract guidance |
| Reads in a practitioner voice | Audience is fellow engineers, not novices |

A page that lacks a topic-relevant diagram or cites no sources is a stub, regardless of how many words it contains.

---

## What NOT to do

- **Don't edit `dist/`.** It is a build artefact and is regenerated on every deploy.
- **Don't edit `index.html` files in `content/`.** There aren't any — content is Markdown.
- **Don't bypass the generator** by uploading directly to S3. The deploy pipeline is the only path to live; direct uploads will be overwritten by the next deploy.
- **Don't re-use the generic governance flowchart** as a placeholder diagram on a topic where it is not actually relevant. An empty diagram slot is more honest than a misleading one.

---

## Operational notes

- **Deploys** trigger on every push to `main`. Watch them at: GitHub → Actions tab.
- **Cache invalidation** happens automatically as part of every deploy. Live site reflects changes within ~60 seconds of merge.
- **Source of truth is git**. If it is not in this repo's `main` branch, it is not live.

---

## Questions

For taxonomy changes (adding a new section, restructuring), open an issue first — these affect navigation and require a coordinated update.

For content questions, ping the Solutions Architecture practice in the team's working channel.
