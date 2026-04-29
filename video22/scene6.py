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
    lbl = Text(label, font_size=11, color=col, weight=BOLD).next_to(icon, DOWN, buff=0.08)
    return VGroup(icon, lbl)


def make_mobile(center, col=ALT_YELLOW, label=""):
    try:
        ico = SVGMobject(UTILS + "mobile.svg").scale(0.30)
    except Exception:
        ico = RoundedRectangle(corner_radius=0.08, width=0.26, height=0.42,
                               color=ALT_YELLOW, fill_opacity=0.5)
    ico.move_to(center)
    if label:
        lbl = Text(label, font_size=11, color=SOFT_WHITE, weight=BOLD).next_to(ico, DOWN, buff=0.06)
        return VGroup(ico, lbl)
    return VGroup(ico)


def make_db(center, svg_name, label, col, scale=0.28):
    try:
        ico = SVGMobject(UTILS + svg_name).scale(scale)
    except Exception:
        ico = RoundedRectangle(corner_radius=0.08, width=0.40, height=0.34,
                               color=col, fill_opacity=0.4)
    ico.move_to(center)
    lbl = Text(label, font_size=11, color=col, weight=BOLD).next_to(ico, DOWN, buff=0.06)
    return VGroup(ico, lbl)


def make_msc(center, label="MSC", col=ACCENT_PURP):
    try:
        ico = SVGMobject(UTILS + "msc_switch.svg").scale(0.38)
    except Exception:
        ico = RoundedRectangle(corner_radius=0.12, width=0.70, height=0.55,
                               color=col, fill_opacity=0.35)
    ico.move_to(center)
    lbl = Text(label, font_size=12, color=col, weight=BOLD).next_to(ico, DOWN, buff=0.06)
    return VGroup(ico, lbl)


def callout_box(text, col=CREAM):
    t = Text(text, font_size=16, color=col, line_spacing=1.2)
    box = SurroundingRectangle(t, corner_radius=0.12, color=col,
                               fill_color="#151522", fill_opacity=0.8,
                               buff=0.18, stroke_width=1.2)
    return VGroup(box, t)


