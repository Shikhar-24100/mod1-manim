from manim import *

class IdealVsReal(Scene):
    """Animation 2: Ideal vs Real World Comparison"""
    
    def construct(self):
        # Title - Use Tex instead of Text
        intro_text = Text("Ideal vs Real World Propagation", font_size=36)
        self.play(Write(intro_text))
        self.wait(1)
        self.play(intro_text.animate.to_edge(UP))
        
        # Create enhanced split screen divider with gradient effect
        # divider = VGroup(
        #     Line(UP * 3.5, DOWN * 3.5, color=BLUE_C, stroke_width=3),
        #     DashedLine(UP * 3.5, DOWN * 3.5, color=BLUE_B, stroke_width=1, dash_length=0.1)
        # )
        
        # Labels - Use Tex with better styling
        ideal_label = Tex("IDEAL", font_size=36, color=GREEN).move_to(LEFT * 3.5 + UP * 2.5)
        real_label = Tex("REAL WORLD", font_size=36, color=RED).move_to(RIGHT * 3 + UP * 2.5)
        
        self.play(
            # Create(divider),
            Write(ideal_label),
            Write(real_label)
        )
        self.wait(0.5)
        
        # ===== IDEAL SIDE =====
        # Load SVG icons
        tx_ideal = SVGMobject("tower.svg").scale(0.5)
        # tx_ideal.set_color(GREEN)
        tx_ideal.move_to(LEFT * 5 + UP * 0.5)
        
        rx_ideal = SVGMobject("mobile.svg").scale(0.5)
        # rx_ideal.set_color(GREEN)
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
        
        ideal_box = SurroundingRectangle(
            VGroup(tx_ideal, ideal_wave, rx_ideal),
            color=GREEN,
            buff=0.3
        )
        
        ideal_note = VGroup(
            Tex(r"$\checkmark$ No loss", font_size=20, color=GREEN),
            Tex(r"$\checkmark$ No interference", font_size=20, color=GREEN),
            Tex(r"$\checkmark$ Direct path", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        ideal_note.next_to(ideal_box, DOWN, buff=0.3)

        


        # ===== REAL WORLD SIDE =====
        tx_real = SVGMobject("tower.svg").scale(0.5)
        # tx_real.set_color(RED)
        tx_real.move_to(RIGHT * 0.5 + UP * 0.5)
        
        rx_real = SVGMobject("mobile.svg").scale(0.5)
        # rx_real.set_color(RED)
        rx_real.move_to(RIGHT * 5.5 + UP * 1)
        
        # Add obstacles using SVG files
        building = SVGMobject("building.svg").scale(0.6)
        # building.set_color(GRAY)
        building.move_to(RIGHT * 2 + UP * 0.8)
        
        person = SVGMobject("person.svg").scale(0.5)
        # person.set_color(GRAY)
        person.move_to(RIGHT * 3.2 + DOWN * 0.3)
        
        trees = SVGMobject("trees.svg").scale(0.5)
        # trees.set_color(GRAY)
        trees.move_to(RIGHT * 4.3 + UP * 0.2)
        
        obstacles = VGroup(building, person, trees)
        
        obstacle_labels = VGroup(
            Tex("Building", font_size=16, color=GRAY),
            Tex("Person", font_size=16, color=GRAY),
            Tex("Trees", font_size=16, color=GRAY)
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
            real_amps.add(amp)
        
        # real_amp_label = Tex("Varying", font_size=20, color=RED).move_to(RIGHT * 3 + DOWN * 1.5)
        
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

        self.play(
            FadeIn(ideal_note, shift=UP)
            # FadeIn(real_note, shift=UP)
        )

        self.wait(10)
        
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
            # Write(real_amp_label)
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
            # FadeIn(ideal_note, shift=UP),
            FadeIn(real_note, shift=UP)
        )
        self.play(
            Create(ideal_box),
            Create(real_box)
        )
        
        self.wait(10)