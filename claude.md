# Eugene Gouws — Recruitment Portfolio Project

## Context & Goal

Eugene met with a recruiting agent. The agent's core observation: Eugene's experience and studies (Mathematician → teacher → software builder → former Brand Manager) don't read as an easy-to-follow story on paper. The work isn't to invent a new story, it's to make the existing transferable-skills story legible to people who only have 30 seconds with a CV.

Recruiter's original pointers (verbatim from his notes):
- CV needs a 1-paragraph narrative: who I am / experience / what I can offer
- A presentation made *to a person* — personal connection, experience ported to new skills
- Originally suggested as a PowerPoint (3–5 pages), transferable skills focus
- Brand management + maths = transferable skills (FMCG example). Build 2–3 case studies across different sectors. Use dashboards/graphs to show tangible results.
- LinkedIn: mark open to work, post regularly, comment on others
- Buzzwords to hit: digital fluency, AI fluency
- Use "transferable skills" instead of "soft skills"

**Format pivoted mid-project**: originally planned as a PowerPoint deck, now an **interactive web dashboard** (static HTML/CSS/JS, no framework dependency) so it can be deployed directly to Cloudflare Pages alongside his other live projects. Single scrolling page with anchored nav, not a click-through deck.

## Current CV (as uploaded: `EGouws_CV_206.docx`)

- BSc (Distinction) Pure & Applied Maths, Programming, Computer Science — Durban, 2020–2025
- MMus, Music Technology — Pretoria, 2014–2017
- BMus, Musicology/Singing/Choral Conducting/Music Tech — Stellenbosch, 2007–2011
- Work history: Brand Manager, SuperVet Southern Africa (2011–2016) → Maths/Music Teacher, Hudson Park High (2016–2022) → Maths/Music Teacher + Head of Music/Curriculum Leader, Crawford International La Lucia (2022–present)
- Current CV under-represents the software work entirely — no mention of TimeView, TimeEditor, Baker's Cost Pro, or GitHub. This is the legibility gap the whole project is fixing.
- Links: github.com/EugeneGouws, linkedin.com/in/eugenegouws

## Dashboard Structure (agreed)

**Locked decisions (this session).** See `plan.md` (living build plan) and `handoff.md` (cross-chat integration contract) for execution detail; this section is the canonical record of *what* is being built.

**Concept = hybrid, tiered.** A linear scroll spine gives 30-second legibility; the hero is an interactive **skills-translation node map**; the map's edges deep-link down to case-study panels. Tier 0 serves the 30s scan, the tiers below reward a hiring manager who explores.

**Hero node map (content locked):**
- Left column — past domains: **Maths · Brand Mgmt · Teaching · Audio Eng**
- Right column — offerings: **Data-Driven · Product Building · Project Mgmt · AI Judgment**
- Edges (the wiring, confirmed): Maths→Data, Maths→AI, Brand→Data, Teaching→Product, Teaching→PM, Audio→PM, Software→Product. The **crossing edges are the visual proof of transfer** — that's the whole point of the map.
- Each edge deep-links to a panel: Brand+Maths→**SuperVet** · Teaching+Software→**EduTech** · Audio+Teaching→**Recording Studio** · Maths→**AI sections**.