class Scene6Case3InterMSC(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        case_tag = Text("CASE 3", font_size=28, color=ACCENT_PURP, weight=BOLD)
        title    = Text("Inter-MSC Call", font_size=38, weight=BOLD, color=SOFT_WHITE)
        sub      = Text("Caller in Cell 1 (MSC-A)  ·  Receiver in Cell 3 (MSC-B)",
                        font_size=20, color=DIM_GREY)
        hdr = VGroup(case_tag, title, sub).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr, shift=DOWN*0.15))
        self.wait(0.3)

        ca_center = LEFT*3.5 + DOWN*0.3
        cb_center = RIGHT*3.5 + DOWN*0.3

        hex_a = make_hex(ca_center, ACCENT_BLUE, scale=1.9)
        hex_b = make_hex(cb_center, ACCENT_BLUE, scale=1.9)
        lbl_a = Text("Cell 1", font_size=16, color=ACCENT_BLUE, weight=BOLD).move_to(ca_center + DOWN*2.2)
        lbl_b = Text("Cell 3", font_size=16, color=ACCENT_BLUE, weight=BOLD).move_to(cb_center + DOWN*2.2)

        self.play(
            LaggedStart(DrawBorderThenFill(hex_a), DrawBorderThenFill(hex_b), lag_ratio=0.3),
            LaggedStart(FadeIn(lbl_a), FadeIn(lbl_b), lag_ratio=0.3),
        )

        bs_a = make_bs(ca_center + UP*0.05, ACCENT_BLUE, "BS-A")
        bs_b = make_bs(cb_center + UP*0.05, ACCENT_BLUE, "BS-B")
        self.play(FadeIn(bs_a, scale=0.7), FadeIn(bs_b, scale=0.7))

        msca = make_msc(ca_center + UP*2.2 + RIGHT*0.4, "MSC-A", ACCENT_BLUE)
        mscb = make_msc(cb_center + UP*2.2 + LEFT*0.4,  "MSC-B", ACCENT_BLUE)
        self.play(FadeIn(msca, scale=0.8), FadeIn(mscb, scale=0.8))

        hlr_a = make_db(ca_center + UP*2.2 + LEFT*1.4, "hlr_box.svg", "HLR-A", ACCENT_BLUE, 0.26)
        vlr_b = make_db(cb_center + UP*2.2 + RIGHT*1.4, "vlr_box.svg", "VLR-B", ACCENT_BLUE, 0.26)
        self.play(FadeIn(hlr_a, scale=0.8), FadeIn(vlr_b, scale=0.8))

        caller   = make_mobile(ca_center + LEFT*1.3 + DOWN*0.7, ALT_YELLOW, "Caller")
        receiver = make_mobile(cb_center + RIGHT*1.3 + DOWN*0.7, ACCENT_GRN,  "Receiver")
        self.play(FadeIn(caller, scale=0.8), FadeIn(receiver, scale=0.8))
        self.wait(0.4)

        step_data = [
            ("① Caller → BS-A → MSC-A", ALT_YELLOW),
            ("② MSC-A queries HLR-A for receiver's location", ALT_YELLOW),
            ("③ HLR-A returns MSC-B address", ALT_YELLOW),
            ("④ Call routed: MSC-A → MSC-B", ALT_YELLOW),
            ("⑤ MSC-B pages receiver via BS-B", ALT_YELLOW),
            ("⑥ Channel allocated → Call connected ✓", ACCENT_GRN),
        ]
        step_texts = VGroup(*[Text(s, font_size=14, color=c, weight=BOLD) for s, c in step_data])
        step_texts.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(DOWN*1.2)

        arrows_grp = VGroup()

        a1 = Arrow(caller.get_top(), bs_a.get_bottom(), buff=0.08, color=ALT_YELLOW,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        a1b= Arrow(bs_a.get_top(), msca.get_bottom(), buff=0.08, color=ALT_YELLOW,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        arrows_grp.add(a1, a1b)
        self.play(Create(a1), Create(a1b), FadeIn(step_texts[0]), run_time=0.8)
        self.wait(2.0)

        a2 = Arrow(msca.get_left(), hlr_a.get_right(), buff=0.08, color=ALT_YELLOW,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        hlr_glow = SurroundingRectangle(hlr_a, color=ACCENT_BLUE, stroke_width=2.5, buff=0.2)
        arrows_grp.add(a2)
        self.play(Create(a2), Create(hlr_glow), FadeIn(step_texts[1]), run_time=0.8)
        self.wait(2.0)

        a3 = Arrow(hlr_a.get_right(), msca.get_left(), buff=0.08, color=ALT_YELLOW,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        arrows_grp.add(a3)
        self.play(Create(a3), FadeIn(step_texts[2]), run_time=0.8)
        self.wait(2.0)

        inter_arr = Arrow(msca.get_right(), mscb.get_left(), buff=0.1, color=ALT_YELLOW,
                          stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        inter_lbl = Text("Inter-MSC Routing", font_size=14, color=ALT_YELLOW,
                         weight=BOLD).move_to(inter_arr.get_center() + UP*0.35)
        arrows_grp.add(inter_arr)
        self.play(Create(inter_arr), FadeIn(inter_lbl), FadeIn(step_texts[3]), run_time=0.8)
        self.wait(2.0)

        a5 = Arrow(mscb.get_bottom(), bs_b.get_top(), buff=0.08, color=ALT_YELLOW,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        a5b= Arrow(bs_b.get_bottom(), receiver.get_top(), buff=0.08, color=ALT_YELLOW,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        arrows_grp.add(a5, a5b)
        self.play(Create(a5), Create(a5b), FadeIn(step_texts[4]), run_time=0.8)
        self.wait(2.0)

        f_box1 = SurroundingRectangle(caller, color=DIM_GREY, corner_radius=0.15, stroke_width=2, buff=0.3)
        f_box2 = SurroundingRectangle(receiver, color=DIM_GREY, corner_radius=0.15, stroke_width=2, buff=0.3)
        dashed_box1 = DashedVMobject(f_box1, num_dashes=20, dashed_ratio=0.5).set_opacity(0.4)
        dashed_box2 = DashedVMobject(f_box2, num_dashes=20, dashed_ratio=0.5).set_opacity(0.4)
        glow = VGroup(dashed_box1, dashed_box2)

        self.play(Create(glow), FadeIn(step_texts[5]), run_time=0.8)
        self.wait(2.0)

        note = callout_box("HLR lookup + inter-MSC signaling", ACCENT_PURP)
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note, shift=UP*0.2))
        self.wait(2.0)

        all_obj = VGroup(hdr, hex_a, hex_b, lbl_a, lbl_b, bs_a, bs_b,
                         msca, mscb, hlr_a, vlr_b, caller, receiver,
                         arrows_grp, hlr_glow, inter_lbl, glow,
                         step_texts, note)
        self.play(FadeOut(all_obj, shift=UP*0.3), run_time=0.7)
        self.wait(0.2)
