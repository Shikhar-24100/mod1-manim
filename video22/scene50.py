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


def make_hex(center, col, scale=1.55):
    return RegularPolygon(
        n=6, start_angle=PI / 6,
        color=col, fill_opacity=0.10, stroke_width=2
    ).scale(scale).move_to(center)


def make_bs(center, col, label="BS"):
    try:
        icon = SVGMobject(UTILS + "bs_tower.svg").scale(0.35)
    except Exception:
        icon = Triangle(color=col, fill_opacity=0.5).scale(0.30)
    icon.move_to(center)
    lbl = Text(label, font_size=12, color=col, weight=BOLD).next_to(icon, DOWN, buff=0.1)
    return VGroup(icon, lbl)


def make_mobile(center, col=ALT_YELLOW, label=""):
    try:
        ico = SVGMobject(UTILS + "mobile.svg").scale(0.30)
    except Exception:
        ico = RoundedRectangle(corner_radius=0.08, width=0.26, height=0.42,
                               color=ALT_YELLOW, fill_opacity=0.5)
    ico.move_to(center)
    if label:
        lbl = Text(label, font_size=12, color=SOFT_WHITE, weight=BOLD).next_to(ico, DOWN, buff=0.08)
        return VGroup(ico, lbl)
    return VGroup(ico)


def make_db(center, svg_name, label, col, scale=0.28):
    try:
        ico = SVGMobject(UTILS + svg_name).scale(scale)
    except Exception:
        ico = RoundedRectangle(corner_radius=0.08, width=0.40, height=0.34,
                               color=col, fill_opacity=0.4)
    ico.move_to(center)
    lbl = Text(label, font_size=12, color=col, weight=BOLD).next_to(ico, DOWN, buff=0.08)
    return VGroup(ico, lbl)


def make_msc(center, label="MSC", col=ACCENT_PURP):
    try:
        ico = SVGMobject(UTILS + "msc_switch.svg").scale(0.38)
    except Exception:
        ico = RoundedRectangle(corner_radius=0.12, width=0.70, height=0.55,
                               color=col, fill_opacity=0.35)
    ico.move_to(center)
    lbl = Text(label, font_size=13, color=col, weight=BOLD).next_to(ico, DOWN, buff=0.08)
    return VGroup(ico, lbl)


def callout_box(text, col=CREAM):
    t = Text(text, font_size=18, color=col, line_spacing=1.2)
    box = SurroundingRectangle(t, corner_radius=0.15, color=col,
                               fill_color="#181825", fill_opacity=0.85,
                               buff=0.25, stroke_width=2)
    glow = box.copy().set_stroke(color=col, width=4, opacity=0.3).scale(1.02)
    return VGroup(glow, box, t)


