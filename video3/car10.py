from manim import *
import numpy as np

class CoherenceBandwidth_Phase4(Scene):
    def construct(self):
        # 4.1: INTUITION - Time Spread vs Frequency Ripples
        self.scene_time_vs_freq_intuition()
        
        # 4.2: INTERACTION - Y(f) = X(f)H(f)
        self.scene_channel_multiplication()
        
        # 4.3 & 4.4: DEFINITION - What is Bc? & Math Relation
        self.scene_define_bc_and_math()
        
        # 4.5: CORRELATION - 0.9 vs 0.5 levels
        self.scene_correlation_levels()
        
        # 4.6: COMPARISON - High vs Low Bc (Impact on Signal)
        self.scene_high_vs_low_bc_comparison()
        
        # 4.7: TRANSITION
        self.scene_transition_question()

    def scene_time_vs_freq_intuition(self):
        # Title
        title = Title("Delay Spread ($\sigma_\\tau$) $\\leftrightarrow$ Frequency Ripples", font_size=36)
        self.add(title)

        # Setup Axes
        ax_left = Axes(x_range=[0, 10], y_range=[0, 2.5], x_length=6, y_length=3.5, 
                      axis_config={"include_tip": False}).to_edge(LEFT, buff=0.5).shift(DOWN*0.5)
        ax_right = Axes(x_range=[0, 10], y_range=[0, 2.5], x_length=6, y_length=3.5,
                       axis_config={"include_tip": False}).to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)

        # Labels
        lbl_left = Text("Small Delay Spread", color=GREEN, font_size=24).next_to(ax_left, UP)
        lbl_right = Text("Large Delay Spread", color=RED, font_size=24).next_to(ax_right, UP)

        # Channel Functions (Randomized look)
        # Small spread -> Slow changes in freq
        def h_small_spread(f):
            return 1.2 + 0.4*np.cos(0.5*f) + 0.2*np.sin(0.8*f)
        
        # Large spread -> Fast ripples in freq
        def h_large_spread(f):
            return 1.2 + 0.4*np.cos(3*f) + 0.3*np.sin(5*f) + 0.15*np.cos(10*f)

        plot_left = ax_left.plot(h_small_spread, color=GREEN)
        plot_right = ax_right.plot(h_large_spread, color=RED)

        self.play(FadeIn(ax_left), FadeIn(ax_right), Write(lbl_left), Write(lbl_right))
        self.play(Create(plot_left), run_time=2)
        self.play(Create(plot_right), run_time=2)
        self.wait(2)
        
        # Clean up
        self.play(FadeOut(Group(ax_left, ax_right, lbl_left, lbl_right, plot_left, plot_right, title)))

    def scene_channel_multiplication(self):
        title = Title("Why Frequency Response Matters: $Y(f) = X(f) \cdot H(f)$", font_size=36)
        self.add(title)

        ax = Axes(x_range=[0, 10], y_range=[0, 2.5], x_length=8, y_length=4,
                  axis_config={"include_tip": False}).shift(DOWN*0.5)
        
        # 1. Signal X(f)
        x_signal = ax.plot(lambda f: 1.5 * np.exp(-5 * (f - 5)**2), color=BLUE, x_range=[3, 7])
        lbl_x = MathTex("X(f)", color=BLUE).next_to(x_signal, UP)
        
        self.play(Create(ax), Create(x_signal), Write(lbl_x))
        self.wait(1)

        # 2. Channel H(f)
        # A channel that varies across the signal bandwidth
        def h_channel(f):
            return 1.0 + 0.5 * np.cos(2 * f)
        
        h_plot = ax.plot(h_channel, color=YELLOW, stroke_opacity=0.6)
        lbl_h = MathTex("H(f)", color=YELLOW).next_to(ax.c2p(9, h_channel(9)), UP)

        self.play(Create(h_plot), Write(lbl_h))
        self.wait(1)

        # 3. Output Y(f)
        # Visually show the product
        y_plot = ax.plot(lambda f: (1.5 * np.exp(-5 * (f - 5)**2)) * h_channel(f), color=GREEN, x_range=[3, 7])
        lbl_y = MathTex("Y(f)", color=GREEN).next_to(y_plot, DR, buff=0.1)

        self.play(Transform(x_signal, y_plot), FadeOut(lbl_x), Write(lbl_y))
        
        distortion_text = Text("Channel shape distorts signal shape", font_size=24, color=WHITE).to_edge(DOWN)
        self.play(Write(distortion_text))
        self.wait(2)

        self.clear()

    def scene_define_bc_and_math(self):
        # Setup similar axis
        ax = Axes(x_range=[0, 10], y_range=[0, 2.5], x_length=9, y_length=4.5).shift(DOWN*0.3)
        
        # A smooth channel curve
        h_curve = ax.plot(lambda f: 1.2 + 0.4*np.cos(0.6*f) + 0.1*np.sin(1.2*f), color=YELLOW)
        
        self.add(ax, h_curve)
        
        # 4.3 Definition
        # Highlight a flat region (e.g., from x=1 to x=3 where it's relatively constant)
        bc_rect = ax.get_area(h_curve, x_range=[1.5, 3.5], color=BLUE, opacity=0.3)
        bc_brace = Brace(bc_rect, UP, color=BLUE)
        bc_text = bc_brace.get_text("Coherence Bandwidth $B_c$").scale(0.8)
        
        def_text = Text("Frequency range where channel gain is constant", font_size=24).to_edge(UP)

        self.play(FadeIn(bc_rect), GrowFromCenter(bc_brace), Write(bc_text))
        self.play(Write(def_text))
        self.wait(2)

        # 4.4 Mathematical Relationship
        # Fade out definition, fade in formula
        math_text = MathTex("B_c \\approx \\frac{1}{5\\sigma_\\tau}", color=BLUE, font_size=60).move_to(UP*2)
        intuition_text = Text("More time spread = Less frequency stability", font_size=24, color=GREY).next_to(math_text, DOWN)

        self.play(
            FadeOut(def_text),
            FadeOut(bc_brace), 
            FadeOut(bc_text),
            Transform(bc_rect, math_text), # Morph the visual region into the math
            Write(intuition_text)
        )
        self.wait(3)
        self.clear()

    def scene_correlation_levels(self):
        title = Title("Defining $B_c$ via Correlation", font_size=36)
        self.add(title)

        ax = Axes(x_range=[0, 5], y_range=[0, 1.2], x_length=6, y_length=4,
                  axis_config={"include_tip": True}).shift(LEFT*2)
        
        # Correlation function (approx sinc-like or exponential decay)
        corr_func = ax.plot(lambda x: np.exp(-x), color=PURPLE)
        corr_label = MathTex("R_H(\\Delta f)", color=PURPLE).next_to(corr_func, UR)
        
        # Lines for 0.9 and 0.5
        line_09 = DashedLine(ax.c2p(0, 0.9), ax.c2p(0.1, 0.9), color=WHITE) # Conceptual x value
        line_05 = DashedLine(ax.c2p(0, 0.5), ax.c2p(0.7, 0.5), color=WHITE)

        # Labels
        label_09 = MathTex("0.9").next_to(ax.c2p(0, 0.9), LEFT)
        label_05 = MathTex("0.5").next_to(ax.c2p(0, 0.5), LEFT)
        
        # Definitions text on the right
        text_09 = MathTex(r"B_{c,0.9} \approx \frac{1}{50\sigma_\tau}", font_size=36).to_edge(RIGHT).shift(UP)
        text_05 = MathTex(r"B_{c,0.5} \approx \frac{1}{5\sigma_\tau}", font_size=36).next_to(text_09, DOWN, buff=1)

        self.play(Create(ax), Create(corr_func), Write(corr_label))
        self.wait(0.5)
        
        self.play(Write(label_09), Create(line_09))
        self.play(Write(text_09))
        self.wait(1)
        
        self.play(Write(label_05), Create(line_05))
        self.play(Write(text_05))
        self.wait(2)
        self.clear()

    def scene_high_vs_low_bc_comparison(self):
        # Setup Side-by-Side
        ax_top = Axes(x_range=[0, 10], y_range=[0, 2], x_length=8, y_length=2.5, axis_config={"include_tip":False}).to_edge(UP, buff=1.0)
        ax_bot = Axes(x_range=[0, 10], y_range=[0, 2], x_length=8, y_length=2.5, axis_config={"include_tip":False}).to_edge(DOWN, buff=1.0)

        # Labels
        lbl_top = Text("High Coherence Bandwidth (Small Delay Spread)", color=GREEN, font_size=24).next_to(ax_top, UP)
        lbl_bot = Text("Low Coherence Bandwidth (Large Delay Spread)", color=RED, font_size=24).next_to(ax_bot, UP)

        # 1. High Bc Channel (Wide flat zones)
        h_high_bc = ax_top.plot(lambda f: 1 + 0.3*np.sin(0.8*f), color=GREEN)
        
        # 2. Low Bc Channel (Frequent notches)
        h_low_bc = ax_bot.plot(lambda f: 1 + 0.5*np.cos(3*f) + 0.3*np.sin(7*f), color=RED)

        # 3. The Signal (Identical in both cases!)
        # Place signal at f=5, width=1
        signal_bw_rect_top = Rectangle(width=1, height=1.5, color=BLUE, fill_opacity=0.3).move_to(ax_top.c2p(5, 0.75))
        signal_bw_rect_bot = Rectangle(width=1, height=1.5, color=BLUE, fill_opacity=0.3).move_to(ax_bot.c2p(5, 0.75))
        
        sig_lbl_top = Text("Signal", font_size=16, color=BLUE).next_to(signal_bw_rect_top, UP, buff=0)
        sig_lbl_bot = Text("Same Signal", font_size=16, color=BLUE).next_to(signal_bw_rect_bot, UP, buff=0)

        # Animation Sequence
        self.play(Write(lbl_top), Create(ax_top), Create(h_high_bc))
        self.play(Write(lbl_bot), Create(ax_bot), Create(h_low_bc))
        self.wait(1)
        
        self.play(FadeIn(signal_bw_rect_top), Write(sig_lbl_top))
        self.play(FadeIn(signal_bw_rect_bot), Write(sig_lbl_bot))
        
        # Narration cues via text
        note = Text("Signal stays the same. Channel changes.", font_size=24, color=YELLOW).move_to(ORIGIN)
        self.play(Write(note))
        self.wait(3)
        self.play(FadeOut(note))

    def scene_transition_question(self):
        # 4.7 Transition
        # Just text centered
        q_text = Text("The Critical Question:", color=BLUE, font_size=36).shift(UP)
        main_text = Text("Does my signal fit inside the flat window?", font_size=42)
        
        self.play(Write(q_text))
        self.play(Write(main_text))
        self.wait(3)