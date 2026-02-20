from manim import *
import numpy as np

class SignalDegradation(Scene):
    """Animation 1: Signal Degradation Overview"""
    
    def construct(self):
        title = Text("Wireless Signal Propagation", font_size=48, weight=BOLD)
        subtitle = Text("WiFi Through Space", font_size=32)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))


        intro_text = Text("Wireless Signal Degradation", font_size=36)
        self.play(Write(intro_text))
        self.wait(1)
        self.play(intro_text.animate.to_edge(UP))

        
        self.wait(1)
        
        # Load SVG images for transmitter and receiver
        try:
            transmitter = SVGMobject("tower.svg").scale(0.8)
        except:
            # Fallback if SVG not found
            transmitter = VGroup(
                Triangle(color=GREEN, fill_opacity=1).scale(0.5).rotate(PI/2),
                Rectangle(height=0.8, width=0.2, color=GREEN, fill_opacity=0.8)
            ).arrange(DOWN, buff=0.1)
        
        transmitter.to_edge(LEFT, buff=1).shift(DOWN * 0.5)
        
        try:
            receiver = SVGMobject("mobile.svg").scale(0.6)
        except:
            # Fallback if SVG not found
            receiver = VGroup(
                Rectangle(height=0.8, width=0.5, color=BLUE, fill_opacity=0.5, stroke_color=BLUE),
                Circle(radius=0.15, color=BLUE, fill_opacity=1).shift(DOWN * 0.5)
            )
        
        receiver.to_edge(RIGHT, buff=1).shift(DOWN * 0.5)
        
        tx_label = Text("Tower", font_size=22).next_to(transmitter, DOWN, buff=0.2)
        rx_label = Text("Mobile", font_size=22).next_to(receiver, DOWN, buff=0.2)
        
        self.play(
            FadeIn(transmitter, scale=1.5),
            FadeIn(receiver, scale=1.5),
            Write(tx_label),
            Write(rx_label)
        )
        self.wait(0.5)
        
        # Create the signal path
        signal_path = Line(
            transmitter.get_right() + RIGHT * 0.3,
            receiver.get_left() + LEFT * 0.3
        )
        
        # Function to create wave with PROGRESSIVE degradation
        def create_degrading_wave(progress, wave_position):
            # wave_position controls how far the wave has traveled (0 to 1)
            # progress controls overall time/animation progress
            
            start_point = signal_path.get_start()
            end_point = signal_path.get_end()
            
            points = []
            num_points = 200
            
            for i in range(num_points):
                t = i / num_points
                
                # Only draw wave up to current position
                if t > wave_position:
                    break
                
                base_pos = start_point + t * (end_point - start_point)
                
                # Degradation increases with distance traveled (t value)
                # Early in path: clean signal
                # Later in path: degraded signal
                local_progress = t  # Degradation based on distance
                
                amplitude = 0.5 * (1 - 0.7 * local_progress)  # Decreases with distance
                frequency = 2 + local_progress * 1.5  # Increases (distortion)
                noise_level = local_progress * 0.35  # Increases with distance
                
                # Color changes based on distance
                color = interpolate_color(GREEN, RED, local_progress)
                
                # Add sinusoidal oscillation with phase shifting
                phase = t * frequency * 2 * PI + progress * 2 * PI  # Moving wave
                noise = np.random.normal(0, noise_level) if local_progress > 0.25 else 0
                offset = (amplitude + noise) * np.sin(phase)
                
                # Perpendicular direction for wave
                direction = rotate_vector(
                    (end_point - start_point) / np.linalg.norm(end_point - start_point),
                    PI/2
                )
                
                point = base_pos + offset * direction
                points.append(point)
            
            if len(points) < 2:
                # Return invisible wave if too short
                wave = VMobject(stroke_width=0)
                wave.set_points_as_corners([start_point, start_point])
                return wave
            
            wave = VMobject(stroke_width=4)
            wave.set_points_smoothly(points)
            
            # Apply gradient color along the wave
            wave.set_color_by_gradient(GREEN, YELLOW, ORANGE, RED)
            
            return wave
        
        # Progress tracker for wave position (0 to 1)
        wave_position_tracker = ValueTracker(0)
        progress_tracker = ValueTracker(0)
        
        # Create distance markers
        distances = VGroup()
        for i in range(4):
            marker = VGroup(
                Line(UP * 0.2, DOWN * 0.2, color=GRAY),
                Text(f"{i*3}m", font_size=20, color=GRAY).shift(DOWN * 0.4)
            )
            pos = signal_path.point_from_proportion(i / 3)
            marker.move_to(pos)
            distances.add(marker)
        
        self.play(FadeIn(distances))
        
        # Signal strength indicator - FIXED ALIGNMENT
        strength_bar = Rectangle(height=0.3, width=3, color=WHITE, stroke_width=3, fill_opacity=0)
        strength_bar.to_edge(DOWN, buff=0.8)
        
        strength_fill = Rectangle(height=0.3, width=3, color=GREEN, fill_opacity=0.8, stroke_width=0)
        strength_fill.move_to(strength_bar.get_center())  # Center alignment first
        strength_fill.align_to(strength_bar, LEFT)  # Then align to left edge
        
        strength_label = Text("Signal Strength", font_size=24).next_to(strength_bar, UP, buff=0.2)
        
        self.play(
            Create(strength_bar),
            FadeIn(strength_fill),
            Write(strength_label)
        )
        
        # Animate signal propagation with PROGRESSIVE degradation
        def update_wave(mob):
            new_wave = create_degrading_wave(
                progress_tracker.get_value(),
                wave_position_tracker.get_value()
            )
            mob.become(new_wave)
        
        def update_strength(mob):
            wave_pos = wave_position_tracker.get_value()
            remaining_strength = 1 - 0.8 * wave_pos
            new_width = max(0.1, 3 * remaining_strength)  # Prevent zero width
            new_fill = Rectangle(
                height=0.3, 
                width=new_width, 
                color=interpolate_color(GREEN, RED, wave_pos),
                fill_opacity=0.8,
                stroke_width=0
            )
            # Properly align the fill bar
            new_fill.move_to(strength_bar.get_center())
            new_fill.align_to(strength_bar, LEFT)
            mob.become(new_fill)
        
        # Create initial wave (empty at start)
        wave = create_degrading_wave(0, 0)
        wave.add_updater(update_wave)
        strength_fill.add_updater(update_strength)
        
        self.add(wave)
        
        # Animate wave traveling and degrading simultaneously
        self.play(
            wave_position_tracker.animate.set_value(1),
            progress_tracker.animate.set_value(3),  # More cycles for wave movement
            run_time=10,
            rate_func=linear
        )
        
        wave.clear_updaters()
        strength_fill.clear_updaters()
        self.play(FadeOut(distances))
        self.wait(5)
        
        # Add impairment labels
        impairments = VGroup(
            Text("• Path Loss", font_size=28, color=WHITE),
            Text("• Distortion", font_size=28, color=WHITE),
            Text("• Noise", font_size=28, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        impairments.to_corner(UR, buff=0.5)
        
        self.play(FadeIn(impairments, shift=LEFT, lag_ratio=0.3))
        self.wait(4)


from manim import *

class IdealVsReal(Scene):
    """Animation 2: Ideal vs Real World Comparison"""
    
    def construct(self):
        # Title - Use Tex instead of Text
        title = Tex("Ideal vs Real World Propagation", font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3))
        
        # Create split screen divider
        divider = Line(UP * 3.5, DOWN * 3.5, color=WHITE, stroke_width=2)
        
        # Labels - Use Tex
        ideal_label = Tex("IDEAL", font_size=36, color=GREEN).move_to(LEFT * 3 + UP * 2.5)
        real_label = Tex("REAL WORLD", font_size=36, color=RED).move_to(RIGHT * 3 + UP * 2.5)
        
        self.play(
            Create(divider),
            Write(ideal_label),
            Write(real_label)
        )
        self.wait(0.5)
        
        # ===== IDEAL SIDE =====
        tx_ideal = Triangle(color=GREEN, fill_opacity=1).scale(0.4).rotate(PI/2)
        tx_ideal.move_to(LEFT * 5 + UP * 0.5)
        
        rx_ideal = Triangle(color=GREEN, fill_opacity=1).scale(0.4).rotate(-PI/2)
        rx_ideal.move_to(LEFT * 1 + UP * 0.5)
        
        ideal_arrow = Arrow(
            tx_ideal.get_right(),
            rx_ideal.get_left(),
            color=GREEN,
            stroke_width=6,
            buff=0.2
        )
        
        # Perfect wave
        def create_perfect_wave():
            points = []
            for t in np.linspace(0, 1, 100):
                pos = ideal_arrow.point_from_proportion(t)
                offset = 0.3 * np.sin(t * 4 * 2 * PI)
                direction = rotate_vector(
                    normalize(ideal_arrow.get_end() - ideal_arrow.get_start()),
                    PI/2
                )
                points.append(pos + offset * direction)
            
            wave = VMobject(color=GREEN, stroke_width=3)
            wave.set_points_smoothly(points)
            return wave
        
        ideal_wave = create_perfect_wave()
        
        # Amplitude indicator (ideal)
        ideal_amp = VGroup(
            Line(ORIGIN, UP * 0.3, color=GREEN),
            Line(ORIGIN, DOWN * 0.3, color=GREEN),
            DoubleArrow(DOWN * 0.3, UP * 0.3, color=GREEN, buff=0, stroke_width=2)
        ).move_to(LEFT * 3 + UP * 0.5)
        ideal_amp_label = Tex("Constant", font_size=20, color=GREEN).next_to(ideal_amp, DOWN, buff=0.2)
        
        # ===== REAL WORLD SIDE =====
        tx_real = Triangle(color=RED, fill_opacity=1).scale(0.4).rotate(PI/2)
        tx_real.move_to(RIGHT * 1 + UP * 0.5)
        
        rx_real = Triangle(color=RED, fill_opacity=1).scale(0.4).rotate(-PI/2)
        rx_real.move_to(RIGHT * 5 + UP * 0.5)
        
        # Add obstacles
        obstacles = VGroup(
            Rectangle(height=1.5, width=0.3, color=GRAY, fill_opacity=0.8),
            Circle(radius=0.4, color=GRAY, fill_opacity=0.6),
            Rectangle(height=0.8, width=0.4, color=GRAY, fill_opacity=0.7)
        )
        obstacles[0].move_to(RIGHT * 2 + UP * 0.8)
        obstacles[1].move_to(RIGHT * 3.2 + DOWN * 0.3)
        obstacles[2].move_to(RIGHT * 4.3 + UP * 0.2)
        
        obstacle_labels = VGroup(
            Tex("Wall", font_size=16, color=GRAY),
            Tex("Person", font_size=16, color=GRAY),
            Tex("Furniture", font_size=16, color=GRAY)
        )
        obstacle_labels[0].next_to(obstacles[0], DOWN, buff=0.1)
        obstacle_labels[1].next_to(obstacles[1], DOWN, buff=0.1)
        obstacle_labels[2].next_to(obstacles[2], DOWN, buff=0.1)
        
        # Complex signal path
        real_path = VMobject(color=ORANGE, stroke_width=3)
        real_points = []
        for i, t in enumerate(np.linspace(0, 1, 50)):
            base_x = tx_real.get_right()[0] + t * (rx_real.get_left()[0] - tx_real.get_right()[0])
            base_y = tx_real.get_right()[1]
            
            y_offset = 0.5 * np.sin(t * 6 * PI) + np.random.normal(0, 0.1)
            
            for obs in obstacles:
                obs_x = obs.get_center()[0]
                distance = abs(base_x - obs_x)
                if distance < 0.5:
                    y_offset += 0.3 * np.exp(-distance * 2)
            
            real_points.append([base_x, base_y + y_offset, 0])
        
        real_path.set_points_smoothly(real_points)
        
        # Varying amplitude indicator
        real_amps = VGroup()
        for i, pos in enumerate([0.2, 0.5, 0.8]):
            scale = 1 - pos * 0.6 + np.random.uniform(-0.2, 0.1)
            amp = DoubleArrow(
                DOWN * 0.3 * scale, 
                UP * 0.3 * scale, 
                color=interpolate_color(ORANGE, RED, pos),
                buff=0,
                stroke_width=2
            )
            point = real_path.point_from_proportion(pos)
            amp.move_to([point[0], 0.5, 0]) 
            # amp.move_to([point[0], UP * 0.5, 0])
            real_amps.add(amp)
        
        real_amp_label = Tex("Varying", font_size=20, color=RED).move_to(RIGHT * 3 + DOWN * 1.5)
        
        # Animate ideal side first
        self.play(
            FadeIn(tx_ideal, scale=1.5),
            FadeIn(rx_ideal, scale=1.5)
        )
        self.play(GrowArrow(ideal_arrow))
        self.play(Create(ideal_wave), run_time=2)
        self.play(
            Create(ideal_amp),
            Write(ideal_amp_label)
        )
        
        self.wait(0.5)
        
        # Animate real world side
        self.play(
            FadeIn(tx_real, scale=1.5),
            FadeIn(rx_real, scale=1.5)
        )
        self.play(
            FadeIn(obstacles, lag_ratio=0.2),
            FadeIn(obstacle_labels, lag_ratio=0.2)
        )
        self.play(Create(real_path), run_time=3, rate_func=linear)
        self.play(
            Create(real_amps, lag_ratio=0.3),
            Write(real_amp_label)
        )
        
        self.wait(1)
        
        # Add comparison annotations
        ideal_box = SurroundingRectangle(
            VGroup(tx_ideal, ideal_wave, rx_ideal),
            color=GREEN,
            buff=0.3
        )
        real_box = SurroundingRectangle(
            VGroup(tx_real, obstacles, rx_real),
            color=RED,
            buff=0.3
        )
        
        # Multi-line text using VGroup of Tex objects
        ideal_note = VGroup(
            Tex(r"$\checkmark$ No loss", font_size=20, color=GREEN),
            Tex(r"$\checkmark$ No interference", font_size=20, color=GREEN),
            Tex(r"$\checkmark$ Direct path", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        ideal_note.next_to(ideal_box, DOWN, buff=0.3)
        
        real_note = VGroup(
            Tex(r"$\times$ Path loss", font_size=20, color=RED),
            Tex(r"$\times$ Multipath", font_size=20, color=RED),
            Tex(r"$\times$ Shadowing", font_size=20, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        real_note.next_to(real_box, DOWN, buff=0.3)
        
        self.play(
            Create(ideal_box),
            Create(real_box)
        )
        self.play(
            FadeIn(ideal_note, shift=UP),
            FadeIn(real_note, shift=UP)
        )
        
        self.wait(3)