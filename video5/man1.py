from manim import *
import numpy as np

class DopplerSection3(Scene):
    def construct(self):
        # This is the master scene that calls all subscenes
        self.scene_3_1_the_missing_link()
        self.clear()
        self.scene_3_2_single_path()
        self.clear()
        self.scene_3_3_multiple_paths()
        self.clear()
        self.scene_3_4_fading_pattern()

    def scene_3_1_the_missing_link(self):
        """3.1: The Missing Link - What Does Doppler Do to h(t)?"""
        
        # Title
        title = Text("3.1: From Doppler Shift to Time-Varying Channel", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Recap from Section 2
        recap_title = Text("What We Know So Far:", font_size=28, color=YELLOW)
        recap_title.move_to(UP * 2)
        self.play(Write(recap_title))
        
        recap_points = VGroup(
            MathTex(r"\text{1. Motion causes Doppler shift: } f_d = \frac{v \cdot f_c}{c}", font_size=28),
            MathTex(r"\text{2. Frequency changes: } f_{obs} = f_c + f_d", font_size=28),
            Text("3. For wireless: fd ≈ 222 Hz at 100 km/h, 2.4 GHz carrier", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        recap_points.next_to(recap_title, DOWN, buff=0.5)
        
        for point in recap_points:
            self.play(Write(point))
            self.wait(0.5)
        
        self.wait(2)
        
        # The key question
        self.play(
            FadeOut(recap_points),
            recap_title.animate.move_to(UP * 2.5)
        )
        
        question = Text(
            "But here's the KEY QUESTION:",
            font_size=32,
            color=RED
        ).move_to(UP * 1.2)
        self.play(Write(question))
        self.wait()
        
        key_question = Text(
            "How does Doppler shift affect our channel h(t)?",
            font_size=36,
            color=YELLOW
        ).next_to(question, DOWN, buff=0.5)
        
        self.play(Write(key_question))
        self.wait(2)
        
        # Channel representation reminder
        channel_eq = MathTex(
            r"r(t) = h(t) \cdot s(t) + n(t)",
            font_size=40
        ).move_to(ORIGIN)
        
        self.play(Write(channel_eq))
        self.wait()
        
        # Highlight h(t)
        h_highlight = SurroundingRectangle(channel_eq[0][2:6], color=BLUE, buff=0.1)
        h_label = Text("Channel", font_size=24, color=BLUE).next_to(h_highlight, DOWN)
        
        self.play(Create(h_highlight), Write(h_label))
        self.wait(2)
        
        # The insight
        insight = VGroup(
            Text("Remember from Lecture 3:", font_size=28),
            MathTex(r"h(t) = \text{phasor sum of multipath components}", font_size=28),
            Text("Each component has a phase based on path length", font_size=26, color=YELLOW)
        ).arrange(DOWN, buff=0.3)
        insight.to_edge(DOWN, buff=0.8)
        
        for line in insight:
            self.play(Write(line))
            self.wait(0.5)
        
        self.wait(2)
        
        # Transition
        transition = Text(
            "Let's see what happens with motion, starting with ONE path...",
            font_size=28,
            color=GREEN
        ).to_edge(DOWN)
        
        self.play(
            FadeOut(insight),
            Write(transition)
        )
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def scene_3_2_single_path(self):
        """3.2: Single Path - The Rotating Phasor"""
        
        title = Text("3.2: Single Path - How Doppler Creates Rotation", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Split screen: Physical setup on left, phasor on right
        divider = Line(UP * 3, DOWN * 3, color=WHITE).move_to(ORIGIN)
        
        left_title = Text("Physical Picture", font_size=28).move_to(LEFT * 3.5 + UP * 2.5)
        right_title = Text("Phasor View", font_size=28).move_to(RIGHT * 3.5 + UP * 2.5)
        
        self.play(
            Create(divider),
            Write(left_title),
            Write(right_title)
        )
        self.wait()
        
        # LEFT SIDE: Physical setup
        # Transmitter
        try:
            tx = SVGMobject("tower.svg").scale(0.4)
        except:
            tx = VGroup(
                Rectangle(height=0.8, width=0.15, fill_opacity=0.8, fill_color=BLUE),
                Triangle(fill_opacity=0.8, fill_color=RED).scale(0.2).next_to(
                    Rectangle(height=0.8, width=0.15), UP, buff=0
                )
            )
        tx.move_to(LEFT * 5.5 + UP * 0.5)
        
        # Reflector
        reflector = Line(UP * 1, DOWN * 1, color=GRAY, stroke_width=6)
        reflector.move_to(LEFT * 3.5 + DOWN * 0.5)
        
        # Receiver
        try:
            rx = SVGMobject("mobile.svg").scale(0.3)
        except:
            rx = VGroup(
                RoundedRectangle(height=0.5, width=0.25, corner_radius=0.08, 
                                fill_opacity=0.8, fill_color=ORANGE)
            )
        rx.move_to(LEFT * 1.5 + UP * 0.5)
        
        # Draw setup
        self.play(FadeIn(tx), Create(reflector), FadeIn(rx))
        
        # Show path
        path1 = Arrow(tx.get_right(), reflector.get_top(), color=BLUE, buff=0.1)
        path2 = Arrow(reflector.get_top(), rx.get_left(), color=BLUE, buff=0.1)
        
        self.play(Create(path1), Create(path2))
        
        # Distance label
        distance_label = MathTex(r"d(t)", font_size=28, color=YELLOW)
        distance_label.move_to(LEFT * 3.5 + UP * 1.5)
        self.play(Write(distance_label))
        self.wait()
        
        # CASE 1: Stationary
        case1_text = Text("Case 1: Stationary (v = 0)", font_size=26, color=GREEN)
        case1_text.move_to(LEFT * 3.5 + DOWN * 2)
        self.play(Write(case1_text))
        
        # RIGHT SIDE: Stationary phasor
        axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=3,
            y_length=3,
            axis_config={"include_tip": True}
        ).move_to(RIGHT * 3.5 + UP * 0.2)
        
        axes_labels = axes.get_axis_labels(x_label="Re", y_label="Im")
        
        self.play(Create(axes), Write(axes_labels))
        
        # Initial phasor
        phase_0 = PI / 4  # 45 degrees
        phasor_length = 1
        phasor = Arrow(
            axes.c2p(0, 0),
            axes.c2p(phasor_length * np.cos(phase_0), phasor_length * np.sin(phase_0)),
            buff=0,
            color=GREEN,
            stroke_width=6
        )
        
        phase_label = MathTex(r"\phi_0", font_size=28, color=GREEN)
        phase_label.next_to(phasor.get_end(), UR, buff=0.1)
        
        self.play(Create(phasor), Write(phase_label))
        
        # Equation for stationary case
        eq1 = MathTex(
            r"h(t) = h_1 \cdot e^{j\phi_0}",
            font_size=32
        ).move_to(RIGHT * 3.5 + DOWN * 2)
        eq1_box = SurroundingRectangle(eq1, color=GREEN, buff=0.15)
        
        self.play(Write(eq1), Create(eq1_box))
        
        stationary_note = Text("Constant!", font_size=24, color=GREEN)
        stationary_note.next_to(eq1_box, DOWN)
        self.play(Write(stationary_note))
        self.wait(3)
        
        # Clear for Case 2
        self.play(
            FadeOut(case1_text),
            FadeOut(eq1),
            FadeOut(eq1_box),
            FadeOut(stationary_note),
            FadeOut(phasor),
            FadeOut(phase_label)
        )
        
        # CASE 2: With motion
        case2_text = Text("Case 2: With Motion (v > 0)", font_size=26, color=RED)
        case2_text.move_to(LEFT * 3.5 + DOWN * 2)
        self.play(Write(case2_text))
        
        # Add velocity arrow to receiver
        velocity_arrow = Arrow(
            rx.get_right(),
            rx.get_right() + RIGHT * 0.8,
            color=RED,
            buff=0
        )
        v_label = MathTex("v", color=RED, font_size=28).next_to(velocity_arrow, UP, buff=0.05)
        
        self.play(Create(velocity_arrow), Write(v_label))
        self.wait()
        
        # Distance changes with time
        distance_eq = MathTex(
            r"d(t) = d_0 + v \cdot t",
            font_size=28,
            color=YELLOW
        ).move_to(LEFT * 3.5 + DOWN * 1)
        self.play(Write(distance_eq))
        self.wait()
        
        # Phase changes with distance
        phase_eq_sequence = VGroup(
            MathTex(r"\phi(t) = \frac{2\pi d(t)}{\lambda}", font_size=28),
            MathTex(r"= \frac{2\pi}{\lambda}(d_0 + vt)", font_size=28),
            MathTex(r"= \phi_0 + \frac{2\pi v t}{\lambda}", font_size=28),
            MathTex(r"= \phi_0 + 2\pi f_d t", font_size=28, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        phase_eq_sequence.move_to(RIGHT * 3.5 + DOWN * 1.5)
        
        for i, eq in enumerate(phase_eq_sequence):
            self.play(Write(eq))
            self.wait(0.8)
            if i == 2:
                doppler_note = Text("where fd = v/λ", font_size=20, color=BLUE)
                doppler_note.next_to(eq, RIGHT, buff=0.3)
                self.play(Write(doppler_note))
                self.wait(1)
        
        # Highlight the key result
        key_box = SurroundingRectangle(phase_eq_sequence[3], color=YELLOW, buff=0.1)
        self.play(Create(key_box))
        self.wait(2)
        
        # Animated rotating phasor
        self.play(
            FadeOut(phase_eq_sequence[0:3]),
            FadeOut(doppler_note),
            phase_eq_sequence[3].animate.move_to(RIGHT * 3.5 + DOWN * 2.5),
            key_box.animate.move_to(RIGHT * 3.5 + DOWN * 2.5)
        )
        
        # Create rotating phasor
        rotation_label = Text("Phasor ROTATES at rate 2πfd!", font_size=26, color=RED)
        rotation_label.move_to(RIGHT * 3.5 + UP * 2)
        self.play(Write(rotation_label))
        
        # Animate rotation
        rotating_phasor = Arrow(
            axes.c2p(0, 0),
            axes.c2p(phasor_length * np.cos(phase_0), phasor_length * np.sin(phase_0)),
            buff=0,
            color=RED,
            stroke_width=6
        )
        self.play(Create(rotating_phasor))
        
        # Rotation animation
        fd = 0.5  # Doppler frequency for visualization
        
        def get_phasor_end(t):
            phase = phase_0 + 2 * PI * fd * t
            return axes.c2p(phasor_length * np.cos(phase), phasor_length * np.sin(phase))
        
        # Create trace circle
        circle_trace = Circle(
            radius=phasor_length * axes.x_axis.get_unit_size(),
            color=YELLOW,
            stroke_width=2,
            stroke_opacity=0.3
        ).move_to(axes.c2p(0, 0))
        self.play(Create(circle_trace))
        
        # Animate rotation for 2 full cycles
        num_rotations = 3
        rotation_time = num_rotations / fd
        
        self.play(
            Rotate(rotating_phasor, angle=2*PI*num_rotations, about_point=axes.c2p(0, 0)),
            run_time=rotation_time,
            rate_func=linear
        )
        self.wait()
        
        # Final equation with rotation
        final_eq = MathTex(
            r"h(t) = h_1 \cdot e^{j(\phi_0 + 2\pi f_d t)}",
            font_size=36,
            color=RED
        ).to_edge(DOWN)
        final_box = SurroundingRectangle(final_eq, color=RED, buff=0.2)
        
        self.play(Write(final_eq), Create(final_box))
        
        time_varying = Text("Time-Varying Channel!", font_size=28, color=RED)
        time_varying.next_to(final_box, DOWN)
        self.play(Write(time_varying))
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def scene_3_3_multiple_paths(self):
        """3.3: Multiple Paths - The Complete Picture"""
        
        title = Text("3.3: Multiple Paths - Each Rotating Differently", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        narration = Text(
            "In reality, we have MANY multipath components...",
            font_size=28
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(narration))
        self.wait(2)
        self.play(FadeOut(narration))
        
        # Split screen again
        divider = Line(UP * 3, DOWN * 3, color=WHITE).move_to(ORIGIN)
        
        left_title = Text("Multipath Scenario", font_size=28).move_to(LEFT * 3.5 + UP * 2.5)
        right_title = Text("Multiple Rotating Phasors", font_size=28).move_to(RIGHT * 3.5 + UP * 2.5)
        
        self.play(
            Create(divider),
            Write(left_title),
            Write(right_title)
        )
        
        # LEFT SIDE: Multipath setup
        try:
            tx = SVGMobject("tower.svg").scale(0.4)
        except:
            tx = VGroup(
                Rectangle(height=0.8, width=0.15, fill_opacity=0.8, fill_color=BLUE),
                Triangle(fill_opacity=0.8, fill_color=RED).scale(0.2)
            )
        tx.move_to(LEFT * 5.5)
        
        try:
            rx = SVGMobject("mobile.svg").scale(0.3)
        except:
            rx = VGroup(
                RoundedRectangle(height=0.5, width=0.25, corner_radius=0.08, 
                                fill_opacity=0.8, fill_color=ORANGE)
            )
        rx.move_to(LEFT * 1.5)
        
        self.play(FadeIn(tx), FadeIn(rx))
        
        # Multiple reflectors at different angles
        reflector_positions = [
            LEFT * 3.5 + UP * 1.5,
            LEFT * 3.5 + UP * 0.5,
            LEFT * 3.5 + DOWN * 0.5,
            LEFT * 3.5 + DOWN * 1.5
        ]
        
        colors = [BLUE, GREEN, YELLOW, RED]
        paths = VGroup()
        angle_labels = VGroup()
        
        for i, (pos, color) in enumerate(zip(reflector_positions, colors)):
            reflector = Line(UP * 0.3, DOWN * 0.3, color=GRAY, stroke_width=4)
            reflector.move_to(pos)
            self.play(Create(reflector), run_time=0.3)
            
            # Path arrows
            path1 = Arrow(tx.get_right(), pos, color=color, buff=0.1, stroke_width=2)
            path2 = Arrow(pos, rx.get_left(), color=color, buff=0.1, stroke_width=2)
            paths.add(path1, path2)
            
            # Angle of arrival
            angle = MathTex(rf"\theta_{i+1}", font_size=20, color=color)
            angle.next_to(pos, LEFT, buff=0.2)
            angle_labels.add(angle)
        
        self.play(Create(paths), Write(angle_labels))
        self.wait()
        
        # Velocity
        velocity_arrow = Arrow(rx.get_right(), rx.get_right() + RIGHT * 0.6, color=RED, buff=0)
        v_label = MathTex("v", color=RED, font_size=24).next_to(velocity_arrow, UP, buff=0.05)
        self.play(Create(velocity_arrow), Write(v_label))
        self.wait()
        
        # Key insight
        insight = VGroup(
            Text("Each path sees", font_size=22),
            Text("DIFFERENT Doppler shift!", font_size=22, color=YELLOW),
            MathTex(r"f_{d,i} = \frac{v}{c} f_c \cos(\theta_i)", font_size=24)
        ).arrange(DOWN, buff=0.2)
        insight.move_to(LEFT * 3.5 + DOWN * 2.2)
        
        for line in insight:
            self.play(Write(line))
            self.wait(0.5)
        
        self.wait(2)
        
        # RIGHT SIDE: Multiple phasors
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=3.5,
            y_length=3.5,
            axis_config={"include_tip": True}
        ).move_to(RIGHT * 3.5 + UP * 0.2)
        
        axes_labels = axes.get_axis_labels(x_label="Re", y_label="Im")
        self.play(Create(axes), Write(axes_labels))
        
        # Create multiple phasors with different initial phases and Doppler shifts
        num_phasors = 4
        initial_phases = [PI/6, 2*PI/3, -PI/4, 5*PI/4]
        amplitudes = [0.8, 1.0, 0.6, 0.9]
        doppler_freqs = [0.3, 0.5, 0.2, 0.4]  # Different rotation rates
        
        phasors = VGroup()
        
        for i in range(num_phasors):
            phasor = Arrow(
                axes.c2p(0, 0),
                axes.c2p(
                    amplitudes[i] * np.cos(initial_phases[i]),
                    amplitudes[i] * np.sin(initial_phases[i])
                ),
                buff=0,
                color=colors[i],
                stroke_width=4
            )
            phasors.add(phasor)
            self.play(Create(phasor), run_time=0.4)
        
        self.wait()
        
        # Show sum phasor
        sum_label = Text("Sum:", font_size=24, color=WHITE).next_to(axes, DOWN, buff=0.3)
        self.play(Write(sum_label))
        
        # Calculate initial sum
        sum_x = sum(amplitudes[i] * np.cos(initial_phases[i]) for i in range(num_phasors))
        sum_y = sum(amplitudes[i] * np.sin(initial_phases[i]) for i in range(num_phasors))
        
        sum_phasor = Arrow(
            axes.c2p(0, 0),
            axes.c2p(sum_x, sum_y),
            buff=0,
            color=WHITE,
            stroke_width=6
        )
        self.play(Create(sum_phasor))
        
        h_label = MathTex("h(t)", font_size=28, color=WHITE).next_to(sum_phasor.get_end(), UR, buff=0.1)
        self.play(Write(h_label))
        self.wait(2)
        
        # Animate all phasors rotating at different rates
        rotation_text = Text(
            "Each rotates at its own fd,i",
            font_size=24,
            color=YELLOW
        ).move_to(RIGHT * 3.5 + DOWN * 2)
        self.play(Write(rotation_text))
        
        # Animation parameters
        animation_duration = 8
        fps = 30
        frames = int(animation_duration * fps)
        
        def update_phasors(mob, alpha):
            t = alpha * animation_duration
            new_phasors = VGroup()
            
            sum_x = 0
            sum_y = 0
            
            for i in range(num_phasors):
                phase = initial_phases[i] + 2 * PI * doppler_freqs[i] * t
                x = amplitudes[i] * np.cos(phase)
                y = amplitudes[i] * np.sin(phase)
                sum_x += x
                sum_y += y
                
                new_phasor = Arrow(
                    axes.c2p(0, 0),
                    axes.c2p(x, y),
                    buff=0,
                    color=colors[i],
                    stroke_width=4
                )
                new_phasors.add(new_phasor)
            
            # Update sum phasor
            new_sum = Arrow(
                axes.c2p(0, 0),
                axes.c2p(sum_x, sum_y),
                buff=0,
                color=WHITE,
                stroke_width=6
            )
            
            mob.become(VGroup(*new_phasors, new_sum))
        
        all_phasors = VGroup(*phasors, sum_phasor)
        self.play(
            UpdateFromAlphaFunc(all_phasors, update_phasors),
            run_time=animation_duration,
            rate_func=linear
        )
        
        self.wait()
        
        # Mathematical expression
        math_expr = MathTex(
            r"h(t) = \sum_{i=1}^{N} h_i e^{j(\phi_i + 2\pi f_{d,i} t)}",
            font_size=36,
            color=YELLOW
        ).to_edge(DOWN)
        math_box = SurroundingRectangle(math_expr, color=YELLOW, buff=0.2)
        
        self.play(Write(math_expr), Create(math_box))
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def scene_3_4_fading_pattern(self):
        """3.4: The Fading Pattern - Visualizing |h(t)|"""
        
        title = Text("3.4: Time-Varying Channel - The Fading Pattern", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        narration = Text(
            "What does this rotating phasor sum look like over time?",
            font_size=28
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(narration))
        self.wait(2)
        self.play(FadeOut(narration))
        
        # Split view: Phasor diagram and |h(t)| plot
        divider = Line(UP * 3, DOWN * 3, color=WHITE).shift(LEFT * 2)
        
        left_title = Text("Phasor Sum", font_size=28).move_to(LEFT * 4.5 + UP * 2.5)
        right_title = Text("Channel Magnitude |h(t)|", font_size=28).move_to(RIGHT * 2 + UP * 2.5)
        
        self.play(
            Create(divider),
            Write(left_title),
            Write(right_title)
        )
        
        # LEFT: Phasor diagram
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=3,
            y_length=3,
            axis_config={"include_tip": True, "include_numbers": False}
        ).move_to(LEFT * 4.5 + DOWN * 0.3)
        
        axes_labels = axes.get_axis_labels(x_label="Re", y_label="Im")
        self.play(Create(axes), Write(axes_labels))
        
        # RIGHT: Time-domain plot
        time_axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 3, 1],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": True}
        ).move_to(RIGHT * 2 + DOWN * 0.3)
        
        time_labels = time_axes.get_axis_labels(x_label="t", y_label="|h(t)|")
        self.play(Create(time_axes), Write(time_labels))
        
        # Setup multiple phasors
        num_phasors = 6
        np.random.seed(42)
        initial_phases = np.random.uniform(0, 2*PI, num_phasors)
        amplitudes = np.random.uniform(0.3, 0.5, num_phasors)
        doppler_freqs = np.random.uniform(0.1, 0.5, num_phasors)
        
        colors_list = [BLUE, GREEN, YELLOW, RED, PURPLE, ORANGE]
        
        # Create initial phasors
        phasors = VGroup()
        for i in range(num_phasors):
            phasor = Arrow(
                axes.c2p(0, 0),
                axes.c2p(
                    amplitudes[i] * np.cos(initial_phases[i]),
                    amplitudes[i] * np.sin(initial_phases[i])
                ),
                buff=0,
                color=colors_list[i % len(colors_list)],
                stroke_width=3,
                stroke_opacity=0.6
            )
            phasors.add(phasor)
        
        self.play(Create(phasors), run_time=1)
        
        # Initial sum phasor
        sum_x = sum(amplitudes[i] * np.cos(initial_phases[i]) for i in range(num_phasors))
        sum_y = sum(amplitudes[i] * np.sin(initial_phases[i]) for i in range(num_phasors))
        
        sum_phasor = Arrow(
            axes.c2p(0, 0),
            axes.c2p(sum_x, sum_y),
            buff=0,
            color=WHITE,
            stroke_width=6
        )
        self.play(Create(sum_phasor))
        self.wait()
        
        # Trace for fading envelope
        fade_trace = VGroup()
        time_points = []
        magnitude_points = []
        
        # Animation
        animation_duration = 10
        dt = 0.1
        num_steps = int(animation_duration / dt)
        
        for step in range(num_steps):
            t = step * dt
            
            # Calculate new phasor positions
            sum_x = 0
            sum_y = 0
            
            new_phasors = VGroup()
            for i in range(num_phasors):
                phase = initial_phases[i] + 2 * PI * doppler_freqs[i] * t
                x = amplitudes[i] * np.cos(phase)
                y = amplitudes[i] * np.sin(phase)
                sum_x += x
                sum_y += y
                
                new_phasor = Arrow(
                    axes.c2p(0, 0),
                    axes.c2p(x, y),
                    buff=0,
                    color=colors_list[i % len(colors_list)],
                    stroke_width=3,
                    stroke_opacity=0.6
                )
                new_p