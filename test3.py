from manim import *

# ── SVG ASSETS (place these files in your utils/ folder) ──────────────────
# utils/mobile.svg       — mobile phone icon
# utils/bs_tower.svg     — cell tower / base station icon
# ──────────────────────────────────────────────────────────────────────────

UTILS = "utils/"

class Scene3ControlChannels(Scene):
    def construct(self):

        # ── Title ──────────────────────────────────────────────────────
        title = Text("Control Channels", font_size=34, weight=BOLD, color=WHITE)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        subtitle = Text(
            "Some channels in the band are reserved purely for signalling & call setup",
            font_size=16, color=BLUE_B, slant=ITALIC
        ).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(subtitle))
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════
        # ICONS — BS left, Mobile right, fixed positions
        # ══════════════════════════════════════════════════════════════

        try:
            bs_icon = SVGMobject(UTILS + "bs_tower.svg").scale(0.85)
        except Exception:
            bs_icon = Triangle(color=WHITE, fill_opacity=0.3).scale(0.65)
        bs_icon.move_to(LEFT * 5.2 + DOWN * 0.5)
        bs_label = Text("Base Station", font_size=15, color=GREY_A).next_to(bs_icon, DOWN, buff=0.12)

        try:
            mob_icon = SVGMobject(UTILS + "mobile.svg").scale(0.65)
        except Exception:
            mob_icon = RoundedRectangle(
                corner_radius=0.12, width=0.45, height=0.78,
                color=WHITE, fill_opacity=0.3
            )
        mob_icon.move_to(RIGHT * 5.2 + DOWN * 0.5)
        mob_label = Text("Mobile Unit", font_size=15, color=GREY_A).next_to(mob_icon, DOWN, buff=0.12)

        self.play(
            FadeIn(bs_icon, shift=RIGHT * 0.2), FadeIn(bs_label),
            FadeIn(mob_icon, shift=LEFT * 0.2), FadeIn(mob_label),
        )
        self.wait(0.4)

        # ══════════════════════════════════════════════════════════════
        # FOCC — upper half
        # ══════════════════════════════════════════════════════════════

        focc_arrow = Arrow(
            start=LEFT * 3.0, end=RIGHT * 3.0,
            color=GREEN_C, buff=0,
            stroke_width=3.5, tip_length=0.2
        ).move_to(ORIGIN + UP * 1.1)

        focc_name = Text("Forward Control Channel", font_size=14, color=GREEN_B, slant=ITALIC)
        focc_name.next_to(focc_arrow, UP, buff=0.12)

        focc_tag = Text("FOCC", font_size=22, color=GREEN_C, weight=BOLD)
        focc_tag.next_to(focc_name, UP, buff=0.08)

        focc_dir = Text("BS  →  Mobile", font_size=13, color=GREEN_B)
        focc_dir.next_to(focc_arrow, DOWN, buff=0.1)

        self.play(GrowArrow(focc_arrow))
        self.play(FadeIn(focc_tag), FadeIn(focc_name), FadeIn(focc_dir))
        self.wait(0.3)

        focc_uses = [
            "●  Broadcasting BS signals",
            "●  Paging incoming calls",
            "●  Resource assignment",
        ]
        focc_bullets = VGroup(*[
            Text(u, font_size=13, color=GREEN_A) for u in focc_uses
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        focc_bullets.next_to(focc_dir, DOWN, buff=0.18)
        focc_bullets.align_to(focc_arrow, LEFT)

        for line in focc_bullets:
            self.play(FadeIn(line, shift=RIGHT * 0.15), run_time=0.4)
        self.wait(0.6)

        # ══════════════════════════════════════════════════════════════
        # Transition: fade FOCC bullets out, slide FOCC block up
        # so RECC gets the lower half cleanly
        # ══════════════════════════════════════════════════════════════

        focc_block = VGroup(focc_tag, focc_name, focc_arrow, focc_dir)

        self.play(
            FadeOut(focc_bullets, shift=UP * 0.1),
            focc_block.animate.shift(UP * 0.5),
            run_time=0.5
        )
        self.wait(0.2)

        # ══════════════════════════════════════════════════════════════
        # RECC — lower half, anchored well below FOCC block
        # ══════════════════════════════════════════════════════════════

        recc_arrow = Arrow(
            start=RIGHT * 3.0, end=LEFT * 3.0,
            color=RED_C, buff=0,
            stroke_width=3.5, tip_length=0.2
        ).move_to(ORIGIN + DOWN * 0.7)

        recc_dir = Text("Mobile  →  BS", font_size=13, color=RED_B)
        recc_dir.next_to(recc_arrow, UP, buff=0.1)

        recc_tag = Text("RECC", font_size=22, color=RED_C, weight=BOLD)
        recc_tag.next_to(recc_arrow, DOWN, buff=0.12)

        recc_name = Text("Reverse Control Channel", font_size=14, color=RED_B, slant=ITALIC)
        recc_name.next_to(recc_tag, DOWN, buff=0.08)

        self.play(GrowArrow(recc_arrow))
        self.play(FadeIn(recc_tag), FadeIn(recc_name), FadeIn(recc_dir))
        self.wait(0.3)

        recc_uses = [
            "●  Sharing Mobile ID on wake-up",
            "●  Call request (making a call)",
            "●  Call answering (receiving a call)",
        ]
        recc_bullets = VGroup(*[
            Text(u, font_size=13, color=RED_A) for u in recc_uses
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        recc_bullets.next_to(recc_name, DOWN, buff=0.15)
        recc_bullets.align_to(recc_arrow, LEFT)

        for line in recc_bullets:
            self.play(FadeIn(line, shift=LEFT * 0.15), run_time=0.4)
        self.wait(0.6)

        # ══════════════════════════════════════════════════════════════
        # COLLISION NOTE — after clearing bullets
        # ══════════════════════════════════════════════════════════════

        self.play(FadeOut(recc_bullets), run_time=0.4)

        collision_note = Text(
            "⚠   RECC uses a Collision / Contention mechanism",
            font_size=17, color=YELLOW
        ).to_edge(DOWN, buff=0.4)
        box = SurroundingRectangle(
            collision_note, color=YELLOW,
            corner_radius=0.1, buff=0.14, stroke_width=1.5
        )

        self.play(FadeIn(collision_note, shift=UP * 0.2), Create(box))
        self.wait(2.2)

        # ── Fade everything out ───────────────────────────────────────
        all_obj = VGroup(
            title, subtitle,
            bs_icon, bs_label, mob_icon, mob_label,
            focc_block,
            recc_arrow, recc_tag, recc_name, recc_dir,
            collision_note, box
        )
        self.play(FadeOut(all_obj, shift=UP * 0.3), run_time=0.8)
        self.wait(0.3)