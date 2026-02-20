from manim import *
import random
import numpy as np

class ResourceAllocationWithShannon(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # CONFIGURATION & ASSETS
        # ---------------------------------------------------------
        try:
            tower_svg = SVGMobject("assets/tower.svg").scale(2)
        except:
            tower_svg = VGroup(Line(DOWN, UP), Triangle()).arrange(UP, buff=0).scale(2).set_color(GRAY)

        # ---------------------------------------------------------
        # Part 1: Single User - The Ideal Case with Shannon
        # ---------------------------------------------------------
        title = Text("The Resource Allocation Problem").to_edge(UP)
        self.play(Write(title), run_time=1)

        tower = tower_svg.copy().to_edge(LEFT, buff=1.5).shift(DOWN * 0.5)
        tower_label = Text("Base Station", font_size=20).next_to(tower, DOWN)

        user_dot = Dot(radius=0.15, color=BLUE).move_to(RIGHT * 4.5 + DOWN * 0.5)
        user_label = Text("User 1", font_size=24).next_to(user_dot, DOWN)

        self.play(
            FadeIn(tower), 
            Write(tower_label),
            FadeIn(user_dot), 
            Write(user_label)
        )

        spectrum_bar = Rectangle(width=6, height=0.6, color=GREEN, fill_opacity=0.5, stroke_width=2)
        spectrum_bar.next_to(title, DOWN, buff=0.5)
        spectrum_label = Text("Available Spectrum: 25 MHz", font_size=24).next_to(spectrum_bar, UP, buff=0.1)

        self.play(Create(spectrum_bar), Write(spectrum_label))

        arrow_1 = Arrow(start=spectrum_bar.get_bottom(), end=user_dot.get_top(), color=GREEN, buff=0.1)
        self.play(GrowArrow(arrow_1))
        
        shannon_title = Text("Shannon's Capacity Theorem:", font_size=22, color=YELLOW).to_edge(DOWN,buff=3.2)
        shannon_formula = MathTex(r"C = B \log_2(1 + \text{SNR})", font_size=32).next_to(shannon_title, DOWN, buff=0.3)
        
        self.play(Write(shannon_title), Write(shannon_formula))
        self.wait(1)
        
        calculation_single = MathTex(r"C = 25 \text{ MHz} \times \log_2(1 + 1000) \approx 250 \text{ Mbps}", font_size=28, color=GREEN).next_to(shannon_formula, DOWN, buff=0.4)
        result_text = Text("Excellent Speed!", color=GREEN, font_size=24).next_to(calculation_single, DOWN, buff=0.3)
        
        self.play(Write(calculation_single))
        self.play(FadeIn(result_text))
        self.wait(2)

        # ---------------------------------------------------------
        # Part 2: Multiple Users - Bandwidth Division
        # ---------------------------------------------------------
        self.play(FadeOut(arrow_1), FadeOut(user_label), FadeOut(calculation_single), FadeOut(result_text))

        crowd = VGroup(user_dot)
        for _ in range(25):
            d = Dot(color=BLUE, radius=0.12)
            offset = [random.uniform(-2, 2), random.uniform(-1.5, 1.5), 0]
            d.move_to(user_dot.get_center() + np.array(offset))
            crowd.add(d)

        crowd_label = Text("(100 Users)", font_size=24).next_to(crowd, DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(d) for d in crowd if d is not user_dot], lag_ratio=0.02), Write(crowd_label), run_time=2)

        division_eq = MathTex(r"\frac{25 \text{ MHz}}{100 \text{ Users}} = 250 \text{ kHz/user}", font_size=28).move_to(RIGHT * 2 + UP * 1.5)
        self.play(Write(division_eq))

        slice_width = spectrum_bar.width / 25 
        red_slice = Rectangle(width=slice_width, height=0.6, color=ORANGE, fill_opacity=0.9, stroke_width=2).align_to(spectrum_bar, LEFT).align_to(spectrum_bar, UP)

        self.play(spectrum_bar.animate.set_opacity(0.1), FadeIn(red_slice))
        self.play(shannon_title.animate.shift(UP * 0.3), shannon_formula.animate.shift(UP * 0.3))
        
        calculation_multi = MathTex(r"C = 250 \text{ kHz} \times \log_2(1 + 1000) \approx 2.5 \text{ Mbps}", font_size=28, color=ORANGE).next_to(shannon_formula, DOWN, buff=0.4)
        still_ok = Text("Still usable... IF no interference!", font_size=22, color=ORANGE).next_to(calculation_multi, DOWN, buff=0.3)
        
        self.play(Write(calculation_multi), Write(still_ok))
        self.wait(1)

        # ---------------------------------------------------------
        # Part 3: The Real Problem - Interference (UPDATED)
        # ---------------------------------------------------------
        assumption_box = SurroundingRectangle(still_ok[16:], color=RED, buff=0.1)
        self.play(Create(assumption_box))
        
        interference_title = Text("But what if users interfere?", font_size=26, color=RED).to_edge(UP)
        self.play(FadeOut(title), FadeIn(interference_title))

        # --- FLUCTUATION EFFECT (5-6 Seconds) ---
        # We turn the bars red first to set the mood
        self.play(
            spectrum_bar.animate.set_color(RED).set_opacity(0.3),
            red_slice.animate.set_color(RED),
            run_time=0.5
        )

        # Loop for ~5 seconds of jittery interference
        for _ in range(10): # 10 iterations * 0.5s = 5 seconds
            self.play(
                *[d.animate.set_opacity(random.uniform(0.1, 1.0)) for d in crowd],
                run_time=0.5,
                rate_func=there_and_back
            )
        
        # Stop fluctuation and settle on a "noisy" look (semi-transparent)
        self.play(crowd.animate.set_opacity(0.4), run_time=0.5)

        # --- Back to "Usual Shit" (Calculations) ---
        shannon_formula_new = MathTex(
            r"C = B \log_2(1 + \frac{S}{I+N}) = B \log_2(1 + \text{SINR})",
            font_size=30, color=RED
        ).move_to(shannon_formula.get_center())
        
        sinr_label = Text("SINR = Signal to Interference + Noise Ratio", font_size=18, color=RED).next_to(shannon_formula_new, DOWN, buff=0.2)
        
        self.play(
            FadeOut(shannon_formula), FadeOut(shannon_title),
            Write(shannon_formula_new), Write(sinr_label),
            FadeOut(assumption_box), FadeOut(still_ok),
            FadeOut(calculation_multi), FadeOut(division_eq)
        )
        
        bad_sinr = MathTex(r"\text{SINR} \downarrow \downarrow \quad \Rightarrow \quad C \downarrow \downarrow", font_size=32, color=RED).next_to(sinr_label, DOWN, buff=0.5)
        self.play(Write(bad_sinr))
        self.wait(2)

        # ---------------------------------------------------------
        # Part 4: The Core Question
        # ---------------------------------------------------------
        cleanup_all = VGroup(
            tower, tower_label, crowd, crowd_label, 
            spectrum_bar, spectrum_label, red_slice,
            shannon_formula_new, sinr_label, bad_sinr, interference_title
        )
        self.play(FadeOut(cleanup_all))

        main_question = VGroup(
            Text("The Core Challenge:", font_size=36, color=YELLOW),
            Text("How do we share limited spectrum", font_size=28),
            Text("among many users", font_size=28),
            Text("without destroying each other's signal?", font_size=28, color=RED)
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        
        self.play(Write(main_question))
        self.wait(1)
        
        # solution_hint = Text("Answer: Orthogonality", font_size=32, color=GREEN).next_to(main_question, DOWN, buff=1)
        # self.play(FadeIn(solution_hint, shift=UP))
        self.wait(5)