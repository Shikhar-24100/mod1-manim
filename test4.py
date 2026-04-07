from manim import *

# ── SVG ASSETS (place these files in your utils/ folder) ──────────────────
# utils/mobile.svg       — mobile phone icon
# utils/bs_tower.svg     — cell tower / base station icon
# utils/hlr_box.svg      — database/server icon (HLR)
# ──────────────────────────────────────────────────────────────────────────

UTILS = "utils/"

def make_hex(center, col, scale=1.6):
    return RegularPolygon(
        n=6, start_angle=PI / 6,
        color=col, fill_opacity=0.10, stroke_width=2
    ).scale(scale).move_to(center)

def load_svg(name, fallback, scale=0.5):
    try:
        obj = SVGMobject(UTILS + name).scale(scale)
    except Exception:
        obj = fallback
    return obj


class Scene4Scenario1(Scene):
    def construct(self):

        # ══════════════════════════════════════════════════════════════
        # INTRO TITLE
        # ══════════════════════════════════════════════════════════════
        title = Text("Mobile Modes & Scenarios", font_size=32, weight=BOLD, color=WHITE)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        intro = Text(
            "A mobile is always in one of two states:  OFF  or  ON",
            font_size=18, color=BLUE_B
        ).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(intro))
        self.wait(0.5)

        # OFF → ON arrow
        off_lbl = Text("OFF", font_size=22, color=RED_C, weight=BOLD).shift(LEFT * 2.5 + DOWN * 0.3)
        on_lbl  = Text("ON",  font_size=22, color=GREEN_C, weight=BOLD).shift(RIGHT * 2.5 + DOWN * 0.3)
        oo_arrow = Arrow(
            off_lbl.get_right(), on_lbl.get_left(),
            color=WHITE, buff=0.15, stroke_width=2.5, tip_length=0.18
        )
        self.play(FadeIn(off_lbl), FadeIn(on_lbl), GrowArrow(oo_arrow))
        self.wait(0.5)

        sub = Text(
            "When it turns ON, behaviour depends on WHERE it wakes up.",
            font_size=16, color=GREY_A, slant=ITALIC
        ).next_to(oo_arrow, DOWN, buff=0.35)
        self.play(FadeIn(sub))
        self.wait(1.0)

        self.play(FadeOut(VGroup(intro, off_lbl, on_lbl, oo_arrow, sub)))
        self.wait(0.2)

        # ══════════════════════════════════════════════════════════════
        # SCENARIO LABEL
        # ══════════════════════════════════════════════════════════════
        sc_label = Text("Scenario 1", font_size=26, color=YELLOW, weight=BOLD)
        sc_label.next_to(title, DOWN, buff=0.25)
        sc_desc = Text(
            "Mobile wakes up in its own HOME cell",
            font_size=18, color=YELLOW, slant=ITALIC
        ).next_to(sc_label, DOWN, buff=0.12)
        self.play(FadeIn(sc_label), FadeIn(sc_desc))
        self.wait(0.6)

        # ══════════════════════════════════════════════════════════════
        # CELL + COMPONENTS
        # ══════════════════════════════════════════════════════════════
        cell_center = DOWN * 0.6
        cell_color  = BLUE_C

        hex_shape = make_hex(cell_center, cell_color, scale=1.9)
        self.play(DrawBorderThenFill(hex_shape))

        # HLR box — top of cell
        hlr_icon = load_svg(
            "hlr_box.svg",
            RoundedRectangle(corner_radius=0.08, width=0.55, height=0.45,
                             color=BLUE_C, fill_opacity=0.4),
            scale=0.4
        )
        hlr_icon.set_color(BLUE_C)
        hlr_icon.move_to(cell_center + UP * 1.3 + LEFT * 1.1)
        hlr_lbl = Text("HLR", font_size=14, color=BLUE_C, weight=BOLD)
        hlr_lbl.next_to(hlr_icon, DOWN, buff=0.05)
        hlr_group = VGroup(hlr_icon, hlr_lbl)

        # BS tower — centre of cell
        bs_icon = load_svg(
            "bs_tower.svg",
            Triangle(color=WHITE, fill_opacity=0.3).scale(0.4),
            scale=0.45
        )
        bs_icon.move_to(cell_center + UP * 0.1)
        bs_lbl = Text("BS", font_size=13, color=GREY_A).next_to(bs_icon, DOWN, buff=0.05)
        bs_group = VGroup(bs_icon, bs_lbl)

        # Mobile — edge of cell (right side), starts OFF (greyed)
        mob_icon = load_svg(
            "mobile.svg",
            RoundedRectangle(corner_radius=0.1, width=0.32, height=0.52,
                             color=GREY, fill_opacity=0.4),
            scale=0.38
        )
        mob_icon.move_to(cell_center + RIGHT * 1.5 + DOWN * 0.5)
        mob_lbl = Text("Mobile", font_size=13, color=GREY_A).next_to(mob_icon, DOWN, buff=0.05)
        mob_group = VGroup(mob_icon, mob_lbl)

        self.play(FadeIn(hlr_group, scale=0.8), FadeIn(bs_group, scale=0.8))
        self.wait(0.2)
        self.play(FadeIn(mob_group, scale=0.8))
        self.wait(0.4)

        # ══════════════════════════════════════════════════════════════
        # STEP-BY-STEP ANIMATION
        # ══════════════════════════════════════════════════════════════

        step_pos = RIGHT * 3.2 + UP * 1.8
        step_spacing = 0.52

        def show_step(num, text, color=WHITE):
            lbl = Text(f"Step {num}:  {text}", font_size=14, color=color)
            lbl.move_to(step_pos + DOWN * (num - 1) * step_spacing)
            lbl.align_to(RIGHT * 2.0, LEFT)
            return lbl

        # ── Step 1: Mobile wakes up (flash green) ─────────────────────
        s1 = show_step(1, "Mobile wakes up (ON)", GREEN_C)
        self.play(FadeIn(s1, shift=LEFT * 0.2))
        self.play(mob_icon.animate.set_color(GREEN_C), run_time=0.5)
        self.wait(0.3)

        # ── Step 2: Scan broadcast signals from BS ────────────────────
        s2 = show_step(2, "Scans BS broadcast signals (FOCC)", BLUE_B)
        self.play(FadeIn(s2, shift=LEFT * 0.2))

        # Ripple waves from BS outward
        ripples = []
        for r in [0.4, 0.7, 1.0]:
            arc = Circle(radius=r, color=GREEN_B, stroke_opacity=0.5, stroke_width=1.5)
            arc.move_to(bs_icon.get_center())
            ripples.append(arc)

        self.play(
            LaggedStart(*[Create(rip) for rip in ripples], lag_ratio=0.25),
            run_time=1.0
        )
        self.wait(0.3)
        self.play(FadeOut(VGroup(*ripples)), run_time=0.4)

        # ── Step 3: Selects strongest BS & connects ───────────────────
        s3 = show_step(3, "Selects strongest BS & connects", BLUE_B)
        self.play(FadeIn(s3, shift=LEFT * 0.2))

        connect_arrow = Arrow(
            mob_icon.get_left(), bs_icon.get_right(),
            color=GREEN_C, buff=0.08,
            stroke_width=2.5, tip_length=0.16
        )
        self.play(GrowArrow(connect_arrow))
        self.wait(0.4)

        # ── Step 4: Shares identity via RECC ─────────────────────────
        s4 = show_step(4, "Shares Mobile ID via RECC", YELLOW)
        self.play(FadeIn(s4, shift=LEFT * 0.2))

        recc_tag = Text("RECC", font_size=13, color=YELLOW, weight=BOLD)
        recc_tag.next_to(connect_arrow, DOWN, buff=0.08)
        self.play(FadeIn(recc_tag))
        self.wait(0.4)

        # ── Step 5: BS updates HLR ────────────────────────────────────
        s5 = show_step(5, "BS updates HLR with user presence", BLUE_C)
        self.play(FadeIn(s5, shift=LEFT * 0.2))

        hlr_arrow = Arrow(
            bs_icon.get_top(), hlr_icon.get_bottom(),
            color=BLUE_C, buff=0.08,
            stroke_width=2, tip_length=0.14
        )
        self.play(GrowArrow(hlr_arrow))

        # HLR flash to indicate update
        self.play(
            hlr_icon.animate.set_color(YELLOW),
            run_time=0.35
        )
        self.play(
            hlr_icon.animate.set_color(BLUE_C),
            run_time=0.35
        )
        self.wait(0.3)

        # ── Step 6: Idle state + 15-min clock ────────────────────────
        s6 = show_step(6, "Goes IDLE — updates every 15 min", GREY_A)
        self.play(FadeIn(s6, shift=LEFT * 0.2))

        clock_circle = Circle(radius=0.32, color=WHITE, stroke_width=2)
        clock_circle.next_to(mob_group, UP, buff=0.18)
        minute_hand = Line(
            clock_circle.get_center(),
            clock_circle.get_center() + UP * 0.25,
            color=WHITE, stroke_width=2
        )
        hour_hand = Line(
            clock_circle.get_center(),
            clock_circle.get_center() + RIGHT * 0.18,
            color=WHITE, stroke_width=2
        )
        clock = VGroup(clock_circle, minute_hand, hour_hand)
        self.play(FadeIn(clock, scale=0.7))

        # Spin minute hand once
        self.play(
            Rotate(minute_hand, angle=-TAU, about_point=clock_circle.get_center()),
            run_time=1.2
        )

        timer_lbl = Text("15 min", font_size=12, color=GREY_A)
        timer_lbl.next_to(clock_circle, DOWN, buff=0.06)
        self.play(FadeIn(timer_lbl))
        self.wait(1.5)

        # ══════════════════════════════════════════════════════════════
        # FADE OUT
        # ══════════════════════════════════════════════════════════════
        all_obj = VGroup(
            title, sc_label, sc_desc,
            hex_shape, hlr_group, bs_group, mob_group,
            s1, s2, s3, s4, s5, s6,
            connect_arrow, recc_tag, hlr_arrow,
            clock, timer_lbl
        )
        self.play(FadeOut(all_obj, shift=UP * 0.3), run_time=0.8)
        self.wait(0.3)