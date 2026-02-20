from manim import *

class CarrierWaveIntro(Scene):
    def construct(self):
        # Title
        title = Text("Carrier wave", font_size=48, weight=BOLD)
        subtitle = Text("Introduction to the modulation params", font_size=32)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))


        intro_text = Text("Introducing thr carrier wave", font_size=36)
        self.play(Write(intro_text))
        self.wait(1)
        self.play(intro_text.animate.to_edge(UP))
        self.wait(0.5)
        
        # ===== Part 1: Show Sine Wave Appearing =====
        
        # Create axes for the sine wave
        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=3,
            axis_config={"include_tip": False, "include_numbers": False},
        )
        axes.shift(UP * 0.5)
        
        # Initial sine wave parameters
        amplitude = 1
        frequency = 2
        phase = 0
        
        # Create the sine wave
        sine_wave = axes.plot(
            lambda t: amplitude * np.cos(frequency * t + phase),
            color=YELLOW,
            stroke_width=4
        )
        
        # Label for carrier wave
        carrier_label = Text("Carrier Wave (High Frequency)", font_size=28, color=YELLOW)
        carrier_label.next_to(axes, UP, buff=0.3)
        
        # Equation
        equation = MathTex(
            r"c(t) = A \cdot \cos(2\pi f_c t + \phi)",
            font_size=36
        )
        equation.next_to(axes, DOWN, buff=0.5)
        
        # Animate sine wave appearing
        self.play(Create(axes))
        self.play(Create(sine_wave), run_time=2)
        self.play(Write(carrier_label))
        self.play(Write(equation))
        self.wait(1)
        
        # ===== Part 2: Highlight Three Properties =====
        
        # Move equation up to make room
        self.play(
            equation.animate.scale(0.8).to_edge(DOWN, buff=0.3).shift(UP * 1),
            carrier_label.animate.to_edge(UP, buff=1)
        )
        # self.play()

        
        # Create property labels with color coding
        amp_label = Text("Amplitude (A)", font_size=24, color=RED)
        freq_label = Text("Frequency (fc)", font_size=24, color=BLUE)
        phase_label = Text("Phase (φ)", font_size=24, color=GREEN)
        
        # Position labels
        amp_label.to_edge(LEFT, buff=0.5).shift(DOWN * 1 + RIGHT*3)
        freq_label.next_to(amp_label, RIGHT, buff=1.5)
        phase_label.next_to(freq_label, RIGHT, buff=1.5)
        
        # Show property labels
        self.play(
            FadeIn(amp_label),
            FadeIn(freq_label),
            FadeIn(phase_label)
        )
        self.wait(0.5)
        
        # Highlight Amplitude in equation
        equation_amp = MathTex(
            r"c(t) = ", r"A", r" \cdot \cos(2\pi f_c t + \phi)",
            font_size=36
        )
        equation_amp[1].set_color(RED)
        equation_amp.move_to(equation)
        
        self.play(Transform(equation, equation_amp))
        
        # Show amplitude visualization - double arrows
        amp_arrow_up = Arrow(
            axes.c2p(PI, 0), axes.c2p(PI, amplitude),
            color=RED, buff=0, stroke_width=6
        )
        amp_arrow_down = Arrow(
            axes.c2p(PI, 0), axes.c2p(PI, -amplitude),
            color=RED, buff=0, stroke_width=6
        )
        amp_arrows = VGroup(amp_arrow_up, amp_arrow_down)
        
        self.play(GrowArrow(amp_arrow_up), GrowArrow(amp_arrow_down))
        self.play(Indicate(amp_label, color=RED, scale_factor=1.2))
        self.wait(1)
        
        # ===== Part 3: Animate Amplitude Changing =====
        
        amp_label_highlight = amp_label.copy().set_color(YELLOW)
        self.play(Transform(amp_label, amp_label_highlight))
        
        # Animate amplitude growing
        new_amplitude = 1.5
        new_sine_wave = axes.plot(
            lambda t: new_amplitude * np.cos(frequency * t + phase),
            color=YELLOW,
            stroke_width=4
        )
        
        new_amp_arrow_up = Arrow(
            axes.c2p(PI, 0), axes.c2p(PI, new_amplitude),
            color=RED, buff=0, stroke_width=6
        )
        new_amp_arrow_down = Arrow(
            axes.c2p(PI, 0), axes.c2p(PI, -new_amplitude),
            color=RED, buff=0, stroke_width=6
        )
        
        self.play(
            Transform(sine_wave, new_sine_wave),
            Transform(amp_arrow_up, new_amp_arrow_up),
            Transform(amp_arrow_down, new_amp_arrow_down),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Animate amplitude shrinking
        new_amplitude = 0.6
        new_sine_wave = axes.plot(
            lambda t: new_amplitude * np.cos(frequency * t + phase),
            color=YELLOW,
            stroke_width=4
        )
        
        new_amp_arrow_up = Arrow(
            axes.c2p(PI, 0), axes.c2p(PI, new_amplitude),
            color=RED, buff=0, stroke_width=6
        )
        new_amp_arrow_down = Arrow(
            axes.c2p(PI, 0), axes.c2p(PI, -new_amplitude),
            color=RED, buff=0, stroke_width=6
        )
        
        self.play(
            Transform(sine_wave, new_sine_wave),
            Transform(amp_arrow_up, new_amp_arrow_up),
            Transform(amp_arrow_down, new_amp_arrow_down),
            run_time=1.5
        )
        
        # Reset amplitude
        amplitude = 1
        sine_wave_reset = axes.plot(
            lambda t: amplitude * np.cos(frequency * t + phase),
            color=YELLOW,
            stroke_width=4
        )
        self.play(
            Transform(sine_wave, sine_wave_reset),
            FadeOut(amp_arrows),
            amp_label.animate.set_color(RED),
            run_time=1
        )
        self.wait(0.5)
        
        # ===== Part 4: Highlight and Animate Frequency =====
        
        equation_freq = MathTex(
            r"c(t) = A \cdot \cos(2\pi ", r"f_c", r" t + \phi)",
            font_size=36
        )
        equation_freq[1].set_color(BLUE)
        equation_freq.move_to(equation)
        
        self.play(Transform(equation, equation_freq))
        
        freq_label_highlight = freq_label.copy().set_color(YELLOW)
        self.play(Transform(freq_label, freq_label_highlight))
        self.play(Indicate(freq_label, color=BLUE, scale_factor=1.2))
        
        # Animate frequency increasing (waves compress)
        new_frequency = 4
        new_sine_wave = axes.plot(
            lambda t: amplitude * np.cos(new_frequency * t + phase),
            color=YELLOW,
            stroke_width=4
        )
        
        self.play(Transform(sine_wave, new_sine_wave), run_time=2)
        self.wait(0.5)
        
        # Animate frequency decreasing (waves expand)
        new_frequency = 1
        new_sine_wave = axes.plot(
            lambda t: amplitude * np.cos(new_frequency * t + phase),
            color=YELLOW,
            stroke_width=4
        )
        
        self.play(Transform(sine_wave, new_sine_wave), run_time=2)
        
        # Reset frequency
        frequency = 2
        sine_wave_reset = axes.plot(
            lambda t: amplitude * np.cos(frequency * t + phase),
            color=YELLOW,
            stroke_width=4
        )
        self.play(
            Transform(sine_wave, sine_wave_reset),
            freq_label.animate.set_color(BLUE),
            run_time=1
        )
        self.wait(0.5)
        
        # ===== Part 5: Highlight and Animate Phase =====
        
        equation_phase = MathTex(
            r"c(t) = A \cdot \cos(2\pi f_c t + ", r"\phi", r")",
            font_size=36
        )
        equation_phase[1].set_color(GREEN)
        equation_phase.move_to(equation)
        
        self.play(Transform(equation, equation_phase))
        
        phase_label_highlight = phase_label.copy().set_color(YELLOW)
        self.play(Transform(phase_label, phase_label_highlight))
        self.play(Indicate(phase_label, color=GREEN, scale_factor=1.2))
        
        # Animate phase shifting right
        new_phase = -PI/2
        new_sine_wave = axes.plot(
            lambda t: amplitude * np.cos(frequency * t + new_phase),
            color=YELLOW,
            stroke_width=4
        )
        
        self.play(Transform(sine_wave, new_sine_wave), run_time=1.5)
        self.wait(0.5)
        
        # Animate phase shifting left
        new_phase = PI/2
        new_sine_wave = axes.plot(
            lambda t: amplitude * np.cos(frequency * t + new_phase),
            color=YELLOW,
            stroke_width=4
        )
        
        self.play(Transform(sine_wave, new_sine_wave), run_time=1.5)
        
        # Reset phase
        phase = 0
        sine_wave_reset = axes.plot(
            lambda t: amplitude * np.cos(frequency * t + phase),
            color=YELLOW,
            stroke_width=4
        )
        self.play(
            Transform(sine_wave, sine_wave_reset),
            phase_label.animate.set_color(GREEN),
            run_time=1
        )
        self.wait(1)
        
        # ===== Final Summary =====
        
        summary = Text(
            "These three properties can carry information!",
            font_size=32,
            color=GOLD,
            weight=BOLD
        )
        summary.to_edge(DOWN, buff=0.2)
        
        self.play(Write(summary))
        self.wait(2)
        
        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
        self.wait(0.5)