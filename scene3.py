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


class Scene3GenericSteps(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ── Professional Title Sequence ──
        title = Text("Generic Steps in Any Call", font_size=40, weight=BOLD, color=SOFT_WHITE)
        sub   = Text("These sequential stages apply to every cellular call", font_size=22, color=ACCENT_BLUE)
        hdr   = VGroup(title, sub).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.45)
        
        self.play(FadeIn(hdr, shift=DOWN*0.3), run_time=1.2, rate_func=rate_functions.ease_out_cubic)
        self.wait(0.5)

        # ── Timeline Data ──
        steps = [
            ("1", "Call Request Initiation",   ALT_YELLOW,  "Mobile dials → sends request via RECC to BS"),
            ("2", "Authentication & Validation", ACCENT_GRN,  "MSC verifies subscriber identity via HLR"),
            ("3", "Location Identification",    ACCENT_BLUE, "HLR/VLR pinpoints which cell the receiver is in"),
            ("4", "Channel Allocation",         ACCENT_PURP, "MSC assigns a Traffic Channel (TCH)"),
            ("5", "Call Routing",               ACCENT_RED,  "Signal routed through designated network path"),
            ("6", "Call Setup — Connected!",    ACCENT_GRN,  "Receiver rings → user answers → call established"),
        ]

        step_items = VGroup()
        for num, title_s, col, desc in steps:
            # Badge
            num_circle = Circle(radius=0.26, color=col, fill_color=col, fill_opacity=0.15, stroke_width=2.5)
            num_text   = Text(num, font_size=20, color=col, weight=BOLD).move_to(num_circle)
            num_mob    = VGroup(num_circle, num_text)

            # Elegant typography
            step_title = Text(title_s, font_size=19, color=col, weight=BOLD)
            step_desc  = Text(desc,   font_size=15, color=SOFT_WHITE)
            text_col   = VGroup(step_title, step_desc).arrange(DOWN, buff=0.1, aligned_edge=LEFT)

            row = VGroup(num_mob, text_col).arrange(RIGHT, buff=0.35)
            step_items.add(row)

        step_items.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        step_items.next_to(hdr, DOWN, buff=0.6)
        step_items.to_edge(LEFT, buff=1.2)

        # ── Timeline Connector ──
        line_x = step_items.get_left()[0] + 0.26
        top_y  = step_items[0].get_center()[1]
        bot_y  = step_items[-1].get_center()[1]
        v_line = DashedLine(
            [line_x, top_y, 0], [line_x, bot_y, 0],
            color=DIM_GREY, stroke_width=1.5, dash_length=0.12
        )

        # ── Decorative SVG Graphic ──
        try:
            call_svg = SVGMobject(UTILS + "on_call.svg").scale_to_fit_height(3.0).set_color(SOFT_WHITE)
        except Exception:
            call_svg = Circle(radius=1.5, color=ALT_YELLOW, fill_opacity=0.3)
        call_svg.to_edge(RIGHT, buff=2.0)

        # ── Fluid Sequential View ──
        self.play(
            Create(v_line),
            FadeIn(call_svg, shift=LEFT*0.3),
            run_time=1.0, rate_func=rate_functions.ease_in_out_sine
        )
        
        for item in step_items:
            self.play(
                FadeIn(item, shift=RIGHT*0.25),
                run_time=0.8,
                rate_func=rate_functions.ease_out_cubic
            )
            self.wait(2.0)

        # Highlight final step dynamically
        final_box = SurroundingRectangle(step_items[-1], color=ACCENT_GRN, corner_radius=0.15, buff=0.15)
        glow = final_box.copy().set_stroke(width=4, opacity=0.3).scale(1.02)
        
        self.play(
            Create(final_box), FadeIn(glow),
            step_items[-1][1][0].animate.set_color(SOFT_WHITE), 
            run_time=0.8,
            rate_func=rate_functions.ease_out_cubic
        )
        self.wait(1.5)

        # Smooth teardown
        self.play(
            FadeOut(VGroup(hdr, step_items, v_line, call_svg, final_box, glow), shift=UP*0.3), 
            run_time=0.9, 
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(0.3)
