from manim import *
import numpy as np

class Part2_Orthogonality(MovingCameraScene):
    def construct(self):
        # Execute all sub-sections
        self.intro_orthogonality_concept()
        self.wait(1)
        self.mathematical_foundation()
        self.wait(1)
        self.why_orthogonality_solves_interference()
        self.wait(1)
        self.three_domains_tdma()
        self.wait(1)
        self.three_domains_fdma()
        self.wait(1)
        self.three_domains_cdma()
        self.wait(1)
        self.comparison_table()
        self.wait(2)

    def intro_orthogonality_concept(self):
    
    # ============================================
    # Transition from Part 1
    # ============================================
    
        transition_text = VGroup(
            Text("The key to avoiding interference", font_size=36),
            Text("isn't just separation—", font_size=36),
            Text("it's ORTHOGONALITY", font_size=48, weight=BOLD, color=YELLOW)
        ).arrange(DOWN, buff=0.3)
        
        self.play(
            Write(transition_text[0]),
            run_time=1.5
        )
        self.play(
            Write(transition_text[1]),
            run_time=1.5
        )
        self.play(
            Write(transition_text[2]),
            Flash(transition_text[2], color=YELLOW, line_length=0.4, num_lines=16),
            run_time=2
        )
        
        self.wait(1)
        self.play(FadeOut(transition_text), run_time=0.8)
        
        # ============================================
        # "But what does that mean?" Hook
        # ============================================
        
        question = Text("But what does that actually mean?", 
                    font_size=36, color=YELLOW, slant=ITALIC)
        self.play(Write(question), run_time=2)
        self.wait(1)
        self.play(FadeOut(question), run_time=0.8)
        
        # ============================================
        # Bridge Animation: Messy → Clean
        # ============================================
        
        # Show messy overlapping signals
        messy_signals = VGroup()
        for i in range(5):
            wave = FunctionGraph(
                lambda x: 0.5 * np.sin(2 * x + i * 0.5),
                x_range=[-3, 3],
                color=random_bright_color()
            )
            wave.shift(UP * (i - 2) * 0.4)
            messy_signals.add(wave)
        
        messy_label = Text("Interfering Signals", font_size=24, color=RED)
        messy_label.next_to(messy_signals, DOWN, buff=0.5)
        
        self.play(
            LaggedStart(
                *[Create(wave) for wave in messy_signals],
                lag_ratio=0.1
            ),
            Write(messy_label),
            run_time=2
        )
        
        self.wait(0.5)
        
        # Transform to perpendicular arrows
        arrow_x = Arrow(ORIGIN, RIGHT * 2.5, color=BLUE, buff=0, stroke_width=6)
        arrow_y = Arrow(ORIGIN, UP * 2.5, color=GREEN, buff=0, stroke_width=6)
        arrows = VGroup(arrow_x, arrow_y)
        
        # Labels
        label_x = MathTex("\\vec{s}_1", font_size=36, color=BLUE)
        label_x.next_to(arrow_x, DOWN)
        
        label_y = MathTex("\\vec{s}_2", font_size=36, color=GREEN)
        label_y.next_to(arrow_y, LEFT)
        
        # Right angle symbol
        right_angle = RightAngle(arrow_x, arrow_y, length=0.3, color=YELLOW)
        
        clean_label = Text("Orthogonal = Perpendicular = Independent", 
                        font_size=24, color=GREEN)
        clean_label.to_edge(DOWN, buff=0.5)
        
        self.play(
            ReplacementTransform(messy_signals, arrows),
            FadeOut(messy_label),
            run_time=1.5
        )
        
        self.play(
            Write(label_x),
            Write(label_y),
            Create(right_angle),
            run_time=1
        )
        
        self.play(Write(clean_label), run_time=1.5)
        
        self.wait(2)
        
        # Cleanup
        self.play(
            *[FadeOut(mob) for mob in [arrows, label_x, label_y, right_angle, clean_label]],
            run_time=1
        )

    def mathematical_foundation(self):
        """
        Build orthogonality concept from geometric to signal domain
        Duration: ~120 seconds
        """
        
        # ============================================
        # Title
        # ============================================
        
        title = Text("Mathematical Foundation of Orthogonality", 
                    font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.5)
        
        # ============================================
        # Stage 1: Geometric Orthogonality (2D Vectors)
        # ============================================
        
        stage1_title = Text("Stage 1: Geometric Orthogonality", 
                        font_size=28, color=YELLOW)
        stage1_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(stage1_title), run_time=1)
        
        # Create 2D coordinate system
        axes_2d = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_tip": True, "tip_length": 0.2}
        )
        axes_2d.shift(DOWN * 0.5)
        
        # Axis labels
        x_label = MathTex("x", font_size=28).next_to(axes_2d.x_axis, RIGHT)
        y_label = MathTex("y", font_size=28).next_to(axes_2d.y_axis, RIGHT)
        
        self.play(
            Create(axes_2d),
            Write(x_label),
            Write(y_label),
            run_time=1.5
        )
        
        # Vector A along x-axis
        vec_a = Arrow(
            axes_2d.c2p(0, 0),
            axes_2d.c2p(2, 0),
            color=BLUE,
            buff=0,
            stroke_width=6
        )
        vec_a_label = MathTex("\\vec{A}", font_size=32, color=BLUE)
        vec_a_label.next_to(vec_a, DOWN)
        
        self.play(
            GrowArrow(vec_a),
            Write(vec_a_label),
            run_time=1
        )
        
        # Vector B along y-axis
        vec_b = Arrow(
            axes_2d.c2p(0, 0),
            axes_2d.c2p(0, 2),
            color=GREEN,
            buff=0,
            stroke_width=6
        )
        vec_b_label = MathTex("\\vec{B}", font_size=32, color=GREEN)
        vec_b_label.next_to(vec_b, LEFT)
        
        self.play(
            GrowArrow(vec_b),
            Write(vec_b_label),
            run_time=1
        )
        
        # Highlight 90° angle
        angle_arc = Arc(
            radius=0.5,
            start_angle=0,
            angle=PI/2,
            color=YELLOW,
            stroke_width=3
        )
        angle_arc.move_arc_center_to(axes_2d.c2p(0, 0))
        
        angle_label = MathTex("90°", font_size=24, color=YELLOW)
        angle_label.move_to(axes_2d.c2p(0.51, 0.51))
        
        self.play(
            Create(angle_arc),
            Write(angle_label),
            run_time=1
        )
        
        # Key insight
        insight1 = Text("Independent directions - no overlap!", 
                    font_size=24, color=GREEN)
        insight1.to_edge(DOWN, buff=0.5)
        self.play(Write(insight1), run_time=1.5)
        
        self.wait(1.5)
        
        # ============================================
        # Stage 2: Extend to Signals
        # ============================================
        
        self.play(
            FadeOut(stage1_title),
            FadeOut(insight1),
            run_time=0.8
        )
        
        stage2_title = Text("Stage 2: Signals as Vectors", 
                        font_size=28, color=YELLOW)
        stage2_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(stage2_title), run_time=1)
        
        # Move axes to left
        self.play(
            VGroup(axes_2d, x_label, y_label, vec_a, vec_a_label, 
                vec_b, vec_b_label, angle_arc, angle_label).animate.scale(0.7).shift(LEFT * 4.4),
            run_time=1.5
        )
        
        # Show signal representations on right
        signal_axes = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False}
        )
        signal_axes.shift(RIGHT * 2.5 + UP * 1)
        
        t_label = MathTex("t", font_size=24).next_to(signal_axes.x_axis, RIGHT)
        
        self.play(
            Create(signal_axes),
            Write(t_label),
            run_time=1
        )
        
        # Signal 1: cos(2πf₁t)
        signal_1 = signal_axes.plot(
            lambda t: np.cos(2*t),
            color=BLUE,
            stroke_width=3
        )
        signal_1_eq = MathTex("s_1(t) = \\cos(2\\pi f_1 t)", 
                            font_size=24, color=BLUE)
        signal_1_eq.next_to(signal_axes, UP, buff=0.3)
        
        self.play(
            Create(signal_1),
            Write(signal_1_eq),
            run_time=1.5
        )
        
        # Signal 2: cos(2πf₂t) with f₂ ≠ f₁
        signal_2_axes = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False}
        )
        signal_2_axes.shift(RIGHT * 2.5 + DOWN * 1.5)
        
        t_label2 = MathTex("t", font_size=24).next_to(signal_2_axes.x_axis, RIGHT)
        
        self.play(
            Create(signal_2_axes),
            Write(t_label2),
            run_time=0.8
        )
        
        signal_2 = signal_2_axes.plot(
            lambda t: np.cos(4*t),  # Different frequency
            color=GREEN,
            stroke_width=3
        )
        signal_2_eq = MathTex("s_2(t) = \\cos(2\\pi f_2 t), \\ f_2 \\neq f_1", 
                            font_size=24, color=GREEN)
        signal_2_eq.next_to(signal_1_eq, RIGHT, buff=0.3)
        
        self.play(
            Create(signal_2),
            Write(signal_2_eq),
            run_time=1.5
        )
        
        # Arrow showing correspondence
        correspondence = Text("Signals → Vectors", font_size=20, color=YELLOW)
        correspondence.move_to(ORIGIN + DOWN * 0.5)
        arrow_corr = Arrow(LEFT * 1.5, RIGHT * 0.5, color=YELLOW)
        arrow_corr.next_to(correspondence, DOWN, buff=0.2)
        
        self.play(
            Write(correspondence),
            GrowArrow(arrow_corr),
            run_time=1
        )
        
        insight2 = Text("Different frequencies = Independent signals!", 
                    font_size=22, color=GREEN, weight=BOLD)
        insight2.to_edge(DOWN, buff=0.3)
        self.play(Write(insight2), run_time=1.5)
        
        self.wait(2)
        
        # Clear for Stage 3
        self.play(
            *[FadeOut(mob) for mob in [
                axes_2d, x_label, y_label, vec_a, vec_a_label,
                vec_b, vec_b_label, angle_arc, angle_label,
                signal_axes, t_label, signal_1, signal_1_eq,
                signal_2_axes, t_label2, signal_2, signal_2_eq,
                correspondence, arrow_corr, insight2, stage2_title
            ]],
            run_time=1
        )
        
        # ============================================
        # Stage 3: Mathematical Definition
        # ============================================
        
        stage3_title = Text("Stage 3: Mathematical Definition", 
                        font_size=28, color=YELLOW)
        stage3_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(stage3_title), run_time=1)
        
        # Inner product definition
        definition_title = Text("Inner Product (Correlation)", 
                            font_size=24, color=ORANGE)
        definition_title.move_to(UP * 1.5)
        self.play(Write(definition_title), run_time=1)
        
        # Inner product formula
        inner_product = MathTex(
            "\\langle s_1, s_2 \\rangle = \\int_{0}^{T} s_1(t) \\cdot s_2(t) \\, dt",
            font_size=36
        )
        inner_product.move_to(UP * 0.5)
        
        self.play(Write(inner_product), run_time=2)
        
        # Orthogonality condition
        orth_condition = MathTex(
            "\\text{Orthogonal if: } \\langle s_1, s_2 \\rangle = 0",
            font_size=36,
            color=GREEN
        )
        orth_condition.next_to(inner_product, DOWN, buff=0.8)
        
        orth_box = SurroundingRectangle(orth_condition, color=GREEN, buff=0.2)
        
        self.play(
            Write(orth_condition),
            Create(orth_box),
            run_time=2
        )
        
        self.wait(1)
        
        # Visual demonstration of integral
        # demo_text = Text("Visual Demonstration:", font_size=24)
        # demo_text.move_to(DOWN * 1.2)
        # self.play(Write(demo_text), run_time=1)
        
        # Small axes for demonstration
        demo_axes = Axes(
            x_range=[0, 2*PI, PI],
            y_range=[-1.2, 1.2, 1],
            x_length=4,
            y_length=2,
            axis_config={"include_tip": False}
        )
        demo_axes.move_to(DOWN * 2.5)
        
        # Two orthogonal signals
        sig1 = demo_axes.plot(lambda t: np.cos(2*t), color=BLUE, stroke_width=2)
        sig2 = demo_axes.plot(lambda t: np.cos(4*t), color=RED, stroke_width=2)
        
        # Product (will average to zero)
        product = demo_axes.plot(
            lambda t: np.cos(2*t) * np.cos(4*t),
            color=PURPLE,
            stroke_width=3
        )
        
        self.play(
            Create(demo_axes),
            Create(sig1),
            Create(sig2),
            run_time=1.5
        )
        
        product_label = MathTex("s_1(t) \\cdot s_2(t)", font_size=20, color=PURPLE)
        product_label.next_to(demo_axes, DOWN, buff=0.2)
        
        self.play(
            ReplacementTransform(VGroup(sig1.copy(), sig2.copy()), product),
            Write(product_label),
            run_time=1.5
        )
        
        # Show area cancellation
        area_positive = demo_axes.get_area(
            product,
            x_range=[0, PI/2],
            color=GREEN,
            opacity=0.5
        )
        area_negative = demo_axes.get_area(
            product,
            x_range=[PI/2, PI],
            color=RED,
            opacity=0.5
        )
        
        self.play(
            FadeIn(area_positive),
            FadeIn(area_negative),
            run_time=1
        )
        self.wait(2)
        self.play(
            FadeOut(sig1),
            FadeOut(sig2),
            run_time=0.5
        )
        
        cancel_text = Text("Positive and negative areas cancel!", 
                        font_size=18, color=YELLOW)
        cancel_text.next_to(product_label, DOWN, buff=0.3)
        
        integral_result = MathTex("\\int = 0", font_size=24, color=GREEN)
        integral_result.next_to(cancel_text, DOWN, buff=0.2)
        
        self.play(
            Write(cancel_text),
            Write(integral_result),
            run_time=1.5
        )
        
        self.wait(2)
        
        # ============================================
        # Key Intuition Box
        # ============================================
        
        self.play(
            *[FadeOut(mob) for mob in [
                stage3_title, definition_title, inner_product,
                orth_condition, orth_box, demo_axes, product, product_label,
                area_positive, area_negative, cancel_text, integral_result
            ]],
            run_time=1
        )
        
        # Final key message
        key_box_bg = Rectangle(
            width=11,
            height=3,
            stroke_color=YELLOW,
            stroke_width=3
        )
        key_box_bg.move_to(ORIGIN)
        
        key_title = Text("KEY INSIGHT", font_size=32, weight=BOLD, color=YELLOW)
        key_title.move_to(UP * 0.8)
        
        key_message = VGroup(
            Text("Orthogonal Signals =", font_size=28),
            Text('"Can exist simultaneously without', font_size=24, slant=ITALIC),
            Text('interfering with each other"', font_size=24, slant=ITALIC),
        ).arrange(DOWN, buff=0.2)
        key_message.move_to(DOWN * 0.3)
        
        # analogy = Text("Like having separate lanes on a highway", 
        #             font_size=20, color=GREEN)
        # analogy.next_to(key_message, DOWN, buff=0.5)
        
        self.play(FadeIn(key_box_bg), run_time=0.5)
        self.play(
            Write(key_title),
            run_time=1
        )
        self.play(
            Write(key_message),
            run_time=2
        )
        # self.play(Write(analogy), run_time=1)
        
        self.wait(3)
        
        # Cleanup
        self.play(
            *[FadeOut(mob) for mob in [
                title, key_box_bg, key_title, key_message
            ]],
            run_time=1
        )


    def why_orthogonality_solves_interference(self):
        """
        Visual proof showing orthogonal vs non-orthogonal signals
        Duration: ~120 seconds
        """
        
        # ============================================
        # Title
        # ============================================
        
        title = Text("Why Orthogonality Solves Interference", 
                    font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.5)
        
        # ============================================
        # Create Split Screen
        # ============================================
        
        divider = Line(UP * 3, DOWN * 3.5, stroke_width=3, color=WHITE)
        self.play(Create(divider), run_time=0.8)
        
        # Labels
        non_orth_label = Text("NON-ORTHOGONAL", font_size=24, color=RED, weight=BOLD)
        non_orth_label.move_to(LEFT * 3.5 + UP * 2.5)
        
        orth_label = Text("ORTHOGONAL", font_size=24, color=GREEN, weight=BOLD)
        orth_label.move_to(RIGHT * 3.5 + UP * 2.5)
        
        self.play(
            Write(non_orth_label),
            Write(orth_label),
            run_time=1
        )
        
        # Subtitle
        subtitle = Text("(Interference)", font_size=18, color=RED)
        subtitle.next_to(non_orth_label, DOWN, buff=0.1)
        
        subtitle2 = Text("(No Interference)", font_size=18, color=GREEN)
        subtitle2.next_to(orth_label, DOWN, buff=0.1)
        
        self.play(
            Write(subtitle),
            Write(subtitle2),
            run_time=0.8
        )
        
        # ============================================
        # LEFT SIDE: Non-Orthogonal (Interference)
        # ============================================
        
        # Signal parameters
        left_info = VGroup(
            MathTex("f_1 = 2.40 \\text{ GHz}", font_size=20),
            MathTex("f_2 = 2.401 \\text{ GHz}", font_size=20),
            Text("(Too close!)", font_size=16, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        left_info.move_to(LEFT * 3.5 + UP * 1.5)
        
        self.play(Write(left_info), run_time=1.5)
        
        # Plot signals
        left_axes = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=3.5,
            y_length=2,
            axis_config={"include_tip": False, "font_size": 16}
        )
        left_axes.move_to(LEFT * 3.5 + UP * 0.2)
        
        left_sig1 = left_axes.plot(lambda t: np.cos(2*t), color=BLUE, stroke_width=2)
        left_sig2 = left_axes.plot(lambda t: np.cos(2.1*t), color=RED, stroke_width=2)
        
        self.play(
            Create(left_axes),
            Create(left_sig1),
            Create(left_sig2),
            run_time=1.5
        )
        
        # Inner product calculation
        inner_prod_left = MathTex(
            "\\langle s_1, s_2 \\rangle \\neq 0",
            font_size=24,
            color=RED
        )
        inner_prod_left.next_to(left_axes, DOWN, buff=0.3)
        self.play(Write(inner_prod_left), run_time=1)
        
        # Received signal (messy)
        left_rx_label = Text("At Receiver:", font_size=18)
        left_rx_label.move_to(LEFT * 3.5 + DOWN * 1.3)
        
        left_rx_axes = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-2, 2, 1],
            x_length=3.5,
            y_length=1.8,
            axis_config={"include_tip": False, "font_size": 16}
        )
        left_rx_axes.move_to(LEFT * 3.5 + DOWN * 2.3)
        
        # Combined signal (interference)
        left_combined = left_rx_axes.plot(
            lambda t: np.cos(2*t) + np.cos(2.1*t),
            color=PURPLE,
            stroke_width=3
        )
        
        self.play(
            Write(left_rx_label),
            Create(left_rx_axes),
            run_time=1
        )
        self.play(Create(left_combined), run_time=1.5)
        
        # Constellation diagram (blurred)
        left_constellation = self._create_constellation_qpsk(
            noise_level=0.7,
            color=RED,
            scale_factor=0.5
        )
        left_constellation.move_to(LEFT * 3.5 + DOWN * 3.5)
        
        left_const_label = Text("Constellation", font_size=14, color=RED)
        left_const_label.next_to(left_constellation, DOWN, buff=0.1)
        
        self.play(
            FadeIn(left_constellation, scale=0.8),
            Write(left_const_label),
            run_time=1
        )
        
        # Result
        left_result = Text("✗ Cannot decode reliably", font_size=18, color=RED, weight=BOLD)
        left_result.next_to(left_const_label, DOWN, buff=0.2)
        self.play(Write(left_result), run_time=1)
        
        # ============================================
        # RIGHT SIDE: Orthogonal (No Interference)
        # ============================================
        
        # Signal parameters
        right_info = VGroup(
            MathTex("f_1 = 2.40 \\text{ GHz}", font_size=20),
            MathTex("f_2 = 2.50 \\text{ GHz}", font_size=20),
            Text("(Well separated!)", font_size=16, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        right_info.move_to(RIGHT * 3.5 + UP * 1.5)
        
        self.play(Write(right_info), run_time=1.5)
        
        # Plot signals
        right_axes = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=3.5,
            y_length=2,
            axis_config={"include_tip": False, "font_size": 16}
        )
        right_axes.move_to(RIGHT * 3.5 + UP * 0.2)
        
        right_sig1 = right_axes.plot(lambda t: np.cos(2*t), color=BLUE, stroke_width=2)
        right_sig2 = right_axes.plot(lambda t: np.cos(5*t), color=GREEN, stroke_width=2)
        
        self.play(
            Create(right_axes),
            Create(right_sig1),
            Create(right_sig2),
            run_time=1.5
        )
        
        # Inner product calculation
        inner_prod_right = MathTex(
            "\\langle s_1, s_2 \\rangle = 0",
            font_size=24,
            color=GREEN
        )
        inner_prod_right.next_to(right_axes, DOWN, buff=0.3)
        
        check_mark = Text("✓", font_size=32, color=GREEN, weight=BOLD)
        check_mark.next_to(inner_prod_right, RIGHT, buff=0.2)
        
        self.play(
            Write(inner_prod_right),
            Write(check_mark),
            run_time=1
        )
        
        # Receiver processing
        right_rx_label = Text("At Receiver:", font_size=18)
        right_rx_label.move_to(RIGHT * 3.5 + DOWN * 1.3)
        
        # Show separation process
        separation_text = VGroup(
            Text("Correlate with", font_size=14),
            MathTex("s_1(t):", font_size=16, color=BLUE),
            Text("Extract Signal 1 ✓", font_size=14, color=BLUE)
        ).arrange(RIGHT, buff=0.1)
        separation_text.move_to(RIGHT * 3.5 + DOWN * 2)
        
        separation_text2 = VGroup(
            Text("Correlate with", font_size=14),
            MathTex("s_2(t):", font_size=16, color=GREEN),
            Text("Extract Signal 2 ✓", font_size=14, color=GREEN)
        ).arrange(RIGHT, buff=0.1)
        separation_text2.next_to(separation_text, DOWN, buff=0.2, aligned_edge=LEFT)
        
        self.play(
            Write(right_rx_label),
            run_time=0.8
        )
        self.play(
            Write(separation_text),
            run_time=1.2
        )
        self.play(
            Write(separation_text2),
            run_time=1.2
        )
        
        # Constellation diagram (clean)
        right_constellation = self._create_constellation_qpsk(
            noise_level=0.1,
            color=GREEN,
            scale_factor=0.5
        )
        right_constellation.move_to(RIGHT * 3.5 + DOWN * 3.5)
        
        right_const_label = Text("Constellation", font_size=14, color=GREEN)
        right_const_label.next_to(right_constellation, DOWN, buff=0.1)
        
        self.play(
            FadeIn(right_constellation, scale=0.8),
            Write(right_const_label),
            run_time=1
        )
        
        # Result
        right_result = Text("✓ Perfect decoding", font_size=18, color=GREEN, weight=BOLD)
        right_result.next_to(right_const_label, DOWN, buff=0.2)
        self.play(Write(right_result), run_time=1)
        
        self.wait(3)
        
        # Cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1
        )

    def three_domains_tdma(self):
        """
        TDMA: Time Division Multiple Access
        Duration: ~90 seconds
        """
        
        # ============================================
        # Title
        # ============================================
        
        title = Text("The Three Domains of Orthogonality", 
                    font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        
        subtitle = Text("Think of them as three different dimensions we can exploit", 
                    font_size=22, slant=ITALIC, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.2)
        
        self.play(
            Write(title),
            Write(subtitle),
            run_time=2
        )
        self.wait(1)
        
        self.play(FadeOut(subtitle), run_time=0.5)
        
        # ============================================
        # TDMA Section
        # ============================================
        
        tdma_title = Text("1. TIME Domain (TDMA)", font_size=32, color=BLUE, weight=BOLD)
        tdma_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(tdma_title), run_time=1)
        
        # Timeline
        timeline_length = 10
        timeline = Line(LEFT * timeline_length/2, RIGHT * timeline_length/2, stroke_width=4)
        timeline.move_to(UP * 1.5)
        
        # Time labels
        t0 = MathTex("0", font_size=20).next_to(timeline.get_start(), DOWN, buff=0.2)
        tT = MathTex("T", font_size=20).next_to(timeline.get_end(), DOWN, buff=0.2)
        
        self.play(
            Create(timeline),
            Write(t0),
            Write(tT),
            run_time=1
        )
        
        # Divide into 4 slots
        slot_width = timeline_length / 4
        slots = VGroup()
        slot_labels = VGroup()
        user_colors = [BLUE, RED, GREEN, ORANGE]
        
        for i in range(4):
            slot = Rectangle(
                width=slot_width,
                height=0.8,
                stroke_width=3,
                stroke_color=user_colors[i],
                fill_color=user_colors[i],
                fill_opacity=0
            )
            slot.move_to(timeline.get_start() + RIGHT * (i * slot_width + slot_width/2) + UP * 1.5)
            slots.add(slot)
            
            label = Text(f"Slot {i+1}", font_size=16, color=user_colors[i])
            label.move_to(slot.get_center())
            slot_labels.add(label)
        
        self.play(
            *[Create(slot) for slot in slots],
            *[Write(label) for label in slot_labels],
            run_time=2
        )
        
        # Show users
        user_labels = VGroup()
        for i in range(4):
            user = Text(f"User {i+1}", font_size=18, color=user_colors[i], weight=BOLD)
            user.next_to(slots[i], DOWN, buff=0.5)
            user_labels.add(user)
        
        self.play(*[Write(user) for user in user_labels], run_time=1)
        
        # Animation: Users take turns
        for i in range(4):
            # Highlight current slot
            self.play(
                slots[i].animate.set_fill(opacity=0.6),
                run_time=0.5
            )
            
            # Show transmission
            wave = self._create_signal_wave(user_colors[i], slots[i].get_center() + DOWN * 1.5)
            tx_label = Text("Transmitting", font_size=14, color=user_colors[i])
            tx_label.next_to(wave, DOWN, buff=0.1)
            
            self.play(
                Create(wave),
                Write(tx_label),
                run_time=0.4
            )
            
            self.wait(0.3)
            
            self.play(
                FadeOut(wave),
                FadeOut(tx_label),
                slots[i].animate.set_fill(opacity=0),
                run_time=0.3
            )
        
        # Orthogonality proof
        proof_box = Rectangle(
            width=6,
            height=2,
            stroke_color=GREEN,
            stroke_width=3,
            fill_color=DARK_GRAY,
            fill_opacity=0.8
        )
        proof_box.move_to(DOWN * 2)
        
        proof_title = Text("Orthogonality Proof:", font_size=18, color=YELLOW)
        proof_title.move_to(proof_box.get_top() + DOWN * 0.3)
        
        proof_lines = VGroup(
            MathTex("s_1(t) \\text{ active during } [0, T/4]", font_size=16),
            MathTex("s_2(t) \\text{ active during } [T/4, T/2]", font_size=16),
            Text("No time overlap!", font_size=16, color=GREEN),
            MathTex("\\int s_1(t) \\cdot s_2(t) dt = 0 \\;\\checkmark", font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        proof_lines.move_to(proof_box.get_center() + DOWN * 0.2)
        
        self.play(
            FadeIn(proof_box),
            Write(proof_title),
            run_time=0.8
        )
        self.play(
            Write(proof_lines),
            run_time=2
        )
        
        self.wait(1)
        
        # Pros/Cons
        pros_cons = VGroup(
            Text("✓ Simple to implement", font_size=16, color=GREEN),
            Text("✓ No frequency planning needed", font_size=16, color=GREEN),
            Text("✗ Delay (must wait for your slot)", font_size=16, color=RED),
            Text("✗ Inefficient for bursty traffic", font_size=16, color=RED),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        pros_cons.to_corner(DR, buff=0.5)
        
        self.play(
            LaggedStart(*[Write(line) for line in pros_cons], lag_ratio=0.3),
            run_time=2
        )
        
        self.wait(2)
        
        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)

    def three_domains_fdma(self):
        """
        FDMA: Frequency Division Multiple Access
        Duration: ~90 seconds
        """
        
        # ============================================
        # Title
        # ============================================
        
        title = Text("The Three Domains of Orthogonality", 
                    font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1)
        
        fdma_title = Text("2. FREQUENCY Domain (FDMA)", font_size=32, color=RED, weight=BOLD)
        fdma_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(fdma_title), run_time=1)
        
        # Frequency axis (vertical)
        freq_axis = Line(DOWN * 3, UP * 3, stroke_width=4)
        freq_axis.move_to(LEFT * 4)
        
        freq_label = Text("Frequency (Hz)", font_size=20).rotate(PI/2)
        freq_label.next_to(freq_axis, LEFT, buff=0.3)
        
        f0 = MathTex("0", font_size=18).next_to(freq_axis.get_bottom(), LEFT, buff=0.2)
        fB = MathTex("B", font_size=18).next_to(freq_axis.get_top(), LEFT, buff=0.2)
        
        self.play(
            Create(freq_axis),
            Write(freq_label),
            Write(f0),
            Write(fB),
            run_time=1.5
        )
        
        # Divide into 4 frequency bands
        band_height = 6 / 4
        bands = VGroup()
        user_colors = [BLUE, RED, GREEN, ORANGE]
        
        for i in range(4):
            band = Rectangle(
                width=2,
                height=band_height,
                stroke_width=3,
                stroke_color=user_colors[i],
                fill_color=user_colors[i],
                fill_opacity=0.4
            )
            band.move_to(freq_axis.get_bottom() + UP * (i * band_height + band_height/2) + RIGHT * 1)
            bands.add(band)
            
            # Band label
            band_label = Text(f"Band {i+1}", font_size=14, color=user_colors[i])
            band_label.move_to(band.get_left() + RIGHT * 0.5)
            bands.add(band_label)
            
            # User label
            user_label = Text(f"User {i+1}", font_size=16, color=user_colors[i], weight=BOLD)
            user_label.next_to(band, RIGHT, buff=0.3)
            bands.add(user_label)
        
        self.play(
            LaggedStart(*[Create(band) for band in bands[::3]], lag_ratio=0.2),
            run_time=2
        )
        self.play(
            *[Write(label) for label in bands[1::3] + bands[2::3]],
            run_time=1
        )
        
        # Show frequencies
        freq_values = VGroup(
            MathTex("f_1 = 2.40 \\text{ GHz}", font_size=16, color=BLUE),
            MathTex("f_2 = 2.42 \\text{ GHz}", font_size=16, color=RED),
            MathTex("f_3 = 2.44 \\text{ GHz}", font_size=16, color=GREEN),
            MathTex("f_4 = 2.46 \\text{ GHz}", font_size=16, color=ORANGE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        freq_values.move_to(RIGHT * 4 + UP * 2)
        
        simultaneous_label = Text("All users transmit SIMULTANEOUSLY", 
                                font_size=18, color=YELLOW, weight=BOLD)
        simultaneous_label.next_to(freq_values, DOWN, buff=0.4)
        
        self.play(
            Write(freq_values),
            run_time=1.5
        )
        self.play(
            Write(simultaneous_label),
            run_time=1
        )
        
        # Show signals at different frequencies
        signal_group = VGroup()
        for i in range(4):
            axes = Axes(
                x_range=[0, 2*PI, PI],
                y_range=[-1, 1],
                x_length=2,
                y_length=0.8,
                axis_config={"include_tip": False}
            )
            axes.move_to(RIGHT * 4 + UP * (1 - i * 0.8))
            
            signal = axes.plot(
                lambda t, freq=(i+1)*2: np.cos(freq*t),
                color=user_colors[i],
                stroke_width=2
            )
            
            signal_group.add(VGroup(axes, signal))
        
        self.play(
            LaggedStart(*[Create(sg) for sg in signal_group], lag_ratio=0.2),
            run_time=2
        )
        
        # Receiver filters
        filter_text = Text("At Receiver: Apply bandpass filters", 
                        font_size=18, color=YELLOW)
        filter_text.move_to(DOWN * 1.5)
        
        self.play(Write(filter_text), run_time=1)
        
        filter_details = VGroup(
            Text("Filter 1 extracts f₁ → User 1's signal", font_size=14, color=BLUE),
            Text("Filter 2 extracts f₂ → User 2's signal", font_size=14, color=RED),
            Text("Filter 3 extracts f₃ → User 3's signal", font_size=14, color=GREEN),
            Text("Filter 4 extracts f₄ → User 4's signal", font_size=14, color=ORANGE),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        filter_details.next_to(filter_text, DOWN, buff=0.3)
        
        self.play(
            LaggedStart(*[Write(line) for line in filter_details], lag_ratio=0.3),
            run_time=2
        )
        
        # Orthogonality proof
        proof = VGroup(
            Text("Orthogonality Proof:", font_size=16, color=YELLOW, weight=BOLD),
            MathTex("\\text{If } f_1 \\neq f_2", font_size=16),
            MathTex("\\text{then } \\int \\cos(2\\pi f_1 t) \\cdot \\cos(2\\pi f_2 t) dt = 0", font_size=14),
            MathTex("\\text{Frequency separation ensures orthogonality } \\checkmark", 
                    font_size=14, color=GREEN)
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        proof.to_corner(DL, buff=0.5)
        
        proof_box = SurroundingRectangle(proof, color=GREEN, buff=0.2)
        
        self.play(
            Create(proof_box),
            Write(proof),
            run_time=2
        )
        
        # Pros/Cons
        pros_cons = VGroup(
            Text("✓ No delay - all transmit simultaneously", font_size=14, color=GREEN),
            Text("✓ Good for continuous traffic (voice)", font_size=14, color=GREEN),
            Text("✗ Requires frequency planning", font_size=14, color=RED),
            Text("✗ Guard bands needed (spectrum waste)", font_size=14, color=RED),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        pros_cons.to_corner(DR, buff=0.5)
        
        self.play(
            LaggedStart(*[Write(line) for line in pros_cons], lag_ratio=0.3),
            run_time=2
        )
        
        self.wait(2)
        
        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)

    def three_domains_cdma(self):
        """
        CDMA: Code Division Multiple Access
        Duration: ~120 seconds
        """
        
        # ============================================
        # Title
        # ============================================
        
        title = Text("The Three Domains of Orthogonality", 
                    font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1)
        
        cdma_title = Text("3. CODE Domain (CDMA)", font_size=32, color=PURPLE, weight=BOLD)
        cdma_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(cdma_title), run_time=1)
        
        special_note = Text("All transmit at SAME time + SAME frequency!", 
                        font_size=22, color=YELLOW, slant=ITALIC)
        special_note.next_to(cdma_title, DOWN, buff=0.3)
        self.play(Write(special_note), run_time=1.5)
        
        self.wait(0.5)
        self.play(FadeOut(special_note), run_time=0.5)
        
        # Walsh codes
        codes_title = Text("Assign Orthogonal Codes (Walsh Codes):", 
                        font_size=20, color=YELLOW)
        codes_title.move_to(UP * 1.8)
        self.play(Write(codes_title), run_time=1)
        
        user_colors = [BLUE, RED, GREEN, ORANGE]
        
        codes = VGroup(
            MathTex("\\text{User 1: } C_1 = [+1, +1, +1, +1]", font_size=20, color=BLUE),
            MathTex("\\text{User 2: } C_2 = [+1, -1, +1, -1]", font_size=20, color=RED),
            MathTex("\\text{User 3: } C_3 = [+1, +1, -1, -1]", font_size=20, color=GREEN),
            MathTex("\\text{User 4: } C_4 = [+1, -1, -1, +1]", font_size=20, color=ORANGE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        codes.next_to(codes_title, DOWN, buff=0.3)
        
        self.play(
            LaggedStart(*[Write(code) for code in codes], lag_ratio=0.3),
            run_time=2
        )
        
        # Show orthogonality check
        orth_check_title = Text("Orthogonality Check:", font_size=18, color=YELLOW)
        orth_check_title.move_to(DOWN * 0.2)
        
        orth_check = VGroup(
            MathTex("C_1 \\cdot C_2 = (+1)(+1) + (+1)(-1) + (+1)(+1) + (+1)(-1)", font_size=14),
            MathTex("= 1 - 1 + 1 - 1 = 0 \\; \\checkmark", font_size=14, color=GREEN),
            MathTex("C_1 \\cdot C_3 = 0 \\; \\checkmark, \\quad C_1 \\cdot C_4 = 0 \\; \\checkmark", 
                    font_size=14, color=GREEN),
            Text("All pairs orthogonal!", font_size=16, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        orth_check.next_to(orth_check_title, DOWN, buff=0.2)
        
        self.play(Write(orth_check_title), run_time=0.8)
        self.play(
            Write(orth_check[0]),
            run_time=1.5
        )
        self.play(
            Write(orth_check[1]),
            run_time=1
        )
        self.play(
            Write(orth_check[2]),
            Write(orth_check[3]),
            run_time=1.5
        )
        
        self.wait(1)
        
        # Clear for transmission example
        self.play(
            FadeOut(codes_title),
            FadeOut(codes),
            FadeOut(orth_check_title),
            FadeOut(orth_check),
            run_time=0.8
        )
        
        # Transmission example
        tx_title = Text("Transmission Example:", font_size=22, color=YELLOW)
        tx_title.move_to(UP * 1.5)
        self.play(Write(tx_title), run_time=0.8)
        
        tx_example = VGroup(
            Text("User 1 data bit: 1", font_size=16, color=BLUE),
            MathTex("\\rightarrow \\text{ Spread with } C_1 \\rightarrow [+1, +1, +1, +1]", 
                    font_size=16, color=BLUE),
            Text("User 2 data bit: 0", font_size=16, color=RED),
            MathTex("\\rightarrow \\text{ Spread with } C_2 \\rightarrow [-1, +1, -1, +1]", 
                    font_size=16, color=RED),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        tx_example.next_to(tx_title, DOWN, buff=0.3)
        
        self.play(
            LaggedStart(*[Write(line) for line in tx_example], lag_ratio=0.4),
            run_time=3
        )
        
        all_tx = Text("All transmit simultaneously on same frequency!", 
                    font_size=16, color=YELLOW, weight=BOLD)
        all_tx.next_to(tx_example, DOWN, buff=0.4)
        self.play(Write(all_tx), run_time=1)
        
        self.wait(1)
        
        # Receiver processing
        rx_title = Text("At Receiver (wants User 1's data):", font_size=20, color=YELLOW)
        rx_title.move_to(DOWN * 0.5)
        
        self.play(
            FadeOut(tx_example),
            FadeOut(all_tx),
            rx_title.animate.move_to(UP * 0.8),
            run_time=0.8
        )
        
        rx_process = VGroup(
            Text("Received signal = Σ (all spread signals) + noise", font_size=14),
            Text("Correlate with C₁:", font_size=14, color=BLUE, weight=BOLD),
            Text("  • User 1 component: High correlation ✓", font_size=13, color=BLUE),
            Text("  • User 2 component: Zero correlation (orthogonal)", font_size=13, color=RED),
            Text("  • User 3 component: Zero correlation (orthogonal)", font_size=13, color=GREEN),
            Text("  • User 4 component: Zero correlation (orthogonal)", font_size=13, color=ORANGE),
            Text("Extract User 1's bit!", font_size=16, color=GREEN, weight=BOLD),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        rx_process.next_to(rx_title, DOWN, buff=0.3)
        
        self.play(
            LaggedStart(*[Write(line) for line in rx_process], lag_ratio=0.4),
            run_time=4
        )
        
        self.wait(1.5)
        
        # Pros/Cons
        self.play(
            FadeOut(tx_title),
            FadeOut(rx_title),
            FadeOut(rx_process),
            run_time=0.8
        )
        
        pros_cons_title = Text("Advantages & Disadvantages:", font_size=20, color=YELLOW)
        pros_cons_title.move_to(UP * 1.5)
        
        pros_cons = VGroup(
            Text("✓ Maximum flexibility (same time + frequency)", font_size=15, color=GREEN),
            Text("✓ Robust to interference", font_size=15, color=GREEN),
            Text("✓ Security (spread spectrum)", font_size=15, color=GREEN),
            Text("✗ Complex receiver processing", font_size=15, color=RED),
            Text("✗ Power control critical (near-far problem)", font_size=15, color=RED),
            Text("✗ Limited number of orthogonal codes", font_size=15, color=RED),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        pros_cons.next_to(pros_cons_title, DOWN, buff=0.4)
        
        self.play(Write(pros_cons_title), run_time=0.8)
        self.play(
            LaggedStart(*[Write(line) for line in pros_cons], lag_ratio=0.3),
            run_time=3
        )
        
        self.wait(2)
        
        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)

    def comparison_table(self):
        """
        Comparison table of TDMA, FDMA, CDMA
        Duration: ~60 seconds
        """
        
        # Title
        title = Text("Summary: Comparison of Multiple Access Schemes", 
                    font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.5)
        
        # Create table
        table_data = [
            ["", "TDMA", "FDMA", "CDMA"],
            ["Resource", "TIME", "FREQUENCY", "CODE"],
            ["Users transmit", "Sequential\n(take turns)", "Simultaneous\n(diff freq)", "Simultaneous\n(diff codes)"],
            ["Delay", "High", "Low", "Low"],
            ["Complexity", "Low", "Medium", "High"],
            ["Real-world\nexample", "GSM (old)", "FM Radio,\nAnalog TV", "CDMA phones\n(3G)"],
        ]
        
        # Colors
        header_color = YELLOW
        tdma_color = BLUE
        fdma_color = RED
        cdma_color = PURPLE
        
        # Create table structure
        table = VGroup()
        
        # Calculate dimensions
        col_widths = [2.5, 2.5, 2.5, 2.5]
        row_height = 0.8
        
        for i, row in enumerate(table_data):
            row_group = VGroup()
            for j, cell_text in enumerate(row):
                # Create cell
                cell = Rectangle(
                    width=col_widths[j],
                    height=row_height if i == 0 else row_height * 1.2,
                    stroke_width=2,
                    stroke_color=WHITE
                )
                
                # Fill header row
                if i == 0:
                    cell.set_fill(DARK_GRAY, opacity=0.8)
                
                # Cell text
                if i == 0 and j == 0:
                    text = Text("")
                else:
                    text = Text(cell_text, font_size=14 if i > 0 else 16, 
                            weight=BOLD if i == 0 else NORMAL)
                    
                    # Color coding
                    if i == 0:
                        if j == 1:
                            text.set_color(tdma_color)
                        elif j == 2:
                            text.set_color(fdma_color)
                        elif j == 3:
                            text.set_color(cdma_color)
                    elif j == 1:
                        text.set_color(tdma_color)
                    elif j == 2:
                        text.set_color(fdma_color)
                    elif j == 3:
                        text.set_color(cdma_color)
                    
                    text.move_to(cell.get_center())
                
                cell_group = VGroup(cell, text)
                row_group.add(cell_group)
            
            row_group.arrange(RIGHT, buff=0)
            table.add(row_group)
        
        table.arrange(DOWN, buff=0)
        table.move_to(ORIGIN + DOWN * 0.5)
        
        # Animate table creation
        self.play(
            LaggedStart(*[Create(row[0][0]) for row in table], lag_ratio=0.1),
            run_time=2
        )
        
        self.play(
            LaggedStart(*[Write(row[0][1]) for row in table if row[0][1].text != ""], lag_ratio=0.1),
            run_time=2
        )
        
        self.play(
            LaggedStart(
                *[Write(cell[1]) for row in table for cell in row[1:]],
                lag_ratio=0.05
            ),
            run_time=3
        )
        
        # Key insight
        insight = Text("Each method exploits a different dimension to achieve orthogonality!", 
                    font_size=18, color=GREEN, slant=ITALIC)
        insight.to_edge(DOWN, buff=0.5)
        
        self.play(Write(insight), run_time=2)
        
        self.wait(3)
        
        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)

    # Helper methods
    def _create_constellation_qpsk(self, noise_level=0.1, color=BLUE, scale_factor=1.0):
        """Create QPSK constellation diagram with noise"""
        constellation = VGroup()
        
        # Axes
        axes = Axes(
            x_range=[-1.5, 1.5],
            y_range=[-1.5, 1.5],
            x_length=2 * scale_factor,
            y_length=2 * scale_factor,
            axis_config={"include_tip": False, "stroke_width": 1}
        )
        constellation.add(axes)
        
        # Ideal points
        ideal_points = [
            (1, 1), (-1, 1), (-1, -1), (1, -1)
        ]
        
        # Add noisy points
        for ideal_x, ideal_y in ideal_points:
            for _ in range(8):
                x = ideal_x + np.random.normal(0, noise_level)
                y = ideal_y + np.random.normal(0, noise_level)
                point = Dot(axes.c2p(x, y), radius=0.03 * scale_factor, color=color)
                constellation.add(point)
        
        return constellation

    def _create_signal_wave(self, color, position):
        """Create a simple signal wave"""
        wave = FunctionGraph(
            lambda x: 0.3 * np.sin(4 * x),
            x_range=[-1, 1],
            color=color,
            stroke_width=3
        )
        wave.move_to(position)
        return wave