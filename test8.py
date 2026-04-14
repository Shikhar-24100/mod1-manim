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


class TransitionToCallMaking(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ══════════════════════════════════════════════════════════════
        # TRANSITION LINES
        # ══════════════════════════════════════════════════════════════
        line1 = Text(
            "We now know how a mobile registers on the network.",
            font_size=21, color=DIM_GREY
        ).move_to(UP * 0.5)
        self.play(FadeIn(line1, shift=UP * 0.15))
        self.wait(1.0)

        line2 = Text(
            "But what happens when it wants to make a call?",
            font_size=23, color=SOFT_WHITE, weight=BOLD
        ).next_to(line1, DOWN, buff=0.35)
        self.play(FadeIn(line2, shift=UP * 0.15))
        self.wait(1.0)

        self.play(FadeOut(VGroup(line1, line2)))

        # ══════════════════════════════════════════════════════════════
        # NEXT VIDEO CARD
        # ══════════════════════════════════════════════════════════════
        next_lbl = Text("Next Video", font_size=16, color=DIM_GREY)
        next_title = Text(
            "Call Making in 1G AMPS",
            font_size=30, color=ALT_YELLOW, weight=BOLD
        )
        next_sub = Text(
            "Call modes across different scenarios",
            font_size=17, color=CREAM, slant=ITALIC
        )
        card = VGroup(next_lbl, next_title, next_sub).arrange(DOWN, buff=0.18)
        card.move_to(ORIGIN)

        box = SurroundingRectangle(
            card, color=ALT_YELLOW, corner_radius=0.15,
            buff=0.3, stroke_width=1.5,
            fill_color=CARD_BG, fill_opacity=0.5
        )

        self.play(FadeIn(box), FadeIn(card, scale=0.9))
        self.wait(2.5)

        self.play(FadeOut(VGroup(box, card)), run_time=0.7)
        self.wait(0.2)
        # ══════════════════════════════════════════════════════════════