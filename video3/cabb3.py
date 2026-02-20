from manim import *
import numpy as np

class FadingClassificationFinal(Scene):
    def construct(self):
        # ============================================
        # 0. STYLE CONFIGURATION
        # ============================================
        C_BG = "#000000"        # Background
        C_TEXT = "#ECECEC"      # Off-white text
        C_INPUT = "#FFD700"     # Gold (Signal)
        C_FLAT = "#40E0D0"      # Turquoise (Flat/Safe)
        C_SELECT = "#FF6B6B"    # Soft Red (Selective/Danger)
        C_AXIS = GREY_C
        
        # Font Sizes
        F_TITLE = 32
        F_SUB = 20
        F_LABEL = 18
        F_MATH = 30 


        title = Text("Small-Scale Fading Classification", font_size=F_TITLE, coalor=C_TEXT)
        title.to_edge(UP, buff=0.2)
        
        subtitle = Text("(Based on Multipath Time Delay Spread)", font_size=F_SUB, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.1)

        self.add(title, subtitle)
        self.wait(3)
        # ============================================
        # 2. COMMON INPUT SIGNAL (TOP CENTER)
        # ============================================
        ax_input = Axes(
            x_range=[0, 4], y_range=[0, 1.2],
            x_length=2.5, y_length=1.2,
            axis_config={"color": C_AXIS, "include_ticks": False, "include_tip": False}
        ).move_to(UP * 2.2)

        plot_input = ax_input.plot(lambda x: 1.0 * np.exp(-10 * (x - 2)**2), color=C_INPUT)
        area_input = ax_input.get_area(plot_input, color=C_INPUT, opacity=0.3)
        lbl_input = Text("Input X(f)", font_size=F_LABEL, color=C_INPUT).next_to(ax_input, RIGHT, buff=0.05)

        # Group input elements
        group_input = VGroup(ax_input, plot_input, area_input, lbl_input)

        self.play(FadeIn(ax_input), Create(plot_input), FadeIn(area_input), Write(lbl_input))

        # ============================================
        # 3. SPLIT PATHS (ARROWS)
        # ============================================
        LEFT_COL = LEFT * 3.5
        RIGHT_COL = RIGHT * 3.5
        
        Y_CHANNEL = 0.2
        Y_OUTPUT = -2.0

        # arrow_l = Arrow(start=ax_input.get_bottom(), end=LEFT_COL + UP*(Y_CHANNEL+0.8), color=GREY, buff=0.2)
        # arrow_r = Arrow(start=ax_input.get_bottom(), end=RIGHT_COL + UP*(Y_CHANNEL+0.8), color=GREY, buff=0.2)
        
        # self.play(Create(arrow_l), Create(arrow_r))

        # ============================================
        # 4. LEFT COLUMN: FLAT FADING
        # ============================================
        title_flat = Text("Flat Fading", font_size=24, color=C_FLAT, weight=BOLD).move_to(LEFT_COL + UP*(Y_CHANNEL+1.2))
        self.play(Write(title_flat))

        # --- Channel H(f) ---
        ax_h_l = Axes(
            x_range=[0, 4], y_range=[0, 1.2], x_length=2.5, y_length=1.0,
            axis_config={"color": C_AXIS, "include_ticks": False, "include_tip": False}
        ).move_to(LEFT_COL + UP*Y_CHANNEL)
        
        plot_h_l = Rectangle(width=2.5, height=0.8, color=C_FLAT, fill_opacity=0.2, stroke_width=2).move_to(ax_h_l.c2p(2, 0.4))
        lbl_h_l = Text("Channel H(f) [Flat]", font_size=F_LABEL, color=C_FLAT).next_to(ax_h_l, UP, buff=0.05)
        
        self.play(FadeIn(ax_h_l), Create(plot_h_l), Write(lbl_h_l))

        arr_down_l = Arrow(start=ax_h_l.get_bottom(), end=LEFT_COL + UP*(Y_OUTPUT+0.7), color=C_FLAT, buff=0.1, max_stroke_width_to_length_ratio=5)
        self.play(Create(arr_down_l))

        # --- Output Y(f) ---
        ax_y_l = Axes(
            x_range=[0, 4], y_range=[0, 1.2], x_length=2.5, y_length=1.0,
            axis_config={"color": C_AXIS, "include_ticks": False, "include_tip": False}
        ).move_to(LEFT_COL + UP*Y_OUTPUT)

        plot_y_l = ax_y_l.plot(lambda x: 1.0 * np.exp(-10 * (x - 2)**2), color=C_FLAT)
        area_y_l = ax_y_l.get_area(plot_y_l, color=C_FLAT, opacity=0.4)
        lbl_y_l = Text("Output Y(f) [Undistorted]", font_size=F_LABEL, color=C_FLAT).next_to(ax_y_l, UP, buff=0.05)

        self.play(FadeIn(ax_y_l), Create(plot_y_l), FadeIn(area_y_l), Write(lbl_y_l))
        
        # Group left visuals
        group_left_visuals = VGroup(ax_h_l, plot_h_l, lbl_h_l, arr_down_l, ax_y_l, plot_y_l, area_y_l, lbl_y_l)

        # ============================================
        # 5. RIGHT COLUMN: SELECTIVE FADING
        # ============================================
        title_select = Text("Selective Fading", font_size=24, color=C_SELECT, weight=BOLD).move_to(RIGHT_COL + UP*(Y_CHANNEL+1.2))
        self.play(Write(title_select))

        # --- Channel H(f) ---
        ax_h_r = Axes(
            x_range=[0, 4], y_range=[0, 1.2], x_length=2.5, y_length=1.0,
            axis_config={"color": C_AXIS, "include_ticks": False, "include_tip": False}
        ).move_to(RIGHT_COL + UP*Y_CHANNEL)

        plot_h_r = ax_h_r.plot(lambda x: 0.8 * np.exp(-30 * (x - 2)**2) + 0.2, color=C_SELECT)
        area_h_r = ax_h_r.get_area(plot_h_r, color=C_SELECT, opacity=0.2)
        lbl_h_r = Text("Channel H(f) [Selective]", font_size=F_LABEL, color=C_SELECT).next_to(ax_h_r, UP, buff=0.05)

        self.play(FadeIn(ax_h_r), Create(plot_h_r), FadeIn(area_h_r), Write(lbl_h_r))

        arr_down_r = Arrow(start=ax_h_r.get_bottom(), end=RIGHT_COL + UP*(Y_OUTPUT+0.7), color=C_SELECT, buff=0.1, max_stroke_width_to_length_ratio=5)
        self.play(Create(arr_down_r))

        # --- Output Y(f) ---
        ax_y_r = Axes(
            x_range=[0, 4], y_range=[0, 1.2], x_length=2.5, y_length=1.0,
            axis_config={"color": C_AXIS, "include_ticks": False, "include_tip": False}
        ).move_to(RIGHT_COL + UP*Y_OUTPUT)

        plot_y_r = ax_y_r.plot(lambda x: 0.8 * np.exp(-30 * (x - 2)**2), color=C_SELECT)
        area_y_r = ax_y_r.get_area(plot_y_r, color=C_SELECT, opacity=0.4)
        lbl_y_r = Text("Output Y(f) [Distorted]", font_size=F_LABEL, color=C_SELECT).next_to(ax_y_r, UP, buff=0.05)

        self.play(FadeIn(ax_y_r), Create(plot_y_r), FadeIn(area_y_r), Write(lbl_y_r))

        # Group right visuals
        group_right_visuals = VGroup(ax_h_r, plot_h_r, area_h_r, lbl_h_r, arr_down_r, ax_y_r, plot_y_r, area_y_r, lbl_y_r)

        self.wait(1)

        # ============================================
        # 6. TRANSITION: FADE EVERYTHING OUT EXCEPT TITLES
        # ============================================
        self.play(
            FadeOut(group_input),
            # FadeOut(arrow_l), FadeOut(arrow_r),
            FadeOut(group_left_visuals),
            FadeOut(group_right_visuals),
            FadeOut(title), FadeOut(subtitle),
            # Move titles to center screen while others fade out
            title_flat.animate.move_to(LEFT * 3.5 + UP * 1),
            title_select.animate.move_to(RIGHT * 3.5 + UP * 1)
        )

        # ============================================
        # 7. REVEAL CONDITIONS CLEANLY
        # ============================================
        # Left Conditions (Flat)
        cond_l = VGroup(
            MathTex(r"1.\, B_{signal} \ll B_{coherence}", color=C_FLAT, font_size=F_MATH),
            MathTex(r"2.\, \sigma_{\tau} \ll T_{symbol}", color=C_FLAT, font_size=F_MATH)
        ).arrange(DOWN, buff=0.4).next_to(title_flat, DOWN, buff=1.0)

        # Right Conditions (Selective)
        cond_r = VGroup(
            MathTex(r"1.\, B_{signal} > B_{coherence}", color=C_SELECT, font_size=F_MATH),
            MathTex(r"2.\, \sigma_{\tau} > T_{symbol}", color=C_SELECT, font_size=F_MATH)
        ).arrange(DOWN, buff=0.4).next_to(title_select, DOWN, buff=1.0)

        # Optional: Add neat boxes around them
        box_l = SurroundingRectangle(cond_l, color=C_FLAT, buff=0.3, corner_radius=0.1, stroke_opacity=0.5)
        box_r = SurroundingRectangle(cond_r, color=C_SELECT, buff=0.3, corner_radius=0.1, stroke_opacity=0.5)

        self.play(Write(cond_l), Create(box_l))
        self.play(Write(cond_r), Create(box_r))

        self.wait(4)