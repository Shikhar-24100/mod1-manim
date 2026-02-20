from manim import *
import numpy as np

class NoiseEffectsAndBER(Scene):
    def construct(self):
        # Title
        title = Text("Part 3: Noise Effects & Bit Error Rate (BER)", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Section 1: Introduction to Noise
        self.noise_introduction()
        self.clear()
        
        # Section 2: Noise on PSK
        self.noise_on_psk()
        self.clear()
        
        # Section 3: Noise on FSK
        self.noise_on_fsk()
        self.clear()
        
        # Section 4: Noise on ASK
        self.noise_on_ask()
        self.clear()
        
        # Section 5: BER Comparison
        self.ber_comparison()
        self.clear()
        
        # Section 6: Analog vs Digital Noise
        self.analog_vs_digital_noise()
    
    def noise_introduction(self):
        """Introduce the concept of noise in communication"""
        intro_title = Text("What is Channel Noise?", font_size=40)
        intro_title.to_edge(UP)
        self.play(Write(intro_title))
        
        # Show clean signal
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=3,
            tips=False
        ).shift(UP*0.5)
        
        clean_signal = axes.plot(lambda x: np.sin(2*PI*x), color=BLUE)
        clean_label = Text("Clean Signal", font_size=24, color=BLUE).next_to(axes, DOWN)
        
        self.play(Create(axes), Create(clean_signal), Write(clean_label))
        self.wait()
        
        # Add noise
        np.random.seed(42)
        noisy_signal = axes.plot(
            lambda x: np.sin(2*PI*x) + 0.3*np.sin(20*x) + 0.2*np.sin(50*x), 
            color=RED
        )
        noisy_label = Text("Signal + Noise", font_size=24, color=RED).next_to(axes, DOWN)
        
        self.play(
            Transform(clean_signal, noisy_signal),
            Transform(clean_label, noisy_label)
        )
        self.wait()
        
        # Explanation text
        explanation = VGroup(
            Text("Noise causes:", font_size=28),
            Text("• Random amplitude variations", font_size=24),
            Text("• Phase distortions", font_size=24),
            Text("• Symbol detection errors", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).shift(DOWN*2)
        
        self.play(Write(explanation))
        self.wait(2)
    
    def noise_on_psk(self):
        """Show how noise affects BPSK constellation"""
        title = Text("Noise Effect on BPSK", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create I-Q plane
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_tip": True}
        ).shift(LEFT*3)
        
        x_label = MathTex("I", font_size=30).next_to(axes.x_axis, RIGHT)
        y_label = MathTex("Q", font_size=30).next_to(axes.y_axis, UP)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # BPSK symbols (clean)
        symbol_0 = Dot(axes.c2p(-1, 0), color=BLUE, radius=0.1)
        symbol_1 = Dot(axes.c2p(1, 0), color=BLUE, radius=0.1)
        label_0 = MathTex("0", font_size=24).next_to(symbol_0, DOWN)
        label_1 = MathTex("1", font_size=24).next_to(symbol_1, DOWN)
        
        self.play(
            Create(symbol_0), Create(symbol_1),
            Write(label_0), Write(label_1)
        )
        self.wait()
        
        # Add noise clouds
        np.random.seed(42)
        noise_points_0 = VGroup(*[
            Dot(axes.c2p(-1 + np.random.normal(0, 0.3), np.random.normal(0, 0.3)), 
                color=BLUE, radius=0.02, fill_opacity=0.3)
            for _ in range(50)
        ])
        
        noise_points_1 = VGroup(*[
            Dot(axes.c2p(1 + np.random.normal(0, 0.3), np.random.normal(0, 0.3)), 
                color=BLUE, radius=0.02, fill_opacity=0.3)
            for _ in range(50)
        ])
        
        noise_label = Text("With Noise", font_size=24, color=YELLOW).next_to(axes, DOWN)
        
        self.play(
            Create(noise_points_0),
            Create(noise_points_1),
            Write(noise_label)
        )
        self.wait()
        
        # Decision boundary
        decision_line = DashedLine(
            axes.c2p(0, -2), axes.c2p(0, 2), 
            color=RED, stroke_width=3
        )
        decision_label = Text("Decision\nBoundary", font_size=20, color=RED).next_to(decision_line, UP)
        
        self.play(Create(decision_line), Write(decision_label))
        self.wait()
        
        # Explanation on the right
        explanation = VGroup(
            Text("Error occurs when:", font_size=26, color=YELLOW),
            Text("Noise pushes symbol", font_size=22),
            Text("across the decision", font_size=22),
            Text("boundary", font_size=22),
            MathTex(r"P_{error} \propto e^{-\frac{d^2}{2\sigma^2}}", font_size=30)
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT*3.5 + UP*0.5)
        
        self.play(Write(explanation))
        self.wait(2)
        
        # Highlight error example
        error_dot = Dot(axes.c2p(0.3, 0.5), color=RED, radius=0.08)
        arrow = Arrow(error_dot.get_center(), axes.c2p(-1, 0), color=RED, buff=0.1)
        error_text = Text("ERROR!", font_size=20, color=RED).next_to(error_dot, RIGHT)
        
        self.play(Create(error_dot), Create(arrow), Write(error_text))
        self.wait(2)
    
    def noise_on_fsk(self):
        """Show how noise affects FSK"""
        title = Text("Noise Effect on FSK", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create frequency domain representation
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 2, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"include_tip": True}
        ).shift(LEFT*2.5 + UP*0.5)
        
        x_label = Text("Frequency", font_size=24).next_to(axes.x_axis, DOWN)
        y_label = Text("Power", font_size=24).rotate(PI/2).next_to(axes.y_axis, LEFT)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Two frequency peaks (clean)
        f1_line = Line(axes.c2p(3, 0), axes.c2p(3, 1.5), color=BLUE, stroke_width=6)
        f2_line = Line(axes.c2p(7, 0), axes.c2p(7, 1.5), color=BLUE, stroke_width=6)
        f1_label = MathTex("f_1 (0)", font_size=24).next_to(f1_line, DOWN)
        f2_label = MathTex("f_2 (1)", font_size=24).next_to(f2_line, DOWN)
        
        self.play(
            Create(f1_line), Create(f2_line),
            Write(f1_label), Write(f2_label)
        )
        self.wait()
        
        # Add noise floor
        noise_floor = axes.plot(lambda x: 0.3 + 0.1*np.sin(10*x), color=YELLOW)
        noise_label = Text("Noise Floor", font_size=20, color=YELLOW).shift(DOWN*2.5 + LEFT*2)
        
        self.play(Create(noise_floor), Write(noise_label))
        self.wait()
        
        # Explanation
        explanation = VGroup(
            Text("FSK is more robust:", font_size=26, color=GREEN),
            Text("• Frequencies are separated", font_size=22),
            Text("• Noise affects both equally", font_size=22),
            Text("• But can cause frequency", font_size=22),
            Text("  detection errors", font_size=22),
            MathTex(r"BER_{FSK} < BER_{ASK}", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT*3.2)
        
        self.play(Write(explanation))
        self.wait(2)
    
    def noise_on_ask(self):
        """Show how noise affects ASK"""
        title = Text("Noise Effect on ASK", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create amplitude representation
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 2, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True}
        ).shift(LEFT*2.5)
        
        x_label = Text("Time", font_size=24).next_to(axes.x_axis, DOWN)
        y_label = Text("Amplitude", font_size=24).rotate(PI/2).next_to(axes.y_axis, LEFT)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Two amplitude levels
        amp_0 = DashedLine(axes.c2p(0, 0.3), axes.c2p(4, 0.3), color=BLUE)
        amp_1 = DashedLine(axes.c2p(0, 1.5), axes.c2p(4, 1.5), color=BLUE)
        label_0 = MathTex("A_0 (0)", font_size=24).next_to(amp_0, LEFT)
        label_1 = MathTex("A_1 (1)", font_size=24).next_to(amp_1, LEFT)
        
        self.play(
            Create(amp_0), Create(amp_1),
            Write(label_0), Write(label_1)
        )
        self.wait()
        
        # Add noise bands
        noise_band_0 = Rectangle(
            width=6, height=0.4, 
            fill_color=YELLOW, fill_opacity=0.3,
            stroke_width=0
        ).move_to(axes.c2p(2, 0.3))
        
        noise_band_1 = Rectangle(
            width=6, height=0.4,
            fill_color=YELLOW, fill_opacity=0.3,
            stroke_width=0
        ).move_to(axes.c2p(2, 1.5))
        
        self.play(FadeIn(noise_band_0), FadeIn(noise_band_1))
        self.wait()
        
        # Decision threshold
        threshold = DashedLine(axes.c2p(0, 0.9), axes.c2p(4, 0.9), color=RED, stroke_width=3)
        threshold_label = Text("Threshold", font_size=20, color=RED).next_to(threshold, RIGHT)
        
        self.play(Create(threshold), Write(threshold_label))
        self.wait()
        
        # Explanation
        explanation = VGroup(
            Text("ASK is most vulnerable:", font_size=26, color=RED),
            Text("• Single parameter (amplitude)", font_size=22),
            Text("• Noise directly affects", font_size=22),
            Text("  amplitude measurement", font_size=22),
            Text("• Easy to cross threshold", font_size=22),
            MathTex(r"BER_{ASK} > BER_{PSK}", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT*3)
        
        self.play(Write(explanation))
        self.wait(2)
    
    def ber_comparison(self):
        """Compare BER performance of all three modulations"""
        title = Text("BER Performance Comparison", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create BER vs SNR plot
        axes = Axes(
            x_range=[0, 15, 3],
            y_range=[-5, 0, 1],
            x_length=7,
            y_length=4,
            axis_config={"include_tip": True}
        ).shift(DOWN*0.5)
        
        x_label = MathTex(r"E_b/N_0 \text{ (dB)}", font_size=28).next_to(axes.x_axis, DOWN)
        y_label = MathTex(r"\log_{10}(BER)", font_size=28).rotate(PI/2).next_to(axes.y_axis, LEFT)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # BER curves (simplified approximations)
        bpsk_curve = axes.plot(
            lambda x: -0.5*x + 1 if x < 12 else -5,
            color=GREEN, x_range=[2, 13]
        )
        fsk_curve = axes.plot(
            lambda x: -0.4*x + 1.5 if x < 13 else -5,
            color=BLUE, x_range=[3, 14]
        )
        ask_curve = axes.plot(
            lambda x: -0.35*x + 2 if x < 14 else -5,
            color=RED, x_range=[4, 15]
        )
        
        # Labels
        bpsk_label = Text("BPSK", font_size=24, color=GREEN).next_to(bpsk_curve.get_end(), RIGHT)
        fsk_label = Text("FSK", font_size=24, color=BLUE).next_to(fsk_curve.get_end(), RIGHT)
        ask_label = Text("ASK", font_size=24, color=RED).next_to(ask_curve.get_end(), RIGHT)
        
        self.play(
            Create(bpsk_curve), Write(bpsk_label),
            Create(fsk_curve), Write(fsk_label),
            Create(ask_curve), Write(ask_label),
            run_time=2
        )
        self.wait()
        
        # Key insights
        insights = VGroup(
            Text("Key Insights:", font_size=28, color=YELLOW),
            Text("• BPSK has best BER performance", font_size=22, color=GREEN),
            Text("• FSK is moderate", font_size=22, color=BLUE),
            Text("• ASK has worst BER", font_size=22, color=RED),
            Text("• All improve with higher SNR", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT).shift(UP*0.5)
        
        self.play(Write(insights))
        self.wait(3)
    
    def analog_vs_digital_noise(self):
        """Compare analog and digital noise measurement"""
        title = Text("Analog vs Digital: Measuring Noise Effects", font_size=34)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Split screen
        analog_title = Text("Analog Signals", font_size=28, color=BLUE).shift(UP*2.5 + LEFT*3.5)
        digital_title = Text("Digital Signals", font_size=28, color=GREEN).shift(UP*2.5 + RIGHT*3.5)
        
        divider = Line(UP*3, DOWN*3, color=WHITE)
        
        self.play(Write(analog_title), Write(digital_title), Create(divider))
        
        # Analog side
        analog_signal = VGroup(
            Text("Continuous distortion", font_size=22),
            MathTex(r"SNR = \frac{P_{signal}}{P_{noise}}", font_size=26),
            Text("Measured in dB", font_size=22),
            MathTex(r"THD, SINAD", font_size=26),
            Text("Gradual degradation", font_size=22, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).shift(LEFT*3.5 + UP*0.3)
        
        # Digital side
        digital_signal = VGroup(
            Text("Discrete errors", font_size=22),
            MathTex(r"BER = \frac{\text{errors}}{\text{total bits}}", font_size=24),
            Text("Binary: correct or wrong", font_size=22),
            MathTex(r"10^{-3}, 10^{-6}, 10^{-9}...", font_size=26),
            Text("Threshold behavior", font_size=22, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT*3.5 + UP*0.3)
        
        self.play(Write(analog_signal))
        self.wait()
        self.play(Write(digital_signal))
        self.wait()
        
        # Connection
        connection = VGroup(
            Text("Both measure quality degradation due to noise", font_size=24),
            Text("Analog: continuous metric (SNR, dB)", font_size=22, color=BLUE),
            Text("Digital: probability metric (BER)", font_size=22, color=GREEN)
        ).arrange(DOWN).shift(DOWN*2.3)
        
        self.play(Write(connection))
        self.wait(3)
        
        # Final summary
        summary = Text("BER is the digital equivalent of SNR degradation!", 
                      font_size=26, color=YELLOW).shift(DOWN*3.2)
        self.play(Write(summary))
        self.wait(2)

# To render: manim -pql script.py NoiseEffectsAndBER