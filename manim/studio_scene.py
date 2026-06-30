"""
studio_scene.py — Case study 3 (Recording studio) hero clip.
A low-frequency room mode is caught in a corner bass trap: the standing wave
decays as the rockwool absorbs it, and — driven by the SAME decay tracker — its
peak in the frequency spectrum attenuates in lock-step. Dark cinematic palette.

Render (from repo root, with tools/ on PATH so manim finds ffmpeg):
  PATH="E:/cvweb/tools:$PATH" python -m manim -qm --format mp4 \
       -o studio manim/studio_scene.py BassTrap
"""
import numpy as np
from manim import (
    Scene, VMobject, Line, Polygon, Text, Arrow, Dot, VGroup,
    ValueTracker, Mobject, always_redraw, config,
    FadeIn, FadeOut, Create, Write, UP, DOWN, LEFT, RIGHT, ORIGIN,
)

BG    = "#0E1330"
ICE   = "#CADCFC"
CYAN  = "#6BD0FF"
CORAL = "#F96167"
WARM  = "#F2A65A"
DIM   = "#46527F"

config.background_color = BG


class BassTrap(Scene):
    def construct(self):
        # ---- shared physics trackers ----
        t = ValueTracker(0.0)     # time (real seconds)
        amp = ValueTracker(1.0)   # energy in the mode (1 -> absorbed)
        omega = 2.6
        k = 1.55

        clock = Mobject()
        clock.add_updater(lambda m, dt: t.increment_value(dt))
        self.add(clock)

        # ============ LEFT PANEL — the room corner ============
        xL, xW = -6.1, -1.0          # room far edge / reflecting wall
        floorY = -2.6
        baseY = 0.5
        scale = 1.05

        wall  = Line([xW, floorY, 0], [xW, 2.7, 0], color=ICE, stroke_width=5)
        floor = Line([xL, floorY, 0], [xW, floorY, 0], color=ICE, stroke_width=5)

        # corner bass trap (rockwool triangle in the wall/floor corner)
        trap = Polygon(
            [xW, floorY, 0], [xW, floorY + 1.7, 0], [xW - 1.5, floorY, 0],
            color=WARM, fill_color=WARM, fill_opacity=0.22, stroke_width=2,
        )
        hatch = VGroup(*[
            Line([xW - 1.5 + i * 0.3, floorY, 0],
                 [xW, floorY + 1.7 - i * 0.34, 0], color=WARM, stroke_width=1.2)
            for i in range(1, 5)
        ])

        def pressure(x, tt, a):
            return baseY + scale * a * np.cos(k * (x - xW)) * np.cos(omega * tt)

        def wave_curve():
            xs = np.linspace(xL, xW, 220)
            pts = [[x, pressure(x, t.get_value(), amp.get_value()), 0] for x in xs]
            m = VMobject(color=CYAN, stroke_width=4)
            m.set_points_smoothly(pts)
            return m

        wave = always_redraw(wave_curve)
        axisL = Line([xL, baseY, 0], [xW, baseY, 0], color=DIM, stroke_width=1.5)

        labL = Text("Room mode caught in the corner", font="Arial",
                    color=ICE, weight="MEDIUM").scale(0.42)
        labL.next_to([(xL + xW) / 2, 2.7, 0], DOWN, buff=0.15)

        # ============ RIGHT PANEL — frequency spectrum ============
        sx0, sx1 = 1.1, 6.4
        sBase = -1.9
        f0 = 3.7                      # the room-mode frequency
        sAxis = Line([sx0, sBase, 0], [sx1, sBase, 0], color=DIM, stroke_width=2)
        yAxis = Line([sx0, sBase, 0], [sx0, 2.4, 0], color=DIM, stroke_width=2)

        def spectrum_curve():
            a = amp.get_value()
            H = 3.6 * a
            sigma = 0.16 + 0.30 * (1 - a)        # damping broadens the peak
            xs = np.linspace(sx0 + 0.05, sx1, 240)
            pts = [[x, sBase + H * np.exp(-((x - f0) ** 2) / (2 * sigma ** 2)), 0]
                   for x in xs]
            m = VMobject(color=CORAL, stroke_width=4)
            m.set_points_smoothly(pts)
            return m

        peak = always_redraw(spectrum_curve)
        f0tick = Line([f0, sBase - 0.12, 0], [f0, sBase + 0.12, 0],
                      color=ICE, stroke_width=2)
        f0lab = Text("room mode", font="Arial", color=DIM).scale(0.34)
        f0lab.next_to([f0, sBase, 0], DOWN, buff=0.18)
        labR = Text("Frequency spectrum", font="Arial", color=ICE,
                    weight="MEDIUM").scale(0.42)
        labR.next_to([(sx0 + sx1) / 2, 2.4, 0], UP, buff=0.12)
        freqlab = Text("frequency", font="Arial", color=DIM).scale(0.32)
        freqlab.next_to([sx1, sBase, 0], DOWN, buff=0.18).shift(LEFT * 0.3)

        # ============ Fourier link ============
        f_arrow = Arrow([xW + 0.2, 0.3, 0], [sx0 - 0.2, 0.3, 0],
                        color=ICE, stroke_width=3, buff=0.1)
        f_text = Text("Fourier transform", font="Arial", color=ICE).scale(0.34)
        f_text.next_to(f_arrow, UP, buff=0.08)

        # ============ choreography ============
        self.play(Create(wall), Create(floor), run_time=1.0)
        self.play(FadeIn(trap), Create(hatch), FadeIn(labL), run_time=1.0)
        self.add(axisL, wave)
        self.wait(1.6)                                   # standing wave oscillates

        self.play(Create(sAxis), Create(yAxis), FadeIn(labR),
                  FadeIn(f0tick), FadeIn(f0lab), FadeIn(freqlab), run_time=1.0)
        self.add(peak)
        self.play(Create(f_arrow), Write(f_text), run_time=1.0)
        self.wait(1.2)

        # absorption: energy drains -> wave flattens AND peak attenuates together
        absorb = Text("rockwool absorbs the energy", font="Arial",
                      color=WARM).scale(0.36)
        absorb.next_to(trap, UP, buff=0.25).shift(RIGHT * 0.2)
        self.play(FadeIn(absorb), run_time=0.6)
        self.play(amp.animate.set_value(0.10), run_time=5.0)
        self.wait(0.8)

        settled = Text("mode attenuated", font="Arial", color=CYAN).scale(0.4)
        settled.move_to([(xL + xW) / 2, baseY - 1.7, 0])
        self.play(FadeIn(settled), run_time=0.6)
        self.wait(1.4)
