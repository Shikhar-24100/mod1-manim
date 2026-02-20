from manim import *
import numpy as np

class OrthogonalityComparison(Scene):
    def construct(self):
        # Title
        title = Text("Orthogonality in Wireless Communication", font_size=36).to_edge(UP)
        self.add(title)

        # 1. SETUP AXES
        # Non-Orthogonal (Left)
        left_axes_top = Axes(x_range=[0, 4, 1], y_range=[-1.5, 1.5, 1], x_length=5, y_length=2.5).shift(LEFT * 3.5 + UP * 1.5)
        left_axes_bottom = Axes(x_range=[0, 4, 1], y_range=[-2.5, 2.5, 1], x_length=5, y_length=2.5).shift(LEFT * 3.5 + DOWN * 1.5)
        
        # Orthogonal (Right)
        right_axes_top = Axes(x_range=[0, 4, 1], y_range=[-1.5, 1.5, 1], x_length=5, y_length=2.5).shift(RIGHT * 3.5 + UP * 1.5)
        right_axes_bottom = Axes(x_range=[0, 4, 1], y_range=[-2.5, 2.5, 1], x_length=5, y_length=2.5).shift(RIGHT * 3.5 + DOWN * 1.5)

        # Labels
        labels = VGroup(
            Text("Non-Orthogonal", color=RED, font_size=24).next_to(left_axes_top, UP),
            Text("Orthogonal", color=GREEN, font_size=24).next_to(right_axes_top, UP),
            Text("TX Signals", font_size=20).move_to(LEFT * 0.5 + UP * 1.5),
            Text("Received (Sum)", font_size=20).move_to(LEFT * 0.5 + DOWN * 1.5)
        )

        # 2. DEFINE FUNCTIONS
        # Non-orthogonal: Frequencies are close but not integer multiples
        f1, f2 = 1.0, 1.3 
        # Orthogonal: Frequencies are integer multiples over the interval (1Hz and 2Hz)
        f3, f4 = 1.0, 2.0

        sig_a = left_axes_top.plot(lambda x: np.sin(2 * np.pi * f1 * x), color=BLUE)
        sig_b = left_axes_top.plot(lambda x: np.sin(2 * np.pi * f2 * x), color=RED)
        sum_non = left_axes_bottom.plot(lambda x: np.sin(2 * np.pi * f1 * x) + np.sin(2 * np.pi * f2 * x), color=PURPLE)

        sig_c = right_axes_top.plot(lambda x: np.sin(2 * np.pi * f3 * x), color=BLUE)
        sig_d = right_axes_top.plot(lambda x: np.sin(2 * np.pi * f4 * x), color=YELLOW)
        sum_ortho = right_axes_bottom.plot(lambda x: np.sin(2 * np.pi * f3 * x) + np.sin(2 * np.pi * f4 * x), color=PURPLE)

        # 3. ANIMATION
        self.play(Write(left_axes_top), Write(left_axes_bottom), Write(right_axes_top), Write(right_axes_bottom))
        self.play(FadeIn(labels))
        
        # Show Transmitted Signals
        self.play(Create(sig_a), Create(sig_b), Create(sig_c), Create(sig_d), run_time=3)
        self.wait(1)

        # Show Summed Signals (The "Mess" at the Receiver)
        self.play(TransformFromCopy(VGroup(sig_a, sig_b), sum_non), 
                  TransformFromCopy(VGroup(sig_c, sig_d), sum_ortho), run_time=2)
        self.wait(1)

        # 4. HIGHLIGHT THE RECOVERY (SAMPLING)
        # On the orthogonal side, show points where Sig D is 0 and Sig C is at Peak
        sample_time = 0.25 # Peak of 1Hz Sine
        dot_c = Dot(right_axes_bottom.c2p(sample_time, np.sin(2 * np.pi * f3 * sample_time) + np.sin(2 * np.pi * f4 * sample_time)), color=WHITE)
        label_sample = Text("Clean Sample Point", font_size=16).next_to(dot_c, UP)
        
        # Show that at 0.25s, the 2Hz wave is at 0
        line_to_zero = DashedLine(
            right_axes_top.c2p(sample_time, 1), 
            right_axes_top.c2p(sample_time, 0), 
            color=GRAY
        )

        self.play(Create(line_to_zero))
        self.play(FadeIn(dot_c), Write(label_sample))
        self.wait(2)