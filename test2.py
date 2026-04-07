from manim import *

# ── SVG ASSETS (place these files in your utils/ folder) ──────────────────
# utils/mobile.svg       — mobile phone icon
# utils/bs_tower.svg     — cell tower / base station icon
# utils/hlr_box.svg      — database cylinder or server icon (for HLR)
# utils/vlr_box.svg      — database cylinder or server icon (for VLR, can reuse hlr_box.svg)
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


class Scene2NetworkComponents(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ── Title ──────────────────────────────────────────────────────
        title = Text("Network Components", font_size=38, weight=BOLD, color=SOFT_WHITE)
        subtitle = Text("The key players in a 1G AMPS network", font_size=21, color=ACCENT_BLUE)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.45)
        
        self.play(FadeIn(title_group, shift=DOWN * 0.25))
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════
        # PART 1 — Introduce each component one by one with description
        # ══════════════════════════════════════════════════════════════

        # ── Helper: icon loader with fallback shape ────────────────────
        def load_icon(svg_name, fallback_shape, scale=0.55):
            try:
                icon = SVGMobject(UTILS + svg_name).scale(scale)
                # Ensure SVGs are NOT colorized to preserve their original design
            except Exception:
                icon = fallback_shape
            return icon

        # Component definitions: (svg, fallback, color, name, description)
        components = [
            (
                "mobile.svg",
                RoundedRectangle(corner_radius=0.12, width=0.5, height=0.85,
                                 color=ALT_YELLOW, fill_opacity=0.3),
                ALT_YELLOW,
                "Mobile Unit",
                "Each mobile has a unique\nidentification number."
            ),
            (
                "bs_tower.svg",
                Triangle(color=ACCENT_GRN, fill_opacity=0.3).scale(0.55),
                ACCENT_GRN,
                "Base Station (BS)",
                "Continuously broadcasts\ncontrol signals (FOCC)."
            ),
            (
                "hlr_box.svg",
                RoundedRectangle(corner_radius=0.1, width=0.7, height=0.6,
                                 color=ACCENT_BLUE, fill_opacity=0.3),
                ACCENT_BLUE,
                "HLR",
                "Holds data of all users\nwhose HOME cell is here."
            ),
            (
                "vlr_box.svg",
                RoundedRectangle(corner_radius=0.1, width=0.7, height=0.6,
                                 color=ACCENT_RED, fill_opacity=0.3),
                ACCENT_RED,
                "VLR",
                "Holds data of VISITING\nusers from other cells."
            ),
        ]

        card_group = VGroup()
        for i, (svg, fallback, col, name, desc) in enumerate(components):
            icon = load_icon(svg, fallback, scale=0.55)

            name_lbl = Text(name, font_size=17, color=col, weight=BOLD)
            desc_lbl = Text(desc, font_size=14, color=SOFT_WHITE)

            card_content = VGroup(icon, name_lbl, desc_lbl).arrange(DOWN, buff=0.18)

            box = SurroundingRectangle(
                card_content, corner_radius=0.15,
                color=DIM_GREY, fill_color='#151522',
                fill_opacity=0.7, buff=0.22,
                stroke_width=1.5
            )
            card = VGroup(box, card_content)
            card_group.add(card)

        card_group.arrange(RIGHT, buff=0.35)
        # Position cards comfortably below the header
        card_group.next_to(title_group, DOWN, buff=0.6)
        card_group.scale_to_fit_width(13)

        # Animate cards one by one
        for card in card_group:
            self.play(FadeIn(card, scale=0.85), run_time=0.6)
            self.wait(0.25)

        self.wait(1.0)

        # ══════════════════════════════════════════════════════════════
        # PART 2 — Multi-cell map: 3 hexagonal cells, each with HLR+VLR+BS+Mobile
        # ══════════════════════════════════════════════════════════════

        self.play(FadeOut(card_group), run_time=0.6)

        map_title = Text("The Network — 3 Cells", font_size=20, color=CREAM, slant=ITALIC)
        # Replacing the subtitle with this new map_title in same position roughly
        map_title.next_to(title_group[0], DOWN, buff=0.25)
        
        self.play(
            FadeOut(title_group[1], shift=UP*0.2), # Fade out original subtitle
            FadeIn(map_title, shift=UP*0.2)
        )
        self.wait(0.3)

        # ── Hexagonal cell factory ─────────────────────────────────────
        def make_hex(center, col):
            return RegularPolygon(
                n=6, start_angle=PI / 6,
                color=col, fill_opacity=0.10, stroke_width=2
            ).scale(1.55).move_to(center)

        cell_colors  = [ACCENT_BLUE, ACCENT_GRN, ACCENT_RED]
        # Shifted slightly UP to ensure no overlap with bottom fact text
        cell_centers = [LEFT * 3.8 + UP * 0.2, UP * 0.2, RIGHT * 3.8 + UP * 0.2]
        cell_numbers = ["1", "2", "3"]

        hexes = [make_hex(c, col) for c, col in zip(cell_centers, cell_colors)]

        # ── Cell number label (bottom of hex) ─────────────────────────
        cell_num_labels = [
            Text(n, font_size=20, color=col, weight=BOLD).move_to(ctr + DOWN * 1.25)
            for n, col, ctr in zip(cell_numbers, cell_colors, cell_centers)
        ]

        self.play(
            LaggedStart(*[DrawBorderThenFill(h) for h in hexes], lag_ratio=0.3),
            LaggedStart(*[FadeIn(l) for l in cell_num_labels], lag_ratio=0.3),
        )
        self.wait(0.4)

        # ── BS tower per cell (centre of each hex) ────────────────────
        def make_bs(center, col):
            try:
                icon = SVGMobject(UTILS + "bs_tower.svg").scale(0.38)
                # No set_color applied to preserve SVG's inherent colors
            except Exception:
                icon = Triangle(color=col, fill_opacity=0.5).scale(0.32)
            icon.move_to(center + UP * 0.15)
            lbl = Text("BS", font_size=12, color=col, weight=BOLD).next_to(icon, DOWN, buff=0.1)
            return VGroup(icon, lbl)

        bs_icons = [make_bs(ctr, col) for ctr, col in zip(cell_centers, cell_colors)]
        self.play(LaggedStart(*[FadeIn(b, scale=0.7) for b in bs_icons], lag_ratio=0.3))
        self.wait(0.3)

        # ── HLR + VLR boxes (top-left corner of each hex) ─────────────
        def make_hlr_vlr(center, col):
            def db_icon(svg_name, label_str, fallback_col):
                try:
                    ico = SVGMobject(UTILS + svg_name).scale(0.28)
                    # No set_color applied to preserve SVG's inherent colors
                except Exception:
                    ico = RoundedRectangle(
                        corner_radius=0.08, width=0.42, height=0.36,
                        color=fallback_col, fill_opacity=0.35
                    )
                lbl = Text(label_str, font_size=11, color=SOFT_WHITE, weight=BOLD)
                lbl.next_to(ico, DOWN, buff=0.06)
                return VGroup(ico, lbl)

            hlr = db_icon("hlr_box.svg", "HLR", ACCENT_BLUE)
            vlr = db_icon("vlr_box.svg", "VLR", ACCENT_RED)
            pair = VGroup(hlr, vlr).arrange(RIGHT, buff=0.18)
            pair.move_to(center + UP * 1.05 + LEFT * 0.5)
            return pair

        hlr_vlr_groups = [make_hlr_vlr(ctr, col) for ctr, col in zip(cell_centers, cell_colors)]
        self.play(LaggedStart(*[FadeIn(g, scale=0.8) for g in hlr_vlr_groups], lag_ratio=0.3))
        self.wait(0.3)

        # ── Mobile unit per cell ───────────────────────────────────────
        def make_mobile(center, col):
            try:
                ico = SVGMobject(UTILS + "mobile.svg").scale(0.32)
                # No set_color applied to preserve SVG's inherent colors
            except Exception:
                ico = RoundedRectangle(
                    corner_radius=0.08, width=0.28, height=0.45,
                    color=ALT_YELLOW, fill_opacity=0.45
                )
            ico.move_to(center + RIGHT * 0.9 + DOWN * 0.6)
            id_lbl = Text("ID", font_size=11, color=SOFT_WHITE).next_to(ico, DOWN, buff=0.06)
            return VGroup(ico, id_lbl)

        mobiles = [make_mobile(ctr, col) for ctr, col in zip(cell_centers, cell_colors)]
        self.play(LaggedStart(*[FadeIn(m, scale=0.7) for m in mobiles], lag_ratio=0.3))
        self.wait(0.5)

        # ── Broadcast signal waves from each BS ───────────────────────
        def signal_ripple(center, col):
            arcs = []
            for r in [0.45, 0.75, 1.05]:
                arc = Arc(
                    radius=r, angle=PI * 0.9,
                    start_angle=PI * 0.55,
                    color=col, stroke_opacity=0.6,
                    stroke_width=1.5
                ).move_arc_center_to(center + UP * 0.15)
                arcs.append(arc)
            return arcs

        all_ripples = []
        for ctr, col in zip(cell_centers, cell_colors):
            all_ripples.extend(signal_ripple(ctr, col))

        self.play(
            LaggedStart(*[Create(r) for r in all_ripples], lag_ratio=0.07),
            run_time=1.4
        )
        self.wait(0.5)

        # ── Key fact callout ──────────────────────────────────────────
        fact = Text(
            "Each BS continuously broadcasts its signal.\nMobiles identify the BS with maximum strength.",
            font_size=19, color=CREAM, line_spacing=1.1
        ).to_edge(DOWN, buff=0.5)
        
        underline = Line(
            fact.get_left() + DOWN * 0.08,
            fact.get_right() + DOWN * 0.08,
            color=ACCENT_BLUE, stroke_width=1.5
        )

        self.play(FadeIn(fact, shift=UP * 0.2))
        self.play(Create(underline, run_time=0.5))
        self.wait(2.2)

        # ── Fade everything out ───────────────────────────────────────
        all_objects = VGroup(
            title_group[0], map_title,
            *hexes, *cell_num_labels,
            *bs_icons, *hlr_vlr_groups, *mobiles,
            *all_ripples, fact, underline
        )
        self.play(FadeOut(all_objects, shift=UP * 0.3), run_time=0.8)
        self.wait(0.3)