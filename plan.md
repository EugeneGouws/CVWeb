# Dashboard CV — Build Plan (living)

This is the working build plan for Eugene's dashboard-style CV. **Source of truth
for *what* and *why* is `claude.md`** (locked design decisions, case-study data,
palette, build notes). The cross-chat integration contract is in `handoff.md`.
Keep this file's component statuses current as work lands.

## Concept (summary)

Hybrid/tiered static page: linear scroll spine for 30-sec legibility; hero =
interactive skills-translation **node map** whose edges deep-link to case-study
panels. Dependency-free (hand-rolled SVG + Chart.js CDN + IntersectionObserver),
deploys straight to Cloudflare Pages. Palette: navy/ice/coral
(`#0E1330` / `#CADCFC` / `#F96167`). Full taxonomy + edge wiring in
`claude.md` → "Dashboard Structure (agreed)".

## Component breakdown

Status legend: ⬜ Not started · 🟡 In progress · 🔴 Blocked · ✅ Done

| # | Component | Anchor | Source folder | Status |
|---|-----------|--------|---------------|--------|
| 1 | Design tokens / shell | — | (frontend-design skill) | ⬜ Not started |
| 2 | Hero + node map | top | narrative copy | ⬜ Not started |
| 3 | SuperVet panel | `#supervet` | SuperVet data (`Packaging.xlsx`, mp4) | ⬜ Not started |
| 4 | EduTech panel | `#edutech` | TimeView/TimeEditor | 🔴 Blocked (outcome data) |
| 5 | Studio panel | `#studio` | studio PDF | ⬜ Not started |
| 6 | AI sections | `#ai` | (copy) | ⬜ Not started |
| 7 | Links / CV / deploy | `#links` | — | 🔴 Blocked (Baker's URL, TimeView deploy) |

### 1. Design tokens / shell — *foundational, build first*
`tokens.css` (palette, type scale, layout grid, nav) + `index.html` shell carrying
the fixed anchor IDs. **Consult the frontend-design skill** before establishing the
token system. Everything else depends on this; defines the integration contract in
practice. See `handoff.md`.

### 2. Hero + node map
Hand-rolled SVG node map: left domains (Maths · Brand Mgmt · Teaching · Audio Eng),
right offerings (Data-Driven · Product Building · Project Mgmt · AI Judgment), edges
per the locked wiring. `<path>` edges animated via `stroke-dashoffset`, pre-animated
on load so transfer reads without interaction; click an edge → smooth-scroll to its
panel anchor. Plus name + one-paragraph narrative copy.

### 3. SuperVet panel (`#supervet`) — Data Driven Solutions
Chart.js native interactive chart built from the **real** `Packaging.xlsx` figures
already extracted in `claude.md` (months-of-stock per variant; fixed/total costs;
per-unit bag costs) + `data_driven_supervet.mp4` embed. Story = print-economics
overstock, not a demand problem. No invented numbers/comparisons.

### 4. EduTech panel (`#edutech`) — Convenience Driven Solutions · 🔴 BLOCKED
TimeView/TimeEditor; technical core (DSatur, backtracking, hill-climbing,
Kempe/ejection chains, custom Marking-Load-Warning constraint). Framed
domain-experience-driven, *not* data-driven. **Blocked on outcome data** — has it
run on real school data, with what result? Until then frame as "built and demoed,"
not deployed-with-results.

### 5. Studio panel (`#studio`) — Outcome Based Project Management
Phased-delivery narrative (undefined head-office brief → self-originated use cases →
3-phase plan with quotes). Planned λ/4 quarter-wavelength acoustics animation
(generic physics, no proprietary data) — awaiting Eugene's animation guidelines. No
cost figures (no budget ever existed).

### 6. AI sections (`#ai`)
Two cohesive units: **AI Understanding & Judgment** (LLM vs ML distinctions, a
when-to-use-AI judgment framework) and **Digital Fluency & Early Adoption**
(`.md`-governed architecture, manual+Claude Code debugging, supervised writes with
token optimisation). Directions settled; copy not yet drafted.

### 7. Links / CV / deploy (`#links`) · 🔴 BLOCKED
GitHub, LinkedIn, Baker's Cost Pro, TimeView live, downloadable CV; Cloudflare Pages
deploy. **Blocked on** Baker's Cost Pro live URL and TimeView deployment decision
(placeholder vs. hold back).

## Dependencies

- **Shell/tokens (1) first** — fixes palette, type scale, layout, and the anchor IDs
  the node map targets. Until those anchors exist, the node-map edges (2) can't wire up.
- **Panels (3–7) are independent of each other** once the contract exists — each can
  be built in its own chat and slotted in.
- Blockers on (4) and (7) don't block the rest; build around them.

## Separate-then-combine sequencing

Each component is built in its own chat/chunk against its real source folder (Eugene
grants access per component), then slotted into the `index.html` shell via the shared
`tokens.css` + fixed anchor IDs defined in `handoff.md`. Build order: **1 → 2 → (3,
5, 6 in any order) → 4, 7 when unblocked → integrate + Cloudflare deploy.** First code
chunk = component 1 + 2 (shell + hero/node-map), opened in a browser locally before deploy.
