from manim import *

UTILS = "utils/"

CREAM       = "#FFFBE6"
DARK_BG     = "#1C1C2E"
ACCENT_BLUE = "#58C4DD"
ACCENT_RED  = "#FF6B6B"
ACCENT_GRN  = "#6BCB77"
DIM_GREY    = "#888899"
SOFT_WHITE  = "#E8E8F0"
ALT_YELLOW  = "#F2D388"
ACCENT_PURP = "#C084FC"


class Scene8Summary(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        title = Text("Summary — All 4 Cases", font_size=38, weight=BOLD, color=SOFT_WHITE)
        sub   = Text("Call Establishment in 1G AMPS Cellular Network",
                     font_size=20, color=ACCENT_BLUE)
        hdr   = VGroup(title, sub).arrange(DOWN, buff=0.20).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr, shift=DOWN*0.15))
        self.wait(0.3)

        col_headers = ["Case", "Caller", "Receiver", "Key Mechanism", "Key Entity"]
        col_colors  = [SOFT_WHITE] * 5
        col_widths  = [1.0, 2.0, 2.5, 3.0, 2.2]
        col_x_pos   = [-5.2, -3.6, -1.8, 0.5, 3.2]

        header_row = VGroup()
        for txt, col, x in zip(col_headers, col_colors, col_x_pos):
            t = Text(txt, font_size=18, color=ACCENT_BLUE, weight=BOLD).move_to([x, 1.9, 0])
            header_row.add(t)

        header_line = Line(LEFT*6.5 + UP*1.60, RIGHT*6.5 + UP*1.60,
                           color=ACCENT_BLUE, stroke_width=1.5)
        self.play(
            LaggedStart(*[FadeIn(h) for h in header_row], lag_ratio=0.1),
            Create(header_line),
            run_time=0.8
        )

        rows_data = [
            ("1", "Home Cell", "Same Cell", "Direct — no routing", ACCENT_BLUE,   ACCENT_GRN),
            ("2", "Home Cell", "Diff Cell\n(Same MSC)", "Paging + VLR lookup", ACCENT_GRN, ACCENT_RED),
            ("3", "Home Cell", "Diff MSC\n(Cell 3)", "HLR lookup +\nInter-MSC route", ACCENT_PURP, ACCENT_PURP),
            ("4", "Visiting\n(Roaming)", "Any cell", "VLR → HLR auth\n+ routing", ACCENT_RED, ACCENT_RED),
        ]

        row_y = [1.0, 0.05, -0.9, -1.9]
        row_colors = [ACCENT_BLUE, ACCENT_GRN, ACCENT_PURP, ACCENT_RED]

        for i, ((case, caller, recv, mech, row_col, key_col), y) in enumerate(
                zip(rows_data, row_y)):

            row_bg = RoundedRectangle(
                corner_radius=0.1, width=13.0, height=0.85,
                color=row_col, fill_opacity=0.07, stroke_width=0.8
            ).move_to([0, y, 0])

            cells = [
                Text(case,   font_size=16, color=row_col, weight=BOLD),
                Text(caller, font_size=15, color=SOFT_WHITE),
                Text(recv,   font_size=15, color=SOFT_WHITE),
                Text(mech,   font_size=14, color=SOFT_WHITE),
                Text("HLR" if i == 0 else "VLR+Paging" if i == 1 else
                     "HLR+MSC" if i == 2 else "VLR→HLR",
                     font_size=15, color=key_col, weight=BOLD),
            ]
            for cell, x in zip(cells, col_x_pos):
                cell.move_to([x, y, 0])

            row_grp = VGroup(row_bg, *cells)
            self.play(
                FadeIn(row_bg, shift=RIGHT*0.4),
                LaggedStart(*[FadeIn(c, shift=RIGHT*0.2) for c in cells], lag_ratio=0.08),
                run_time=0.65
            )
            self.wait(5)

        self.wait(0.5)

        final_sub = Text(
            "HLR (permanent) + VLR (temporary) = seamless mobility",
            font_size=18, color=DIM_GREY
        ).to_edge(DOWN, buff=0.25)
        final_msg = Text(
            "The network ALWAYS knows where you are.",
            font_size=28, color=ALT_YELLOW, weight=BOLD
        ).next_to(final_sub, UP, buff=0.2)

        self.play(
            FadeIn(final_msg, scale=0.9),
            run_time=0.7
        )
        self.play(FadeIn(final_sub, shift=UP*0.15), run_time=0.5)
        self.wait(2.5)

        self.play(FadeOut(Group(*self.mobjects), shift=UP*0.3), run_time=0.9)
        self.wait(0.3)
