from manim import *
import numpy as np

class PowerDelayProfileScene(Scene):
    def construct(self):
        # === TITLE ===
        title = Text("Power Delay Profile", font_size=40, weight=BOLD, color=BLUE)
        title.to_edge(UP, buff=0.4)
        
        subtitle = Text("Time domain view of multipath", font_size=26, color=YELLOW, slant=ITALIC)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(subtitle, shift=DOWN*0.2), run_time=0.6)
        self.wait(0.5)
        
        self.play(FadeOut(subtitle), run_time=0.3)
        
        # ============================================
        # TOP: IMPULSE RESPONSE (STEM PLOT)
        # ============================================
        
        # Create top axes for impulses
        impulse_axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.2, 0.5],
            x_length=9,
            y_length=1.8,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
            },
        ).shift(UP * 1.8)
        
        impulse_y_label = Text("Amplitude", font_size=20, color=WHITE)
        impulse_y_label.next_to(impulse_axes.y_axis, LEFT, buff=0.2)
        impulse_y_label.rotate(90 * DEGREES)
        
        self.play(
            Create(impulse_axes),
            Write(impulse_y_label),
            run_time=0.8
        )
        self.wait(0.3)
        
        # Define 4 impulses with delays and amplitudes
        impulses_data = [
            (1.5, 1.0, WHITE, r"a_0\delta(t-\tau_0)"),
            (3.5, 0.7, WHITE, r"a_1\delta(t-\tau_1)"),
            (5.5, 0.5, WHITE, r"a_2\delta(t-\tau_2)"),
            (7.5, 0.3, WHITE, r"a_3\delta(t-\tau_3)"),
        ]
        
        impulses = []
        impulse_labels = []
        
        for delay, amplitude, color, label_text in impulses_data:
            # Impulse arrow
            impulse = Arrow(
                impulse_axes.c2p(delay, 0),
                impulse_axes.c2p(delay, amplitude),
                color=RED,
                buff=0,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.2
            )
            impulses.append(impulse)
            
            # Label
            label = MathTex(label_text, font_size=18, color=color)
            label.next_to(impulse, UP, buff=0.1)
            impulse_labels.append(label)
        
        # Animate impulses appearing
        self.play(
            LaggedStart(*[
                AnimationGroup(GrowArrow(imp), FadeIn(lbl, shift=DOWN*0.1))
                for imp, lbl in zip(impulses, impulse_labels)
            ], lag_ratio=0.3),
            run_time=2.0
        )
        self.wait(0.5)
        
        # Add "Amplitude Variation" bracket
        amp_bracket = BraceBetweenPoints(
            impulse_axes.c2p(8.5, 0.3),
            impulse_axes.c2p(8.5, 1.0),
            direction=RIGHT,
            color=GREEN
        )
        amp_label = Text("Amplitude\nVariation", font_size=16, color=GRAY)
        amp_label.next_to(amp_bracket, RIGHT, buff=0.1)
        
        self.play(
            Create(amp_bracket),
            FadeIn(amp_label, shift=LEFT*0.1),
            run_time=0.6
        )
        self.wait(0.4)
        
        # Add time label
        time_label = Text("time", font_size=18, color=WHITE, slant=ITALIC)
        time_label.next_to(impulse_axes.x_axis, RIGHT, buff=0.2)
        self.play(Write(time_label), run_time=0.4)
        self.wait(0.5)
        
        # ============================================
        # BOTTOM: SINE WAVES WITH PHASE VARIATIONS
        # ============================================
        
        # Create bottom axes for sine waves
        wave_axes = Axes(
            x_range=[0, 10, 2],
            y_range=[-1.5, 1.5, 1],
            x_length=9,
            y_length=3.5,
            axis_config={
                "include_tip": False,
                "include_numbers": False,
            },
        ).shift(DOWN * 1.2)
        
        # wave_y_label = Text("Delay Variation", font_size=20, color=WHITE)
        # wave_y_label.next_to(wave_axes.y_axis, LEFT, buff=0.2)
        # wave_y_label.rotate(90 * DEGREES)
        
        # copies_label = Text("Multiple copies of signal", font_size=18, color=PURPLE)
        # copies_label.next_to(wave_axes.y_axis, RIGHT, buff=0.3).shift(DOWN * 1.8)
        
        # self.play(
        #     # Create(wave_axes),
        #     # Write(wave_y_label),
        #     # Write(copies_label),
        #     run_time=0.8
        # )
        self.wait(0.4)
        
        # Create vertical dashed lines from impulses
        # Horizontal dashed red lines from impulse tips
        dashed_lines = []
        for delay, amplitude, color, _ in impulses_data:
            dashed_line = DashedLine(
                impulse_axes.c2p(delay, 0),
                wave_axes.c2p(delay, -1.5),
                color=GREEN,
                stroke_width=2,
                dash_length=0.08
            )
            dashed_lines.append(dashed_line)
         
        self.play(
            LaggedStart(*[Create(line) for line in dashed_lines], lag_ratio=0.2),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Create sine waves starting from each delay with different phases
        # Add slight hand-drawn variation
        waves = []
        
        # Phase offsets for each wave
        phase_offsets = [0, PI/3, 2*PI/3, PI]
        
        # Vertical positions for waves (stacked)
        wave_positions = [0.9, 0.3, -0.3, -0.9]
        
        for i, (delay, amplitude, color, _) in enumerate(impulses_data):
            phase = phase_offsets[i]
            y_offset = wave_positions[i]
            
            # Create sine wave starting ONLY from delay point (no line before)
            wave = wave_axes.plot(
                lambda t, d=delay, p=phase, y=y_offset: (
                    y + 0.25 * np.sin(3*(t - d) + p) * (1 + 0.05 * np.sin(7*(t - d)))
                ),
                x_range=[delay, 10],  # Start from delay, not from 0
                color=BLUE,
                stroke_width=3,
                use_smoothing=True
            )
            waves.append(wave)
        
        # Animate waves appearing
        self.play(
            LaggedStart(*[Create(wave) for wave in waves], lag_ratio=0.3),
            run_time=2.0
        )
        self.wait(0.6)
        
        # ============================================
        # SHOW DELAY SPREAD
        # ============================================
        
        # Bracket showing delay spread at bottom
        bracket_start = wave_axes.c2p(impulses_data[0][0], -1.6)
        bracket_end = wave_axes.c2p(impulses_data[-1][0], -1.6)
        
        bracket = BraceBetweenPoints(bracket_start, bracket_end, direction=DOWN, color=YELLOW)
        
        spread_label = Text("Delay Spread", font_size=22, color=YELLOW, weight=BOLD)
        spread_label.next_to(bracket, DOWN, buff=0.2)
        
        self.play(
            Create(bracket),
            Write(spread_label),
            run_time=0.8
        )
        self.wait(0.6)
        
        # ============================================
        # KEY INSIGHT
        # ============================================
        
        # Key message
        # insight = VGroup(
        #     Text("Spread in time =", font_size=26, color=WHITE),
        #     Text("Interference between symbols", font_size=26, color=RED, weight=BOLD)
        # ).arrange(RIGHT, buff=0.3)
        # insight.to_edge(DOWN, buff=0.3)
        
        # insight_box = SurroundingRectangle(insight, color=YELLOW, buff=0.2, stroke_width=2)
        
        # self.play(
        #     FadeIn(insight_box),
        #     Write(insight),
        #     run_time=0.8
        # )
        
        # Emphasize the spread
        self.play(
            bracket.animate.set_color(RED).set_stroke(width=4),
            spread_label.animate.set_color(RED).scale(1.15),
            rate_func=there_and_back,
            run_time=0.9
        )
        
        self.wait(1.5)
        
        # === FADE OUT ===
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8
        )