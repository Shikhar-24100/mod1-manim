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


class Scene6Scenario3(Scene):
    def construct(self):

        # ══════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════
        title = Text("Scenario 3", font_size=30, weight=BOLD, color=YELLOW)
        title.to_edge(UP, buff=0.3)
        desc = Text(
            "Mobile returns to Cell B  —  VLR-B already has a valid record",
            font_size=16, color=YELLOW, slant=ITALIC
        ).next_to(title, DOWN, buff=0.14)
        self.play(FadeIn(title, shift=DOWN * 0.2), FadeIn(desc))
        self.wait(0.7)

        # ══════════════════════════════════════════════════════════════
        # TWO CELLS
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
        self.wait(0.2)

        # ── Cell A components ─────────────────────────────────────────
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

        bs_a = load_svg("bs_tower.svg",
                        Triangle(color=WHITE, fill_opacity=0.25).scale(0.35), scale=0.38)
        bs_a.move_to(ca_center + UP * 0.05)
        bs_a_lbl = Text("BS-A", font_size=11, color=GREY_A).next_to(bs_a, DOWN, buff=0.04)
        bs_a_grp = VGroup(bs_a, bs_a_lbl)

        # ── Cell B components ─────────────────────────────────────────
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

        bs_b = load_svg("bs_tower.svg",
                        Triangle(color=WHITE, fill_opacity=0.25).scale(0.35), scale=0.38)
        bs_b.move_to(cb_center + UP * 0.05)
        bs_b_lbl = Text("BS-B", font_size=11, color=GREY_A).next_to(bs_b, DOWN, buff=0.04)
        bs_b_grp = VGroup(bs_b, bs_b_lbl)

        self.play(
            FadeIn(hlr_a_grp, scale=0.8), FadeIn(vlr_a_grp, scale=0.8), FadeIn(bs_a_grp, scale=0.8),
            FadeIn(hlr_b_grp, scale=0.8), FadeIn(vlr_b_grp, scale=0.8), FadeIn(bs_b_grp, scale=0.8),
        )
        self.wait(0.3)

        # ── Pre-existing VLR-B record highlight ───────────────────────
        # Show that VLR-B already has an entry BEFORE mobile arrives
        existing_tag = Text("existing record", font_size=11, color=GREEN_C, slant=ITALIC)
        existing_tag.next_to(vlr_b_grp, RIGHT, buff=0.1)
        existing_box = SurroundingRectangle(
            vlr_b, color=GREEN_C, corner_radius=0.08,
            buff=0.08, stroke_width=1.5
        )
        self.play(Create(existing_box), FadeIn(existing_tag))
        self.wait(0.6)

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
        self.wait(0.4)

        # ══════════════════════════════════════════════════════════════
        # STEP 1 — Mobile moves into Cell B (again)
        # ══════════════════════════════════════════════════════════════
        st1 = Text("Step 1: Mobile returns to Cell B  (OFF → ON)", font_size=15, color=YELLOW)
        st1.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(st1))

        mob_dest = cb_center + LEFT * 0.9 + DOWN * 0.7
        self.play(mob_grp.animate.move_to(mob_dest), run_time=1.1)
        self.play(mob.animate.set_color(GREEN_C), run_time=0.4)
        self.wait(0.3)
        self.play(FadeOut(st1))

        # ══════════════════════════════════════════════════════════════
        # STEP 2 — Scans & connects to BS-B
        # ══════════════════════════════════════════════════════════════
        st2 = Text("Step 2: Scans FOCC — BS-B is strongest", font_size=15, color=BLUE_B)
        st2.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(st2))

        ripples = VGroup(*[
            Circle(radius=r, color=GREEN_B, stroke_opacity=0.45, stroke_width=1.4)
            .move_to(bs_b.get_center())
            for r in [0.35, 0.6, 0.9]
        ])
        self.play(LaggedStart(*[Create(r) for r in ripples], lag_ratio=0.25), run_time=0.9)
        self.play(FadeOut(ripples), run_time=0.3)
        self.play(FadeOut(st2))

        # ══════════════════════════════════════════════════════════════
        # STEP 3 — Sends Mobile ID via RECC
        # ══════════════════════════════════════════════════════════════
        st3 = Text("Step 3: Sends Mobile ID to BS-B via RECC", font_size=15, color=YELLOW)
        st3.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(st3))

        recc_arrow = Arrow(
            mob.get_center(), bs_b.get_center(),
            color=YELLOW, buff=0.12,
            stroke_width=2.5, tip_length=0.15
        )
        recc_lbl = Text("RECC", font_size=12, color=YELLOW, weight=BOLD)
        recc_lbl.next_to(recc_arrow.get_center(), UP, buff=0.08)
        self.play(GrowArrow(recc_arrow), FadeIn(recc_lbl))
        self.wait(0.4)
        self.play(FadeOut(st3))

        # ══════════════════════════════════════════════════════════════
        # STEP 4 — VLR-B HIT  (the key difference from Scenario 2)
        # ══════════════════════════════════════════════════════════════
        st4 = Text("Step 4: BS-B checks VLR-B  →  record FOUND!", font_size=15, color=GREEN_C)
        st4.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(st4))

        # Arrow from BS-B to VLR-B (check)
        bs_to_vlrb = Arrow(
            bs_b.get_top(), vlr_b.get_bottom(),
            color=GREEN_C, buff=0.08,
            stroke_width=2, tip_length=0.13
        )
        self.play(GrowArrow(bs_to_vlrb))

        # VLR-B big green flash — cache HIT
        self.play(
            vlr_b.animate.set_color(GREEN_C),
            existing_box.animate.set_color(GREEN_C),
            run_time=0.4
        )
        self.play(
            vlr_b.animate.set_color(RED_B),
            run_time=0.4
        )

        hit_tag = Text("✓  CACHE HIT", font_size=14, color=GREEN_C, weight=BOLD)
        hit_tag.next_to(vlr_b_grp, RIGHT, buff=0.12)
        self.play(FadeOut(existing_tag), FadeIn(hit_tag, scale=0.7))
        self.wait(0.5)
        self.play(FadeOut(st4))

        # ══════════════════════════════════════════════════════════════
        # STEP 5 — Lightweight refresh only, NO full HLR chain
        # ══════════════════════════════════════════════════════════════
        st5 = Text("Step 5: VLR-B refreshes entry — lightweight notify to HLR-A only",
                   font_size=14, color=BLUE_C)
        st5.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(st5))

        # Short dashed arrow VLR-B → HLR-A  (lightweight, not the full chain)
        light_arrow = DashedVMobject(
            CurvedArrow(
                vlr_b.get_top(),
                hlr_a.get_top(),
                angle=-TAU / 6,
                color=BLUE_C,
                stroke_width=1.8,
                tip_length=0.13
            ),
            num_dashes=18
        )
        self.play(Create(light_arrow), run_time=0.9)

        # HLR-A gentle pulse — much softer than Scenario 2
        self.play(hlr_a.animate.set_color(TEAL_C), run_time=0.35)
        self.play(hlr_a.animate.set_color(BLUE_C), run_time=0.35)

        light_tag = Text("lightweight refresh", font_size=11, color=BLUE_C, slant=ITALIC)
        light_tag.next_to(hlr_a_grp, LEFT, buff=0.1)
        self.play(FadeIn(light_tag))
        self.wait(0.5)
        self.play(FadeOut(st5))

        # ══════════════════════════════════════════════════════════════
        # CONTRAST CALLOUT — vs Scenario 2
        # ══════════════════════════════════════════════════════════════
        contrast = Text(
            "vs Scenario 2:  No full  Mobile → BS-B → VLR-B → HLR-B → HLR-A  chain needed",
            font_size=13, color=GREY_A, slant=ITALIC
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(contrast, shift=UP * 0.1))
        self.wait(0.4)

        # ══════════════════════════════════════════════════════════════
        # STEP 6 — Idle + clock
        # ══════════════════════════════════════════════════════════════
        st6 = Text("Step 6: Mobile enters IDLE — updates every 15 min", font_size=15, color=GREY_A)
        st6.to_edge(DOWN, buff=0.28)
        self.play(FadeOut(contrast), FadeIn(st6))

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
        self.play(Rotate(m_hand, angle=-TAU, about_point=clock_c.get_center()), run_time=1.1)
        self.wait(0.8)
        self.play(FadeOut(st6))

        # ══════════════════════════════════════════════════════════════
        # FINAL SUMMARY
        # ══════════════════════════════════════════════════════════════
        summary = Text(
            "VLR caching avoids expensive full HLR lookups for repeat visitors",
            font_size=15, color=GREEN_C, weight=BOLD
        ).to_edge(DOWN, buff=0.28)
        box = SurroundingRectangle(summary, color=GREEN_C,
                                   corner_radius=0.1, buff=0.12, stroke_width=1.4)
        self.play(FadeIn(summary, shift=UP * 0.15), Create(box))
        self.wait(2.5)

        # ══════════════════════════════════════════════════════════════
        # FADE OUT
        # ══════════════════════════════════════════════════════════════
        all_obj = VGroup(
            title, desc,
            hex_a, hex_b, cell_a_lbl, cell_b_lbl,
            hlr_a_grp, vlr_a_grp, bs_a_grp,
            hlr_b_grp, vlr_b_grp, bs_b_grp,
            existing_box, mob_grp,
            recc_arrow, recc_lbl,
            bs_to_vlrb, hit_tag,
            light_arrow, light_tag,
            clock, timer_lbl,
            summary, box
        )
        self.play(FadeOut(all_obj, shift=UP * 0.3), run_time=0.8)
        self.wait(0.3)