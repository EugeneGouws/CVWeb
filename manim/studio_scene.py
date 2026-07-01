"""
studio_scene.py — Case study 3 (Recording studio) hero clip.

Three acoustic treatments, staged back to back, sharing one right-hand
frequency-spectrum panel so the payoff of each is legible in isolation:

  Act 1 — Corner bass trap.        Broadband: a travelling wave slows and
                                    fades as it enters the corner wedge.
                                    BOTH spectrum peaks (low + high) drop.
  Act 2 — Quarter-wave panel absorber. A single wave-cycle (wavelength = the
                                    air-gap depth, itself 3x the panel's own
                                    thickness) crosses the gap, reflects off
                                    the rigid wall, crosses back — the panel
                                    resistively damps it on each pass because
                                    a rigid wall's quarter-wave point is where
                                    particle velocity peaks. Frequency-
                                    selective: only the HIGH spike drops.
  Act 3 — Quadratic-residue diffuser. A stepped well sequence (depths =
                                    (n^2 mod 7) * unit, equal well widths)
                                    scatters the wavefront into many
                                    directions instead of reflecting or
                                    absorbing it. Both spikes drop by half —
                                    and the broadband floor rises to meet
                                    them, since it's redistribution, not loss.

Render (from repo root, with tools/ on PATH so manim finds ffmpeg):
  PATH="E:/cvweb/tools:$PATH" python -m manim -qm --format mp4 \
       -o studio manim/studio_scene.py AcousticTreatments
"""
import numpy as np
from manim import (
    Scene, VMobject, Line, Polygon, Rectangle, Text, Arrow, VGroup,
    ValueTracker, Mobject, always_redraw, config,
    FadeIn, FadeOut, Create, Write, Transform,
    UP, DOWN, LEFT, RIGHT, ORIGIN,
)

BG    = "#0E1330"
ICE   = "#CADCFC"
CYAN  = "#6BD0FF"
CORAL = "#F96167"
WARM  = "#F2A65A"
DIM   = "#46527F"

config.background_color = BG

# ---- shared layout (left = physical panel, right = spectrum panel) ----
xL, xW = -6.9, -1.0          # left panel: far edge -> corner/wall
floorY = -2.6
baseY = 0.4

sx0, sx1 = 1.0, 6.4           # right panel: spectrum axis extent
sBase = -1.9
sTop = 2.6
F_LOW, F_HIGH = 2.1, 4.9      # the two spectral lines every act reacts to


