from manim import *

# ── SVG ASSETS (place these files in your utils/ folder) ──────────────────
# utils/mobile.svg       — mobile phone icon
# utils/bs_tower.svg     — cell tower / base station icon
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

class Scene3ControlChannels(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ── Title ──────────────────────────────────────────────────────
        title = Text("Control Channels", font_size=38, weight=BOLD, color=SOFT_WHITE)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        subtitle = Text(
            "Some channels are reserved purely for signalling & call setup",
            font_size=19, color=ACCENT_BLUE
        ).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(subtitle))
        self.wait(2.5)

        # ══════════════════════════════════════════════════════════════
        # ICONS — BS left, Mobile right, fixed positions
        # ══════════════════════════════════════════════════════════════

        try:
            bs_icon = SVGMobject(UTILS + "bs_tower.svg").scale(0.85)
        except Exception:
            bs_icon = Triangle(color=ACCENT_GRN, fill_opacity=0.3).scale(0.65)
        
        # Position slightly lower to give the diagram some breathing room
        bs_icon.move_to(LEFT * 4.8 + DOWN * 0.6)
        bs_label = Text("Base Station", font_size=15, color=SOFT_WHITE, weight=BOLD).next_to(bs_icon, DOWN, buff=0.15)

        try:
            mob_icon = SVGMobject(UTILS + "mobile.svg").scale(0.65)
        except Exception:
            mob_icon = RoundedRectangle(
                corner_radius=0.12, width=0.45, height=0.78,
                color=ALT_YELLOW, fill_opacity=0.3
            )
        mob_icon.move_to(RIGHT * 4.8 + DOWN * 0.6)
        mob_label = Text("Mobile Unit", font_size=15, color=SOFT_WHITE, weight=BOLD).next_to(mob_icon, DOWN, buff=0.15)

        self.play(
            FadeIn(bs_icon, shift=RIGHT * 0.2), FadeIn(bs_label),
            FadeIn(mob_icon, shift=LEFT * 0.2), FadeIn(mob_label),
        )
        self.wait(2.4)

        # ══════════════════════════════════════════════════════════════
        # FOCC — upper half
        # ══════════════════════════════════════════════════════════════

        focc_arrow = Arrow(
            start=LEFT * 2.6, end=RIGHT * 2.6,
            color=ACCENT_GRN, buff=0,
            stroke_width=4, tip_length=0.2
        ).move_to(ORIGIN + UP * 0.8)

        focc_name = Text("Forward Control Channel", font_size=15, color=CREAM, slant=ITALIC)
        focc_name.next_to(focc_arrow, UP, buff=0.15)

        focc_tag = Text("FOCC", font_size=24, color=ACCENT_GRN, weight=BOLD)
        focc_tag.next_to(focc_name, UP, buff=0.1)

        focc_dir = Text("BS  →  Mobile", font_size=14, color=ACCENT_GRN)
        focc_dir.next_to(focc_arrow, DOWN, buff=0.12)

        self.play(GrowArrow(focc_arrow))
        self.play(FadeIn(focc_tag), FadeIn(focc_name), FadeIn(focc_dir))
        self.wait(2.3)

        focc_uses = [
            "●  Broadcasting BS signals",
            "●  Paging incoming calls",
            "●  Resource assignment",
        ]
        focc_bullets = VGroup(*[
            Text(u, font_size=14, color=SOFT_WHITE) for u in focc_uses
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        focc_bullets.next_to(focc_dir, DOWN, buff=0.25)
        # Shift slightly right so it centers better between the icons
        focc_bullets.align_to(focc_arrow, LEFT).shift(RIGHT * 0.3)

        for line in focc_bullets:
            self.play(FadeIn(line, shift=RIGHT * 0.15), run_time=0.4)
        self.wait(2.6)

        # ══════════════════════════════════════════════════════════════
        # Transition: fade FOCC bullets out, slide FOCC block up
        # so RECC gets the lower half cleanly
        # ══════════════════════════════════════════════════════════════

        focc_block = VGroup(focc_tag, focc_name, focc_arrow, focc_dir)

        self.play(
            FadeOut(focc_bullets, shift=UP * 0.1),
            focc_block.animate.shift(UP * 0.6), # Move FOCC up significantly
            run_time=0.6
        )
        self.wait(2.2)

        # ══════════════════════════════════════════════════════════════
        # RECC — lower half, anchored well below FOCC block
        # ══════════════════════════════════════════════════════════════

        recc_arrow = Arrow(
            start=RIGHT * 2.6, end=LEFT * 2.6,
            color=ACCENT_RED, buff=0,
            stroke_width=4, tip_length=0.2
        ).move_to(ORIGIN + DOWN * 0.9)

        recc_dir = Text("Mobile  →  BS", font_size=14, color=ACCENT_RED)
        recc_dir.next_to(recc_arrow, UP, buff=0.12)

        recc_tag = Text("RECC", font_size=24, color=ACCENT_RED, weight=BOLD)
        recc_tag.next_to(recc_arrow, DOWN, buff=0.15)

        recc_name = Text("Reverse Control Channel", font_size=15, color=CREAM, slant=ITALIC)
        recc_name.next_to(recc_tag, DOWN, buff=0.1)

        self.play(GrowArrow(recc_arrow))
        self.play(FadeIn(recc_tag), FadeIn(recc_name), FadeIn(recc_dir))
        self.wait(2.3)

        recc_uses = [
            "●  Sharing Mobile ID on wake-up",
            "●  Call request (making a call)",
            "●  Call answering (receiving a call)",
        ]
        recc_bullets = VGroup(*[
            Text(u, font_size=14, color=SOFT_WHITE) for u in recc_uses
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        # Place bullets neatly below the RECC name
        recc_bullets.next_to(recc_name, DOWN, buff=0.25)
        recc_bullets.align_to(recc_arrow, LEFT).shift(RIGHT * 0.3)

        for line in recc_bullets:
            self.play(FadeIn(line, shift=LEFT * 0.15), run_time=0.4)
        self.wait(2.6)

        # ══════════════════════════════════════════════════════════════
        # COLLISION NOTE — after clearing bullets
        # ══════════════════════════════════════════════════════════════

        self.play(FadeOut(recc_bullets), run_time=0.4)

        collision_note = Text(
            "RECC uses a Collision / Contention mechanism",
            font_size=18, color=ALT_YELLOW, weight=BOLD
        ).to_edge(DOWN, buff=0.4)
        
        box = SurroundingRectangle(
            collision_note, color=ALT_YELLOW, fill_color=DARK_BG,
            corner_radius=0.12, buff=0.16, stroke_width=1.8, fill_opacity=0.8
        )
        coll_group = VGroup(box, collision_note)

        self.play(FadeIn(coll_group, shift=UP * 0.2))
        self.wait(4.2)

        # ── Fade everything out ───────────────────────────────────────
        all_obj = VGroup(
            title, subtitle,
            bs_icon, bs_label, mob_icon, mob_label,
            focc_block,
            recc_arrow, recc_tag, recc_name, recc_dir,
            coll_group
        )
        self.play(FadeOut(all_obj, shift=UP * 0.3), run_time=0.8)
        self.wait(1.3)