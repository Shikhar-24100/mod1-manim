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


class Scene4Case1SameCell(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ── Title ──
        case_tag = Text("CASE 1", font_size=16, color=ACCENT_BLUE, weight=BOLD)
        title    = Text("Caller & Receiver — Same Cell", font_size=38, weight=BOLD, color=SOFT_WHITE)
        sub      = Text("Same Base Station  ·  Same MSC  ·  No Inter-Cell Routing",
                        font_size=20, color=DIM_GREY)
        hdr = VGroup(case_tag, title, sub).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr, shift=DOWN*0.2), run_time=1.2,
                  rate_func=rate_functions.ease_out_cubic)
        self.wait(0.3)

        # ── Topology ──
        base_center = LEFT * 1.6 + DOWN * 0.1

        hex1     = make_hex(base_center, ACCENT_BLUE, scale=2.1)
        cell_lbl = Text("Cell 1", font_size=18, color=ACCENT_BLUE,
                        weight=BOLD).move_to(base_center + DOWN*1.75)

        self.play(
            DrawBorderThenFill(hex1), FadeIn(cell_lbl, shift=UP*0.1),
            run_time=1.2, rate_func=rate_functions.ease_in_out_sine
        )

        bs       = make_bs(base_center + UP*0.1, ACCENT_BLUE)
        msc      = make_msc(base_center + RIGHT*2.8 + UP*1.4)
        hlr      = make_db(base_center + LEFT*2.4 + UP*1.4,  "hlr_box.svg", "HLR", ACCENT_BLUE)
        vlr      = make_db(base_center + LEFT*2.4 + UP*0.35, "vlr_box.svg", "VLR", ACCENT_RED)
        caller   = make_mobile(base_center + LEFT*1.5  + DOWN*0.5, ALT_YELLOW, "Caller")
        receiver = make_mobile(base_center + RIGHT*1.5 + DOWN*0.5, ACCENT_GRN, "Receiver")

        self.play(
            LaggedStart(
                FadeIn(bs, scale=0.8), FadeIn(msc, scale=0.8),
                FadeIn(hlr, scale=0.8), FadeIn(vlr, scale=0.8),
                FadeIn(caller, shift=RIGHT*0.2), FadeIn(receiver, shift=LEFT*0.2),
                lag_ratio=0.1
            ),
            run_time=1.8, rate_func=rate_functions.ease_out_cubic
        )
        self.wait(0.4)

        steps_grp = VGroup()

        # ── Arrow helper ──
        def flash_arrow(start_mob, end_mob, col, lbl, direction=UP):
            arr = Arrow(start_mob.get_center(), end_mob.get_center(),
                        buff=0.35, color=col, stroke_width=3.5,
                        max_tip_length_to_length_ratio=0.12)
            mid = arr.get_center()
            t    = Text(lbl, font_size=12, color=col, weight=BOLD).move_to(mid + direction*0.25)
            t_bg = SurroundingRectangle(t, color=DARK_BG, fill_opacity=0.85,
                                        stroke_width=0, buff=0.03)
            grp  = VGroup(arr, t_bg, t)
            steps_grp.add(grp)
            return grp

        # ── Step labels ──
        step_data = [
            ("① Caller → BS  (Request via RECC)",    ALT_YELLOW),
            ("② BS → MSC  (Forward request)",        ACCENT_GRN),
            ("③ MSC ↔ HLR/VLR  (Verify user)",      ACCENT_BLUE),
            ("④ MSC → BS → Receiver  (Paging)",      ACCENT_PURP),
            ("⑤ TCH allocated  (Traffic Channel)",   DIM_GREY),
            ("⑥ Call Connected! ✓",                  ACCENT_GRN),
        ]
        step_texts = VGroup(*[
            Text(s, font_size=15, color=c, weight=BOLD) for s, c in step_data
        ])
        step_texts.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        step_texts.to_edge(RIGHT, buff=0.35).shift(DOWN*0.3)

        # ── Step 1: Caller → BS ──
        a1 = flash_arrow(caller, bs, ALT_YELLOW, "Call Req")
        self.play(Create(a1[0]), FadeIn(VGroup(a1[1], a1[2])),
                  FadeIn(step_texts[0]),
                  run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        self.wait(1.8)

        # ── Step 2: BS → MSC ──
        a2 = flash_arrow(bs, msc, ACCENT_GRN, "Forward", direction=LEFT)
        self.play(Create(a2[0]), FadeIn(VGroup(a2[1], a2[2])),
                  FadeIn(step_texts[1]),
                  run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        self.wait(1.8)

        # ── Step 3: MSC ↔ HLR/VLR ──
        a3  = Arrow(msc.get_center(), hlr.get_center(), buff=0.4, color=ACCENT_BLUE,
                    stroke_width=3.5, max_tip_length_to_length_ratio=0.25)
        a3b = Arrow(hlr.get_center(), msc.get_center(), buff=0.4, color=ACCENT_BLUE,
                    stroke_width=3.0, max_tip_length_to_length_ratio=0.25).shift(DOWN*0.1)
        verify_lbl = Text("Verify", font_size=12, color=ACCENT_BLUE,
                          weight=BOLD).move_to(a3.get_center() + UP*0.25)
        v_bg   = SurroundingRectangle(verify_lbl, color=DARK_BG, fill_opacity=0.85,
                                      stroke_width=0, buff=0.03)
        lbl_grp= VGroup(v_bg, verify_lbl)
        steps_grp.add(VGroup(a3, a3b, lbl_grp))
        self.play(Create(a3), Create(a3b), FadeIn(lbl_grp),
                  FadeIn(step_texts[2]),
                  run_time=1.0, rate_func=rate_functions.ease_out_cubic)
        self.wait(1.8)

        # ── Step 4: MSC → BS → Receiver (paging, no direct MSC→mobile) ──
        a4 = Arrow(msc.get_center(), bs.get_center(), buff=0.35, color=ACCENT_PURP,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.12)
        a4b= Arrow(bs.get_center(), receiver.get_center(), buff=0.35, color=ACCENT_PURP,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.12)
        page_lbl = Text("Page", font_size=12, color=ACCENT_PURP,
                         weight=BOLD).move_to(a4.get_center() + UP*0.25)
        page_bg  = SurroundingRectangle(page_lbl, color=DARK_BG, fill_opacity=0.85,
                                        stroke_width=0, buff=0.03)
        page_grp = VGroup(page_bg, page_lbl)
        steps_grp.add(VGroup(a4, a4b, page_grp))
        self.play(Create(a4), Create(a4b), FadeIn(page_grp),
                  FadeIn(step_texts[3]),
                  run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        self.wait(1.8)

        # ── Step 5: TCH allocated ──
        tch     = DashedLine(caller.get_right(), receiver.get_left(),
                             color=DIM_GREY, stroke_width=2.5, dash_length=0.15)
        tch_lbl = Text("TCH", font_size=13, color=DIM_GREY,
                        weight=BOLD).move_to(tch.get_center() + UP*0.22)
        tch_bg  = SurroundingRectangle(tch_lbl, color=DARK_BG, fill_opacity=0.85,
                                       stroke_width=0, buff=0.03)
        tch_grp = VGroup(tch_bg, tch_lbl)
        steps_grp.add(VGroup(tch, tch_grp))
        self.play(Create(tch), FadeIn(tch_grp),
                  FadeIn(step_texts[4]),
                  run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        self.wait(1.8)

        # ── Step 6: Connected glow ──
        f_glow    = SurroundingRectangle(VGroup(caller, receiver, bs), color=GRAY, 
                                         corner_radius=0.25, stroke_width=0.5, buff=0.2, )
        glow_fx   = f_glow.copy().set_stroke(width=6, opacity=0.3).scale(1.02)
        self.play(Create(f_glow), FadeIn(glow_fx),
                  FadeIn(step_texts[5]),
                  run_time=1.0, rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)

        # ── Callout ──
        note = callout_box("No inter-cell routing → exceptionally low latency", ACCENT_GRN)
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note, shift=UP*0.2), run_time=0.8)
        self.wait(2.2)

        # ── Fade out ──
        all_obj = Group(*self.mobjects)
        self.play(FadeOut(all_obj, shift=UP*0.3), run_time=1.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.2)