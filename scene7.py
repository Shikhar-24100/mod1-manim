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


class Scene7Case4Roaming(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        case_tag = Text("CASE 4", font_size=28, color=ACCENT_RED, weight=BOLD)
        title    = Text("Roaming Caller — Visiting Cell", font_size=38, weight=BOLD, color=SOFT_WHITE)
        sub      = Text("Caller's home is Cell A  ·  Currently visiting Cell B",
                        font_size=20, color=DIM_GREY)
        hdr = VGroup(case_tag, title, sub).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr, shift=DOWN*0.15))
        self.wait(0.3)

        ca_center = LEFT*3.5 + DOWN*0.3
        cb_center = RIGHT*3.5 + DOWN*0.3

        hex_home  = make_hex(ca_center, ACCENT_BLUE, scale=1.75)
        hex_visit = make_hex(cb_center, ACCENT_RED,  scale=1.75)

        # Matched DOWN*2.2 offset from Scene6
        home_lbl  = Text("Cell A\n(Home)",    font_size=16, color=ACCENT_BLUE,
                         weight=BOLD).move_to(ca_center + DOWN*2.2)
        visit_lbl = Text("Cell B\n(Visited)", font_size=16, color=ACCENT_RED,
                         weight=BOLD).move_to(cb_center + DOWN*2.2)

        self.play(
            LaggedStart(DrawBorderThenFill(hex_home), DrawBorderThenFill(hex_visit), lag_ratio=0.3),
            LaggedStart(FadeIn(home_lbl), FadeIn(visit_lbl), lag_ratio=0.3),
        )

        bs_a = make_bs(ca_center + UP*0.05, ACCENT_BLUE, "BS-A")
        bs_b = make_bs(cb_center + UP*0.05, ACCENT_RED,  "BS-B")
        self.play(FadeIn(bs_a, scale=0.7), FadeIn(bs_b, scale=0.7))

        msc_a = make_msc(ca_center + UP*1.8 + LEFT*0.8, "MSC-A", ACCENT_BLUE)
        hlr_a = make_db(ca_center + UP*1.8 + RIGHT*0.8, "hlr_box.svg", "HLR-A", ACCENT_BLUE, 0.26)
        vlr_b = make_db(cb_center + UP*1.8 + LEFT*0.8,  "vlr_box.svg", "VLR-B", ACCENT_RED,  0.26)
        msc_b = make_msc(cb_center + UP*1.8 + RIGHT*0.8, "MSC-B", ACCENT_RED)
        self.play(FadeIn(hlr_a, scale=0.8), FadeIn(msc_a, scale=0.8),
                  FadeIn(vlr_b, scale=0.8), FadeIn(msc_b, scale=0.8))

        caller = make_mobile(cb_center + DOWN*0.8, ACCENT_RED, "Caller\n(Visitor)")
        self.play(FadeIn(caller, scale=0.8))
        self.wait(0.4)

        # Step colors: ALT_YELLOW for all except last which is ACCENT_GRN — matches Scene6 pattern
        step_data = [
            ("① Caller sends request via visited BS-B",  ALT_YELLOW),
            ("② Visited MSC-B checks VLR-B",             ALT_YELLOW),
            ("③ VLR-B queries HLR-A (home network)",     ALT_YELLOW),
            ("④ Authentication performed by HLR-A",      ALT_YELLOW),
            ("⑤ Call proceeds — routed via MSC-B",       ALT_YELLOW),
            ("⑥ VLR plays the major role ✓",             ACCENT_GRN),
        ]
        step_texts = VGroup(*[Text(s, font_size=14, color=c, weight=BOLD) for s, c in step_data])
        # Matched .move_to(DOWN*1.2) from Scene6
        step_texts.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(DOWN*1.2)

        arrows_grp = VGroup()

        # Step 1 — ALT_YELLOW arrows, stroke_width=3.5, tip ratio=0.15 (matches Scene6)
        a1  = Arrow(caller.get_top(), bs_b.get_bottom(), buff=0.08, color=ALT_YELLOW,
                    stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        a1b = Arrow(bs_b.get_top() + LEFT*0.15, msc_b.get_bottom() + LEFT*0.15, buff=0.08, color=ALT_YELLOW,
                    stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        arrows_grp.add(a1, a1b)
        self.play(Create(a1), Create(a1b), FadeIn(step_texts[0]), run_time=0.8)
        self.wait(2.0)

        # Step 2 — solid SurroundingRectangle glow (matches Scene6's hlr_glow style)
        vlr_glow = SurroundingRectangle(vlr_b, color=ACCENT_RED, stroke_width=2.5, buff=0.2)
        a2 = Arrow(msc_b.get_left(), vlr_b.get_right(), buff=0.08, color=ALT_YELLOW,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        arrows_grp.add(a2)
        self.play(Create(a2), Create(vlr_glow), FadeIn(step_texts[1]), run_time=0.8)
        self.wait(2.0)

        # Step 3
        cross_arr = Arrow(vlr_b.get_left(), hlr_a.get_right(), buff=0.1, color=ALT_YELLOW,
                          stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        cross_lbl = Text("Query HLR-A", font_size=14, color=ALT_YELLOW,
                         weight=BOLD).move_to(cross_arr.get_center() + UP*0.35)
        c_bg  = SurroundingRectangle(cross_lbl, color=DARK_BG, fill_opacity=0.85, stroke_width=0, buff=0.03)
        lbl_grp = VGroup(c_bg, cross_lbl)
        arrows_grp.add(cross_arr)
        self.play(Create(cross_arr), FadeIn(lbl_grp), FadeIn(step_texts[2]), run_time=0.8)
        self.wait(2.0)

        # Step 4 — solid glow on HLR (matches Scene6's hlr_glow)
        try:
            shield = SVGMobject(UTILS + "shield.svg").scale(0.40)
        except Exception:
            shield = RegularPolygon(n=5, color=ACCENT_GRN, fill_opacity=0.4).scale(0.30)
        shield.move_to(hlr_a.get_center() + RIGHT*0.7)
        auth_lbl = Text("Auth ✓", font_size=14, color=ACCENT_GRN,
                        weight=BOLD).next_to(shield, DOWN, buff=0.1)
        hlr_glow = SurroundingRectangle(hlr_a, color=ACCENT_BLUE, stroke_width=2.5, buff=0.2)
        self.play(FadeIn(shield, scale=0.5), FadeIn(auth_lbl),
                  Create(hlr_glow), FadeIn(step_texts[3]), run_time=0.8)
        self.wait(2.0)

        # Step 5
        a5 = Arrow(msc_b.get_bottom() + RIGHT*0.15, bs_b.get_top() + RIGHT*0.15, buff=0.08, color=ALT_YELLOW,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        arrows_grp.add(a5)
        self.play(Create(a5), FadeIn(step_texts[4]), run_time=0.8)
        self.wait(2.0)

        # Step 6 — emphasis box on VLR (solid, matches Scene6 dashed_box style)
        f_box = SurroundingRectangle(vlr_b, color=DIM_GREY, corner_radius=0.15, stroke_width=2, buff=0.3)
        dashed_box = DashedVMobject(f_box, num_dashes=20, dashed_ratio=0.5).set_opacity(0.4)
        self.play(Create(dashed_box), FadeIn(step_texts[5]), run_time=0.8)
        self.wait(2.0)

        note = callout_box("VLR lookup + inter-network authentication", ACCENT_PURP)
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note, shift=UP*0.2))
        self.wait(2.0)

        all_obj = VGroup(hdr, hex_home, hex_visit, home_lbl, visit_lbl,
                         bs_a, bs_b, hlr_a, msc_a, vlr_b, msc_b,
                         caller, arrows_grp,
                         vlr_glow, lbl_grp, shield, auth_lbl, hlr_glow,
                         dashed_box, step_texts, note)
        self.play(FadeOut(all_obj, shift=UP*0.3), run_time=0.7)
        self.wait(0.2)