class Scene5Case2DiffCellSameMSC(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ── Title ──
        case_tag = Text("CASE 2", font_size=28, color=ACCENT_GRN, weight=BOLD)
        title    = Text("Different Cell — Same MSC", font_size=38, weight=BOLD, color=SOFT_WHITE)
        sub      = Text("Caller in Cell 1  ·  Receiver in Cell 2  ·  Shared MSC",
                        font_size=20, color=DIM_GREY)
        hdr = VGroup(case_tag, title, sub).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr, shift=DOWN*0.2), run_time=1.2,
                  rate_func=rate_functions.ease_out_cubic)
        self.wait(0.3)

        # ── Layout ──
        c1_center = LEFT*0.3  + DOWN*0.2
        c2_center = RIGHT*4.0 + DOWN*0.2
        mid_x     = (c1_center[0] + c2_center[0]) / 2

        hex1 = make_hex(c1_center, ACCENT_BLUE, scale=1.9)
        hex2 = make_hex(c2_center, ACCENT_BLUE, scale=1.9)
        lbl1 = Text("Cell 1", font_size=16, color=ACCENT_BLUE,
                    weight=BOLD).move_to(c1_center + DOWN*2.2)
        lbl2 = Text("Cell 2", font_size=16, color=ACCENT_BLUE,
                    weight=BOLD).move_to(c2_center + DOWN*2.2)

        self.play(
            LaggedStart(DrawBorderThenFill(hex1), DrawBorderThenFill(hex2), lag_ratio=0.15),
            LaggedStart(FadeIn(lbl1, shift=UP*0.1), FadeIn(lbl2, shift=UP*0.1), lag_ratio=0.15),
            run_time=1.2, rate_func=rate_functions.ease_in_out_sine
        )

        bs1 = make_bs(c1_center + UP*0.1, ACCENT_BLUE, "BS₁")
        bs2 = make_bs(c2_center + UP*0.1, ACCENT_BLUE, "BS₂")

        msc = make_msc(RIGHT*mid_x + UP*1.8, col=ACCENT_BLUE)

        # HLR left of MSC, VLR right of MSC
        hlr = make_db(RIGHT*mid_x + LEFT*2.2  + UP*1.8, "hlr_box.svg", "HLR", ACCENT_BLUE, scale=0.26)
        vlr = make_db(RIGHT*mid_x + RIGHT*2.2 + UP*1.8, "vlr_box.svg", "VLR", ACCENT_RED,  scale=0.26)

        caller   = make_mobile(c1_center + LEFT*1.4 + DOWN*0.6, ALT_YELLOW, "Caller")
        receiver = make_mobile(c2_center + RIGHT*1.4 + DOWN*0.6, ACCENT_GRN, "Receiver")

        self.play(
            LaggedStart(
                FadeIn(bs1, scale=0.8), FadeIn(bs2, scale=0.8),
                FadeIn(msc, scale=0.8),
                FadeIn(hlr, scale=0.8), FadeIn(vlr, scale=0.8),
                FadeIn(caller, shift=RIGHT*0.2), FadeIn(receiver, shift=LEFT*0.2),
                lag_ratio=0.1
            ),
            run_time=2.0, rate_func=rate_functions.ease_out_cubic
        )
        self.wait(0.4)

        # ── Step Labels ──
        step_data = [
            ("① Caller → BS₁ → MSC",                            ALT_YELLOW),
            ("② MSC → HLR\n    (Confirm subscriber + get pointer)", ACCENT_BLUE),
            ("③ HLR → MSC\n    (Receiver is in this MSC area)",  ACCENT_BLUE),
            ("④ MSC → VLR\n    (Get exact cell → Cell 2)",       ACCENT_RED),
            ("⑤ Paging → BS₂ → Receiver",                       ALT_YELLOW),
            ("⑥ Channel allocated\n    in both cells",           DIM_GREY),
            ("⑦ Call connected\n    via MSC ✓",                  ACCENT_GRN),
        ]
        step_texts = VGroup(*[
            Text(s, font_size=15, color=c, weight=BOLD) for s, c in step_data
        ])
        step_texts.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        step_texts.to_edge(LEFT, buff=0.45).shift(DOWN*0.5)

        arrows_grp = VGroup()

        # ── Step 1: Caller → BS₁ → MSC ──
        a1 = Arrow(caller.get_top(), bs1.get_center(), buff=0.3, color=ALT_YELLOW,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        a1b= Arrow(bs1.get_top(), msc.get_bottom() + LEFT*0.2, buff=0.25, color=ALT_YELLOW,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        arrows_grp.add(a1, a1b)
        self.play(Create(a1), Create(a1b),
                  FadeIn(step_texts[0], shift=RIGHT*0.2),
                  run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        self.wait(6.0)

        # ── Step 2: MSC → HLR (query) ──
        a2 = Arrow(msc.get_left(), hlr.get_right(), buff=0.15, color=ACCENT_BLUE,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        hlr_highlight = SurroundingRectangle(hlr, color=ACCENT_BLUE, stroke_width=3.5,
                                             buff=0.2, corner_radius=0.15)
        hlr_glow = hlr_highlight.copy().set_stroke(width=6, opacity=0.3).scale(1.05)
        arrows_grp.add(a2)
        self.play(Create(a2), Create(hlr_highlight), FadeIn(hlr_glow),
                  FadeIn(step_texts[1], shift=RIGHT*0.2),
                  run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        self.wait(6.0)

        # ── Step 3: HLR → MSC (response) ──
        a3 = Arrow(hlr.get_right(), msc.get_left(), buff=0.15, color=ACCENT_BLUE,
                   stroke_width=3.0, max_tip_length_to_length_ratio=0.15)
        hlr_resp = Text("In this MSC", font_size=11, color=ACCENT_BLUE,
                        slant=ITALIC).move_to(a3.get_center() + DOWN*0.22)
        arrows_grp.add(a3)
        self.play(Create(a3), FadeIn(hlr_resp),
                  FadeIn(step_texts[2], shift=RIGHT*0.2),
                  run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        self.wait(6.0)

        # ── Step 4: MSC → VLR (exact cell) ──
        a4  = Arrow(msc.get_right(), vlr.get_left(), buff=0.15, color=ACCENT_RED,
                    stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        a4b = Arrow(vlr.get_left(), msc.get_right(), buff=0.15, color=ACCENT_RED,
                    stroke_width=3.0, max_tip_length_to_length_ratio=0.15)
        vlr_highlight = SurroundingRectangle(vlr, color=ACCENT_RED, stroke_width=3.5,
                                             buff=0.2, corner_radius=0.15)
        vlr_glow = vlr_highlight.copy().set_stroke(width=6, opacity=0.3).scale(1.05)
        vlr_lbl  = Text("Cell 2", font_size=11, color=ACCENT_RED,
                        weight=BOLD).move_to(a4.get_center() + UP*0.22)
        arrows_grp.add(a4, a4b)
        self.play(Create(a4), Create(a4b),
                  Create(vlr_highlight), FadeIn(vlr_glow), FadeIn(vlr_lbl),
                  FadeIn(step_texts[3], shift=RIGHT*0.2),
                  run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        self.wait(6.0)

        # ── Step 5: Paging → BS₂ → Receiver ──
        a5  = Arrow(msc.get_bottom() + RIGHT*0.2, bs2.get_top(), buff=0.25, color=ALT_YELLOW,
                    stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        a5b = Arrow(bs2.get_center(), receiver.get_top(), buff=0.3, color=ALT_YELLOW,
                    stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        arrows_grp.add(a5, a5b)
        self.play(Create(a5), Create(a5b),
                  FadeIn(step_texts[4], shift=RIGHT*0.2),
                  run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        self.wait(6.0)

        # ── Step 6: TCH allocated in both cells ──
        tch1 = DashedLine(caller.get_top(), msc.get_left(),
                          color=DIM_GREY, stroke_width=2.5, dash_length=0.15)
        tch2 = DashedLine(msc.get_right(), receiver.get_top(),
                          color=DIM_GREY, stroke_width=2.5, dash_length=0.15)
        arrows_grp.add(tch1, tch2)
        self.play(Create(tch1), Create(tch2),
                  FadeIn(step_texts[5], shift=RIGHT*0.2),
                  run_time=1.0, rate_func=rate_functions.ease_out_cubic)
        self.wait(6.0)

        # ── Step 7: Connected ──
        subtle_box1 = SurroundingRectangle(caller,   color=DIM_GREY, corner_radius=0.15,
                                           stroke_width=2, buff=0.3)
        subtle_box2 = SurroundingRectangle(receiver, color=DIM_GREY, corner_radius=0.15,
                                           stroke_width=2, buff=0.3)
        dashed_box1 = DashedVMobject(subtle_box1, num_dashes=20, dashed_ratio=0.5).set_opacity(0.4)
        dashed_box2 = DashedVMobject(subtle_box2, num_dashes=20, dashed_ratio=0.5).set_opacity(0.4)
        self.play(Create(dashed_box1), Create(dashed_box2),
                  FadeIn(step_texts[6], shift=RIGHT*0.2),
                  run_time=1.0, rate_func=rate_functions.ease_in_out_sine)
        self.wait(4.5)

        # ── Callout ──
        note = callout_box(
            "HLR confirms subscriber → VLR gives exact location\nwithin the same MSC area",
            ACCENT_GRN
        )
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note, shift=UP*0.2), run_time=0.8)
        self.wait(8.2)

        # ── Fade Out ──
        all_obj = Group(*self.mobjects)
        self.play(FadeOut(all_obj, shift=UP*0.3), run_time=1.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.2)