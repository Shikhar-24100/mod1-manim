from manim import *
import numpy as np

class CoherenceInteraction(Scene):
    def construct(self):
        # --- PART 1: FORMULAS ---
        formula_09 = MathTex(r"B_c \approx \frac{1}{50\sigma_\tau} \text{ (0.9 corr)}", color=BLUE).shift(UP)
        formula_05 = MathTex(r"B_c \approx \frac{1}{5\sigma_\tau} \text{ (0.5 corr)}", color=BLUE).shift(DOWN)
        self.play(Write(formula_09), Write(formula_05))
        self.wait(2)
        self.play(FadeOut(formula_09, formula_05))

        # --- PART 2: SIDE-BY-SIDE SETUP ---
        # We create a random-looking channel using a sum of a few sines to mimic the picture
        def random_channel(f):
            return 1.2 + 0.5*np.sin(f*0.8) + 0.3*np.cos(f*2.5) + 0.2*np.sin(f*4)

        ax_l = Axes(x_range=[0, 10], y_range=[0, 2.5], x_length=5, y_length=3).to_edge(LEFT, buff=0.5)
        ax_r = Axes(x_range=[0, 10], y_range=[0, 2.5], x_length=5, y_length=3).to_edge(RIGHT, buff=0.5)
        
        # H(f) for both
        h_func = lambda f: random_channel(f)
        h_plot_l = ax_l.plot(h_func, color=PURPLE)
        h_plot_r = ax_r.plot(h_func, color=PURPLE)
        
        self.add(ax_l, ax_r, h_plot_l, h_plot_r)
        self.add(Text("Y(f) = X(f)H(f)", font_size=24).to_edge(UP))

        # --- CASE 1: Narrow Signal (Bs < Bc) ---
        # Signal fits in a "flat" zone
        x_flat = ax_l.plot(lambda f: 1.8 * np.exp(-15 * (f - 5)**2), x_range=[4, 6], color=GREEN)
        bc_brace_l = BraceBetweenPoints(ax_l.c2p(3.5, 2.2), ax_l.c2p(6.5, 2.2), color=BLUE)
        bc_lab_l = bc_brace_l.get_text("$B_c$").scale(0.6)
        bs_lab_l = MathTex("B_s < B_c", color=GREEN, font_size=24).next_to(x_flat, UP)

        self.play(Create(x_flat), GrowFromCenter(bc_brace_l), Write(bc_lab_l), Write(bs_lab_l))
        
        # --- CASE 2: Wide Signal (Bs > Bc) ---
        # Signal spans across multiple "notches"
        x_wide = ax_r.plot(lambda f: 1.8 * np.exp(-0.5 * (f - 5)**2), x_range=[1, 9], color=RED)
        bc_brace_r = BraceBetweenPoints(ax_r.c2p(4.5, 2.2), ax_r.c2p(5.5, 2.2), color=BLUE) # Narrower Bc
        bc_lab_r = bc_brace_r.get_text("$B_c$").scale(0.6)
        bs_lab_r = MathTex("B_s > B_c", color=RED, font_size=24).next_to(x_wide, UP)

        self.play(Create(x_wide), GrowFromCenter(bc_brace_r), Write(bc_lab_r), Write(bs_lab_r))
        self.wait(3)

        # FINAL REVEAL: Highlight the affected Y(f)
        y_flat = ax_l.get_area(h_plot_l, x_range=[4.5, 5.5], color=YELLOW, opacity=0.5)
        y_distorted = ax_r.get_area(h_plot_r, x_range=[1, 9], color=YELLOW, opacity=0.5)
        
        self.play(FadeIn(y_flat), FadeIn(y_distorted))
        self.play(Indicate(y_distorted, color=RED, scale_factor=1.1)) # Show distortion effect
        self.wait(2)