class AcousticTreatments(Scene):
    def construct(self):
        t = ValueTracker(0.0)
        clock = Mobject()
        clock.add_updater(lambda m, dt: t.increment_value(dt))
        self.add(clock)

        # ============ shared right-hand spectrum rig ============
        ampLow = ValueTracker(1.0)
        ampHigh = ValueTracker(1.0)
        floor = ValueTracker(0.0)     # broadband floor level (0 = silent)

        sAxis = Line([sx0, sBase, 0], [sx1, sBase, 0], color=DIM, stroke_width=2)
        yAxis = Line([sx0, sBase, 0], [sx0, sTop, 0], color=DIM, stroke_width=2)
        labR = Text("Frequency spectrum", font="Arial", color=ICE,
                    weight="MEDIUM").scale(0.42)
        labR.next_to([(sx0 + sx1) / 2, sTop, 0], UP, buff=0.12)
        freqlab = Text("frequency", font="Arial", color=DIM).scale(0.32)
        freqlab.next_to([sx1, sBase, 0], DOWN, buff=0.18).shift(LEFT * 0.3)

        lo_tick = Line([F_LOW, sBase - 0.12, 0], [F_LOW, sBase + 0.12, 0],
                       color=ICE, stroke_width=2)
        hi_tick = Line([F_HIGH, sBase - 0.12, 0], [F_HIGH, sBase + 0.12, 0],
                       color=ICE, stroke_width=2)
        lo_lab = Text("low", font="Arial", color=DIM).scale(0.32)
        lo_lab.next_to([F_LOW, sBase, 0], DOWN, buff=0.18)
        hi_lab = Text("high", font="Arial", color=DIM).scale(0.32)
        hi_lab.next_to([F_HIGH, sBase, 0], DOWN, buff=0.18)

        H = 3.4  # peak height at amp = 1.0

        def gauss(x, mu, sigma, height):
            return sBase + height * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

        def spectrum_curve():
            fl, fh, fb = floor.get_value(), None, None
            al, ah = ampLow.get_value(), ampHigh.get_value()
            xs = np.linspace(sx0 + 0.05, sx1, 260)
            ys = []
            for x in xs:
                base = sBase + fl * 0.85 * (0.55 + 0.45 * np.sin(6.0 * (x - sx0)))
                v = max(
                    base,
                    gauss(x, F_LOW, 0.16 + 0.22 * (1 - al), H * al),
                    gauss(x, F_HIGH, 0.16 + 0.22 * (1 - ah), H * ah),
                )
                ys.append(v)
            pts = [[x, y, 0] for x, y in zip(xs, ys)]
            m = VMobject(color=CORAL, stroke_width=4)
            m.set_points_smoothly(pts)
            return m

        spectrum = always_redraw(spectrum_curve)

        act_label = Text("", font="Arial", color=WARM, weight="BOLD").scale(0.44)
        act_label.move_to([(xL + xW) / 2, 3.15, 0])

        def set_act_label(txt):
            new = Text(txt, font="Arial", color=WARM, weight="BOLD").scale(0.44)
            new.move_to([(xL + xW) / 2, 3.15, 0])
            return Transform(act_label, new)

        self.play(Create(sAxis), Create(yAxis), FadeIn(labR), FadeIn(freqlab),
                  FadeIn(lo_tick), FadeIn(hi_tick), FadeIn(lo_lab), FadeIn(hi_lab),
                  FadeIn(act_label), run_time=1.0)
        self.add(spectrum)

        # ================================================================
        # ACT 1 — corner bass trap: broadband wave slows + fades into it
        # ================================================================
        self.play(set_act_label("Corner bass trap"), run_time=0.6)

        wall = Line([xW, floorY, 0], [xW, 2.7, 0], color=ICE, stroke_width=5)
        flr = Line([xL, floorY, 0], [xW, floorY, 0], color=ICE, stroke_width=5)
        xTrapStart = xW - 2.0
        trap = Polygon(
            [xW, floorY, 0], [xW, floorY + 1.9, 0], [xTrapStart, floorY, 0],
            color=WARM, fill_color=WARM, fill_opacity=0.22, stroke_width=2,
        )
        hatch = VGroup(*[
            Line([xTrapStart + i * 0.28, floorY, 0],
                 [xW, floorY + 1.9 - i * 0.32, 0], color=WARM, stroke_width=1.2)
            for i in range(1, 6)
        ])
        capL = Text("Wave slows and fades entering the trap", font="Arial",
                    color=ICE).scale(0.36)
        capL.next_to([(xL + xW) / 2, 2.7, 0], DOWN, buff=0.15)

        k_free, k_trap = 1.35, 3.6
        omega = 2.4
        alpha = 1.9  # spatial absorption rate inside the trap

        xs_dense = np.linspace(xL, xW, 400)

        def k_profile(x):
            if x <= xTrapStart:
                return k_free
            frac = (x - xTrapStart) / (xW - xTrapStart)
            return k_free + (k_trap - k_free) * frac

        ks = np.array([k_profile(x) for x in xs_dense])
        phase_cum = np.concatenate([[0.0], np.cumsum(
            (ks[1:] + ks[:-1]) / 2 * np.diff(xs_dense))])

        def amp_profile(x):
            if x <= xTrapStart:
                return 1.0
            return float(np.exp(-alpha * (x - xTrapStart)))

        amps = np.array([amp_profile(x) for x in xs_dense])

        def act1_wave_curve():
            a = ampLow.get_value()  # shared decay driving this act
            tv = t.get_value()
            ys = baseY + 0.95 * a * amps * np.sin(phase_cum - omega * tv)
            pts = [[x, y, 0] for x, y in zip(xs_dense, ys)]
            m = VMobject(color=CYAN, stroke_width=4)
            m.set_points_smoothly(pts)
            return m

        act1_wave = always_redraw(act1_wave_curve)
        axisL1 = Line([xL, baseY, 0], [xW, baseY, 0], color=DIM, stroke_width=1.5)

        self.play(Create(wall), Create(flr), run_time=0.8)
        self.play(FadeIn(trap), Create(hatch), FadeIn(capL), run_time=0.8)
        self.add(axisL1, act1_wave)
        self.wait(1.4)

        absorb1 = Text("both frequencies attenuate together", font="Arial",
                       color=WARM).scale(0.36)
        absorb1.next_to(trap, UP, buff=0.22).shift(RIGHT * 0.3)
        self.play(FadeIn(absorb1), run_time=0.5)
        self.play(ampLow.animate.set_value(0.08),
                  ampHigh.animate.set_value(0.08), run_time=4.0)
        self.wait(1.0)

        self.play(
            FadeOut(wall), FadeOut(flr), FadeOut(trap), FadeOut(hatch),
            FadeOut(capL), FadeOut(absorb1), FadeOut(axisL1), FadeOut(act1_wave),
            run_time=0.8,
        )
        ampLow.set_value(1.0)
        ampHigh.set_value(1.0)

        # ================================================================
        # ACT 2 — quarter-wave panel absorber: only the HIGH spike drops
        # ================================================================
        self.play(set_act_label("Quarter-wave panel absorber"), run_time=0.6)

        thickness = 0.55
        gap = 3 * thickness           # gap = 3x the panel's own thickness
        xWall2 = xW
        xPanelOuter = xWall2 - gap
        xPanelInner = xPanelOuter - thickness
        xEnter = xL + 0.4

        wall2 = Line([xWall2, floorY, 0], [xWall2, 2.7, 0], color=ICE, stroke_width=5)
        flr2 = Line([xL, floorY, 0], [xWall2, floorY, 0], color=ICE, stroke_width=5)
        panel = Rectangle(width=thickness, height=3.6, color=WARM,
                           fill_color=WARM, fill_opacity=0.35, stroke_width=2)
        panel.move_to([(xPanelOuter + xPanelInner) / 2, floorY + 1.8, 0])
        gaplab = Text("gap = 3x panel thickness = wavelength",
                      font="Arial", color=ICE).scale(0.34)
        gaplab.next_to([(xPanelOuter + xWall2) / 2, 2.7, 0], DOWN, buff=0.15)

        axisL2 = Line([xL, baseY, 0], [xWall2, baseY, 0], color=DIM, stroke_width=1.5)

        wavelength2 = gap
        env_w = wavelength2 * 0.55
        pos = ValueTracker(xEnter)
        polarity = ValueTracker(1.0)
        atten2 = ValueTracker(1.0)

        def act2_wave_curve():
            c = pos.get_value()
            xs = np.linspace(xL, xWall2, 300)
            env = np.exp(-((xs - c) ** 2) / (2 * env_w ** 2))
            ys = baseY + 0.95 * atten2.get_value() * polarity.get_value() * env * \
                np.sin(2 * np.pi * (xs - c) / wavelength2)
            pts = [[x, y, 0] for x, y in zip(xs, ys)]
            m = VMobject(color=CYAN, stroke_width=4)
            m.set_points_smoothly(pts)
            return m

        act2_wave = always_redraw(act2_wave_curve)

        self.play(Create(wall2), Create(flr2), run_time=0.7)
        self.play(FadeIn(panel), FadeIn(gaplab), run_time=0.7)
        self.add(axisL2, act2_wave)

        # pass 1: enter through panel, cross gap toward wall
        self.play(pos.animate.set_value(xWall2), run_time=1.6, rate_func=lambda x: x)
        # attenuate on the pass through the panel (already crossed on the way in)
        self.play(atten2.animate.set_value(0.72), run_time=0.3)
        # reflect off rigid wall
        self.play(polarity.animate.set_value(-1.0), run_time=0.25)
        # pass 2: back across gap and out through the panel again
        self.play(pos.animate.set_value(xEnter), run_time=1.6, rate_func=lambda x: x)
        self.play(atten2.animate.set_value(0.30), run_time=0.3)

        onlyhi = Text("only the high frequency is tuned to this gap",
                      font="Arial", color=WARM).scale(0.36)
        onlyhi.next_to(panel, UP, buff=0.22).shift(LEFT * 1.3)
        self.play(FadeIn(onlyhi), run_time=0.5)
        self.play(ampHigh.animate.set_value(0.15), run_time=2.2)  # ampLow untouched
        self.wait(1.0)

        self.play(
            FadeOut(wall2), FadeOut(flr2), FadeOut(panel), FadeOut(gaplab),
            FadeOut(onlyhi), FadeOut(axisL2), FadeOut(act2_wave),
            run_time=0.8,
        )
        ampHigh.set_value(1.0)

        # ================================================================
        # ACT 3 — quadratic-residue diffuser: scatters, doesn't absorb
        # ================================================================
        self.play(set_act_label("Quadratic-residue diffuser"), run_time=0.6)

        N = 7
        seq = [(n * n) % N for n in range(N)]     # 0,1,4,2,2,4,1
        unit = 0.34                                # visual unit for "7mm"
        wellw = 0.6                                # equal well width ("30mm")
        xDiffStart = xW - N * wellw
        wells = VGroup()
        for i, s in enumerate(seq):
            depth = s * unit
            x0 = xDiffStart + i * wellw
            x1 = x0 + wellw
            face_x = xW - depth
            block = Polygon(
                [x0, floorY, 0], [x0, floorY + 2.6, 0],
                [face_x, floorY + 2.6, 0], [face_x, floorY, 0],
                color=WARM, fill_color=WARM, fill_opacity=0.30, stroke_width=1.6,
            )
            wells.add(block)
        backwall = Line([xW, floorY, 0], [xW, floorY + 2.6, 0],
                        color=ICE, stroke_width=2)
        flr3 = Line([xL, floorY, 0], [xW, floorY, 0], color=ICE, stroke_width=5)
        qrdlab = Text("well depths follow (n² mod 7) × unit, equal widths",
                      font="Arial", color=ICE).scale(0.34)
        qrdlab.next_to([(xL + xW) / 2, 2.7, 0], DOWN, buff=0.15)

        xEnter3 = xL + 0.4
        wf_pos = ValueTracker(xEnter3)

        def incoming_curve():
            c = wf_pos.get_value()
            xs = np.linspace(xL, xDiffStart, 200)
            env = np.exp(-((xs - c) ** 2) / (2 * (0.5) ** 2))
            wl = 0.9
            ys = baseY + 0.5 * env * np.sin(2 * np.pi * (xs - c) / wl)
            pts = [[x, y, 0] for x, y in zip(xs, ys)]
            m = VMobject(color=CYAN, stroke_width=4)
            m.set_points_smoothly(pts)
            return m

        incoming = always_redraw(incoming_curve)
        axisL3 = Line([xL, baseY, 0], [xW, baseY, 0], color=DIM, stroke_width=1.5)

        self.play(Create(flr3), Create(backwall), run_time=0.6)
        self.play(FadeIn(wells), FadeIn(qrdlab), run_time=0.8)
        self.add(axisL3, incoming)
        self.play(wf_pos.animate.set_value(xDiffStart - 0.2), run_time=1.4,
                  rate_func=lambda x: x)
        self.remove(incoming)

        # scatter fan: many diverging rays off the diffuser face
        origin = np.array([xDiffStart + (wellw * N) / 2 - 0.3, floorY + 1.4, 0])
        angles = np.linspace(-70, 70, 7)
        rays = VGroup()
        for ang in angles:
            rad = np.radians(ang)
            direction = np.array([np.cos(rad), np.sin(rad), 0])
            end = origin + direction * 2.3
            ray = Arrow(origin, end, color=CYAN, stroke_width=3, buff=0.05,
                        max_tip_length_to_length_ratio=0.15)
            rays.add(ray)
        scatterlab = Text("scattered — not absorbed, redirected", font="Arial",
                          color=WARM).scale(0.36)
        scatterlab.next_to([(xL + xW) / 2, floorY - 0.35, 0], DOWN, buff=0.1)

        self.play(Create(rays, lag_ratio=0.08), FadeIn(scatterlab), run_time=1.2)

        halved = Text("both spikes fall by half — the floor rises to meet them",
                      font="Arial", color=WARM).scale(0.34)
        halved.next_to([(sx0 + sx1) / 2, sTop, 0], DOWN, buff=1.9)
        self.play(FadeIn(halved), run_time=0.4)
        self.play(ampLow.animate.set_value(0.5), ampHigh.animate.set_value(0.5),
                  floor.animate.set_value(0.5), run_time=2.4)
        self.wait(1.6)

        self.play(
            FadeOut(wells), FadeOut(backwall), FadeOut(flr3), FadeOut(qrdlab),
            FadeOut(rays), FadeOut(scatterlab), FadeOut(halved), FadeOut(axisL3),
            FadeOut(act_label),
            run_time=1.0,
        )
        self.wait(0.6)
