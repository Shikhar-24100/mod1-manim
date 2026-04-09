from manim import *

# ── SVG ASSETS (place these files in your utils/ folder) ──────────────────
# utils/mobile.svg       — mobile phone icon
# utils/bs_tower.svg     — cell tower / base station icon
# utils/hlr_box.svg      — database/server icon (HLR)
# utils/vlr_box.svg      — database/server icon (VLR)
# ──────────────────────────────────────────────────────────────────────────

UTILS = "utils/"

# ── Palette (3B1B-inspired) ────────────────────────────────────────────────
CREAM       = "#FFFBE6"
DARK_BG     = "#1C1C2E"
ACCENT_BLUE = "#58C4DD"
ACCENT_RED  = "#FF6B6B"
ACCENT_GRN  = "#6BCB77"
DIM_GREY    = "#888899"
SOFT_WHITE  = "#E8E8F0"
ALT_YELLOW  = "#F2D388"

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
    # Intentionally removed ico.set_color(col) to preserve SVG colors natively
    return ico


class Scene6Scenario3(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ══════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════
        title = Text("Scenario 3", font_size=32, weight=BOLD, color=ALT_YELLOW)
        title.to_edge(UP, buff=0.35)
        desc = Text(
            "Mobile returns to Cell B  —  VLR-B already has a valid record",
            font_size=18, color=CREAM, slant=ITALIC
        ).next_to(title, DOWN, buff=0.18)
        self.play(FadeIn(title, shift=DOWN * 0.2), FadeIn(desc))
        self.wait(0.7)

        # ══════════════════════════════════════════════════════════════
        # TWO CELLS
        # ══════════════════════════════════════════════════════════════
        # Shift slightly up to make room for the step tracker below
        ca_center = LEFT * 3.4 + DOWN * 0.3
        cb_center = RIGHT * 3.4 + DOWN * 0.3

        hex_a = make_hex(ca_center, ACCENT_BLUE)
        hex_b = make_hex(cb_center, ACCENT_RED)

        cell_a_lbl = Text("Cell A\n(Home)", font_size=14, color=ACCENT_BLUE, weight=BOLD)
        cell_a_lbl.move_to(ca_center + DOWN * 2.1)
        cell_b_lbl = Text("Cell B\n(Foreign)", font_size=14, color=ACCENT_RED, weight=BOLD)
        cell_b_lbl.move_to(cb_center + DOWN * 2.1)

        self.play(
            DrawBorderThenFill(hex_a), DrawBorderThenFill(hex_b),
            FadeIn(cell_a_lbl), FadeIn(cell_b_lbl)
        )
        self.wait(0.2)

        # ── Cell A components ─────────────────────────────────────────
        hlr_a = db_icon("hlr_box.svg", ACCENT_BLUE)
        hlr_a.move_to(ca_center + UP * 1.25 + LEFT * 0.55)
        hlr_a_lbl = Text("HLR-A", font_size=13, color=ACCENT_BLUE, weight=BOLD)
        hlr_a_lbl.next_to(hlr_a, UP, buff=0.06)
        hlr_a_grp = VGroup(hlr_a, hlr_a_lbl)

        vlr_a = db_icon("vlr_box.svg", ACCENT_BLUE)
        vlr_a.move_to(ca_center + UP * 1.25 + RIGHT * 0.45)
        vlr_a_lbl = Text("VLR-A", font_size=13, color=ACCENT_BLUE, weight=BOLD)
        vlr_a_lbl.next_to(vlr_a, UP, buff=0.06)
        vlr_a_grp = VGroup(vlr_a, vlr_a_lbl)

        bs_a = load_svg("bs_tower.svg",
                        Triangle(color=ACCENT_GRN, fill_opacity=0.25).scale(0.35), scale=0.38)
        bs_a.move_to(ca_center + UP * 0.05)
        bs_a_lbl = Text("BS-A", font_size=12, color=SOFT_WHITE, weight=BOLD).next_to(bs_a, DOWN, buff=0.08)
        bs_a_grp = VGroup(bs_a, bs_a_lbl)

        # ── Cell B components ─────────────────────────────────────────
        hlr_b = db_icon("hlr_box.svg", ACCENT_RED)
        hlr_b.move_to(cb_center + UP * 1.25 + LEFT * 0.55)
        hlr_b_lbl = Text("HLR-B", font_size=13, color=ACCENT_RED, weight=BOLD)
        hlr_b_lbl.next_to(hlr_b, UP, buff=0.06)
        hlr_b_grp = VGroup(hlr_b, hlr_b_lbl)

        vlr_b = db_icon("vlr_box.svg", ACCENT_RED)
        vlr_b.move_to(cb_center + UP * 1.25 + RIGHT * 0.45)
        vlr_b_lbl = Text("VLR-B", font_size=13, color=ACCENT_RED, weight=BOLD)
        vlr_b_lbl.next_to(vlr_b, UP, buff=0.06)
        vlr_b_grp = VGroup(vlr_b, vlr_b_lbl)

        bs_b = load_svg("bs_tower.svg",
                        Triangle(color=ACCENT_GRN, fill_opacity=0.25).scale(0.35), scale=0.38)
        bs_b.move_to(cb_center + UP * 0.05)
        bs_b_lbl = Text("BS-B", font_size=12, color=SOFT_WHITE, weight=BOLD).next_to(bs_b, DOWN, buff=0.08)
        bs_b_grp = VGroup(bs_b, bs_b_lbl)

        self.play(
            FadeIn(hlr_a_grp, scale=0.8), FadeIn(vlr_a_grp, scale=0.8), FadeIn(bs_a_grp, scale=0.8),
            FadeIn(hlr_b_grp, scale=0.8), FadeIn(vlr_b_grp, scale=0.8), FadeIn(bs_b_grp, scale=0.8),
        )
        self.wait(0.3)

        # ── Pre-existing VLR-B record highlight ───────────────────────
        existing_tag = Text("existing record", font_size=12, color=ACCENT_GRN, slant=ITALIC)
        existing_tag.next_to(vlr_b_grp, RIGHT, buff=0.12)
        existing_box = SurroundingRectangle(
            vlr_b, color=ACCENT_GRN, corner_radius=0.1,
            buff=0.1, stroke_width=2
        )
        self.play(Create(existing_box), FadeIn(existing_tag))
        self.wait(0.6)

        # ── Mobile starts in Cell A ───────────────────────────────────
        mob = load_svg(
            "mobile.svg",
            RoundedRectangle(corner_radius=0.1, width=0.28, height=0.46,
                             color=DIM_GREY, fill_opacity=0.4),
            scale=0.36
        )
        mob.move_to(ca_center + RIGHT * 0.9 + DOWN * 0.7)
        mob_lbl = Text("Mobile\n(Home: A)", font_size=12, color=DIM_GREY)
        mob_lbl.next_to(mob, DOWN, buff=0.06)
        mob_grp = VGroup(mob, mob_lbl)
        self.play(FadeIn(mob_grp, scale=0.8))
        self.wait(0.4)

        # ══════════════════════════════════════════════════════════════
        # STEP 1 — Mobile moves into Cell B (again)
        # ══════════════════════════════════════════════════════════════
        st1 = Text("Step 1: Mobile returns to Cell B  (OFF → ON)", font_size=16, color=ALT_YELLOW)
        st1.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(st1))

        mob_dest = cb_center + LEFT * 0.9 + DOWN * 0.7
        self.play(mob_grp.animate.move_to(mob_dest), run_time=1.1)
        
        # Color label instead of SVG painting internally
        self.play(
            mob_lbl.animate.set_color(ACCENT_GRN),
            mob.animate.scale(1.15),
            run_time=0.4
        )
        self.play(mob.animate.scale(1/1.15), run_time=0.2)
        self.wait(0.3)
        self.play(FadeOut(st1))

        # ══════════════════════════════════════════════════════════════
        # STEP 2 — Scans & connects to BS-B
        # ══════════════════════════════════════════════════════════════
        st2 = Text("Step 2: Scans FOCC — BS-B is strongest", font_size=16, color=ACCENT_BLUE)
        st2.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(st2))

        ripples = VGroup(*[
            Circle(radius=r, color=ACCENT_GRN, stroke_opacity=0.5, stroke_width=2)
            .move_to(bs_b.get_center())
            for r in [0.4, 0.7, 1.0]
        ])
        self.play(LaggedStart(*[Create(r) for r in ripples], lag_ratio=0.25), run_time=1.0)
        self.play(FadeOut(ripples), run_time=0.3)
        self.play(FadeOut(st2))

        # ══════════════════════════════════════════════════════════════
        # STEP 3 — Sends Mobile ID via RECC
        # ══════════════════════════════════════════════════════════════
        st3 = Text("Step 3: Sends Mobile ID to BS-B via RECC", font_size=16, color=ALT_YELLOW)
        st3.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(st3))

        recc_arrow = Arrow(
            mob.get_center(), bs_b.get_center(),
            color=ALT_YELLOW, buff=0.15,
            stroke_width=3, tip_length=0.18
        )
        recc_lbl = Text("RECC", font_size=13, color=ALT_YELLOW, weight=BOLD)
        recc_lbl.next_to(recc_arrow.get_center(), UP*0.4+LEFT*0.12, buff=0.1)
        self.play(GrowArrow(recc_arrow), FadeIn(recc_lbl))
        self.wait(0.4)
        self.play(FadeOut(st3))

        # ══════════════════════════════════════════════════════════════
        # STEP 4 — VLR-B HIT
        # ══════════════════════════════════════════════════════════════
        st4 = Text("Step 4: BS-B checks VLR-B  →  record FOUND!", font_size=16, color=ACCENT_GRN)
        st4.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(st4))

        # Arrow from BS-B to VLR-B
        bs_to_vlrb = Arrow(
            bs_b.get_top(), vlr_b.get_bottom(),
            color=ACCENT_GRN, buff=0.1,
            stroke_width=2.5, tip_length=0.15
        )
        self.play(GrowArrow(bs_to_vlrb))

        # Flash label instead of breaking SVG colors internally
        self.play(
            vlr_b_lbl.animate.set_color(ACCENT_GRN),
            existing_box.animate.scale(1.1).set_color(SOFT_WHITE),
            run_time=0.4
        )
        self.play(
            vlr_b_lbl.animate.set_color(ACCENT_RED),
            existing_box.animate.scale(1/1.1).set_color(ACCENT_GRN),
            run_time=0.4
        )

        hit_tag = Text("✓  CACHE HIT", font_size=15, color=ACCENT_GRN, weight=BOLD)
        hit_tag.next_to(vlr_b_grp, RIGHT, buff=0.12)
        self.play(FadeOut(existing_tag), FadeIn(hit_tag, scale=0.7))
        self.wait(0.5)
        self.play(FadeOut(st4))

        # ══════════════════════════════════════════════════════════════
        # STEP 5 — Lightweight refresh only, NO full HLR chain
        # ══════════════════════════════════════════════════════════════
        st5 = Text("Step 5: VLR-B refreshes entry — lightweight notify to HLR-A only",
                   font_size=16, color=ACCENT_BLUE)
        st5.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(st5))

        # Short dashed arrow VLR-B → HLR-A
        light_arrow = DashedVMobject(
            CurvedArrow(
                vlr_b.get_top(),
                hlr_a.get_top(),
                angle=-TAU / 6,
                color=ACCENT_BLUE,
                stroke_width=2.5,
                tip_length=0.15
            ),
            num_dashes=18
        )
        self.play(Create(light_arrow), run_time=0.9)

        # HLR-A gentle pulse
        self.play(
            hlr_a_lbl.animate.set_color(SOFT_WHITE),
            hlr_a.animate.scale(1.1),
            run_time=0.35
        )
        self.play(
            hlr_a_lbl.animate.set_color(ACCENT_BLUE),
            hlr_a.animate.scale(1/1.1),
            run_time=0.35
        )

        light_tag = Text("lightweight refresh", font_size=12, color=ACCENT_BLUE, slant=ITALIC)
        light_tag.next_to(hlr_a_grp, LEFT, buff=0.1)
        self.play(FadeIn(light_tag))
        self.wait(0.5)
        self.play(FadeOut(st5))

        # ══════════════════════════════════════════════════════════════
        # CONTRAST CALLOUT — vs Scenario 2
        # ══════════════════════════════════════════════════════════════
        contrast = Text(
            "vs Scenario 2:  No full  Mobile → BS-B → VLR-B → HLR-B → HLR-A  chain needed",
            font_size=14, color=CREAM, slant=ITALIC
        ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(contrast, shift=UP * 0.1))
        self.wait(0.4)

        # ══════════════════════════════════════════════════════════════
        # STEP 6 — Idle + clock
        # ══════════════════════════════════════════════════════════════
        st6 = Text("Step 6: Mobile enters IDLE — updates every 15 min", font_size=16, color=DIM_GREY)
        st6.to_edge(DOWN, buff=0.35)
        self.play(FadeOut(contrast), FadeIn(st6))

        clock_c = Circle(radius=0.28, color=SOFT_WHITE, stroke_width=2.5)
        clock_c.next_to(mob, UP*0.15, buff=0.18)
        m_hand = Line(clock_c.get_center(),
                      clock_c.get_center() + UP * 0.2,
                      color=SOFT_WHITE, stroke_width=2.5)
        h_hand = Line(clock_c.get_center(),
                      clock_c.get_center() + RIGHT * 0.15,
                      color=SOFT_WHITE, stroke_width=2.5)
        clock = VGroup(clock_c, m_hand, h_hand)
        timer_lbl = Text("15 min", font_size=12, color=CREAM).next_to(clock_c, RIGHT, buff=0.1)

        self.play(FadeIn(clock, scale=0.7), FadeIn(timer_lbl))
        self.play(Rotate(m_hand, angle=-TAU, about_point=clock_c.get_center()), run_time=1.1)
        self.wait(0.8)
        self.play(FadeOut(st6))
        
        # ══════════════════════════════════════════════════════════════
        # FINAL SUMMARY
        # ══════════════════════════════════════════════════════════════
        summary = Text(
            "VLR caching avoids expensive full HLR lookups for repeat visitors",
            font_size=16, color=ACCENT_GRN, weight=BOLD
        ).to_edge(DOWN, buff=0.35)
        box = SurroundingRectangle(summary, color=ACCENT_GRN, fill_color=DARK_BG,
                                   corner_radius=0.12, buff=0.15, stroke_width=1.6, fill_opacity=0.8)
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