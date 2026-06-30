# Dashboard CV — Cross-Chat Handoff

The project is **chunked into separate chats per component** (see `claude.md` →
"Working Style Notes"). This file is the contract that lets independently-built
components combine without rework. Read alongside `claude.md` (what/why + real data)
and `plan.md` (component status + sequencing).

## Integration contract — read this first

Every component chat MUST honour these so the pieces slot together:

1. **One shared `tokens.css`** — the single source for palette and type scale. No
   component defines its own colours or font sizes; they consume the tokens.
   - Palette (carried from the Manim animation): navy `#0E1330` (background),
     ice `#CADCFC` (primary text/lines), coral `#F96167` (accent/highlight).
   - Type scale + layout grid + nav: established in component 1 (consult the
     frontend-design skill). Later components inherit, never redefine.
2. **Fixed anchor IDs** — the node-map edges deep-link to these exact IDs; do not
   rename: `#supervet`, `#edutech`, `#studio`, `#ai`, `#links`.
3. **Single `index.html` shell** — components are sections slotted into one shell,
   not separate pages. Proposed file layout:
   ```
   index.html          # shell: <head> + nav + section stubs w/ the 5 anchor IDs
   css/tokens.css      # palette + type scale (shared)
   css/styles.css      # layout/component styles consuming tokens
   js/nodemap.js       # SVG edge animation + smooth-scroll wiring
   js/panels.js        # Chart.js setup for data panels
   assets/             # data_driven_supervet.mp4, images, downloadable CV
   ```
4. **Dependency-free** — only external dependency permitted is Chart.js via a single
   CDN `<script>`. No framework, no build step (Cloudflare Pages serves the static files).

## Per-component handoff

| Component | Needs as input | Draws from (source folder) | Blocker |
|-----------|----------------|----------------------------|---------|
| 1. Tokens / shell | frontend-design principles; palette above | — | none |
| 2. Hero + node map | narrative paragraph; node taxonomy + edge wiring (in `claude.md`); anchor IDs from shell | narrative copy | none |
| 3. SuperVet panel | extracted figures (already in `claude.md`); the mp4 | SuperVet data — `Packaging.xlsx`, `data_driven_supervet.mp4` | none |
| 4. EduTech panel | algorithm summary (in `claude.md`); **outcome data** | TimeView / TimeEditor project folder | 🔴 outcome data |
| 5. Studio panel | phased-plan narrative; acoustics theory | studio PDF (`2103_2_405-Music_Centre_Alterations`) | 🟡 animation guidelines for λ/4 clip |
| 6. AI sections | settled content directions (in `claude.md`) | — (copywriting) | none |
| 7. Links / CV / deploy | live URLs; CV file | Baker's Cost Pro; TimeView | 🔴 Baker's URL, 🔴 TimeView deploy |

## Outstanding blockers (carried from `claude.md`)

- **Baker's Cost Pro live URL** — not yet provided. Needed for the links section.
- **TimeView Cloudflare deployment** — not yet live. Decide: placeholder "shipping
  soon" link, or hold that section back until live.
- **EduTech outcome data** — has TimeView/TimeEditor run against real school
  timetable data yet, and with what result (clashes eliminated, time saved vs manual,
  staff feedback)? Until known, frame as "built and demoed," not deployed-with-results.
- **Animation style guidelines** — Eugene to provide specific guidelines before more
  Manim clips (incl. the studio λ/4 acoustics clip) are built. Treat the SuperVet clip
  as a working baseline, not a locked template.

## Working rule

Eugene gives dense, real-data-bearing instructions and expects them followed
precisely — no invented numbers, research, or placeholder achievements. When data is
missing, **ask rather than fabricate**. This file and `claude.md`/`plan.md` are the
shared memory across chats — update them as decisions are made or blockers resolve.