**Page tiers:**
- **Tier 0 — hero / 30s read:** name, one-paragraph narrative (who-I-am / experience / what-I-offer), the node map with edges *pre-animated* so transfer reads without interaction.
- **Tier 1 — case-study panels (deep-link targets):** **SuperVet** `#supervet` (Data Driven Solutions — Chart.js native chart + `data_driven_supervet.mp4`), **EduTech** `#edutech` (Convenience Driven Solutions — TimeView/TimeEditor, framed domain-experience-driven not data-driven), **Recording Studio** `#studio` (Outcome Based Project Management — phased delivery + planned acoustics animation).
- **Tier 2 — AI + links:** **AI Understanding & Judgment** and **Digital Fluency & Early Adoption** `#ai`; then **Links / CV** `#links` (GitHub, LinkedIn, live demos — Baker's Cost Pro, TimeView — downloadable CV).

**Palette** = carry the navy/ice/coral from the delivered Manim animation (`#0E1330` / `#CADCFC` / `#F96167`) so the embedded video and the page read as one piece.

**Tech = dependency-free static.** Hand-rolled SVG node map (`<path>` edges animated via `stroke-dashoffset`; click → smooth-scroll to the panel anchor). Chart.js via a single CDN tag for the data panels. IntersectionObserver for scroll reveals. No framework, no build step → deploys straight to **Cloudflare Pages**.

**Integration contract** (so components built in separate chats combine without rework): one shared `tokens.css` (palette + type scale), fixed anchor IDs `#supervet #edutech #studio #ai #links` that the node-map edges target, and a single `index.html` shell that components slot into. No component invents its own palette or layout. Full contract lives in `handoff.md`.

Note: Baker's Cost Pro (kitchen costing webapp) is **not** one of the three case studies — it's a separate standalone portfolio link in Tier 2, grouped conceptually with TimeView/TimeEditor as "software built to solve a problem I personally had," but doesn't get its own narrative panel.

## Case Study 1: Data Driven Solutions (SuperVet)

Source data: `Packaging.xlsx` (uploaded), `SuperVet_Packaging_1bright.jpg` (early packaging design draft).

**The real story** (extracted from the spreadsheet, not invented): bag printer minimum order quantities (3,000–6,000 units/variant) didn't match actual sell-through velocity. At current sales pace:
- Adult 20kg: 6.4 months of stock per minimum order
- Adult 8kg: 12.1 months
- LB Pup 20kg: 21.3 months
- Pup 8kg: 34.7 months
- LB Pup 8kg: **51.9 months** (4+ years of stock from a single print run)

Total fixed costs (design + stereos/plates): R108,660. Total cost across 5 variants: R352,710. Bag costs ranged R10.29–R14.65/unit depending on size and print minimum.

**The resolution**: not a marketing push — redirecting surplus stock from slow-moving variants to Namibia, Botswana, and bulk-buy channels before it became dead stock. This is the actual "hidden problem" insight: the constraint wasn't demand, it was print economics creating structural overstock risk.

The original qualitative research (what justified the packaging change in the first place) is lost/unavailable — case study deliberately does not reference it or invent industry comparisons. It stands on Eugene's own numbers alone.

**Status**: Manim animation built and delivered (`data_driven_supervet.mp4`, dark navy/ice/coral palette, ~12s). Eugene's feedback: "good start" but he will provide **specific guidelines for the animations** before further ones are built — treat current animation as a working style baseline, not a locked-in template. Native interactive chart (Chart.js, not just the video) still to be built into the actual dashboard page.

## Case Study 2: Convenience Driven Solutions (EduTech)

TimeView + TimeEditor — timetabling/exam scheduling tools. Technical core: DSatur graph colouring, backtracking, hill-climbing, Kempe/ejection chains, and a custom "Marking Load Warning" constraint (prevents exam clustering that creates invisible teacher marking-burden spikes — this was Eugene's own addition, not a standard scheduling constraint).

Framing is deliberately **not** data-driven — it's convenience/domain-experience-driven: Eugene built these because he personally lived the scheduling pain as a teacher, not because he ran a formal data analysis first. This is the contrast point against the SuperVet slide.

**Outstanding**: deployment/outcome status unconfirmed — has it run against real school timetable data yet, and with what result (clashes eliminated, time saved vs. manual, staff feedback)? If not yet live, frame honestly as "built and demoed," not as deployed-with-results.

## Case Study 3: Outcome Based Project Management (Recording Studio)

Real brief (from Eugene, confirmed): 7 existing music practice rooms at Crawford International La Lucia to be altered to include a recording studio. **The entire original brief was just an idea from head office — no budget, no defined use case.** Eugene had to originate the use cases himself.

Architect's construction drawings uploaded (`2103_2_405-Music_Centre_Alterations-3-20250708.pdf`, ADTECH Architects, Project 2103.2, Drawing 405 Rev 3, "FOR CONSTRUCTION", Crawford La Lucia, 79 Armstrong Ave). Shows: Recording/Sound Studio, Control Room, Practice Room 1, Practice Room 2, Music Room. Spec includes acoustic panelling and acoustic ceilings with insulation (per specialist), acoustically-treated aircon, new carpet/vinyl flooring (Almond Oak), solid timber doors with rubber door-bottom seals, floor boxes for cabling. Carpet pattern across all rooms designed as musical keys motif.

**Eugene's actual process** (real, to build the narrative around):
1. Research phase: room sizing and wet-work scope (breaking/building walls), acoustic treatment, wiring/cabling routing
2. Hardware/signal chain planning: mic/DI inputs, cabling, channel count needed at the interface, computer and monitor speaker chain
3. Room treatment and window planning, designed for the space to be modular — usable for recording, rehearsal, or teaching (Eugene had to invent and justify these use cases himself, since head office gave none)
4. Delivered a **3-phase plan with quotes**, each phase unlocking more use cases — this is the project management / staged-delivery angle for the slide
5. Acoustic phase: measured the rooms for standing waves, consulted acousticians on suitable materials and absorption coefficients

**No budget figures exist** — there was never a budget given, so the case study should not claim cost figures. The actual achievement to highlight is scoping an undefined brief into a phased, justified, technically-grounded delivery plan, which is itself the "outcome-based project management" story.

**Planned animation**: quarter-wavelength absorption theory (generic acoustics physics, doesn't need Eugene's proprietary data) — depth of absorber ≈ λ/4 at the target frequency, technical math + practical/budget framing. Not yet built — awaiting Eugene's specific animation guidelines (see below).

## AI Sections

**AI Understanding & Judgment** (slide 1 of 2): Eugene's thesis — AI abuse/dependence is impeding genuine intelligence by outsourcing thinking and creativity. Section should distinguish AI types with specific terms (LLMs vs. ML vs. other), name possible legitimate uses for such models, and lay out Eugene's own judgment framework for *when* to use AI vs. not.

**Digital Fluency & Early Adoption** (slide 2 of 2, workflow-based): covers Eugene's actual development workflow —
- `.md` files governing architecture, skills, and commands (project-level governance/instructions)
- Manual coding combined with Claude Code for debugging
- Full supervised Claude Code writes, with token-optimisation strategies

Both sections to be written as one cohesive AI-fluency unit. Content directions are settled; copy not yet drafted.

## Technical Build Notes (environment-specific, for reproducibility)

- **Manim** (Community Edition) works in this environment but required manual setup: `apt-get install libpango1.0-dev pkg-config dvisvgm` before `pip install manim --break-system-packages` would succeed. ffmpeg, latex, pdflatex were already present.
- **pptxgenjs** supports native video embedding via `slide.addMedia({ type: 'video', path, cover })` — relevant if the project ever reverts to a pptx deliverable, but not needed now that the format is a web dashboard (HTML5 `<video>` is simpler and more reliable there).
- **Manim BarChart gotcha #1**: if you only animate `chart.bars` (e.g. via `GrowFromEdge`) without explicitly adding `chart.x_axis` / `chart.y_axis` to the scene first, the axis lines and bar-name labels never appear — they exist on the object but are never added to the scene. Fix: `self.add(chart.x_axis, chart.y_axis)` or `FadeIn` them before/alongside animating the bars.
- **Manim BarChart gotcha #2**: calling `.set_color()` on the whole `BarChart` mobject after construction overwrites the per-bar `bar_colors` you set, flattening every bar to one colour. Don't call `set_color` on the whole chart if bars need distinct colours — style sub-elements individually instead.
- First animation delivered: `data_driven_supervet.mp4` (script: SuperVet bar chart story, dark navy `#0E1330` background, ice `#CADCFC` / coral `#F96167` accents, 1920×1080).

## Outstanding Blockers

- **Baker's Cost Pro live URL** — needed for the links section. Not yet provided.
- **TimeView Cloudflare deployment** — not yet live. Eugene plans to deploy it. Decide: placeholder "shipping soon" link, or hold that section back until live.
- **EduTech outcome data** — has TimeView/TimeEditor run against real school data yet, and with what result?
- **Animation style guidelines** — Eugene is going to provide specific guidelines for future Manim animations before more are built. Don't assume the SuperVet clip's exact treatment is final/locked.

## Working Style Notes

- Eugene gives dense, specific, real-data-bearing instructions and expects them followed precisely — doesn't want invented numbers, invented research, or filled-in placeholder achievements. When data is missing, ask rather than fabricate.
- He's technically fluent (maths, software, audio engineering) — explanations can go straight to the technical substance without over-simplifying.
- Prefers concrete progress (a rendered asset, real extracted data) over long planning prose when work can just be shown.
- Project is now being deliberately chunked into separate chats per component. This file is the shared memory across those chats — keep it updated as decisions are made or blockers are resolved.

## Suggested Chunking for Future Chats

1. CV narrative paragraph + CV document refresh (weave software work into existing roles)
2. Manim animation guidelines + recording studio acoustic animation (and any restyle of the SuperVet clip)
3. Dashboard skeleton build (HTML/CSS/JS structure, nav, design token system per frontend-design principles)
4. AI Understanding & Digital Fluency section copywriting
5. EduTech case study content (pending outcome data)
6. Links, live deployment (TimeView, Baker's Cost Pro), final QA
