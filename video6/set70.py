from manim import *
import numpy as np


class CellularTransitionImproved(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        self.R_SMALL = 1.0
        self.STROKE_WIDTH = 4

        # --- TITLE ---
        title = Text(
            "The Cellular Concept: Solving the Interference Limit",
            font_size=28,
            color=BLUE_A,
        ).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- INITIAL SETUP: Two adjacent cells ---
        cell_left = self.create_hex(LEFT * 1.1, BLUE)
        cell_right = self.create_hex(RIGHT * 1.1, BLUE)

        tower_left = (
            Triangle(color=WHITE, fill_opacity=1)
            .scale(0.15)
            .move_to(cell_left.get_center())
        )
        tower_right = (
            Triangle(color=WHITE, fill_opacity=1)
            .scale(0.15)
            .move_to(cell_right.get_center())
        )

        label_a = Text("Cell A", font_size=18, color=BLUE_B).next_to(
            cell_left, DOWN, buff=0.15
        )
        label_b = Text("Cell B", font_size=18, color=BLUE_B).next_to(
            cell_right, DOWN, buff=0.15
        )

        self.play(
            DrawBorderThenFill(cell_left),
            DrawBorderThenFill(cell_right),
            FadeIn(tower_left),
            FadeIn(tower_right),
            FadeIn(label_a),
            FadeIn(label_b),
        )
        self.wait(0.5)

        # -------------------------------------------------------
        # CHAPTER 1: Same frequency → Interference
        # -------------------------------------------------------
        s1_label = Text(
            "Scenario 1: Full Frequency Reuse", font_size=22, color=RED
        ).next_to(title, DOWN, buff=0.3)

        f1_left = MathTex("f_1", color=YELLOW, font_size=36).next_to(
            cell_left, UP, buff=0.15
        )
        f1_right = MathTex("f_1", color=YELLOW, font_size=36).next_to(
            cell_right, UP, buff=0.15
        )

        self.play(Write(s1_label), FadeIn(f1_left), FadeIn(f1_right))
        self.wait(0.5)

        # Turn cells red
        self.play(
            cell_left.animate.set_color(RED).set_fill(RED, opacity=0.4),
            cell_right.animate.set_color(RED).set_fill(RED, opacity=0.4),
            run_time=0.6,
        )

        # Lightning bolt path between towers
        lp = [
            tower_left.get_center(),
            tower_left.get_center() + RIGHT * 0.45 + UP * 0.25,
            tower_left.get_center() + RIGHT * 0.9 + DOWN * 0.25,
            tower_left.get_center() + RIGHT * 1.35 + UP * 0.25,
            tower_right.get_center(),
        ]
        lightning = VMobject(color=YELLOW, stroke_width=3)
        lightning.set_points_as_corners(lp)

        clash_text = Text(
            "INTERFERENCE!", font_size=26, color=YELLOW, weight=BOLD
        ).move_to(ORIGIN + DOWN * 1.8)
        clash_bg = BackgroundRectangle(clash_text, color=BLACK, fill_opacity=0.85)

        self.play(
            Create(lightning),
            Wiggle(VGroup(cell_left, cell_right, tower_left, tower_right),
                   rotation_angle=0.008 * TAU),
            FadeIn(clash_bg),
            Write(clash_text),
        )
        self.wait(5.5)

        # Clean up Chapter 1
        self.play(
            FadeOut(s1_label),
            FadeOut(lightning),
            FadeOut(clash_text),
            FadeOut(clash_bg),
            cell_left.animate.set_color(BLUE).set_fill(BLUE, opacity=0.2),
            cell_right.animate.set_color(BLUE).set_fill(BLUE, opacity=0.2),
        )
        self.wait(4)

        # -------------------------------------------------------
        # CHAPTER 2: Split frequencies → Low capacity
        # -------------------------------------------------------
        s2_label = Text(
            "Scenario 2: Splitting Frequencies", font_size=22, color=ORANGE
        ).next_to(title, DOWN, buff=0.3)
        self.play(Write(s2_label))

        # Cell B switches to f2
        f2_right = MathTex("f_2", color=GREEN, font_size=36).next_to(
            cell_right, UP, buff=0.15
        )
        self.play(
            Transform(f1_right, f2_right),
            cell_right.animate.set_color(GREEN).set_fill(GREEN, opacity=0.35),
        )

        bw_text = MathTex(
            r"C_{\text{user}} = \frac{C_{\text{total}}}{2}", color=ORANGE, font_size=36
        ).next_to(VGroup(cell_left, cell_right), DOWN, buff=0.6)
        self.play(Write(bw_text))
        self.wait(2)

        # Clean up Chapter 2
        self.play(
            FadeOut(s2_label),
            FadeOut(bw_text),
            FadeOut(f1_right),   # this is the transformed f2 label
            FadeOut(f1_left),
            cell_right.animate.set_color(BLUE).set_fill(BLUE, opacity=0.2),
        )
        self.wait(5.3)

        # -------------------------------------------------------
        # CHAPTER 3: Spatial reuse → Solution
        # -------------------------------------------------------
        s3_label = Text(
            "Scenario 3: Spatial Reuse (The Solution)", font_size=22, color=GREEN
        ).next_to(title, DOWN, buff=0.3)
        self.play(Write(s3_label))

        # Move both cells apart symmetrically
        cell_a_group = VGroup(cell_left, tower_left, label_a)
        cell_b_group = VGroup(cell_right, tower_right, label_b)
        half_shift = RIGHT * 1.6

        # Arrow spans between the final tower centers (after shift)
        start_pt = tower_left.get_center() - half_shift
        end_pt = tower_right.get_center() + half_shift

        dist_arrow = DoubleArrow(
            start_pt + DOWN * 0.5,
            end_pt + DOWN * 0.5,
            buff=0,
            color=GRAY_B,
            stroke_width=2,
            tip_length=0.18,
        )
        dist_label = MathTex(r"D_{\text{reuse}}", font_size=22, color=GRAY_B).next_to(
            dist_arrow, DOWN, buff=0.12
        )

        self.play(
            cell_a_group.animate.shift(-half_shift),
            cell_b_group.animate.shift(half_shift),
            Create(dist_arrow),
            Write(dist_label),
        )

        # Both cells now share f1 again (same colour/freq, different location)
        f1_reuse_left = MathTex("f_1", color=YELLOW, font_size=36).next_to(
            cell_left, UP, buff=0.15
        )
        f1_reuse_right = MathTex("f_1", color=YELLOW, font_size=36).next_to(
            cell_right, UP, buff=0.15
        )
        self.play(
            cell_left.animate.set_color(BLUE).set_fill(BLUE, opacity=0.35),
            cell_right.animate.set_color(BLUE).set_fill(BLUE, opacity=0.35),
            Write(f1_reuse_left),
            Write(f1_reuse_right),
        )
        self.wait(5.5)

        # Success checkmarks — placed safely below each cell
        check_capacity = Text(
            "✔ Full Bandwidth", color=GREEN, font_size=18
        ).next_to(cell_left, DOWN, buff=0.55)
        check_interference = Text(
            "✔ Low Interference", color=GREEN, font_size=18
        ).next_to(cell_right, DOWN, buff=0.55)

        self.play(FadeIn(check_capacity), FadeIn(check_interference))
        self.wait(5)

        # Final fade-out (optional clean finish)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5,
        )

    # --- GEOMETRY HELPER ---
    def create_hex(self, position, color):
        hex_shape = RegularPolygon(
            n=6,
            radius=self.R_SMALL,
            color=color,
            stroke_width=self.STROKE_WIDTH,
        )
        hex_shape.rotate(PI / 2)
        hex_shape.move_to(position)
        hex_shape.set_fill(color, opacity=0.2)
        return hex_shape