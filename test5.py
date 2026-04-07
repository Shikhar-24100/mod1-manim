from manim import *

# ── SVG ASSETS (place these files in your utils/ folder) ──────────────────
# utils/mobile.svg       — mobile phone icon
# utils/bs_tower.svg     — cell tower / base station icon
# utils/hlr_box.svg      — database/server icon (HLR)
# utils/vlr_box.svg      — database/server icon (VLR)
# ──────────────────────────────────────────────────────────────────────────

UTILS = "utils/"

def make_hex(center, col, scale=1.8):
    return RegularPolygon(
        n=6, start_angle=PI / 6,
        color=col, fill_opacity=0.10, stroke_width=2
    ).scale(scale).move_to(center)

def load_svg(name, fallback, scale=0.4):
    try:
        obj = SVGMobject(UTILS + name).scale(scale)
    except Exception:
        obj = fallback
    return obj

def db_icon(svg_name, col, scale=0.35):
    ico = load_svg(
        svg_name,
        RoundedRectangle(corner_radius=0.08, width=0.5, height=0.4,
                         color=col, fill_opacity=0.4),
        scale=scale
    )
    ico.set_color(col)
    return ico


class Scene5Scenario2(Scene):
    def construct(self):

        # ══════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════
        title = Text("Scenario 2", font_size=30, weight=BOLD, color=YELLOW)
        title.to_edge(UP, buff=0.3)
        desc = Text(
            "Mobile wakes up in a FOREIGN cell  —  no prior record in HLR-B or VLR-B",
            font_size=16, color=YELLOW, slant=ITALIC
        ).next_to(title, DOWN, buff=0.14)
        self.play(FadeIn(title, shift=DOWN * 0.2), FadeIn(desc))
        self.wait(0.7)

        # ══════════════════════════════════════════════════════════════
        # TWO CELLS — Cell A (home, left)  &  Cell B (foreign, right)
        # ══════════════════════════════════════════════════════════════
        ca_center = LEFT * 3.4 + DOWN * 0.5
        cb_center = RIGHT * 3.4 + DOWN * 0.5

        hex_a = make_hex(ca_center, BLUE_C)
        hex_b = make_hex(cb_center, RED_C)

        cell_a_lbl = Text("Cell A\n(Home)", font_size=14, color=BLUE_C, weight=BOLD)
        cell_a_lbl.move_to(ca_center + DOWN * 1.55)
        cell_b_lbl = Text("Cell B\n(Foreign)", font_size=14, color=RED_C, weight=BOLD)
        cell_b_lbl.move_to(cb_center + DOWN * 1.55)

        self.play(
            DrawBorderThenFill(hex_a), DrawBorderThenFill(hex_b),
            FadeIn(cell_a_lbl), FadeIn(cell_b_lbl)
        )
        self.wait(0.3)

        # ── HLR-A + VLR-A (Cell A, top) ──────────────────────────────
        hlr_a = db_icon("hlr_box.svg", BLUE_C)
        hlr_a.move_to(ca_center + UP * 1.25 + LEFT * 0.55)
        hlr_a_lbl = Text("HLR-A", font_size=12, color=BLUE_C, weight=BOLD)
        hlr_a_lbl.next_to(hlr_a, DOWN, buff=0.04)
        hlr_a_grp = VGroup(hlr_a, hlr_a_lbl)

        vlr_a = db_icon("vlr_box.svg", BLUE_B)
        vlr_a.move_to(ca_center + UP * 1.25 + RIGHT * 0.45)
        vlr_a_lbl = Text("VLR-A", font_size=12, color=BLUE_B, weight=BOLD)
        vlr_a_lbl.next_to(vlr_a, DOWN, buff=0.04)
        vlr_a_grp = VGroup(vlr_a, vlr_a_lbl)

        # ── BS-A (Cell A centre) ──────────────────────────────────────
        bs_a = load_svg("bs_tower.svg",
                        Triangle(color=WHITE, fill_opacity=0.25).scale(0.35), scale=0.38)
        bs_a.move_to(ca_center + UP * 0.05)
        bs_a_lbl = Text("BS-A", font_size=11, color=GREY_A).next_to(bs_a, DOWN, buff=0.04)
        bs_a_grp = VGroup(bs_a, bs_a_lbl)

        # ── HLR-B + VLR-B (Cell B, top) ──────────────────────────────
        hlr_b = db_icon("hlr_box.svg", RED_C)
        hlr_b.move_to(cb_center + UP * 1.25 + LEFT * 0.55)
        hlr_b_lbl = Text("HLR-B", font_size=12, color=RED_C, weight=BOLD)
        hlr_b_lbl.next_to(hlr_b, DOWN, buff=0.04)
        hlr_b_grp = VGroup(hlr_b, hlr_b_lbl)

        vlr_b = db_icon("vlr_box.svg", RED_B)
        vlr_b.move_to(cb_center + UP * 1.25 + RIGHT * 0.45)
        vlr_b_lbl = Text("VLR-B", font_size=12, color=RED_B, weight=BOLD)
        vlr_b_lbl.next_to(vlr_b, DOWN, buff=0.04)
        vlr_b_grp = VGroup(vlr_b, vlr_b_lbl)

        # ── BS-B (Cell B centre) ──────────────────────────────────────
        bs_b = load_svg("bs_tower.svg",
                        Triangle(color=WHITE, fill_opacity=0.25).scale(0.35), scale=0.38)
        bs_b.move_to(cb_center + UP * 0.05)
        bs_b_lbl = Text("BS-B", font_size=11, color=GREY_A).next_to(bs_b, DOWN, buff=0.04)
        bs_b_grp = VGroup(bs_b, bs_b_lbl)

        self.play(
            FadeIn(hlr_a_grp, scale=0.8), FadeIn(vlr_a_grp, scale=0.8),
            FadeIn(bs_a_grp,  scale=0.8),
            FadeIn(hlr_b_grp, scale=0.8), FadeIn(vlr_b_grp, scale=0.8),
            FadeIn(bs_b_grp,  scale=0.8),
        )
        self.wait(0.4)

        # ── Mobile starts in Cell A ───────────────────────────────────
        mob = load_svg(
            "mobile.svg",
            RoundedRectangle(corner_radius=0.1, width=0.28, height=0.46,
                             color=GREY, fill_opacity=0.4),
            scale=0.36
        )
        mob.move_to(ca_center + RIGHT * 0.9 + DOWN * 0.7)
        mob_lbl = Text("Mobile\n(Home: A)", font_size=11, color=GREY_A)
        mob_lbl.next_to(mob, DOWN, buff=0.04)
        mob_grp = VGroup(mob, mob_lbl)

        self.play(FadeIn(mob_grp, scale=0.8))
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════
        # STEP TRACKER  (bottom strip)
        # ══════════════════════════════════════════════════════════════
        step_tracker = always_redraw(lambda: VGroup())  # placeholder

        def flash_step(text, col=WHITE):
            lbl = Text(text, font_size=15, color=col)
            lbl.to_edge(DOWN, buff=0.28)
            return lbl

        # ══════════════════════════════════════════════════════════════
        # STEP 1 — Mobile crosses into Cell B
        # ══════════════════════════════════════════════════════════════
        st1 = flash_step("Step 1: Mobile moves into Cell B  (OFF → ON)", YELLOW)
        self.play(FadeIn(st1))

        # Animate mobile sliding from Cell A to Cell B
        mob_dest = cb_center + LEFT * 0.9 + DOWN * 0.7
        self.play(
            mob_grp.animate.move_to(mob_dest),
            run_time=1.2
        )
        # Flash green on arrival
        self.play(mob.animate.set_color(GREEN_C), run_time=0.4)
        self.wait(0.3)
        self.play(FadeOut(st1))

        # ══════════════════════════════════════════════════════════════
        # STEP 2 — Scans & connects to BS-B (strongest)
        # ══════════════════════════════════════════════════════════════
        st2 = flash_step("Step 2: Scans FOCC signals — BS-B is strongest", BLUE_B)
        self.play(FadeIn(st2))

        ripples = VGroup(*[
            Circle(radius=r, color=GREEN_B, stroke_opacity=0.45, stroke_width=1.4)
            .move_to(bs_b.get_center())
            for r in [0.35, 0.6, 0.9]
        ])
        self.play(LaggedStart(*[Create(r) for r in ripples], lag_ratio=0.25), run_time=0.9)
        self.play(FadeOut(ripples), run_time=0.3)
        self.wait(0.2)
        self.play(FadeOut(st2))

        # ══════════════════════════════════════════════════════════════
        # STEP 3 — Sends Mobile ID via RECC to BS-B
        # ══════════════════════════════════════════════════════════════
        st3 = flash_step("Step 3: Sends Mobile ID to BS-B via RECC", YELLOW)
        self.play(FadeIn(st3))

        recc_arrow = Arrow(
            mob.get_center(), bs_b.get_center(),
            color=YELLOW, buff=0.12,
            stroke_width=2.5, tip_length=0.15
        )
        recc_lbl = Text("RECC", font_size=12, color=YELLOW, weight=BOLD)
        recc_lbl.next_to(recc_arrow.get_center(), UP, buff=0.08)
        self.play(GrowArrow(recc_arrow), FadeIn(recc_lbl))
        self.wait(0.5)
        self.play(FadeOut(st3))

        # ══════════════════════════════════════════════════════════════
        # STEP 4 — BS-B marks mobile as VISITOR in VLR-B
        # ══════════════════════════════════════════════════════════════
        st4 = flash_step("Step 4: BS-B does not recognise Mobile → marks as VISITOR in VLR-B", RED_B)
        self.play(FadeIn(st4))

        bs_to_vlrb = Arrow(
            bs_b.get_top(), vlr_b.get_bottom(),
            color=RED_B, buff=0.08,
            stroke_width=2, tip_length=0.13
        )
        self.play(GrowArrow(bs_to_vlrb))

        # VLR-B flashes + "VISITOR" tag
        self.play(vlr_b.animate.set_color(YELLOW), run_time=0.35)
        self.play(vlr_b.animate.set_color(RED_B),  run_time=0.35)

        visitor_tag = Text("VISITOR", font_size=12, color=YELLOW, weight=BOLD)
        visitor_tag.next_to(vlr_b_grp, RIGHT, buff=0.12)
        self.play(FadeIn(visitor_tag, scale=0.7))
        self.wait(0.4)
        self.play(FadeOut(st4))

        # ══════════════════════════════════════════════════════════════
        # STEP 5 — Notify HLR-A (home cell)
        # ══════════════════════════════════════════════════════════════
        st5 = flash_step("Step 5: HLR-B notifies HLR-A — subscriber is now in Cell B", BLUE_C)
        self.play(FadeIn(st5))

        # VLR-B → HLR-B
        vlrb_to_hlrb = Arrow(
            vlr_b.get_left(), hlr_b.get_right(),
            color=RED_C, buff=0.06,
            stroke_width=1.8, tip_length=0.12
        )
        self.play(GrowArrow(vlrb_to_hlrb))
        self.wait(0.2)

        # HLR-B → HLR-A  (long cross-cell arrow, goes above the hexes)
        hlrb_to_hlra = CurvedArrow(
            hlr_b.get_top(),
            hlr_a.get_top(),
            angle=-TAU / 5,
            color=BLUE_C,
            stroke_width=2,
            tip_length=0.14
        )
        self.play(Create(hlrb_to_hlra), run_time=0.9)

        # HLR-A flashes — it now knows the subscriber is in Cell B
        self.play(hlr_a.animate.set_color(YELLOW), run_time=0.35)
        self.play(hlr_a.animate.set_color(BLUE_C),  run_time=0.35)

        update_tag = Text("Updated!", font_size=12, color=YELLOW)
        update_tag.next_to(hlr_a_grp, LEFT, buff=0.12)
        self.play(FadeIn(update_tag, scale=0.7))
        self.wait(0.5)
        self.play(FadeOut(st5))

        # ══════════════════════════════════════════════════════════════
        # STEP 6 — Idle + 15-min cycle
        # ══════════════════════════════════════════════════════════════
        st6 = flash_step("Step 6: Mobile enters IDLE state — updates every 15 min", GREY_A)
        self.play(FadeIn(st6))

        clock_c = Circle(radius=0.28, color=WHITE, stroke_width=2)
        clock_c.next_to(mob, UP, buff=0.15)
        m_hand = Line(clock_c.get_center(),
                      clock_c.get_center() + UP * 0.2,
                      color=WHITE, stroke_width=2)
        h_hand = Line(clock_c.get_center(),
                      clock_c.get_center() + RIGHT * 0.15,
                      color=WHITE, stroke_width=2)
        clock = VGroup(clock_c, m_hand, h_hand)
        timer_lbl = Text("15 min", font_size=11, color=GREY_A).next_to(clock_c, RIGHT, buff=0.08)

        self.play(FadeIn(clock, scale=0.7), FadeIn(timer_lbl))
        self.play(
            Rotate(m_hand, angle=-TAU, about_point=clock_c.get_center()),
            run_time=1.1
        )
        self.wait(1.2)
        self.play(FadeOut(st6))

        # ══════════════════════════════════════════════════════════════
        # SUMMARY CALLOUT
        # ══════════════════════════════════════════════════════════════
        summary = Text(
            "Full update chain:  Mobile → BS-B → VLR-B → HLR-B → HLR-A",
            font_size=15, color=YELLOW
        ).to_edge(DOWN, buff=0.28)
        box = SurroundingRectangle(summary, color=YELLOW,
                                   corner_radius=0.1, buff=0.12, stroke_width=1.4)
        self.play(FadeIn(summary, shift=UP * 0.15), Create(box))
        self.wait(2.2)

        # ══════════════════════════════════════════════════════════════
        # FADE OUT
        # ══════════════════════════════════════════════════════════════
        all_obj = VGroup(
            title, desc,
            hex_a, hex_b, cell_a_lbl, cell_b_lbl,
            hlr_a_grp, vlr_a_grp, bs_a_grp,
            hlr_b_grp, vlr_b_grp, bs_b_grp,
            mob_grp,
            recc_arrow, recc_lbl,
            bs_to_vlrb, visitor_tag,
            vlrb_to_hlrb, hlrb_to_hlra, update_tag,
            clock, timer_lbl,
            summary, box
        )
        self.play(FadeOut(all_obj, shift=UP * 0.3), run_time=0.8)
        self.wait(0.3)