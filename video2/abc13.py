from manim import *
import numpy as np

class FadingDistributionsScene(Scene):
    def construct(self):
        # ============================================
        # TITLE
        # ============================================
        title = Text("Fading Distributions", font_size=44, weight=BOLD, color=BLUE)
        title.to_edge(UP, buff=0.5)
        subtitle = Text('"When does your signal disappear?"', 
                       font_size=28, color=YELLOW, slant=ITALIC)
        subtitle.next_to(title, DOWN, buff=0.2)
        
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(subtitle, shift=DOWN*0.2), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(subtitle), run_time=0.4)
        
        # ============================================
        # PART A: MANY RANDOM PHASORS (~40 sec)
        # ============================================
        
        scenario_text = Text("Scenario: No Line-of-Sight (NLOS)", 
                           font_size=30, color=ORANGE, weight=BOLD)
        scenario_text.next_to(title, DOWN, buff=0.4)
        
        self.play(FadeIn(scenario_text, shift=DOWN*0.2), run_time=0.6)
        self.wait(0.4)
        
        # Create environment illustration on the left
        env_center = LEFT * 4.5 + DOWN * 0.3
        
        # Phone and tower with building blocking
        phone = SVGMobject("mobile.svg").scale(0.4).move_to(env_center + DOWN * 1.2)
        tower = SVGMobject("tower.svg").scale(0.5).move_to(env_center + UP * 1.5 + RIGHT * 1.5)
        building = SVGMobject("building.svg").scale(0.6).move_to(env_center + UP * 0.3 + RIGHT * 0.5)
        
        # X mark showing blocked LOS
        x_mark = VGroup(
            Line(LEFT*0.3 + UP*0.3, RIGHT*0.3 + DOWN*0.3, color=RED, stroke_width=6),
            Line(LEFT*0.3 + DOWN*0.3, RIGHT*0.3 + UP*0.3, color=RED, stroke_width=6)
        ).move_to(building.get_center() + LEFT * 0.3)
        
        nlos_label = Text("No LOS!", font_size=18, color=RED, weight=BOLD)
        nlos_label.next_to(x_mark, LEFT, buff=0.2)
        
        self.play(
            FadeIn(phone),
            FadeIn(tower),
            FadeIn(building),
            run_time=0.8
        )
        self.play(Create(x_mark), Write(nlos_label), run_time=0.5)
        self.wait(0.3)
        
        # Show multiple scattered paths
        scatter_paths = VGroup()
        for i in range(5):
            angle = -90 + i * 30
            path = DashedLine(
                tower.get_bottom(),
                phone.get_top() + np.array([0.3*np.cos(angle*DEGREES), 0.3*np.sin(angle*DEGREES), 0]),
                color=YELLOW,
                stroke_width=2,
                dash_length=0.1
            )
            scatter_paths.add(path)
        
        self.play(LaggedStart(*[Create(path) for path in scatter_paths], lag_ratio=0.15), run_time=1.0)
        self.wait(0.3)
        
        paths_text = Text("Many paths,\nrandom phases", font_size=20, color=YELLOW)
        paths_text.next_to(phone, DOWN, buff=0.3)
        self.play(FadeIn(paths_text, shift=UP*0.2), run_time=0.5)
        self.wait(0.5)
        
        # ============================================
        # PHASOR CIRCLE WITH MANY RANDOM PHASORS
        # ============================================
        
        phasor_center = RIGHT * 3 + UP * 0.8
        circle_radius = 1.8
        
        phasor_circle = Circle(radius=circle_radius, color=WHITE, stroke_width=3)
        phasor_circle.move_to(phasor_center)
        
        phasor_label = Text("Phasor Diagram", font_size=22, weight=BOLD)
        phasor_label.next_to(phasor_circle, UP, buff=0.3)
        
        self.play(Create(phasor_circle), Write(phasor_label), run_time=0.6)
        self.wait(0.3)
        
        # Create 12 random phasors
        np.random.seed(42)
        num_phasors = 12
        phasors = VGroup()
        phasor_colors = [RED, BLUE, GREEN, ORANGE, PURPLE, PINK, TEAL, MAROON, 
                        GOLD, LIGHT_BROWN, LIGHT_PINK, GRAY_BROWN]
        
        angles = np.random.uniform(0, 2*PI, num_phasors)
        magnitudes = np.random.uniform(0.3, 0.8, num_phasors) * circle_radius
        
        for i in range(num_phasors):
            endpoint = phasor_center + magnitudes[i] * np.array([
                np.cos(angles[i]), np.sin(angles[i]), 0
            ])
            phasor = Arrow(
                phasor_center, endpoint,
                color=phasor_colors[i % len(phasor_colors)],
                buff=0,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.12
            )
            phasors.add(phasor)
        
        self.play(
            LaggedStart(*[GrowArrow(p) for p in phasors], lag_ratio=0.08),
            run_time=2.0
        )
        self.wait(0.5)
        
        # ============================================
        # TIP-TO-TAIL ADDITION
        # ============================================
        
        addition_text = Text("Adding tip-to-tail...", font_size=24, color=YELLOW)
        addition_text.move_to(RIGHT * 3 + DOWN * 2.5)
        self.play(FadeIn(addition_text, shift=UP*0.2), run_time=0.5)
        
        # Calculate cumulative sum for tip-to-tail
        cumulative_pos = phasor_center
        translated_phasors = VGroup()
        
        for i, phasor in enumerate(phasors):
            vector = phasor.get_end() - phasor.get_start()
            new_phasor = Arrow(
                cumulative_pos,
                cumulative_pos + vector,
                color=phasor.get_color(),
                buff=0,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.12
            )
            translated_phasors.add(new_phasor)
            cumulative_pos = cumulative_pos + vector
        
        # Animate transformation to tip-to-tail
        self.play(
            *[Transform(phasors[i], translated_phasors[i]) for i in range(num_phasors)],
            run_time=1.5
        )
        self.wait(0.3)
        
        # Show resultant
        resultant_endpoint = cumulative_pos
        resultant = Arrow(
            phasor_center, resultant_endpoint,
            color=YELLOW,
            buff=0,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15
        )
        
        resultant_label = Text("Resultant", font_size=20, color=YELLOW, weight=BOLD)
        resultant_label.next_to(resultant.get_center(), UP, buff=0.1)
        
        self.play(
            GrowArrow(resultant),
            Write(resultant_label),
            phasors.animate.set_opacity(0.3),
            run_time=0.8
        )
        self.wait(0.5)
        
        # Show amplitude (length of resultant)
        resultant_length = np.linalg.norm(resultant_endpoint - phasor_center)
        amplitude_value = Text(f"Amplitude: {resultant_length:.2f}", 
                             font_size=20, color=YELLOW)
        amplitude_value.next_to(addition_text, DOWN, buff=0.2)
        
        self.play(Write(amplitude_value), run_time=0.5)
        self.wait(0.5)
        
        # Animate fluctuation
        fluctuate_text = Text("Amplitude fluctuates!", font_size=22, color=RED, slant=ITALIC)
        fluctuate_text.next_to(amplitude_value, DOWN, buff=0.3)
        self.play(FadeIn(fluctuate_text, shift=UP*0.2), run_time=0.5)
        
        # Show 3 different random configurations
        for iteration in range(3):
            new_angles = np.random.uniform(0, 2*PI, num_phasors)
            new_magnitudes = np.random.uniform(0.3, 0.8, num_phasors) * circle_radius
            
            new_cumulative = phasor_center
            new_translated = VGroup()
            
            for i in range(num_phasors):
                vector = new_magnitudes[i] * np.array([
                    np.cos(new_angles[i]), np.sin(new_angles[i]), 0
                ])
                new_phasor = Arrow(
                    new_cumulative,
                    new_cumulative + vector,
                    color=phasor_colors[i % len(phasor_colors)],
                    buff=0,
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.12
                )
                new_translated.add(new_phasor)
                new_cumulative = new_cumulative + vector
            
            new_resultant = Arrow(
                phasor_center, new_cumulative,
                color=YELLOW,
                buff=0,
                stroke_width=8,
                max_tip_length_to_length_ratio=0.15
            )
            
            new_length = np.linalg.norm(new_cumulative - phasor_center)
            new_amplitude_value = Text(f"Amplitude: {new_length:.2f}", 
                                      font_size=20, color=YELLOW)
            new_amplitude_value.move_to(amplitude_value.get_center())
            
            self.play(
                *[Transform(phasors[i], new_translated[i]) for i in range(num_phasors)],
                Transform(resultant, new_resultant),
                Transform(amplitude_value, new_amplitude_value),
                run_time=0.8
            )
            self.wait(0.4)
        
        self.wait(0.8)
        
        # ============================================
        # TRANSITION TO RAYLEIGH DISTRIBUTION
        # ============================================
        
        self.play(
            *[FadeOut(mob) for mob in [
                scenario_text, phone, tower, building, x_mark, nlos_label,
                scatter_paths, paths_text, phasor_circle, phasor_label,
                phasors, resultant, resultant_label, addition_text,
                amplitude_value, fluctuate_text
            ]],
            run_time=0.8
        )
        
        # ============================================
        # PART B: RAYLEIGH DISTRIBUTION (~30 sec)
        # ============================================
        
        rayleigh_title = Text("Rayleigh Fading Distribution", 
                            font_size=34, color=GREEN, weight=BOLD)
        rayleigh_title.next_to(title, DOWN, buff=0.4)
        
        self.play(Write(rayleigh_title), run_time=0.7)
        self.wait(0.4)
        
        # Create Rayleigh PDF plot
        axes = Axes(
            x_range=[0, 3, 0.5],
            y_range=[0, 0.7, 0.1],
            x_length=6,
            y_length=3.5,
            axis_config={"include_tip": True, "include_numbers": False},
        ).shift(DOWN * 0.5)
        
        x_label = Text("Signal Amplitude (r)", font_size=22).next_to(axes.x_axis, DOWN)
        y_label = Text("Probability", font_size=22).next_to(axes.y_axis, LEFT).rotate(90*DEGREES)
        
        # Rayleigh PDF: f(r) = (r/σ²)exp(-r²/2σ²)
        sigma = 1.0
        rayleigh_curve = axes.plot(
            lambda r: (r / sigma**2) * np.exp(-r**2 / (2 * sigma**2)),
            x_range=[0.01, 3],
            color=GREEN,
            stroke_width=5
        )
        
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            run_time=1.0
        )
        self.play(Create(rayleigh_curve), run_time=1.2)
        self.wait(0.5)
        
        # Highlight key features
        # Peak location
        peak_r = sigma  # Peak at r = σ
        peak_point = axes.c2p(peak_r, (peak_r / sigma**2) * np.exp(-peak_r**2 / (2 * sigma**2)))
        peak_dot = Dot(peak_point, color=YELLOW, radius=0.08)
        peak_label = Text("Most likely\namplitude", font_size=18, color=YELLOW)
        peak_label.next_to(peak_dot, UP + RIGHT, buff=0.2)
        peak_arrow = Arrow(peak_label.get_bottom(), peak_dot.get_center(), 
                          color=YELLOW, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        
        self.play(
            FadeIn(peak_dot),
            GrowArrow(peak_arrow),
            Write(peak_label),
            run_time=0.8
        )
        self.wait(0.5)
        
        # Low probability regions
        # Very weak signals
        weak_region = axes.get_area(
            rayleigh_curve,
            x_range=[0, 0.3],
            color=RED,
            opacity=0.4
        )
        weak_label = Text("Rare:\nVery weak", font_size=18, color=RED)
        weak_label.move_to(axes.c2p(0.15, 0.4))
        
        self.play(FadeIn(weak_region), Write(weak_label), run_time=0.7)
        self.wait(0.4)
        
        # Very strong signals
        strong_region = axes.get_area(
            rayleigh_curve,
            x_range=[2.5, 3],
            color=RED,
            opacity=0.4
        )
        strong_label = Text("Rare:\nVery strong", font_size=18, color=RED)
        strong_label.move_to(axes.c2p(2.7, 0.15))
        
        self.play(FadeIn(strong_region), Write(strong_label), run_time=0.7)
        self.wait(0.4)
        
        # Medium region (most common)
        medium_region = axes.get_area(
            rayleigh_curve,
            x_range=[0.5, 2],
            color=GREEN,
            opacity=0.3
        )
        medium_label = Text("Common:\nMedium signal", font_size=20, color=GREEN, weight=BOLD)
        medium_label.move_to(axes.c2p(1.3, 0.45))
        
        self.play(FadeIn(medium_region), Write(medium_label), run_time=0.8)
        self.wait(0.6)
        
        # Key insight box
        insight_box = VGroup(
            Text("NLOS Environment", font_size=22, color=ORANGE, weight=BOLD),
            Text("→ Rayleigh distributed amplitude", font_size=20, color=WHITE),
            Text("→ Unpredictable fading", font_size=20, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        insight_box.to_corner(UR, buff=0.5)
        
        box_rect = SurroundingRectangle(insight_box, color=ORANGE, buff=0.2, corner_radius=0.1)
        
        self.play(
            FadeIn(box_rect),
            Write(insight_box),
            run_time=1.0
        )
        self.wait(1.2)
        
        # ============================================
        # TRANSITION TO RICIAN
        # ============================================
        
        self.play(
            *[FadeOut(mob) for mob in [
                rayleigh_title, axes, x_label, y_label, rayleigh_curve,
                peak_dot, peak_label, peak_arrow, weak_region, weak_label,
                strong_region, strong_label, medium_region, medium_label,
                insight_box, box_rect
            ]],
            run_time=0.8
        )
        
        # ============================================
        # PART C: RICIAN DISTRIBUTION (~20 sec)
        # ============================================
        
        rician_title = Text("Rician Fading: LOS + Scatter", 
                          font_size=34, color=BLUE, weight=BOLD)
        rician_title.next_to(title, DOWN, buff=0.4)
        
        self.play(Write(rician_title), run_time=0.7)
        self.wait(0.4)
        
        # Left side: Environment with LOS
        env_center2 = LEFT * 4 + DOWN * 0.3
        
        phone2 = SVGMobject("mobile.svg").scale(0.4).move_to(env_center2 + DOWN * 1)
        tower2 = SVGMobject("tower.svg").scale(0.5).move_to(env_center2 + UP * 1.2 + RIGHT * 1)
        
        # Strong LOS path
        los_path = Line(tower2.get_bottom(), phone2.get_top(), 
                       color=GREEN, stroke_width=6)
        los_label = Text("Strong LOS", font_size=18, color=GREEN, weight=BOLD)
        los_label.next_to(los_path, LEFT, buff=0.2)
        
        self.play(
            FadeIn(phone2),
            FadeIn(tower2),
            run_time=0.6
        )
        self.play(Create(los_path), Write(los_label), run_time=0.6)
        self.wait(0.3)
        
        # Add scattered paths
        scatter_paths2 = VGroup()
        for i in range(4):
            angle = -110 + i * 20
            path = DashedLine(
                tower2.get_bottom(),
                phone2.get_top() + 0.2*np.array([np.cos(angle*DEGREES), np.sin(angle*DEGREES), 0]),
                color=YELLOW,
                stroke_width=2,
                dash_length=0.1
            )
            scatter_paths2.add(path)
        
        scatter_label = Text("+ scatter", font_size=16, color=YELLOW)
        scatter_label.next_to(phone2, DOWN, buff=0.3)
        
        self.play(
            LaggedStart(*[Create(path) for path in scatter_paths2], lag_ratio=0.2),
            Write(scatter_label),
            run_time=0.8
        )
        self.wait(0.4)
        
        # Right side: Phasor diagram
        phasor_center2 = RIGHT * 3.5 + DOWN * 0.3
        circle_radius2 = 2.0
        
        phasor_circle2 = Circle(radius=circle_radius2, color=WHITE, stroke_width=3)
        phasor_circle2.move_to(phasor_center2)
        
        self.play(Create(phasor_circle2), run_time=0.5)
        self.wait(0.2)
        
        # ONE LARGE LOS phasor
        los_phasor = Arrow(
            phasor_center2,
            phasor_center2 + RIGHT * circle_radius2 * 0.85,
            color=GREEN,
            buff=0,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.12
        )
        los_phasor_label = Text("LOS", font_size=18, color=GREEN, weight=BOLD)
        los_phasor_label.next_to(los_phasor, DOWN, buff=0.1)
        
        self.play(GrowArrow(los_phasor), Write(los_phasor_label), run_time=0.6)
        self.wait(0.3)
        
        # Many small random scattered phasors
        num_scatter = 8
        scatter_phasors = VGroup()
        scatter_angles = np.random.uniform(0, 2*PI, num_scatter)
        scatter_mags = np.random.uniform(0.15, 0.35, num_scatter) * circle_radius2
        
        for i in range(num_scatter):
            endpoint = phasor_center2 + scatter_mags[i] * np.array([
                np.cos(scatter_angles[i]), np.sin(scatter_angles[i]), 0
            ])
            phasor = Arrow(
                phasor_center2, endpoint,
                color=YELLOW,
                buff=0,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )
            scatter_phasors.add(phasor)
        
        self.play(
            LaggedStart(*[GrowArrow(p) for p in scatter_phasors], lag_ratio=0.1),
            run_time=1.0
        )
        self.wait(0.4)
        
        # Show resultant (dominated by LOS)
        # Calculate with LOS + scatter
        scatter_sum = np.array([0.0, 0.0, 0.0])
        for i in range(num_scatter):
            scatter_sum += scatter_mags[i] * np.array([
                np.cos(scatter_angles[i]), np.sin(scatter_angles[i]), 0
            ])
        
        resultant_rician = Arrow(
            phasor_center2,
            phasor_center2 + (los_phasor.get_end() - phasor_center2) + scatter_sum,
            color=BLUE,
            buff=0,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15
        )
        
        self.play(
            los_phasor.animate.set_opacity(0.4),
            scatter_phasors.animate.set_opacity(0.4),
            los_phasor_label.animate.set_opacity(0.4),
            run_time=0.4
        )
        self.play(GrowArrow(resultant_rician), run_time=0.7)
        self.wait(0.4)
        
        # Stability annotation
        stable_text = VGroup(
            Text("More stable!", font_size=24, color=BLUE, weight=BOLD),
            Text("Less fading", font_size=20, color=GREEN)
        ).arrange(DOWN, buff=0.1)
        stable_text.next_to(phasor_circle2, DOWN, buff=0.5)
        
        self.play(Write(stable_text), run_time=0.7)
        self.wait(0.5)
        
        # ============================================
        # COMPARISON TABLE
        # ============================================
        
        comparison_title = Text("Quick Comparison:", font_size=28, color=YELLOW, weight=BOLD)
        comparison_title.move_to(UP * 2.5)
        
        comparison_table = VGroup(
            VGroup(
                Text("Rayleigh (NLOS)", font_size=22, color=GREEN, weight=BOLD),
                Text("• No dominant path", font_size=18, color=WHITE),
                Text("• High fading", font_size=18, color=RED),
                Text("• Unpredictable", font_size=18, color=RED)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            VGroup(
                Text("Rician (LOS)", font_size=22, color=BLUE, weight=BOLD),
                Text("• Strong LOS path", font_size=18, color=WHITE),
                Text("• Less fading", font_size=18, color=GREEN),
                Text("• More stable", font_size=18, color=GREEN)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        ).arrange(RIGHT, buff=1.5, aligned_edge=UP)
        comparison_table.move_to(DOWN * 1.2)
        
        rayleigh_box = SurroundingRectangle(comparison_table[0], color=GREEN, buff=0.2, corner_radius=0.1)
        rician_box = SurroundingRectangle(comparison_table[1], color=BLUE, buff=0.2, corner_radius=0.1)
        
        self.play(
            *[FadeOut(mob) for mob in [
                phone2, tower2, los_path, los_label, scatter_paths2, scatter_label,
                phasor_circle2, los_phasor, los_phasor_label, scatter_phasors,
                resultant_rician, stable_text, rician_title
            ]],
            run_time=0.6
        )
        
        self.play(Write(comparison_title), run_time=0.6)
        self.wait(0.3)
        
        self.play(
            FadeIn(rayleigh_box),
            Write(comparison_table[0]),
            run_time=0.8
        )
        self.wait(0.4)
        
        self.play(
            FadeIn(rician_box),
            Write(comparison_table[1]),
            run_time=0.8
        )
        self.wait(1.0)
        
        # ============================================
        # FINAL MESSAGE
        # ============================================
        
        final_message = VGroup(
            Text("Understanding fading", font_size=28, color=YELLOW, weight=BOLD),
            Text("= Better wireless system design!", font_size=26, color=GREEN)
        ).arrange(DOWN, buff=0.2)
        final_message.to_edge(DOWN, buff=0.8)
        
        final_box = SurroundingRectangle(final_message, color=YELLOW, buff=0.3, corner_radius=0.15, stroke_width=4)
        
        self.play(
            FadeIn(final_box),
            Write(final_message),
            run_time=1.0
        )
        
        # Pulse effect
        self.play(
            final_box.animate.set_color(GREEN).set_stroke(width=6),
            rate_func=there_and_back,
            run_time=1.0
        )
        
        self.wait(2.0)
        
        # ============================================
        # FADE OUT EVERYTHING
        # ============================================
        
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.2
        )
        self.wait(0.5)