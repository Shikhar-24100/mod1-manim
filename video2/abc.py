from manim import *
import numpy as np

class PhaseEquationScene(Scene):
    def construct(self):
        # === TITLE ===
        title = Text("The Phase Equation", font_size=40, weight=BOLD, color=BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)
        
        # =====================
        # STEP 1: Introduce the general formula
        # =====================
        
        main_formula = MathTex(
            r"\phi = \frac{2\pi d}{\lambda}",
            font_size=56,
            color=YELLOW
        )
        main_formula.move_to(ORIGIN + UP * 1.5)
        
        formula_box = SurroundingRectangle(main_formula, color=GREEN, buff=0.25, stroke_width=3)
        
        explain_text = Text("Phase depends on distance traveled", font_size=26, color=WHITE)
        explain_text.next_to(main_formula, DOWN, buff=0.5)
        
        self.play(Write(main_formula), run_time=1.0)
        self.play(Create(formula_box), run_time=0.5)
        self.play(FadeIn(explain_text, shift=UP * 0.2), run_time=0.6)
        
        self.wait(1.0)
        
        # =====================
        # STEP 2: Two receivers setup
        # =====================
        
        self.play(
            FadeOut(explain_text),
            VGroup(main_formula, formula_box).animate.scale(0.7).to_edge(UP, buff=0.8).shift(DOWN * 0.3),
            FadeOut(title),
            run_time=0.8
        )
        
        # Show two receiver scenario
        scenario_title = Text("Two receivers at different distances:", font_size=28, color=WHITE)
        scenario_title.next_to(main_formula, DOWN, buff=0.6)
        self.play(FadeIn(scenario_title), run_time=0.5)
        
        # Phi 1 equation
        phi1_eq = MathTex(
            r"\phi_1", r"=", r"\frac{2\pi \cdot d_1}{\lambda}",
            font_size=44
        )
        phi1_eq.set_color_by_tex(r"\phi_1", GREEN)
        phi1_eq.move_to(LEFT * 3 + DOWN * 0.5)
        
        # Phi 2 equation  
        phi2_eq = MathTex(
            r"\phi_2", r"=", r"\frac{2\pi \cdot (d_1 + \frac{\lambda}{2})}{\lambda}",
            font_size=44
        )
        phi2_eq.set_color_by_tex(r"\phi_2", ORANGE)
        phi2_eq.move_to(RIGHT * 2.5 + DOWN * 0.5)
        
        # Labels
        label1 = Text("Receiver 1", font_size=22, color=GREEN)
        label1.next_to(phi1_eq, UP, buff=0.3)
        
        label2 = Text("Receiver 2 (λ/2 further)", font_size=22, color=ORANGE)
        label2.next_to(phi2_eq, UP, buff=0.3)
        
        # Animate both appearing
        self.play(
            Write(phi1_eq),
            FadeIn(label1),
            run_time=1.0
        )
        self.wait(0.5)
        
        self.play(
            Write(phi2_eq),
            FadeIn(label2),
            run_time=1.0
        )
        
        self.wait(1.0)
        
        # =====================
        # STEP 3: Simplify Phi 2
        # =====================
        
        simplify_text = Text("Let's simplify φ₂:", font_size=26, color=YELLOW)
        simplify_text.move_to(DOWN * 1.8)
        self.play(FadeIn(simplify_text), run_time=0.5)
        
        self.wait(0.5)
        
        # Expand phi2
        phi2_expand = MathTex(
            r"\phi_2 = \frac{2\pi \cdot d_1}{\lambda} + \frac{2\pi \cdot \frac{\lambda}{2}}{\lambda}",
            font_size=40,
            color=ORANGE
        )
        phi2_expand.move_to(DOWN * 2.5)
        
        self.play(Write(phi2_expand), run_time=1.2)
        self.wait(0.8)
        
        # Simplify further
        phi2_simple = MathTex(
            r"\phi_2 = \phi_1 + \pi",
            font_size=48,
            color=ORANGE
        )
        phi2_simple.move_to(DOWN * 2.5)
        
        self.play(Transform(phi2_expand, phi2_simple), run_time=1.0)
        
        self.wait(0.8)
        
        # =====================
        # STEP 4: Phase difference
        # =====================
        
        self.play(FadeOut(simplify_text), run_time=0.3)
        
        # Clear and show phase difference
        phase_diff_title = Text("Phase Difference:", font_size=28, color=YELLOW)
        phase_diff_title.move_to(DOWN * 1.6)
        
        self.play(FadeIn(phase_diff_title), run_time=0.5)
        
        # The key result
        phase_diff = MathTex(
            r"\phi_2 - \phi_1", r"=", r"\pi", r"= 180°",
            font_size=52
        )
        phase_diff.set_color_by_tex(r"\phi_2", ORANGE)
        phase_diff.set_color_by_tex(r"\phi_1", GREEN)
        phase_diff.set_color_by_tex(r"\pi", RED)
        phase_diff.set_color_by_tex(r"180°", RED)
        phase_diff.move_to(DOWN * 2.5)
        
        result_box = SurroundingRectangle(phase_diff, color=RED, buff=0.2, stroke_width=4)
        
        self.play(
            FadeOut(phi2_expand),
            Write(phase_diff),
            run_time=1.0
        )
        self.play(Create(result_box), run_time=0.5)
        
        self.wait(0.8)
        
        # =====================
        # STEP 5: Visual confirmation with phasors
        # =====================
        
        # Fade out equations, show phasors
        self.play(
            FadeOut(phi1_eq), FadeOut(phi2_eq),
            FadeOut(label1), FadeOut(label2),
            FadeOut(scenario_title),
            FadeOut(main_formula), FadeOut(formula_box),
            VGroup(phase_diff_title, phase_diff, result_box).animate.shift(UP * 2.5),
            run_time=0.8
        )
        
        self.wait(3)