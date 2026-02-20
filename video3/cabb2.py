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
        self.wait(13)

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
        lbl_left = MathTex(r"\text{Case A: } B_s \ll B_c", color=C_TEXT, font_size=22).next_to(ax_left, UP, buff=0.15)
        lbl_right = MathTex(r"\text{Case B: } B_s \gg B_c", color=C_TEXT, font_size=22).next_to(ax_right, UP, buff=0.15)

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
        self.wait(9)

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
        self.wait(9)

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
        
        self.wait(6)
        
        # --- TRANSITION: Scale down frequency domain and add time domain ---
        # Fade out the header formula
        self.play(FadeOut(header))
        
        # Group frequency domain objects (WITHOUT labels) for smooth collective animation
        freq_left_group = VGroup(ax_left, h_flat, x_plot_l, x_area_l, x_label_l, line_bc_l1, line_bc_l2, bc_text_l)
        freq_right_group = VGroup(ax_right, h_select, x_plot_r, y_area)
        
        # Scale and move as unified groups
        scaling_factor = 0.6
        new_center_left = LEFT * 3.5 + UP * 1.8
        new_center_right = RIGHT * 3.5 + UP * 1.8
        
        # Target positions for labels (just move, don't scale)
        lbl_left_new_pos = new_center_left + UP * 1.2
        lbl_right_new_pos = new_center_right + UP * 1.2
        
        # Single smooth animation for all frequency domain content
        self.play(
            freq_left_group.animate.scale(scaling_factor).move_to(new_center_left),
            freq_right_group.animate.scale(scaling_factor).move_to(new_center_right),
            lbl_left.animate.move_to(lbl_left_new_pos),
            lbl_right.animate.move_to(lbl_right_new_pos),
            FadeOut(res_left),
            FadeOut(res_right),
            run_time=2
        )
        
        self.wait(3.5)
        
        # Create time domain axes with SAME dimensions as scaled frequency axes
        # Original frequency axes: x_length=6, y_length=3.5
        # Scaled by 0.5: x_length=3, y_length=1.75
        ax_time_left = Axes(
            x_range=[0, 10, 1], y_range=[0, 1.5, 1],
            x_length=3.6, y_length=2.1,
            axis_config={"include_tip": False, "color": GREY},
        ).move_to(LEFT * 3.5 + DOWN * 1.5)
        
        ax_time_right = Axes(
            x_range=[0, 10, 1], y_range=[0, 1.5, 1],
            x_length=3.6, y_length=2.1,
            axis_config={"include_tip": False, "color": GREY},
        ).move_to(RIGHT * 3.5 + DOWN * 1.5)
        
        # Labels for time domain (scaled to match frequency labels)
        lbl_time_left = MathTex(r"\sigma_\tau \geq T_r", color=C_TEXT, font_size=22).next_to(ax_time_left, UP, buff=0.15)
        lbl_time_right = MathTex(r"\sigma_\tau \ll T_r", color=C_TEXT, font_size=22).next_to(ax_time_right, UP, buff=0.15)
        
        # Helper function to create symbol blocks (like cab6.py)
        def get_time_block(axes, start, width, height, color, opacity=1.0, label=""):
            rect = Rectangle(
                width=axes.c2p(width, 0)[0] - axes.c2p(0, 0)[0],
                height=axes.c2p(0, height)[1] - axes.c2p(0, 0)[1],
                fill_color=color, fill_opacity=opacity, stroke_color=WHITE, stroke_width=1
            )
            rect.move_to(axes.c2p(start + width/2, height/2))
            txt = Text(label, font_size=9, color=BLACK if opacity > 0.5 else WHITE).move_to(rect.get_center())
            return VGroup(rect, txt)
        
        # CASE A: ISI - Symbol 1 (GREEN) with 4 copies, Symbol 2 (BLUE) with 4 copies OVERLAPPING
        sym1_main_a = get_time_block(ax_time_left, 1, 1, 1, GREEN, opacity=0.9, label="1")
        sym1_g1_a = get_time_block(ax_time_left, 1.4, 1, 0.8, GREEN, opacity=0.7, label="1'")
        sym1_g2_a = get_time_block(ax_time_left, 1.8, 1, 0.6, GREEN, opacity=0.5, label="1''")
        sym1_g3_a = get_time_block(ax_time_left, 2.2, 1, 0.4, GREEN, opacity=0.3, label="1'''")
        
        sym2_main_a = get_time_block(ax_time_left, 3, 1, 1, BLUE, opacity=0.9, label="2")
        sym2_g1_a = get_time_block(ax_time_left, 3.4, 1, 0.8, BLUE, opacity=0.7, label="2'")
        sym2_g2_a = get_time_block(ax_time_left, 3.8, 1, 0.6, BLUE, opacity=0.5, label="2''")
        sym2_g3_a = get_time_block(ax_time_left, 4.2, 1, 0.4, BLUE, opacity=0.3, label="2'''")
        
        # Highlight the collision region
        collision_rect_a = Rectangle(
            width=ax_time_left.c2p(0.2, 0)[0] - ax_time_left.c2p(0, 0)[0],
            height=ax_time_left.c2p(0, 0.4)[1] - ax_time_left.c2p(0, 0)[1],
            color=RED, fill_opacity=0.4, stroke_width=0
        ).move_to(ax_time_left.c2p(3.1, 0.2))
        
        # CASE B: No ISI - Symbol 1 (GREEN) with 4 copies WELL SEPARATED, Symbol 2 (BLUE) with 4 copies WELL SEPARATED
        sym1_main_b = get_time_block(ax_time_right, 0.5, 1, 1, GREEN, opacity=0.9, label="1")
        sym1_g1_b = get_time_block(ax_time_right, 1.5, 1, 0.8, GREEN, opacity=0.7, label="1'")
        sym1_g2_b = get_time_block(ax_time_right, 2.5, 1, 0.6, GREEN, opacity=0.5, label="1''")
        sym1_g3_b = get_time_block(ax_time_right, 3.5, 1, 0.4, GREEN, opacity=0.3, label="1'''")
        
        sym2_main_b = get_time_block(ax_time_right, 5.5, 1, 1, BLUE, opacity=0.9, label="2")
        sym2_g1_b = get_time_block(ax_time_right, 6.5, 1, 0.8, BLUE, opacity=0.7, label="2'")
        sym2_g2_b = get_time_block(ax_time_right, 7.5, 1, 0.6, BLUE, opacity=0.5, label="2''")
        sym2_g3_b = get_time_block(ax_time_right, 8.5, 1, 0.4, BLUE, opacity=0.3, label="2'''")
        
        # Animate time domain axes appearance
        self.play(
            Create(ax_time_left), Create(ax_time_right),
            Write(lbl_time_left), Write(lbl_time_right),
            run_time=1
        )
        
        # Create all symbol blocks for Case A (ISI)
        self.play(
            LaggedStart(*[FadeIn(g, shift=RIGHT*0.1) for g in [sym1_main_a, sym1_g1_a, sym1_g2_a, sym1_g3_a]], lag_ratio=0.3),
            LaggedStart(*[FadeIn(g, shift=RIGHT*0.1) for g in [sym2_main_a, sym2_g1_a, sym2_g2_a, sym2_g3_a]], lag_ratio=0.3),
            run_time=1.5
        )
        self.play(FadeIn(collision_rect_a))
        
        # Create all symbol blocks for Case B (No ISI)
        self.play(
            LaggedStart(*[FadeIn(g, shift=RIGHT*0.1) for g in [sym1_main_b, sym1_g1_b, sym1_g2_b, sym1_g3_b]], lag_ratio=0.3),
            LaggedStart(*[FadeIn(g, shift=RIGHT*0.1) for g in [sym2_main_b, sym2_g1_b, sym2_g2_b, sym2_g3_b]], lag_ratio=0.3),
            run_time=1.5
        )
        
        self.wait(4)