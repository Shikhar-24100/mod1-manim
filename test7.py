from manim import *

# ── Palette (3B1B-inspired) ────────────────────────────────────────────────
CREAM       = "#FFFBE6"
DARK_BG     = "#1C1C2E"
ACCENT_BLUE = "#58C4DD"
ACCENT_RED  = "#FF6B6B"
ACCENT_GRN  = "#6BCB77"
DIM_GREY    = "#888899"
SOFT_WHITE  = "#E8E8F0"
ALT_YELLOW  = "#F2D388"
CARD_BG     = "#2A2A3D" # Slightly lighter than DARK_BG for cards

class Scene7Summary(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ══════════════════════════════════════════════════════════════
        # TITLE
        # ══════════════════════════════════════════════════════════════
        title = Text("Module Summary", font_size=34, weight=BOLD, color=ALT_YELLOW)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        subtitle = Text(
            "Mobile Network Registration Workflows",
            font_size=18, color=CREAM, slant=ITALIC
        ).next_to(title, DOWN, buff=0.18)
        self.play(FadeIn(subtitle))
        self.wait(0.4)

        # ══════════════════════════════════════════════════════════════
        # THREE MINI CARDS
        # ══════════════════════════════════════════════════════════════
        card_data = [
            (
                "Scenario 1",
                "Home Network",
                ["Scans and locks to FOCC", "Connects to active BS", "HLR database updated", "→ Enters IDLE state"]
            ),
            (
                "Scenario 2",
                "Foreign Network (Initial)",
                ["RECC transmits Mobile ID", "VLR-B flags as VISITOR", "Cross-network HLR query", "→ Enters IDLE state"]
            ),
            (
                "Scenario 3",
                "Foreign Network (Cached)",
                ["RECC transmits Mobile ID", "VLR identifies cache HIT", "Lightweight HLR refresh", "→ Enters IDLE state"]
            ),
        ]

        cards = VGroup()
        for sc_title, sc_sub, steps in card_data:
            # Fixed-size card background ensures perfect visual alignment across all three
            box = RoundedRectangle(
                corner_radius=0.12, width=3.8, height=3.2,
                fill_color=CARD_BG, fill_opacity=0.5,
                stroke_color=DIM_GREY, stroke_width=1.5
            )

            # Header
            sc_lbl  = Text(sc_title, font_size=16, color=ACCENT_BLUE, weight=BOLD)
            sub_lbl = Text(sc_sub,   font_size=14, color=SOFT_WHITE)
            header  = VGroup(sc_lbl, sub_lbl).arrange(DOWN, buff=0.12)
            
            # Clean separator line
            sep = Line(LEFT, RIGHT, color=DIM_GREY, stroke_opacity=0.3).set_width(3.2)

            # Body Bullet points
            step_grp = VGroup(*[
                Text(f"•  {s}", font_size=12, color=CREAM) for s in steps
            ]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)

            # Internal arrangement rigidly centered within the fixed box
            content = VGroup(header, sep, step_grp).arrange(DOWN, buff=0.22)
            content.move_to(box.get_center())

            cards.add(VGroup(box, content))

        cards.arrange(RIGHT, buff=0.45)
        cards.next_to(subtitle, DOWN, buff=0.5)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.1), run_time=0.45)
            self.wait(0.15)
        self.wait(0.6)

        # ══════════════════════════════════════════════════════════════
        # KEY INSIGHT
        # ══════════════════════════════════════════════════════════════
        insight = Text(
            "Architectural Insight: VLR caching prevents catastrophic signaling overhead across core networks.",
            font_size=15, color=ALT_YELLOW
        )
        insight.next_to(cards, DOWN, buff=0.45)
        ins_box = SurroundingRectangle(insight, color=ALT_YELLOW,
                                       corner_radius=0.1, buff=0.13, stroke_width=1.0, stroke_opacity=0.7)
        self.play(FadeIn(insight, shift=UP * 0.1), Create(ins_box))
        self.wait(1.5)

        # ══════════════════════════════════════════════════════════════
        # CONTROL CHANNEL RECAP ROW
        # ══════════════════════════════════════════════════════════════
        focc_pill = Text("FOCC (Forward Control Channel)  —  Downlink: Broadcast, Paging, Resource Mapping",
                         font_size=13, color=SOFT_WHITE)
        recc_pill = Text("RECC (Reverse Control Channel)  —  Uplink: Session Request, Page Responses",
                         font_size=13, color=SOFT_WHITE)
        ch_grp = VGroup(focc_pill, recc_pill).arrange(DOWN, buff=0.12)
        ch_grp.next_to(insight, DOWN, buff=0.30)
        self.play(FadeIn(ch_grp, shift=UP * 0.1))
        self.wait(2.0)

        # ══════════════════════════════════════════════════════════════
        # TEASER
        # ══════════════════════════════════════════════════════════════
        self.play(FadeOut(VGroup(cards, insight, ins_box, ch_grp, subtitle)))

        teaser_line1 = Text("Coming Up Next", font_size=20, color=DIM_GREY)
        teaser_line2 = Text("Call Flow in 1G AMPS Networks", font_size=30, color=ALT_YELLOW, weight=BOLD)
        teaser_line3 = Text(
            "Call Origination  •  Call Termination  •  Inter-cell Handoffs",
            font_size=16, color=SOFT_WHITE
        )
        teaser = VGroup(teaser_line1, teaser_line2, teaser_line3).arrange(DOWN, buff=0.25)
        teaser.move_to(ORIGIN)

        self.play(FadeIn(teaser_line1))
        self.play(FadeIn(teaser_line2, scale=0.95))
        self.play(FadeIn(teaser_line3))
        self.wait(2.5)

        self.play(FadeOut(VGroup(title, teaser)), run_time=0.8)
        self.wait(0.5)