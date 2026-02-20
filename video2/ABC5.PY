from manim import *
import numpy as np

class PhasorIntroScene(Scene):
    def construct(self):
        # === TITLE ===
        title = Text("What is a Phasor?", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.4)
        
        self.play(Write(title), run_time=0.8)
        self.wait(0.4)
        
        # === SETUP: CIRCLE AND SINE WAVE SIDE BY SIDE ===
        # Circle on the left
        circle_center = LEFT * 3.5 + DOWN * 0.3
        circle_radius = 1.2
        
        circle = Circle(
            radius=circle_radius,
            color=WHITE,
            stroke_width=3
        )
        circle.move_to(circle_center)
        
        # Phasor (rotating arrow) - starts horizontal
        phasor_arrow = Arrow(
            circle_center,
            circle_center + RIGHT * circle_radius,
            color=BLUE,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.15
        )
        
        # Dot at the tip of phasor
        phasor_dot = Dot(phasor_arrow.get_end(), color=BLUE, radius=0.1)
        
        # Sine wave axes on the right
        axes = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-1.2, 1.2, 0.4],
            x_length=5.5,
            y_length=2.5,
            axis_config={"include_tip": False, "include_numbers": False},
        )
        axes.next_to(circle, RIGHT, buff=1.5).shift(DOWN * 0.3)
        
        # Sine wave
        sine_wave = axes.plot(
            lambda t: 1.2*np.cos(t),
            x_range=[0, 4*PI],
            color=YELLOW,
            stroke_width=4
        )
        
        # Wave label
        wave_label = MathTex(r"A \cdot \cos(\omega t + \phi)", font_size=32, color=YELLOW)
        wave_label.next_to(axes, UP, buff=0.2)
        
        # Show circle and wave
        self.play(
            Create(circle),
            Create(axes),
            run_time=0.7
        )
        self.play(
            GrowArrow(phasor_arrow),
            FadeIn(phasor_dot),
            Create(sine_wave),
            Write(wave_label),
            run_time=1.0
        )
        self.wait(0.5)
        
        # === HORIZONTAL DASHED LINE (measures amplitude) ===
        # This line goes from phasor tip horizontally across to the sine wave
        horizontal_line = always_redraw(
            lambda: DashedLine(
                phasor_dot.get_center(),
                [axes.get_right()[0], phasor_dot.get_center()[1], 0],
                color=WHITE,
                stroke_width=3,
                dash_length=0.12
            )
        )
        
        # === VERTICAL DASHED LINE (shows position on wave) ===
        # Track the current angle for x-position on wave
        angle_tracker = ValueTracker(0)
        
        # Vertical line intersects horizontal line on sine wave
        vertical_line = always_redraw(
            lambda: DashedLine(
                [axes.c2p(angle_tracker.get_value(), 0)[0], axes.get_bottom()[1], 0],
                [axes.c2p(angle_tracker.get_value(), 0)[0], phasor_dot.get_center()[1], 0],
                color=WHITE,
                stroke_width=3,
                dash_length=0.12
            )
        )
        
        self.add(horizontal_line, vertical_line)
        self.wait(0.3)
        
        # === ANIMATE ROTATION ===
        # Updaters for phasor rotation
        def update_phasor(mob):
            angle = angle_tracker.get_value()
            new_end = circle_center + np.array([
                circle_radius * np.cos(angle),
                circle_radius * np.sin(angle),
                0
            ])
            mob.put_start_and_end_on(circle_center, new_end)
        
        def update_dot(mob):
            mob.move_to(phasor_arrow.get_end())
        
        phasor_arrow.add_updater(update_phasor)
        phasor_dot.add_updater(update_dot)
        
        # Rotate for ONE complete rotation (2π)
        self.play(
            angle_tracker.animate.set_value(2 * PI),
            run_time=4.0,
            rate_func=linear
        )
        
        self.wait(0.3)
        
        # === STOP AT RANDOM POSITION (e.g., 50 degrees) ===
        freeze_angle = 50 * DEGREES
        
        self.play(
            angle_tracker.animate.set_value(2 * PI + freeze_angle),
            run_time=1.0,
            rate_func=smooth
        )
        
        # Remove updaters
        phasor_arrow.clear_updaters()
        phasor_dot.clear_updaters()
        
        self.wait(0.5)
        
        # === LABEL: AMPLITUDE ===
        # Length of phasor (radius)
        amplitude_brace = Brace(
            Line(circle_center, phasor_dot.get_center()),
            direction=phasor_arrow.copy().rotate(PI/2).get_unit_vector(),
            buff=0.1
        )
        amplitude_label = MathTex("Amplitude(A)", color=YELLOW, font_size=36)
        amplitude_label.next_to(amplitude_brace, RIGHT, buff=0.1).shift(LEFT * 0.2 + UP*0.7)
        
        # amplitude_text = Text("Amplitude", font_size=24, color=YELLOW, weight=BOLD)
        # amplitude_text.next_to(amplitude_label, UP, buff=0.15)
        
        self.play(
            # GrowFromCenter(amplitude_brace),
            FadeIn(amplitude_label, shift=DOWN*0.1),
            # FadeIn(amplitude_text, shift=DOWN*0.1),
            run_time=0.8
        )
        self.wait(0.4)
        
        # === LABEL: PHASE (ANGLE) ===
        # Arc showing the angle from horizontal
        phase_arc = Arc(
            radius=0.5,
            start_angle=0,
            angle=freeze_angle,
            color=YELLOW,
            stroke_width=4,
            arc_center=circle_center
        )
        
        phase_label = MathTex(r"Phase(\phi)", color=YELLOW, font_size=36)
        phase_label.move_to(circle_center + RIGHT * 2.1 + UP * 0.2)
        
        # phase_text = Text("Phase", font_size=24, color=YELLOW, weight=BOLD)
        # phase_text.next_to(phase_label, RIGHT, buff=0.3)
        
        self.play(
            Create(phase_arc),
            FadeIn(phase_label, scale=0.8),
            # FadeIn(phase_text, shift=LEFT*0.1),
            run_time=0.8
        )
        self.wait(0.6)
        
        # === REMOVE WAVE AND CENTER CIRCULAR AREA ===
        # Fade out wave-related elements
        self.play(
            FadeOut(axes),
            FadeOut(sine_wave),
            FadeOut(wave_label),
            FadeOut(horizontal_line),
            FadeOut(vertical_line),
            run_time=0.6
        )
        
        # Group the phasor elements
        phasor_group = VGroup(
            circle, phasor_arrow, phasor_dot, amplitude_label,
            phase_arc, phase_label
        )
        self.play(FadeOut(phasor_dot))
        # Move to center and scale up
        self.play(
            phasor_group.animate.move_to(ORIGIN + DOWN * 0.2).scale(1.3),
            run_time=0.9
        )
        
        self.wait(0.4)
        
        # === KEY MESSAGE ===
        key_message = VGroup(
            Text("Phasor =", font_size=28),
            Text("Amplitude + Phase", font_size=28)
        ).arrange(RIGHT, buff=0.3)
        key_message.to_edge(DOWN, buff=0.5)
        
        self.play(
            FadeIn(key_message, shift=UP*0.2),
            run_time=0.8
        )
        
        # Emphasize the phasor
        self.play(
            phasor_arrow.animate.set_stroke(width=8),
            phasor_dot.animate.scale(1.4),
            rate_func=there_and_back,
            run_time=0.9
        )
        
        self.wait(1.5)
        
        # === FADE OUT ===
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8
        )