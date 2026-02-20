from manim import *
import numpy as np

class Part1_Interference(MovingCameraScene):
    def construct(self):
        # Execute all sub-sections
        self.signal_collision_concept()
        self.wait(1)
        self.sinr_quantification()
        self.wait(1)
        self.types_of_interference()
        self.wait(1)
        # self.fundamental_tradeoff()
        # self.wait(2)
    

    def signal_collision_concept(self):
    
        # ============================================
        # Title Card
        # ============================================
        title = Text("Understanding Interference", font_size=48, weight=BOLD)
        subtitle = Text("Signal Collision at the Receiver", font_size=28, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.4)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP*0.3), run_time=1)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.8)
        
        # ============================================
        # Setup: Two Phones and Base Station
        # ============================================
        
        # Base station in center
        tower = self._create_simple_tower().scale(0.8)
        tower.move_to(ORIGIN)
        
        # Phone A on left
        phone_a = self._create_simple_phone(BLUE)
        phone_a.move_to(LEFT * 5 + UP * 1.5)
        label_a = Text("Phone A", font_size=20, color=BLUE)
        label_a.next_to(phone_a, UP, buff=0.2)
        
        # Phone B on right
        phone_b = self._create_simple_phone(RED)
        phone_b.move_to(RIGHT * 5 + DOWN * 1.5)
        label_b = Text("Phone B", font_size=20, color=RED)
        label_b.next_to(phone_b, UP, buff=0.2)
        
        # Tower label
        tower_label = Text("Base Station", font_size=20, color=WHITE)
        tower_label.next_to(tower, DOWN, buff=0.3)
        
        self.play(
            LaggedStart(
                FadeIn(phone_a, shift=RIGHT*0.5),
                FadeIn(tower, scale=0.8),
                FadeIn(phone_b, shift=LEFT*0.5),
                lag_ratio=0.3
            ),
            run_time=2
        )
        self.play(
            Write(label_a),
            Write(label_b),
            Write(tower_label),
            run_time=1
        )
        self.wait(0.5)
        
        # ============================================
        # STEP 1: Phone A Transmits Alone
        # ============================================
        
        # Signal A equation
        signal_a_eq = MathTex(
            r"\text{Signal A: } s_A(t) = \cos(2\pi f_0 t)",
            font_size=32,
            color=BLUE
        )
        signal_a_eq.to_edge(UP, buff=0.5)
        
        self.play(Write(signal_a_eq), run_time=1.5)
        
        # Create sine wave from Phone A to Tower
        wave_a = self._create_traveling_wave(
            phone_a.get_center(),
            tower.get_center(),
            color=BLUE,
            frequency=2
        )
        
        self.play(Create(wave_a), run_time=2)
        
        # Pulsing effect on Phone A
        self.play(
            Indicate(phone_a, color=BLUE, scale_factor=1.2),
            run_time=0.8
        )
        
        self.wait(0.5)
        
        # ============================================
        # STEP 2: Phone B Also Transmits (Same Frequency!)
        # ============================================
        
        # Signal B equation
        signal_b_eq = MathTex(
            r"\text{Signal B: } s_B(t) = \cos(2\pi f_0 t + \phi)",
            font_size=32,
            color=RED
        )
        signal_b_eq.next_to(signal_a_eq, DOWN, buff=0.3)
        
        # Emphasize same frequency
        same_freq_box = SurroundingRectangle(
            VGroup(signal_a_eq[0][17:19], signal_b_eq[0][17:19]),
            color=YELLOW,
            buff=0.1
        )
        same_freq_label = Text("SAME f₀!", font_size=24, color=YELLOW, weight=BOLD)
        same_freq_label.next_to(same_freq_box, RIGHT, buff=0.3)
        same_freq_label.shift(RIGHT*0.8)
        
        self.play(Write(signal_b_eq), run_time=1.5)
        self.play(
            # Create(same_freq_box),
            Write(same_freq_label),
            run_time=1
        )
        
        # Create sine wave from Phone B to Tower
        wave_b = self._create_traveling_wave(
            phone_b.get_center(),
            tower.get_center(),
            color=RED,
            frequency=2,
            phase=PI/3  # Different phase
        )
        
        self.play(Create(wave_b), run_time=2)
        
        # Pulsing effect on Phone B
        self.play(
            Indicate(phone_b, color=RED, scale_factor=1.2),
            run_time=0.8
        )
        
        self.wait(0.5)
        
        # ============================================
        # STEP 3: Split Screen - Individual vs Received
        # ============================================
        
        self.play(
            # FadeOut(same_freq_box),
            FadeOut(same_freq_label),
            run_time=0.5
        )
        
        # Create dividing line
        divider = Line(UP*3.5, DOWN*3, color=WHITE, stroke_width=3)
        group_all = VGroup(phone_a, phone_b, tower, label_a, label_b, tower_label, wave_a, wave_b)
        self.play(
            # Move elements to left side
            group_all.animate.scale(0.5).to_edge(LEFT, buff=1.0),
            FadeOut(signal_a_eq),
            FadeOut(signal_b_eq),
            Create(divider),
            run_time=2
        )
        
        # Labels for each side
        left_label = Text("Individual Signals", font_size=24)
        left_label.move_to(LEFT*3.5 + DOWN*2.2)
        
        right_label = Text("Received at Tower", font_size=24)
        right_label.move_to(RIGHT*3.5 + DOWN*2.2)
        
        self.play(
            Write(left_label),
            Write(right_label),
            run_time=1
        )
        
        # ============================================
        # Right Side: Show received signal (interference)
        # ============================================
        
        # Create axes for signal plots (right side)
        axes_right = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False, "font_size": 20},
        )
        axes_right.move_to(RIGHT*3.5 + UP*0.5)
        
        # Labels
        t_label = MathTex("t", font_size=24).next_to(axes_right.x_axis, RIGHT)
        r_label = MathTex("r(t)", font_size=24).next_to(axes_right.y_axis, UP)
        
        self.play(
            Create(axes_right),
            Write(t_label),
            Write(r_label),
            run_time=1.5
        )
        
        # Plot individual signals (faded)
        signal_a_plot = axes_right.plot(
            lambda t: np.cos(2*t),
            color=BLUE,
            stroke_width=2,
            stroke_opacity=0.4
        )
        signal_b_plot = axes_right.plot(
            lambda t: np.cos(2*t + PI/3),
            color=RED,
            stroke_width=2,
            stroke_opacity=0.4
        )
        
        # Plot combined signal (highlighted)
        combined_signal = axes_right.plot(
            lambda t: np.cos(2*t) + np.cos(2*t + PI/3),
            color=PURPLE,
            stroke_width=4
        )
        
        self.play(
            Create(signal_a_plot),
            Create(signal_b_plot),
            run_time=1.5
        )
        
        self.play(
            Create(combined_signal),
            run_time=2
        )
        
        # Received signal equation
        received_eq = MathTex(
            r"r(t) = s_A(t) + s_B(t) + n(t)",
            font_size=28,
            color=PURPLE
        )
        received_eq.next_to(axes_right, DOWN, buff=0.5)
        
        self.play(Write(received_eq), run_time=1.5)
        
        # ============================================
        # STEP 4: Show Receiver Confusion
        # ============================================
        
        # Confusion visualization at tower
        confusion_marks = VGroup(
            Text("?", font_size=36, color=YELLOW),
            Text("?", font_size=36, color=YELLOW),
            Text("?", font_size=36, color=YELLOW)
        ).arrange(RIGHT, buff=0.2)
        confusion_marks.next_to(tower, UP, buff=0.2)
        
        self.play(
            LaggedStart(
                *[FadeIn(mark, scale=1.5) for mark in confusion_marks],
                lag_ratio=0.2
            ),
            Flash(tower, color=YELLOW, line_length=0.2, num_lines=8),
            run_time=1.5
        )
        
        # Problem statement
        problem_text = Text(
            "Base station CANNOT separate the signals!",
            font_size=24,
            color=ORANGE,
            weight=BOLD
        )
        problem_text.to_edge(DOWN, buff=0.5)
        
        self.play(Write(problem_text), run_time=2)
        
        self.wait(2)
        
        # ============================================
        # Cleanup for next section
        # ============================================
        
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1
        )


    # ============================================
    # Helper Methods for Signal Collision
    # ============================================

    def _create_simple_tower(self):
        """Create a simple tower icon"""
        # base = Rectangle(height=1.5, width=0.3, fill_color=GRAY, fill_opacity=1, stroke_width=2)
        # antenna = Triangle(fill_color=RED, fill_opacity=1, stroke_width=2).scale(0.25)
        # antenna.next_to(base, UP, buff=0)
        # tower = VGroup(base, antenna)
        tower = SVGMobject("assets/tower.svg").scale(0.8)
        return tower

    def _create_simple_phone(self, color=BLUE):
        """Create a simple phone icon"""
        body = RoundedRectangle(
            height=0.8, 
            width=0.5, 
            corner_radius=0.1,
            fill_color=color, 
            fill_opacity=0.8, 
            stroke_width=2,
            stroke_color=WHITE
        )
        screen = Rectangle(
            height=0.5, 
            width=0.35, 
            fill_color=BLACK, 
            fill_opacity=0.5, 
            stroke_width=1
        )
        screen.move_to(body.get_center() + UP*0.05)
        # phone = VGroup(body, screen)
        phone= SVGMobject("assets/mobile.svg").scale(0.5)
        return phone

    def _create_traveling_wave(self, start, end, color=BLUE, frequency=2, phase=0, amplitude=0.3):
        """Create a sinusoidal wave from start to end"""
        direction = end - start
        length = np.linalg.norm(direction)
        angle = np.arctan2(direction[1], direction[0])
        
        # Create wave along x-axis first
        wave = ParametricFunction(
            lambda t: np.array([
                t,
                amplitude * np.sin(frequency * t + phase),
                0
            ]),
            t_range=[0, length],
            color=color,
            stroke_width=3
        )
        
        # Rotate and position
        wave.rotate(angle, about_point=ORIGIN)
        wave.shift(start)
        
        return wave


    def sinr_quantification(self):
    
        # ============================================
        # Transition
        # ============================================
        transition_text = Text(
            "How do we measure this degradation?",
            font_size=36,
            color=YELLOW
        )
        self.play(Write(transition_text), run_time=2)
        self.wait(1)
        self.play(FadeOut(transition_text), run_time=0.8)
        
        # ============================================
        # Title
        # ============================================
        title = Text("Signal-to-Interference-plus-Noise Ratio (SINR)", 
                    font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.5)
        
        # ============================================
        # STEP 1: Build SINR Formula Visually
        # ============================================
        
        # Stage 1: Desired signal power (Green bar)
        signal_label = Text("Desired Signal Power", font_size=24, color=GREEN)
        signal_label.move_to(UP*1.5 + LEFT*3)
        
        signal_bar = Rectangle(
            width=3, 
            height=0.8,
            fill_color=GREEN,
            fill_opacity=0.7,
            stroke_color=WHITE,
            stroke_width=2
        )
        signal_bar.next_to(signal_label, DOWN, buff=0.3)
        
        p_signal = MathTex("P_{\\text{signal}}", font_size=28, color=WHITE)
        p_signal.move_to(signal_bar.get_center())
        
        self.play(
            Write(signal_label),
            FadeIn(signal_bar, shift=UP*0.3),
            Write(p_signal),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Stage 2: Interference power (Red bar)
        interference_label = Text("Interference Power", font_size=24, color=RED)
        interference_label.move_to(UP*1.5 + RIGHT*1)
        
        interference_bar = Rectangle(
            width=2,
            height=0.8,
            fill_color=RED,
            fill_opacity=0.7,
            stroke_color=WHITE,
            stroke_width=2
        )
        interference_bar.next_to(interference_label, DOWN, buff=0.3)
        
        p_interference = MathTex("P_{\\text{interference}}", font_size=24, color=WHITE)
        p_interference.move_to(interference_bar.get_center())
        
        self.play(
            Write(interference_label),
            FadeIn(interference_bar, shift=UP*0.3),
            Write(p_interference),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Stage 3: Noise power (Gray bar)
        noise_label = Text("Noise Power", font_size=24, color=GRAY)
        noise_label.move_to(UP*1.5 + RIGHT*4)
        
        noise_bar = Rectangle(
            width=1,
            height=0.8,
            fill_color=GRAY,
            fill_opacity=0.7,
            stroke_color=WHITE,
            stroke_width=2
        )
        noise_bar.next_to(noise_label, DOWN, buff=0.3)
        
        p_noise = MathTex("P_{\\text{noise}}", font_size=24, color=WHITE)
        p_noise.move_to(noise_bar.get_center())
        
        self.play(
            Write(noise_label),
            FadeIn(noise_bar, shift=UP*0.3),
            Write(p_noise),
            run_time=1.5
        )
        self.wait(0.5)
        
        # ============================================
        # STEP 2: Build the Ratio Visualization
        # ============================================
        
        # Move bars to form fraction
        self.play(
            FadeOut(signal_label),
            FadeOut(interference_label),
            FadeOut(noise_label),
            signal_bar.animate.move_to(UP*0.5),
            p_signal.animate.move_to(UP*0.5),
            interference_bar.animate.move_to(DOWN*1.2 + LEFT*0.75),
            p_interference.animate.move_to(DOWN*1.2 + LEFT*0.75),
            noise_bar.animate.move_to(DOWN*1.2 + RIGHT*1.25),
            p_noise.animate.move_to(DOWN*1.2 + RIGHT*1.25),
            
            # signal_label.animate.scale(0.7).move_to(UP*1.2),
            run_time=2.5
        )

        
        
        # Horizontal line (division)
        division_line = Line(LEFT*2, RIGHT*2, color=WHITE, stroke_width=3)
        division_line.move_to(DOWN*0.3)
        
        self.play(Create(division_line), run_time=0.8)
        
        # Move interference and noise to denominator
        
        
        # Plus sign
        plus_sign = MathTex("+", font_size=36, color=WHITE)
        plus_sign.move_to(DOWN*1.2 + RIGHT*0.55)
        self.play(Write(plus_sign), run_time=0.5)
        
        self.wait(1)
        
        # ============================================
        # STEP 3: Show Mathematical Formula
        # ============================================


        self.play(
            *[FadeOut(mob) for mob in [
                signal_bar, p_signal,
                interference_bar, p_interference,
                noise_bar, p_noise,
                division_line, plus_sign
            ]],
            
            run_time=1
        )
        self.wait(0.5)
        # Create formula
        sinr_formula = MathTex(
            r"\text{SINR} = \frac{P_{\text{signal}}}{P_{\text{interference}} + P_{\text{noise}}}",
            font_size=40
        )
        sinr_formula.move_to(ORIGIN)
        
        # Highlight box
        formula_box = SurroundingRectangle(sinr_formula, color=YELLOW, buff=0.2)
        
        self.play(
            Write(sinr_formula),
            Create(formula_box),
            run_time=2
        )
        
        self.wait(1)
        
        # dB conversion
        sinr_db = MathTex(
            r"\text{SINR (dB)} = 10 \log_{10}\left(\frac{P_{\text{signal}}}{P_{\text{interference}} + P_{\text{noise}}}\right)",
            font_size=32
        )
        sinr_db.next_to(sinr_formula, DOWN, buff=0.5)
        
        self.play(Write(sinr_db), run_time=2)
        
        self.wait(2)
        
        # ============================================
        # STEP 4: Interactive Demonstration
        # ============================================
        
        # Clear previous content
        self.play(FadeOut(formula_box),
            sinr_formula.animate.scale(0.8).to_edge(UP, buff=1),
            FadeOut(sinr_db),
            FadeOut(title),run_time=1.5)
        
        
        # Create split comparison
        comparison_title = Text("SINR Impact on Communication Quality", 
                            font_size=32, weight=BOLD)
        comparison_title.to_edge(UP, buff=0.3)
        self.play(Write(comparison_title), run_time=1)
        self.wait(24)
        # Divider
        # divider = Line(UP*2, DOWN*3.5, color=WHITE, stroke_width=2)
        # self.play(Create(divider), run_time=0.5)
        
        # ============================================
        # Left Panel: Good SINR (20 dB)
        # ============================================
        
        # good_sinr_label = Text("Good SINR = 20 dB", font_size=28, color=GREEN, weight=BOLD)
        # good_sinr_label.move_to(LEFT*3.5 + UP*2)
        
        # Scenario details
        # good_scenario = VGroup(
        #     Text("• 1 interferer", font_size=18),
        #     Text("• High data rate", font_size=18),
        #     Text("• 100 Mbps", font_size=18, color=GREEN)
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        # good_scenario.move_to(LEFT*3.5 + UP*0.8)
        
        # Constellation diagram (clean)
        # good_constellation = self._create_constellation_diagram(
        #     noise_level=0.1,
        #     color=GREEN
        # )
        # good_constellation.move_to(LEFT*3.5 + DOWN*1.2)
        
        # Quality indicator
        # good_indicator = self._create_quality_indicator(quality=0.9, color=GREEN)
        # good_indicator.move_to(LEFT*3.5 + DOWN*2.8)
        
        # self.play(
        #     Write(good_sinr_label),
        #     FadeIn(good_scenario, shift=UP*0.3),
        #     run_time=1.5
        # )
        # self.play(
        #     Create(good_constellation),
        #     FadeIn(good_indicator, scale=0.8),
        #     run_time=1.5
        # )
        
        # ============================================
        # Right Panel: Poor SINR (0 dB)
        # ============================================
        
        # poor_sinr_label = Text("Poor SINR = 0 dB", font_size=28, color=RED, weight=BOLD)
        # poor_sinr_label.move_to(RIGHT*3.5 + UP*2)
        
        # # Scenario details
        # poor_scenario = VGroup(
        #     Text("• 10 interferers", font_size=18),
        #     Text("• Low data rate", font_size=18),
        #     Text("• 10 Mbps", font_size=18, color=RED)
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        # poor_scenario.move_to(RIGHT*3.5 + UP*0.8)
        
        # Constellation diagram (noisy)
        # poor_constellation = self._create_constellation_diagram(
        #     noise_level=0.8,
        #     color=RED
        # )
        # poor_constellation.move_to(RIGHT*3.5 + DOWN*1.2)
        
        # # Quality indicator
        # poor_indicator = self._create_quality_indicator(quality=0.2, color=RED)
        # poor_indicator.move_to(RIGHT*3.5 + DOWN*2.8)
        
        # self.play(
        #     Write(poor_sinr_label),
        #     FadeIn(poor_scenario, shift=UP*0.3),
        #     run_time=1.5
        # )
        # self.play(
        #     Create(poor_constellation),
        #     FadeIn(poor_indicator, scale=0.8),
        #     run_time=1.5
        # )
        
        # self.wait(2)
        
        # ============================================
        # STEP 5: SINR Thresholds Table
        # ============================================
        
        # Fade out comparison
        self.play(
            FadeOut(comparison_title, sinr_formula),
            run_time=1
        )
        
        # Show typical SINR values table
        table_title = Text("Typical SINR Values", font_size=36, weight=BOLD)
        table_title.to_edge(UP, buff=0.5)
        subtitle = Text("For 4G and 5G service mode", font_size=24, color=YELLOW)
        subtitle.next_to(table_title, DOWN, buff=0.2)
        
        # Create table
        table_data = [
            ["SINR (dB)", "Quality", "Status"],
            [">= 20 dB", "Excellent", "✓"],
            ["13-20 dB", "Good", "✓"],
            ["0-13 dB", "Fair to poor", "--"],
            ["<= 0 dB", "Poor", "✗"],
        ]
        source = Text("(Source: Teltonika Networks)", font_size=16, color=GRAY)
        source.to_edge(DOWN, buff=0.2)
        
        table = self._create_table(table_data)
        table.scale(0.8).move_to(DOWN*0.5)
        
        self.play(Write(table_title), run_time=1)
        self.play(Write(subtitle), run_time=1)
        self.play(Create(table), run_time=2)
        self.play(Write(source), run_time=1)
        
        self.wait(3)
        
        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


    # ============================================
    # Helper Methods for SINR
    # ============================================

    def _create_constellation_diagram(self, noise_level=0.1, color=BLUE, num_points=16):
        """Create a QPSK/16-QAM constellation diagram with noise"""
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=3,
            y_length=3,
            axis_config={"include_tip": False, "stroke_width": 1},
        )
        
        # Ideal constellation points (QPSK)
        ideal_points = [
            np.array([1, 1, 0]),
            np.array([1, -1, 0]),
            np.array([-1, 1, 0]),
            np.array([-1, -1, 0])
        ]
        
        dots = VGroup()
        for ideal_point in ideal_points:
            # Add noise
            for _ in range(num_points):
                noisy_point = ideal_point + np.random.randn(3) * noise_level
                noisy_point[2] = 0  # Keep z=0
                dot = Dot(
                    axes.c2p(noisy_point[0], noisy_point[1]),
                    radius=0.03,
                    color=color,
                    fill_opacity=0.6
                )
                dots.add(dot)
        
        # Ideal points (larger, bright)
        for ideal_point in ideal_points:
            dot = Dot(
                axes.c2p(ideal_point[0], ideal_point[1]),
                radius=0.08,
                color=color,
                fill_opacity=1,
                stroke_width=2,
                stroke_color=WHITE
            )
            dots.add(dot)
        
        constellation = VGroup(axes, dots)
        return constellation

    def _create_quality_indicator(self, quality=0.8, color=GREEN):
        """Create a quality bar indicator"""
        bg = Rectangle(
            width=2.5,
            height=0.4,
            stroke_color=WHITE,
            stroke_width=2,
            fill_opacity=0
        )
        
        fill = Rectangle(
            width=2.5 * quality,
            height=0.4,
            fill_color=color,
            fill_opacity=0.8,
            stroke_width=0
        )
        fill.align_to(bg, LEFT)
        
        label = Text(f"{int(quality*100)}%", font_size=18, color=color)
        label.next_to(bg, RIGHT, buff=0.2)
        
        indicator = VGroup(bg, fill, label)
        return indicator

    def _create_table(self, data):
        """Create a table from 2D list"""
        rows = VGroup()
        
        for i, row_data in enumerate(data):
            row = VGroup()
            for j, cell_data in enumerate(row_data):
                # Cell background
                cell_bg = Rectangle(
                    width=2.5,
                    height=0.6,
                    stroke_color=WHITE,
                    stroke_width=1,
                    fill_color=BLACK if i == 0 else DARK_GRAY,
                    fill_opacity=0.3 if i == 0 else 0.1
                )
                
                # Cell text
                if i == 0:  # Header
                    cell_text = Text(cell_data, font_size=20, weight=BOLD)
                else:  # Data
                    # Color code status
                    if j == 2:  # Status column
                        if cell_data == "✓":
                            color = GREEN
                        elif cell_data == "--":
                            color=YELLOW
                        else:
                            color = RED
                        cell_text = Text(cell_data, font_size=24, color=color, weight=BOLD)
                    elif j == 1:  # Quality column
                        if "Excellent" in cell_data or "Good" in cell_data:
                            color = GREEN
                        elif "Fair" in cell_data:
                            color = YELLOW
                        else:
                            color = RED
                        cell_text = Text(cell_data, font_size=18, color=color)
                    else:
                        cell_text = Text(cell_data, font_size=18)
                
                cell_text.move_to(cell_bg.get_center())
                
                cell = VGroup(cell_bg, cell_text)
                row.add(cell)
            
            row.arrange(RIGHT, buff=0)
            rows.add(row)
        
        rows.arrange(DOWN, buff=0)
        return rows


    def types_of_interference(self):
        transition_text = Text(
        "Not all interference is the same...",
        font_size=36,
        color=YELLOW
        )
        self.play(Write(transition_text), run_time=2)
        self.wait(1)
        self.play(FadeOut(transition_text), run_time=0.8)

        # ============================================
        # Title
        # ============================================
        title = Text("Types of Interference", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.5)

        # ============================================
        # Create 3 Panels
        # ============================================

        # Panel dividers
        divider1 = Line(UP*2.5 + LEFT*2.33, DOWN*3 + LEFT*2.33, stroke_width=2)
        divider2 = Line(UP*2.5 + RIGHT*2.33, DOWN*3 + RIGHT*2.33, stroke_width=2)

        self.play(
            Create(divider1),
            Create(divider2),
            run_time=0.8
        )

        # ============================================
        # Panel 1: Co-Channel Interference (CCI)
        # ============================================

        # Title
        cci_title = Text("Co-Channel\nInterference (CCI)", 
                        font_size=20, weight=BOLD, color=PURPLE)
        cci_title.move_to(LEFT*4.7 + UP*2)

        self.play(Write(cci_title), run_time=1)

        # Visual: Two adjacent cells
        cell1 = RegularPolygon(n=6, color=BLUE, stroke_width=2)
        cell1.scale(0.8).move_to(LEFT*5.3)

        cell2 = RegularPolygon(n=6, color=BLUE, stroke_width=2)
        cell2.scale(0.8).move_to(LEFT*4.1)

        # Towers
        tower1 = self._create_simple_tower().scale(0.3)
        tower1.move_to(cell1.get_center())

        tower2 = self._create_simple_tower().scale(0.3)
        tower2.move_to(cell2.get_center())

        # Frequency labels
        freq1 = MathTex("f_1", font_size=20, color=YELLOW)
        freq1.next_to(tower1, DOWN, buff=0.1)

        freq2 = MathTex("f_1", font_size=20, color=YELLOW)
        freq2.next_to(tower2, DOWN, buff=0.1)

        # Same frequency highlight
        same_freq = Text("SAME frequency!", font_size=16, color=RED, weight=BOLD)
        same_freq.move_to(LEFT*4.7 + UP*1.2)

        self.play(
            Create(cell1),
            Create(cell2),
            FadeIn(tower1, tower2, scale=0.5),
            run_time=1
        )
        self.play(
            Write(freq1),
            Write(freq2),
            Write(same_freq),
            run_time=1
        )

        # Interference zone
        interference_zone = Ellipse(
            width=0.8,
            height=1.5,
            color=RED,
            fill_opacity=0.3,
            stroke_width=0
        )
        interference_zone.rotate(PI/6)
        interference_zone.move_to((cell1.get_center() + cell2.get_center())/2)

        self.play(FadeIn(interference_zone), run_time=1)

        # Description
        cci_desc = Text("Same channel,\ndifferent cells", 
                    font_size=16, color=WHITE)
        cci_desc.move_to(LEFT*4.7 + DOWN*1.5)
        self.play(Write(cci_desc), run_time=1)

        # ============================================
        # Panel 2: Adjacent Channel Interference (ACI)
        # ============================================

        # Title
        aci_title = Text("Adjacent Channel\nInterference (ACI)", 
                        font_size=20, weight=BOLD, color=PURPLE)
        aci_title.move_to(ORIGIN + UP*2)

        self.play(Write(aci_title), run_time=1)

        # Visual: Frequency spectrum with overlapping skirts
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.5, 0.5],
            x_length=4,
            y_length=2.5,
            axis_config={"include_tip": False, "stroke_width": 1},
        )
        axes.move_to(UP*0.3)

        # Frequency axis label
        freq_label = Text("Frequency →", font_size=14)
        freq_label.next_to(axes.x_axis, DOWN, buff=0.1)

        # Channel 1 (centered at f=3)
        channel1 = axes.plot(
            lambda x: 1.2 * np.exp(-2*(x-3)**2),
            x_range=[0, 6],
            color=BLUE,
            stroke_width=3
        )

        # Channel 2 (centered at f=5, overlaps slightly)
        channel2 = axes.plot(
            lambda x: 1.2 * np.exp(-2*(x-5)**2),
            x_range=[2, 8],
            color=GREEN,
            stroke_width=3
        )

        # Overlap region (interference)
        overlap_region1 = axes.get_area(
            channel1,
            x_range=[3.5, 4],
            color=RED,
            opacity=0.5
        )
        overlap_region2 = axes.get_area(
            channel2,
            x_range=[4, 4.5],
            color=RED,
            opacity=0.5
        )

        self.play(
            Create(axes),
            Write(freq_label),
            run_time=1
        )
        self.play(
            Create(channel1),
            Create(channel2),
            run_time=1.5
        )
        self.play(FadeIn(overlap_region1), FadeIn(overlap_region2), run_time=1)

        # Labels
        ch1_label = MathTex("f_1", font_size=18, color=BLUE)
        ch1_label.move_to(axes.c2p(3, 1.3))

        ch2_label = MathTex("f_2", font_size=18, color=GREEN)
        ch2_label.move_to(axes.c2p(5, 1.3))

        self.play(Write(ch1_label), Write(ch2_label), run_time=0.8)

        # Description
        aci_desc = Text("Nearby channels,\nimperfect filtering", 
                    font_size=14, color=WHITE)
        aci_desc.move_to(DOWN*1.5)
        self.play(Write(aci_desc), run_time=1)

        # ============================================
        # Panel 3: Inter-Symbol Interference (ISI)
        # ============================================

        # Title
        isi_title = Text("Inter-Symbol\nInterference (ISI)", 
                        font_size=20, weight=BOLD, color=PURPLE)
        isi_title.move_to(RIGHT*4.7 + UP*2)

        self.play(Write(isi_title), run_time=1)

        # Visual: Delayed pulses overlapping
        time_axes = Axes(
            x_range=[0, 8, 2],
            y_range=[0, 1.2, 0.5],
            x_length=4,
            y_length=2.5,
            axis_config={"include_tip": False, "stroke_width": 1},
        )
        time_axes.move_to(RIGHT*4.7 + UP*0.3)
        time_label = Text("Time →", font_size=14)
        time_label.next_to(time_axes.x_axis, DOWN, buff=0.1)
        self.play(
            Create(time_axes),
            Write(time_label),
            run_time=1
        )
        # Time axis label
        


        def get_isi_group(start_x, color, label_char):
            group = VGroup()
            # 3 components: Main, Delay 1, Delay 2
            offsets = [0, 0.7, 1.4]
            heights = [1.0, 0.7, 0.4]
            opacities = [0.6, 0.4, 0.2]
            labels = ["", "'", "''"]
            
            for i in range(3):
                rect = Rectangle(
                    width=0.8, 
                    height=heights[i],
                    fill_color=color, 
                    fill_opacity=opacities[i],
                    stroke_width=1
                )
                # Position relative to axes
                rect.move_to(time_axes.c2p(start_x + offsets[i], 0), aligned_edge=DOWN)
                
                # Label (e.g., 1, 1', 1'')
                lbl = Text(f"{label_char}{labels[i]}", font_size=12, color=WHITE)
                lbl.move_to(rect.get_center())
                
                group.add(VGroup(rect, lbl))
            return group

        
        # Original pulse
        symbol1 = get_isi_group(1.5, GREEN, "1")
        symbol2 = get_isi_group(4, BLUE, "2")

        # overlap_width = 3.7 - 3.3
        # isi_highlight = Rectangle(
        #     width= (time_axes.x_length / 8) * overlap_width, # Scaling to axis length
        #     height= 0.4 * (time_axes.y_length / 1.2),        # Scaling to axis height
        #     fill_color="#FF9999", # Light red / Salmon
        #     fill_opacity=0.8,
        #     stroke_width=0
        # )
        # Position it precisely at the collision point
        isi_highlight.move_to(time_axes.c2p(3.3, 0), aligned_edge=DOWN + LEFT)
        # Overlap highlight
        for comp in symbol1:
            self.play(FadeIn(comp, shift=UP*0.2), run_time=0.4)

        for comp in symbol2:
            self.play(FadeIn(comp, shift=UP*0.2), run_time=0.4)
        
        self.wait(0.5)
        # self.play(FadeIn(isi_highlight), run_time=1)
        self.wait(4)
        
        # self.play(
        #     FadeIn(pulse1, shift=UP*0.3),
        #     FadeIn(pulse2, shift=UP*0.3),
        #     FadeIn(pulse3, shift=UP*0.3),
        #     run_time=1.5
        # )
        # self.play(Create(overlap_box), run_time=0.8)

        # Labels
        # original_label = Text("Original", font_size=12, color=BLUE)
        # original_label.next_to(pulse1, UP, buff=0.1)

        # delayed_label = Text("Delayed", font_size=12, color=RED)
        # delayed_label.next_to(pulse2, UP, buff=0.1)

        # self.play(
        #     Write(original_label),
        #     Write(delayed_label),
        #     run_time=0.8
        # )

        # Description
        isi_desc = Text("Self-interference\nfrom multipath", 
                    font_size=14, color=WHITE)
        isi_desc.move_to(RIGHT*4.7 + DOWN*1.5)

        # Reference to previous lecture
        ref_note = Text("(See Lecture-4)", font_size=12, color=GRAY, slant=ITALIC)
        ref_note.next_to(isi_desc, DOWN, buff=0.1)

        self.play(
            Write(isi_desc),
            Write(ref_note),
            run_time=1
        )

        self.wait(3)

        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


    def fundamental_tradeoff(self):
    
        # ============================================
        # Transition
        # ============================================
        transition_text = Text(
            "The Fundamental Trade-off",
            font_size=42,
            weight=BOLD,
            color=YELLOW
        )
        self.play(Write(transition_text), run_time=2)
        self.wait(1)
        self.play(FadeOut(transition_text), run_time=0.8)
        
        # ============================================
        # Balance Scale Animation
        # ============================================
        
        # Create balance scale
        pivot = Triangle(color=GRAY, fill_opacity=1).scale(0.4)
        pivot.rotate(PI)
        pivot.move_to(DOWN*0.5)
        
        beam = Rectangle(width=8, height=0.2, fill_color=GRAY, fill_opacity=1)
        beam.move_to(pivot.get_top() + UP*0.1)
        
        # Left side platform
        left_chain = Line(beam.get_left() + UP*0.1, beam.get_left() + DOWN*1.5, stroke_width=2)
        left_platform = Rectangle(width=2, height=0.3, fill_color=BLUE, fill_opacity=0.8)
        left_platform.next_to(left_chain, DOWN, buff=0)
        
        # Right side platform
        right_chain = Line(beam.get_right() + UP*0.1, beam.get_right() + DOWN*1.5, stroke_width=2)
        right_platform = Rectangle(width=2, height=0.3, fill_color=RED, fill_opacity=0.8)
        right_platform.next_to(right_chain, DOWN, buff=0)
        
        scale = VGroup(pivot, beam, left_chain, left_platform, right_chain, right_platform)
        
        self.play(Create(scale), run_time=2)
        beam.current_angle = 0
        
        # ============================================
        # Left Side: Number of Users (Increasing)
        # ============================================
        
        left_label = Text("Number of Users", font_size=24, weight=BOLD)
        left_label.next_to(left_platform, DOWN, buff=0.5)
        
        self.play(Write(left_label), run_time=1)
        
        # Stack of phones (growing)
        phones_stack = VGroup()
        for i in range(5):
            phone = self._create_simple_phone(BLUE).scale(0.6)
            phones_stack.add(phone)
        
        phones_stack.arrange(UP, buff=0.05)
        phones_stack.move_to(left_platform.get_center() + UP*0.5)
        phones_stack.scale(0)  # Start small
        
        self.add(phones_stack)
        
        # ============================================
        # Right Side: Quality per User (Decreasing)
        # ============================================
        
        right_label = Text("Quality per User", font_size=24, weight=BOLD)
        right_label.next_to(right_platform, DOWN, buff=0.5)
        
        self.play(Write(right_label), run_time=1)
        
        # Quality bars
        quality_bars = VGroup()
        for i in range(5):
            bar_height = 1.2 - (i * 0.2)  # Decreasing height
            bar = Rectangle(
                width=0.25,
                height=bar_height,
                fill_color=[GREEN, YELLOW, ORANGE, RED, MAROON_E][i],
                fill_opacity=0.8,
                stroke_width=1
            )
            quality_bars.add(bar)
        
        quality_bars.arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
        quality_bars.move_to(right_platform.get_center() + UP*0.3)
        
        # ============================================
        # Animate the Trade-off
        # ============================================
       
        # ValueTracker for users
        users = ValueTracker(1)
        
        # Updater for phones stack
        def update_phones(mob):
            n = int(users.get_value())
            for i, phone in enumerate(phones_stack):
                if i < n:
                    phone.set_opacity(1)
                    target_scale = 0.6
                else:
                    phone.set_opacity(0)
                    target_scale = 0
        
        phones_stack.add_updater(update_phones)
        
        # Updater for quality bars (color changes)
        def update_quality(mob):
            n = int(users.get_value())
            for i, bar in enumerate(quality_bars):
                if i < n:
                    opacity = 1 - (i * 0.15)
                    bar.set_fill_opacity(opacity)
                else:
                    bar.set_fill_opacity(0.2)
        
        quality_bars.add_updater(update_quality)

        users = ValueTracker(1)
        # Updater for scale tilt
        def update_scale_tilt(mob):
            n = users.get_value()
            target_angle = -(n - 3) * 0.08  # Calculate target tilt
            angle_diff = target_angle - mob.current_angle  # Difference from current
            mob.rotate(angle_diff, about_point=pivot.get_top())
            mob.current_angle = target_angle  # Update stored angle
    
        beam.add_updater(update_scale_tilt)
        
        # beam.add_updater(update_scale_tilt)
        left_chain.add_updater(lambda m: m.become(Line(beam.get_left() + UP*0.1, left_platform.get_top(), stroke_width=2)))
        right_chain.add_updater(lambda m: m.become(Line(beam.get_right() + UP*0.1, right_platform.get_top(), stroke_width=2)))
        
        # Show quality bars
        self.play(
            *[GrowFromEdge(bar, DOWN) for bar in quality_bars],
            run_time=1.5
        )
        
        # Animate increasing users (1 to 5)
        self.play(
            users.animate.set_value(5),
            run_time=4,
            rate_func=smooth
        )
        
        self.wait(1)
        
        # ============================================
        # Final Message
        # ============================================
        
        conclusion = Text(
            "We need a smarter approach!",
            font_size=36,
            weight=BOLD,
            color=YELLOW
        )
        conclusion.to_edge(UP, buff=0.5)
        
        self.play(
            Write(conclusion),
            Flash(conclusion, color=YELLOW, line_length=0.3, num_lines=12),
            run_time=2
        )
        
        self.wait(2)
        
        # Cleanup
        phones_stack.clear_updaters()
        quality_bars.clear_updaters()
        beam.clear_updaters()
        left_chain.clear_updaters()
        right_chain.clear_updaters()
        
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)