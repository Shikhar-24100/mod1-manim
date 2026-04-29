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


def make_msc(center):
    """Use msc_switch.svg; fall back to a labeled rounded rect if missing."""
    try:
        icon = SVGMobject(UTILS + "msc_switch.svg").scale(0.55)
    except Exception:
        icon = RoundedRectangle(corner_radius=0.12, width=1.4, height=0.70,
                                color=ACCENT_PURP, fill_opacity=0.25)
    icon.move_to(center)
    lbl = Text("MSC", font_size=14, color=ACCENT_PURP, weight=BOLD).next_to(icon, DOWN, buff=0.08)
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


def callout_box(text, col=CREAM):
    t = Text(text, font_size=18, color=col, line_spacing=1.2)
    box = SurroundingRectangle(t, corner_radius=0.15, color=col,
                               fill_color="#181825", fill_opacity=0.85,
                               buff=0.25, stroke_width=2)
    glow = box.copy().set_stroke(color=col, width=4, opacity=0.3).scale(1.02)
    return VGroup(glow, box, t)


class Scene9Handoff(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ── Title ──────────────────────────────────────────────────────────
        title = Text("But what if you move during a call?",
                     font_size=34, weight=BOLD, color=SOFT_WHITE)
        sub   = Text("A brief note on Handoff", font_size=20, color=ACCENT_BLUE)
        hdr   = VGroup(title, sub).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.35)
        self.play(FadeIn(hdr, shift=DOWN * 0.2), run_time=1.2,
                  rate_func=rate_functions.ease_out_cubic)
        self.wait(0.4)

        # ── Cell centers — well separated, vertically centred in the frame ─
        c1_center = LEFT  * 3.4 + DOWN * 0.6
        c2_center = RIGHT * 3.4 + DOWN * 0.6

        hex1 = make_hex(c1_center, ACCENT_BLUE, scale=1.75)
        hex2 = make_hex(c2_center, ACCENT_GRN,  scale=1.75)

        lbl1 = Text("Cell 1", font_size=15, color=ACCENT_BLUE,
                    weight=BOLD).move_to(c1_center + DOWN * 1.65)
        lbl2 = Text("Cell 2", font_size=15, color=ACCENT_GRN,
                    weight=BOLD).move_to(c2_center + DOWN * 1.65)

        self.play(
            LaggedStart(DrawBorderThenFill(hex1), DrawBorderThenFill(hex2), lag_ratio=0.25),
            LaggedStart(FadeIn(lbl1), FadeIn(lbl2), lag_ratio=0.25),
            run_time=1.2, rate_func=rate_functions.ease_in_out_sine
        )

        # ── Base Stations — placed at cell centres (top half of hex) ───────
        bs1 = make_bs(c1_center + UP * 0.3, ACCENT_BLUE, "BS₁")
        bs2 = make_bs(c2_center + UP * 0.3, ACCENT_GRN,  "BS₂")
        self.play(FadeIn(bs1, scale=0.8), FadeIn(bs2, scale=0.8), run_time=0.8)

        # ── MSC — high above centre, using SVG ──────────────────────────────
        msc = make_msc(UP * 1.7)
        self.play(FadeIn(msc, scale=0.8), run_time=0.7)

        # Wire lines: MSC ↔ BS1, MSC ↔ BS2 (thin, dim, always visible)
        wire1 = Line(msc.get_bottom(), bs1.get_top(), color=DIM_GREY,
                     stroke_width=1.2, stroke_opacity=0.45)
        wire2 = Line(msc.get_bottom(), bs2.get_top(), color=DIM_GREY,
                     stroke_width=1.2, stroke_opacity=0.45)
        self.play(Create(wire1), Create(wire2), run_time=0.6)

        # ── Signal-strength bars — placed outside hex, never overlapping BS ─
        # Anchored to the outer edge of each hex
        sig1_strong = Text("▐▐▐▐", font_size=16, color=ACCENT_BLUE).next_to(hex1, RIGHT, buff=0.15)
        sig2_weak   = Text("▐░░░", font_size=16, color=DIM_GREY).next_to(hex2, LEFT,  buff=0.15)
        self.play(FadeIn(sig1_strong), FadeIn(sig2_weak), run_time=0.6)
        self.wait(0.4)

        # ── Mobile starts deep inside Cell 1 ────────────────────────────────
        mob_start = c1_center + LEFT * 0.9 + DOWN * 0.2
        mobile    = make_mobile(mob_start, ALT_YELLOW, "User")
        self.play(FadeIn(mobile, scale=0.8), run_time=0.7)
        self.wait(0.3)

        # Active call line: dashed, mobile top → BS1 bottom
        call_line = always_redraw(lambda: DashedLine(
            mobile.get_top(),
            bs1.get_bottom(),
            color=ACCENT_BLUE, stroke_width=2.5, dash_length=0.12
        ))
        call_lbl = Text("Active Call", font_size=11, color=ACCENT_BLUE,
                        weight=BOLD).next_to(mobile, LEFT, buff=0.12)
        self.play(Create(call_line), FadeIn(call_lbl), run_time=0.7)
        self.wait(0.5)

        # ── Monitor caption ─────────────────────────────────────────────────
        monitor_txt = Text("MSC continuously monitors signal strength from all BSs",
                           font_size=15, color=DIM_GREY)
        monitor_txt.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(monitor_txt, shift=UP * 0.15), run_time=0.7)
        self.wait(1.5)

        # ── Mobile moves toward boundary (centre of frame) ───────────────────
        mob_mid = LEFT * 0.6 + DOWN * 0.6        # near the cell boundary
        self.play(
            mobile.animate.move_to(mob_mid),
            FadeOut(call_lbl),                   # stale label — remove during move
            run_time=2.0, rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(0.3)

        # ── Signal flip ──────────────────────────────────────────────────────
        sig1_weak   = Text("▐░░░", font_size=16, color=DIM_GREY ).next_to(hex1, RIGHT, buff=0.15)
        sig2_strong = Text("▐▐▐▐", font_size=16, color=ACCENT_GRN).next_to(hex2, LEFT,  buff=0.15)
        self.play(
            FadeOut(sig1_strong), FadeIn(sig1_weak),
            FadeOut(sig2_weak),   FadeIn(sig2_strong),
            run_time=0.8
        )
        self.wait(0.4)

        # ── Handoff decision arrow: MSC → BS2 (ALT_YELLOW) ─────────────────
        handoff_arr = Arrow(
            msc.get_right(),
            bs2.get_top(),
            buff=0.18,
            color=ALT_YELLOW,
            stroke_width=3.5,
            max_tip_length_to_length_ratio=0.14
        )
        handoff_lbl = Text("Handoff!", font_size=13, color=ALT_YELLOW,
                           weight=BOLD).next_to(handoff_arr.get_center(), UP, buff=0.12)
        self.play(FadeOut(monitor_txt), run_time=0.3)
        self.play(Create(handoff_arr), FadeIn(handoff_lbl),
                  run_time=0.9, rate_func=rate_functions.ease_out_cubic)
        self.wait(0.4)

        # ── Call seamlessly switches to BS2 ─────────────────────────────────
        # Remove always_redraw version; draw new static green dashed line
        self.remove(call_line)
        new_call_line = DashedLine(
            mobile.get_top(),
            bs2.get_bottom(),
            color=ACCENT_GRN, stroke_width=2.5, dash_length=0.12
        )
        self.play(
            Create(new_call_line),
            run_time=1.0, rate_func=rate_functions.ease_in_out_sine
        )
        new_call_lbl = Text("Call continues ✓", font_size=11, color=ACCENT_GRN,
                            weight=BOLD).next_to(mobile, RIGHT, buff=0.12)
        self.play(FadeIn(new_call_lbl), run_time=0.6)
        self.wait(0.8)

        # ── Callout box ──────────────────────────────────────────────────────
        note = callout_box(
            "MSC tracks you even mid-call.\nSeamless switch = Handoff.",
            ACCENT_PURP
        )
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)

        # ── Disclaimer ───────────────────────────────────────────────────────
        not_covered = Text("* Handoff will not be covered in detail in this series.",
                           font_size=13, color=DIM_GREY, slant=ITALIC)
        not_covered.next_to(note, DOWN, buff=0.18)
        self.play(FadeIn(not_covered), run_time=0.6)
        self.wait(2.5)

        # ── Fade everything out ──────────────────────────────────────────────
        all_obj = Group(*self.mobjects)
        self.play(FadeOut(all_obj, shift=UP * 0.3), run_time=1.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.3)