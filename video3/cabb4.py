from manim import *
import numpy as np

class FadingScenarios_LeftRight(Scene):
    def construct(self):
        # PALETTE
        C_TEXT = WHITE
        C_MATH = BLUE_C      # Equations
        C_CHANNEL = YELLOW   # Channel H(f)
        C_SIGNAL = BLUE      # Signal X(f)
        C_OUTPUT = RED       # Output Y(f) - Distorted

        # 1. HEADER
        # ---------
        header = MathTex(
            r"Y(f) = X(f) \cdot H(f)",
            font_size=40, color=C_TEXT
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(header))
        self.wait(4)

        # 2. SETUP AXES (Left vs Right)
        # -----------------------------
        ax_left = Axes(
            x_range=[0, 10], y_range=[0, 2],
            x_length=6, y_length=3.5,
            axis_config={"include_tip": False, "color": GREY},
        ).to_edge(LEFT, buff=0.5).shift(DOWN*0.5)

        ax_right = Axes(
            x_range=[0, 10], y_range=[0, 2],
            x_length=6, y_length=3.5,
            axis_config={"include_tip": False, "color": GREY},
        ).to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)

        # Labels
        lbl_left = MathTex(r"\text{Case A: } B_s << B_c", color=C_TEXT, font_size=28).next_to(ax_left, UP)
        lbl_right = MathTex(r"\text{Case B: } B_s >> B_c", color=C_TEXT, font_size=28).next_to(ax_right, UP)

        self.play(FadeIn(ax_left), FadeIn(ax_right), Write(lbl_left), Write(lbl_right))

        # 3. DEFINE THE SIGNAL (X(f)) - IDENTICAL FOR BOTH
        # ------------------------------------------------
        # A Gaussian pulse centered at f=5
        def get_signal_func(f):
            # Wider Gaussian: reduce exponent coefficient (larger sigma)
            return 1.2 * np.exp(-1.0 * (f - 5)**2)

        # 4. LEFT SCENARIO: FLAT FADING (Wide Bc)
        # ---------------------------------------
        # Channel: Very broad, flat top
        h_flat_func = lambda f: 1.0 + 0.1 * np.cos(0.5 * (f - 5))
        h_flat = ax_left.plot(h_flat_func, color=C_CHANNEL, x_range=[0, 10], stroke_width=3)
        
        # Signal Plot
        x_plot_l = ax_left.plot(get_signal_func, color=C_SIGNAL, x_range=[2, 8], stroke_width=2)
        x_area_l = ax_left.get_area(x_plot_l, color=C_SIGNAL, opacity=0.3)
        x_label_l = MathTex("X(f)", color=C_SIGNAL, font_size=24).next_to(x_plot_l, UP, buff=0.1)

        self.play(Create(h_flat), FadeIn(x_area_l), Create(x_plot_l), Write(x_label_l))

        # Bc Markers (Vertical Lines) - Wide
        # Visualizing a region from 2 to 8 where gain is roughly constant
        line_bc_l1 = DashedLine(ax_left.c2p(2, 0), ax_left.c2p(2, 1.5), color=C_CHANNEL)
        line_bc_l2 = DashedLine(ax_left.c2p(8, 0), ax_left.c2p(8, 1.5), color=C_CHANNEL)
        bc_text_l = MathTex("B_c", color=C_CHANNEL, font_size=24).next_to(line_bc_l1, UP).shift(RIGHT*1.5) # Roughly center
        
        self.play(Create(line_bc_l1), Create(line_bc_l2), Write(bc_text_l))
        
        # Output Y(f) (Essentially same as X(f))
        res_left = Text("Signal Undistorted", font_size=20, color=C_TEXT).next_to(ax_left, DOWN)
        self.play(Write(res_left))
        self.wait(1)

        # 5. RIGHT SCENARIO: SELECTIVE FADING (Narrow Bc)
        # -----------------------------------------------
        # Channel: Ripples (Notches)
        h_select_func = lambda f: 1.0 + 0.8 * np.cos(2.5 * (f - 5)) # Deep notch at 5? No, peak at 5. Let's shift phase.
        # We want a NOTCH inside the signal. Signal is at 5.
        # cos(pi) = -1. So if we want notch at 5... 2.5(5-5) = 0 (peak).
        # Let's use sin or shift it so there's a dip at 5.
        # Try: 1.0 - 0.7 * exp(...) to simulate a deep fade right in the middle? 
        # Or just standard ripples:
        h_select_func = lambda f: 1.0 + 0.6 * np.cos(3 * (f - 4.5)) 
        
        h_select = ax_right.plot(h_select_func, color=C_CHANNEL, x_range=[0, 10], stroke_width=3)

        # Signal Plot (IDENTICAL to Left)
        x_plot_r = ax_right.plot(get_signal_func, color=C_SIGNAL, x_range=[2, 8], stroke_width=2)
        x_area_r = ax_right.get_area(x_plot_r, color=C_SIGNAL, opacity=0.3)
        x_label_r = MathTex("X(f)", color=C_SIGNAL, font_size=24).next_to(x_plot_r, UP, buff=0.1)

        self.play(Create(h_select), FadeIn(x_area_r), Create(x_plot_r), Write(x_label_r))

        # Bc Markers (Vertical Lines) - Narrow
        # Visualizing a small peak width, e.g., from 3.5 to 4.5
        # line_bc_r1 = DashedLine(ax_right.c2p(3.8, 0), ax_right.c2p(3.8, 1.5), color=C_CHANNEL)
        # line_bc_r2 = DashedLine(ax_right.c2p(4.8, 0), ax_right.c2p(4.8, 1.5), color=C_CHANNEL)
        # bc_text_r = MathTex("B_c", color=C_CHANNEL, font_size=24).next_to(line_bc_r1, UP).shift(RIGHT*0.3)

        # self.play(Create(line_bc_r1), Create(line_bc_r2), Write(bc_text_r))

        # 6. VISUALIZE DISTORTION (Y = H*X)
        # ---------------------------------
        # Calculate the product
        y_func = lambda f: get_signal_func(f) * h_select_func(f)
        
        y_plot = ax_right.plot(y_func, color=C_OUTPUT, x_range=[2, 8], stroke_width=2)
        y_area = ax_right.get_area(y_plot, color=C_OUTPUT, opacity=0.6)
        
        # Flash the distortion
        self.play(
            FadeOut(x_area_r), 
            FadeIn(y_area), 
            FadeOut(x_label_r),
            Transform(x_plot_r, y_plot)
        )
        
        res_right = Text("Signal Distorted", font_size=20, color=C_OUTPUT).next_to(ax_right, DOWN)
        self.play(Write(res_right))
        
        self.wait(3)