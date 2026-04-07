from manim import *

# ── Palette (3B1B-inspired) ────────────────────────────────────────────────
CREAM       = "#FFFBE6"
DARK_BG     = "#1C1C2E"
ACCENT_BLUE = "#58C4DD"
ACCENT_RED  = "#FF6B6B"
ACCENT_GRN  = "#6BCB77"
DIM_GREY    = "#888899"
SOFT_WHITE  = "#E8E8F0"


class Scene1Recap(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ── Layout constants ────────────────────────────────────────────
        AXIS_Y       = -0.85
        POOL_Y       = AXIS_Y
        POOL_LABEL_Y = AXIS_Y - 0.58
        CELL_Y       =  1.55
        POOL_X       = [-3.6, 0.0, 3.6]
        POOL_W       = 3.0
        COLORS       = [ACCENT_RED, ACCENT_GRN, ACCENT_BLUE]
        POOL_LBL     = ["Pool-1", "Pool-2", "Pool-3"]
        CELL_LBL     = ["A", "B", "C"]

        # ── Title ──────────────────────────────────────────────────────
        title = Text("Introduction to 1G AMPS", font_size=38, weight=BOLD, color=SOFT_WHITE)
        subtitle = Text("Call Flow in 1G Cellular", font_size=22, color=ACCENT_BLUE)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.45)
        self.play(FadeIn(title_group, shift=DOWN*0.25))
        self.wait(0.4)

        # ── Recap label ─────────────────────────────────────────────────
        # recap = Text("Quick Recap from Module 1", font_size=20, color=CREAM, slant=ITALIC)
        # recap.next_to(title_group, DOWN, buff=0.35)
        # self.play(FadeIn(recap))
        self.wait(0.5)

        # ── Frequency Axis ──────────────────────────────────────────────
        axis = Arrow(
            start=LEFT * 5.5, end=RIGHT * 5.5,
            color=DIM_GREY, buff=0, stroke_width=2.5,
            tip_length=0.2
        ).set_y(AXIS_Y)

        label_mhz = Text("MHz", font_size=18, color=DIM_GREY).next_to(axis, RIGHT, buff=0.1)
        label_825 = Text("825", font_size=16, color=DIM_GREY).next_to(axis.get_left(), DOWN, buff=0.15)
        label_849 = Text("849", font_size=16, color=DIM_GREY).next_to(axis.get_right() + LEFT*0.3, DOWN, buff=0.15)

        self.play(GrowArrow(axis), FadeIn(label_mhz, label_825, label_849))
        self.wait(0.3)

        # ── Three pools on the axis ─────────────────────────────────────
        pools = VGroup()
        pool_texts = VGroup()
        for xp, pc, pl in zip(POOL_X, COLORS, POOL_LBL):
            rect = Rectangle(
                width=POOL_W, height=0.45,
                fill_color=pc, fill_opacity=0.35,
                stroke_color=pc, stroke_width=1.5
            ).move_to([xp, POOL_Y, 0])
            lbl = Text(pl, font_size=17, color=pc, weight=BOLD).move_to([xp, POOL_LABEL_Y, 0])
            pools.add(rect)
            pool_texts.add(lbl)

        self.play(
            LaggedStart(*[FadeIn(p, scale=0.8) for p in pools], lag_ratio=0.3),
            LaggedStart(*[FadeIn(t) for t in pool_texts], lag_ratio=0.3),
        )
        self.wait(0.4)

        # ── Hexagonal cells ─────────────────────────────────────────────
        def hex_cell(center, color, label_str):
            h = RegularPolygon(n=6, start_angle=PI/6,
                               color=color, fill_opacity=0.18,
                               stroke_width=2).scale(0.72)
            h.move_to(center)
            lbl = Text(label_str, font_size=22, color=color, weight=BOLD).move_to(center)
            return VGroup(h, lbl)

        cell_centers = [LEFT*3.5 + UP*CELL_Y, UP*CELL_Y, RIGHT*3.5 + UP*CELL_Y]
        cells = [
            hex_cell(cell_centers[0], ACCENT_RED, "A"),
            hex_cell(cell_centers[1], ACCENT_GRN, "B"),
            hex_cell(cell_centers[2], ACCENT_BLUE, "C"),
        ]

        # Arrows from pool rect top-centre → hex bottom
        arrows = []
        for i in range(3):
            arr = Arrow(
                start=pools[i].get_top(), end=cells[i][0].get_bottom(),
                color=COLORS[i], buff=0.05,
                stroke_width=2, tip_length=0.15,
                max_tip_length_to_length_ratio=0.3
            )
            arrows.append(arr)

        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in cells], lag_ratio=0.25))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25))
        self.wait(0.5)

        # ── Closing text ────────────────────────────────────────────────
        closing = Text(
            "No two adjacent cells share the same spectrum.",
            font_size=21, color=YELLOW, weight=BOLD
        ).to_edge(DOWN, buff=0.5)

        self.play(Write(closing))
        self.wait(2)

        # ── Fade out all ────────────────────────────────────────────────
        everything = VGroup(
            title_group, axis, label_mhz, label_825, label_849,
            pools, pool_texts, *cells, *arrows, closing
        )
        self.play(FadeOut(everything, shift=UP*0.3))
        self.wait(0.3)