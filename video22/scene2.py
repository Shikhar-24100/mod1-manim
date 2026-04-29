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


def load_icon(svg_name, fallback_shape, scale=0.55):
    try:
        icon = SVGMobject(UTILS + svg_name).scale(scale)
    except Exception:
        icon = fallback_shape
    return icon


def make_card(icon_svg, fallback, col, name, desc, icon_scale=0.5):
    icon = load_icon(icon_svg, fallback, scale=icon_scale)
    name_lbl = Text(name, font_size=18, color=col, weight=BOLD)
    desc_lbl = Text(desc, font_size=14, color=SOFT_WHITE, line_spacing=1.3)
    content = VGroup(icon, name_lbl, desc_lbl).arrange(DOWN, buff=0.25)
    
    # Modern premium card look
    box = SurroundingRectangle(
        content, corner_radius=0.2,
        color=DIM_GREY, fill_color="#181825",
        fill_opacity=0.85, buff=0.3, stroke_width=2
    )
    
    # Subtle glow/border effect
    glow = box.copy().set_color(col).set_stroke(width=4, opacity=0.3).scale(1.02)
    
    return VGroup(glow, box, content)


class Scene2NewEntities(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ── Professional Title Sequence ──
        title = Text("Key Players in Call Establishment", font_size=38, weight=BOLD, color=SOFT_WHITE)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN*0.3), run_time=1.2, rate_func=rate_functions.ease_out_cubic)
        self.wait(0.5)

        # ── Elegant Card Data ──
        cards_data = [
            (
                "mobile.svg",
                RoundedRectangle(corner_radius=0.12, width=0.5, height=0.8, color=ALT_YELLOW, fill_opacity=0.3),
                ALT_YELLOW,
                "MS",
                "Mobile Station\nCaller / Receiver"
            ),
            (
                "bs_tower.svg",
                Triangle(color=ACCENT_GRN, fill_opacity=0.3).scale(0.5),
                ACCENT_GRN,
                "BTS / BS",
                "Base Station\nRadio Interface"
            ),
            (
                "msc_switch.svg",
                RoundedRectangle(corner_radius=0.12, width=0.7, height=0.55, color=ACCENT_PURP, fill_opacity=0.3),
                ACCENT_PURP,
                "MSC",
                "Mobile Switching Center\nCall Control Brain"
            ),
        ]

        card_group = VGroup()
        for svg, fallback, col, name, desc in cards_data:
            card_group.add(make_card(svg, fallback, col, name, desc, icon_scale=0.4))
            
        card_group.arrange(RIGHT, buff=0.4)
        card_group.scale_to_fit_width(8.5)
        card_group.next_to(title, DOWN, buff=0.45)

        # ── Fluid Sequential Animation ──
        for card in card_group:
            self.play(
                FadeIn(card, shift=UP*0.2, scale=0.95),
                run_time=1.2,
                rate_func=rate_functions.ease_out_cubic
            )
            self.wait(4.0)

        # ── Network Topology Diagram ──
        diag_title = Text("Network Topology", font_size=20, color=DIM_GREY, slant=ITALIC)
        diag_title.next_to(card_group, DOWN, buff=0.45)
        self.play(FadeIn(diag_title, shift=UP*0.1), run_time=0.8, rate_func=rate_functions.ease_out_sine)

        ms_node  = Circle(radius=0.22, color=ALT_YELLOW, fill_opacity=0.35).shift(LEFT*4.5 + DOWN*2.0)
        bs_node  = Circle(radius=0.22, color=ACCENT_GRN, fill_opacity=0.35).shift(LEFT*2.0 + DOWN*2.0)
        msc_node = RoundedRectangle(corner_radius=0.15, width=1.0, height=0.55,
                                    color=ACCENT_PURP, fill_opacity=0.35).shift(DOWN*2.0)
        hlr_node = Circle(radius=0.22, color=ACCENT_BLUE, fill_opacity=0.35).shift(RIGHT*2.4 + DOWN*1.5)
        vlr_node = Circle(radius=0.22, color=ACCENT_RED,  fill_opacity=0.35).shift(RIGHT*2.4 + DOWN*2.5)
        pstn_node= RoundedRectangle(corner_radius=0.15, width=1.0, height=0.45,
                                    color=DIM_GREY, fill_opacity=0.25).shift(RIGHT*4.4 + DOWN*2.0)

        node_labels = [
            Text("MS",   font_size=12, color=ALT_YELLOW).move_to(ms_node),
            Text("BS",   font_size=12, color=ACCENT_GRN).move_to(bs_node),
            Text("MSC",  font_size=12, color=ACCENT_PURP).move_to(msc_node),
            Text("HLR",  font_size=12, color=ACCENT_BLUE).move_to(hlr_node),
            Text("VLR",  font_size=12, color=ACCENT_RED ).move_to(vlr_node),
            Text("PSTN", font_size=12, color=DIM_GREY   ).move_to(pstn_node),
        ]

        nodes = VGroup(ms_node, bs_node, msc_node, hlr_node, vlr_node, pstn_node)
        lbls  = VGroup(*node_labels)

        edges_data = [
            (ms_node, bs_node,  SOFT_WHITE),
            (bs_node, msc_node, SOFT_WHITE),
            (msc_node, hlr_node, ACCENT_BLUE),
            (msc_node, vlr_node, ACCENT_RED),
            (msc_node, pstn_node, DIM_GREY),
        ]
        edges = VGroup(*[
            Line(a.get_right() if a.get_right()[0] < b.get_left()[0] else a.get_center(),
                 b.get_left()  if a.get_right()[0] < b.get_left()[0] else b.get_center(),
                 color=c, stroke_width=2.5)
            for a, b, c in edges_data
        ])

        # ── Elegant Topology Render ──
        self.play(
            LaggedStart(*[FadeIn(n, scale=0.8) for n in nodes], lag_ratio=0.15),
            LaggedStart(*[FadeIn(l, shift=UP*0.1) for l in lbls],  lag_ratio=0.15),
            run_time=1.5, rate_func=rate_functions.ease_out_cubic
        )
        # 1. MS to BS
        self.play(Create(edges[0]), run_time=0.8)
        self.wait(2.0)
        # 2. BS to MSC
        self.play(Create(edges[1]), run_time=0.8)
        self.wait(2.0)
        # 3. MSC to HLR, VLR, PSTN sequentially
        for e in edges[2:]:
            self.play(Create(e), run_time=0.8)
            self.wait(0.2)

        # Smooth teardown
        self.play(
            FadeOut(VGroup(title, card_group, diag_title, nodes, lbls, edges), shift=UP*0.3), 
            run_time=0.9, rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(0.3)
