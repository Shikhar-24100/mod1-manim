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


class Scene1Recap(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ── Professional Title Sequence ──
        title = Text("Video 1 Recap", font_size=42, weight=BOLD, color=SOFT_WHITE)
        sub   = Text("The Mobile Registration Sequence", font_size=24, color=ACCENT_BLUE)
        hdr   = VGroup(title, sub).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)
        
        self.play(FadeIn(hdr, shift=DOWN * 0.3), run_time=1.2, rate_func=rate_functions.ease_out_cubic)
        self.wait(0.5)

        # ── Elegant Card Data ──
        cards_data = [
            (
                "mobile.svg",
                RoundedRectangle(corner_radius=0.12, width=0.5, height=0.8, color=ALT_YELLOW, fill_opacity=0.3),
                ALT_YELLOW,
                "Device Startup",
                "Mobile powers on and\nscans for FOCC signals."
            ),
            (
                "bs_tower.svg",
                Triangle(color=ACCENT_GRN, fill_opacity=0.3).scale(0.5),
                ACCENT_GRN,
                "Signal Selection",
                "Connects to the BS with\nthe strongest signal level."
            ),
            (
                "hlr_box.svg",
                RoundedRectangle(corner_radius=0.12, width=0.7, height=0.55, color=ACCENT_BLUE, fill_opacity=0.3),
                ACCENT_BLUE,
                "Location Registration",
                "HLR / VLR is updated with\nthe user's precise location."
            ),
        ]

        card_group = VGroup()
        for svg, fallback, col, name, desc in cards_data:
            card_group.add(make_card(svg, fallback, col, name, desc))
            
        card_group.arrange(RIGHT, buff=0.6).next_to(hdr, DOWN, buff=0.8)
        card_group.scale_to_fit_width(12.5)

        # ── Fluid Sequential Animation ──
        for card in card_group:
            self.play(
                FadeIn(card, shift=UP*0.2, scale=0.95),
                run_time=1.2,
                rate_func=rate_functions.ease_out_cubic
            )
            self.wait(4.0)

        # ── Polished Transition Prompt ──
        q = Text("Now — what happens when a call is placed?", font_size=26, color=ALT_YELLOW, weight=BOLD)
        q.to_edge(DOWN, buff=0.8)
        
        underline = Line(LEFT, RIGHT).match_width(q).next_to(q, DOWN, buff=0.1)
        underline.set_color(ALT_YELLOW).set_stroke(width=2)
        
        self.play(FadeIn(q, shift=UP*0.2), run_time=1.0, rate_func=rate_functions.ease_out_cubic)
        self.play(Create(underline), run_time=0.8, rate_func=rate_functions.ease_in_out_sine)
        self.wait(1.8)

        # Smooth teardown
        self.play(
            FadeOut(VGroup(hdr, card_group, q, underline), shift=UP*0.3), 
            run_time=0.9, 
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(0.3)
