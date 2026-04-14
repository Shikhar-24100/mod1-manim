from manim import *

# ── Palette (3B1B-inspired) ────────────────────────────────────────────────
CREAM       = "#FFFBE6"
DARK_BG     = "#1C1C2E"
ACCENT_BLUE = "#58C4DD"
ACCENT_RED  = "#FF6B6B"
ACCENT_GRN  = "#6BCB77"
DIM_GREY    = "#888899"
SOFT_WHITE  = "#E8E8F0"
ALT_YELLOW  = "#F2D388"
CARD_BG     = "#2A2A3D"

class TransitionMod1toMod2(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ══════════════════════════════════════════════════════════════
        # BEAT 1 — The problem we left with (Lecture 6 ending)
        # ══════════════════════════════════════════════════════════════

        problem = Text(
            "Limited spectrum. Growing users. How do we scale?",
            font_size=22, color=DIM_GREY, slant=ITALIC
        ).move_to(ORIGIN)
        self.play(FadeIn(problem, shift=UP * 0.2))
        self.wait(3.2)

        # ── Answer fades in below ─────────────────────────────────────
        answer = Text(
            "Reuse the same spectrum — across different cells.",
            font_size=24, color=SOFT_WHITE, weight=BOLD
        ).next_to(problem, DOWN, buff=0.4)
        self.play(FadeIn(answer, shift=UP * 0.15))
        self.wait(4.0)

        self.play(FadeOut(VGroup(problem, answer)))

        # ══════════════════════════════════════════════════════════════
        # BEAT 2 — Frequency reuse visualised (3 cells, 3 pools)
        # Fast, no text — just the visual clicking into place
        # ══════════════════════════════════════════════════════════════

        colors = [ACCENT_BLUE, ACCENT_GRN, ACCENT_RED]
        centers = [LEFT * 3.2, ORIGIN, RIGHT * 3.2]
        pool_labels = ["Pool 1", "Pool 2", "Pool 3"]

        hexes = []
        pool_lbls = []
        for ctr, col, pl in zip(centers, colors, pool_labels):
            h = RegularPolygon(n=6, start_angle=PI/6,
                               color=col, fill_opacity=0.15,
                               stroke_width=2).scale(1.5).move_to(ctr)
            l = Text(pl, font_size=16, color=col, weight=BOLD).move_to(ctr)
            hexes.append(h)
            pool_lbls.append(l)

        self.play(
            LaggedStart(*[DrawBorderThenFill(h) for h in hexes], lag_ratio=0.25),
            run_time=0.9
        )
        self.play(
            LaggedStart(*[FadeIn(l, scale=0.8) for l in pool_lbls], lag_ratio=0.2),
            run_time=0.6
        )
        self.wait(2.5)

        # ── "But this raises a question..." ──────────────────────────
        question = Text(
            "But how does a mobile actually USE this network?",
            font_size=20, color=ALT_YELLOW
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(question, shift=UP * 0.15))
        self.wait(3.2)

        self.play(FadeOut(VGroup(*hexes, *pool_lbls, question)))

        # ══════════════════════════════════════════════════════════════
        # BEAT 3 — Module 2 title card
        # ══════════════════════════════════════════════════════════════

        mod_label = Text("Module 2", font_size=18, color=DIM_GREY)
        mod_title = Text("1G AMPS & Call Flow\nin Cellular Networks",
                         font_size=34, weight=BOLD, color=ALT_YELLOW,
                         line_spacing=1.2)
        mod_group = VGroup(mod_label, mod_title).arrange(DOWN, buff=0.2)
        mod_group.move_to(ORIGIN)

        self.play(FadeIn(mod_label))
        self.play(Write(mod_title), run_time=1.2)
        self.wait(3.2)

        self.play(FadeOut(mod_group), run_time=0.7)
        self.wait(1.2)