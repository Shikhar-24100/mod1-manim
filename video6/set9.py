from manim import *
import numpy as np

class AdjacentChannelInterference(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # TITLE
        # ---------------------------------------------------------
        title = Text("Adjacent Channel Interference (ACI)", font_size=38).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # ---------------------------------------------------------
        # SCENE 1: THE PROBLEM - Frequency Spectrum Visual
        # ---------------------------------------------------------
        
        intro = Text("Imperfect filters cause frequency overlap", font_size=26)
        intro.next_to(title, DOWN, buff=0.5)
        self.play(Write(intro))
        self.wait(0.8)
        
        # Frequency axis
        freq_axis = NumberLine(
            x_range=[0, 10, 1],
            length=10,
            include_numbers=False,
            include_tip=True,
            tip_length=0.2
        ).shift(DOWN * 0.5)
        
        freq_label = Text("Frequency →", font_size=20).next_to(freq_axis, RIGHT, buff=0.2)
        
        self.play(Create(freq_axis), Write(freq_label))
        self.wait(0.3)
        
        # Desired channel (center)
        desired_center = 5
        desired_bw = 1.2
        
        desired_rect = Rectangle(
            height=2,
            width=desired_bw,
            color=GREEN,
            fill_opacity=0.4,
            stroke_width=2
        ).move_to(freq_axis.n2p(desired_center) + UP * 1.5)
        
        desired_label = Text("Desired\nChannel", font_size=18, color=GREEN).move_to(desired_rect.get_center())
        
        # Ideal spectrum (perfect rectangle)
        ideal_spectrum = VGroup(
            Line(desired_rect.get_corner(DL), desired_rect.get_corner(UL), color=GREEN, stroke_width=3),
            Line(desired_rect.get_corner(UL), desired_rect.get_corner(UR), color=GREEN, stroke_width=3),
            Line(desired_rect.get_corner(UR), desired_rect.get_corner(DR), color=GREEN, stroke_width=3)
        )
        
        self.play(Create(ideal_spectrum), FadeIn(desired_rect), Write(desired_label))
        self.wait(0.5)
        
        # Adjacent channels
        adj_left_center = desired_center - 1.5
        adj_right_center = desired_center + 1.5
        
        adj_left = Rectangle(
            height=2,
            width=desired_bw,
            color=BLUE,
            fill_opacity=0.3,
            stroke_width=2
        ).move_to(freq_axis.n2p(adj_left_center) + UP * 1.5)
        
        adj_right = Rectangle(
            height=2,
            width=desired_bw,
            color=BLUE,
            fill_opacity=0.3,
            stroke_width=2
        ).move_to(freq_axis.n2p(adj_right_center) + UP * 1.5)
        
        adj_label_l = Text("Adj", font_size=16, color=BLUE).move_to(adj_left.get_center())
        adj_label_r = Text("Adj", font_size=16, color=BLUE).move_to(adj_right.get_center())
        
        self.play(
            FadeIn(adj_left), FadeIn(adj_right),
            Write(adj_label_l), Write(adj_label_r)
        )
        self.wait(0.8)
        
        # Show REAL filter response (with spectral leakage)
        real_filter_note = Text("Reality: Imperfect filters leak power", font_size=22, color=YELLOW)
        real_filter_note.next_to(freq_axis, DOWN, buff=0.3)
        self.play(Write(real_filter_note))
        self.wait(0.5)
        
        # Create realistic filter shapes (Gaussian-like curves showing leakage)
        def create_filter_curve(center_x, color, height=2):
            points = []
            for x in np.linspace(-0.8, 0.8, 40):
                y = height * np.exp(-2 * x**2)  # Gaussian
                point = freq_axis.n2p(center_x + x) + UP * y
                points.append(point)
            return VMobject().set_points_smoothly(points).set_color(color).set_stroke(width=3)
        
        # Fade out ideal rectangles
        self.play(
            FadeOut(ideal_spectrum),
            FadeOut(desired_rect),
            FadeOut(adj_left),
            FadeOut(adj_right)
        )
        
        # Show realistic curves
        real_desired = create_filter_curve(desired_center, GREEN)
        real_adj_left = create_filter_curve(adj_left_center, BLUE)
        real_adj_right = create_filter_curve(adj_right_center, BLUE)
        
        # Fill under curves for better visualization
        real_desired_fill = real_desired.copy().set_fill(GREEN, opacity=0.3).add_line_to(freq_axis.n2p(desired_center - 0.8)).add_line_to(freq_axis.n2p(desired_center + 0.8)).close_path()
        real_adj_left_fill = real_adj_left.copy().set_fill(BLUE, opacity=0.2).add_line_to(freq_axis.n2p(adj_left_center - 0.8)).add_line_to(freq_axis.n2p(adj_left_center + 0.8)).close_path()
        real_adj_right_fill = real_adj_right.copy().set_fill(BLUE, opacity=0.2).add_line_to(freq_axis.n2p(adj_right_center - 0.8)).add_line_to(freq_axis.n2p(adj_right_center + 0.8)).close_path()
        
        self.play(
            Create(real_desired), FadeIn(real_desired_fill),
            Create(real_adj_left), FadeIn(real_adj_left_fill),
            Create(real_adj_right), FadeIn(real_adj_right_fill),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Highlight overlap regions
        overlap_left = Rectangle(
            height=2.5,
            width=0.3,
            color=RED,
            fill_opacity=0.5,
            stroke_width=0
        ).move_to(freq_axis.n2p(desired_center - 0.75) + UP * 1.25)
        
        overlap_right = Rectangle(
            height=2.5,
            width=0.3,
            color=RED,
            fill_opacity=0.5,
            stroke_width=0
        ).move_to(freq_axis.n2p(desired_center + 0.75) + UP * 1.25)
        
        overlap_label = Text("Interference!", font_size=15, color=RED, weight=BOLD)
        overlap_label.next_to(intro, DOWN, buff=0.3)
        # arrow = Arrow(overlap_label.get_left(), overlap_right.get_right(), color=RED, buff=0.1, stroke_width=3)
        
        self.play(
            FadeIn(overlap_left), FadeIn(overlap_right),
            Write(overlap_label)
        )
        self.wait(2)
        
        # Clear for next scene
        self.play(
            *[FadeOut(mob) for mob in [
                freq_axis, freq_label, desired_label, adj_label_l, adj_label_r,
                real_desired, real_desired_fill, real_adj_left, real_adj_left_fill,
                real_adj_right, real_adj_right_fill, overlap_left, overlap_right,
                overlap_label, intro, real_filter_note
            ]]
        )
        self.wait(0.5)
        
        # ---------------------------------------------------------
        # SCENE 2: MATHEMATICAL RELATIONSHIP
        # ---------------------------------------------------------
        
        math_title = Text("Adjacent Channel Interference Ratio (ACIR)", font_size=28, color=YELLOW)
        math_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(math_title))
        self.wait(0.5)
        
        # Create side-by-side comparison
        # LEFT: Causes
        causes_title = Text("Causes:", font_size=24, weight=BOLD, color=BLUE).shift(LEFT * 3.5 + UP * 1.5)
        
        causes = VGroup(
            Text("• Imperfect receiver filters", font_size=18),
            Text("• Transmitter spectral leakage", font_size=18),
            Text("• Non-linear power amplifiers", font_size=18),
            Text("• Insufficient guard bands", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(causes_title, DOWN, buff=0.3)
        
        # RIGHT: Key parameters
        params_title = Text("Key Parameter:", font_size=24, weight=BOLD, color=BLUE).shift(RIGHT * 2.5 + UP * 1.5)
        
        acir_formula = MathTex(
            r"\text{ACIR (dB)} = -10\log_{10}\left(\frac{P_{adj}}{P_{desired}}\right)",
            font_size=32
        ).next_to(params_title, DOWN, buff=0.4)
        
        acir_box = SurroundingRectangle(acir_formula, color=WHITE, buff=0.2, stroke_width=2)
        
        param_explain = VGroup(
            MathTex(r"P_{adj} = \text{adjacent power}", font_size=18),
            MathTex(r"P_{desired} = \text{desired power}", font_size=18),
            Text("Higher ACIR = Better isolation", font_size=16, color=YELLOW, slant=ITALIC)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(acir_formula, DOWN, buff=0.5)
        
        self.play(Write(causes_title))
        for cause in causes:
            self.play(Write(cause), run_time=0.4)
            self.wait(0.2)
        
        self.wait(0.5)
        
        self.play(Write(params_title))
        self.play(Create(acir_box), Write(acir_formula))
        self.wait(0.5)
        
        for param in param_explain:
            self.play(Write(param), run_time=0.5)
            self.wait(0.2)
        
        self.wait(2)
        
        # Clear for mitigation
        self.play(
            *[FadeOut(mob) for mob in [
                math_title, causes_title, causes, params_title,
                acir_box, acir_formula, param_explain
            ]]
        )
        self.wait(0.5)
        
        # ---------------------------------------------------------
        # SCENE 3: MITIGATION STRATEGIES
        # ---------------------------------------------------------
        
        mitigation_title = Text("Mitigation Strategies", font_size=30, color=YELLOW, weight=BOLD)
        mitigation_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(mitigation_title))
        self.wait(0.5)
        
        # Create visual comparison: Before vs After
        before_label = Text("Problem", font_size=22, color=RED).shift(LEFT * 3.5 + UP * 1.8)
        after_label = Text("Solutions", font_size=22, color=GREEN).shift(RIGHT * 2.8 + UP * 1.8)
        
        self.play(Write(before_label), Write(after_label))
        
        # Before: Overlapping channels
        before_channels = VGroup()
        for i in range(3):
            rect = Rectangle(height=1.2, width=1, color=RED, fill_opacity=0.3, stroke_width=2)
            rect.shift(LEFT * 3.5 + RIGHT * i * 0.9 + UP * 0.5)
            before_channels.add(rect)
        
        # overlap_arrows = VGroup(
        #     Arrow(before_channels[0].get_right(), before_channels[1].get_left(), color=RED, buff=0, stroke_width=2),
        #     Arrow(before_channels[1].get_right(), before_channels[2].get_left(), color=RED, buff=0, stroke_width=2)
        # )
        
        self.play(FadeIn(before_channels))
        self.wait(0.5)
        
        # After: Solutions list
        solutions = VGroup(
            Text("1. Increase guard bands", font_size=1, color=GREEN),
            Text("2. Better filter design", font_size=18, color=GREEN),
            Text("3. Tight power control", font_size=18, color=GREEN),
            Text("4. Advanced modulation", font_size=18, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(RIGHT * 2.8 + UP * 0.2)
        
        for solution in solutions:
            self.play(Write(solution), run_time=0.5)
            self.wait(0.3)
        
        self.wait(1.5)
        
        # Final comparison table
        self.play(
            *[FadeOut(mob) for mob in [
                before_label, after_label, before_channels,
                solutions, mitigation_title
            ]]
        )
        self.wait(0.5)
        
        # Summary comparison
        summary_title = Text("Co-channel vs Adjacent Channel", font_size=28, color=BLUE, weight=BOLD)
        summary_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(summary_title))
        
        comparison = Table(
            [
                ["Type", "Cause", "Mitigation"],
                ["Co-channel", "Same frequency\nreuse", "Increase N\n(cell planning)"],
                ["Adjacent", "Filter imperfection\nspectral leakage", "Guard bands\nbetter filters"]
            ],
            include_outer_lines=True,
            line_config={"stroke_width": 2}
        ).scale(0.48).shift(DOWN * 0.8)
        
        comparison.get_horizontal_lines()[0].set_color(YELLOW)
        comparison.get_horizontal_lines()[1].set_color(YELLOW)
        
        self.play(Create(comparison))
        self.wait(2)
        
        # Final note
        final_note = Text(
            "Both interference types must be managed for quality cellular systems",
            font_size=20,
            color=GOLD,
            slant=ITALIC
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(final_note))
        self.wait(3)
        
        # Fadeout
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()