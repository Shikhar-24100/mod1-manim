from manim import *
import random
import numpy as np

class ResourceAllocationFixed(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # ASSETS & SETUP
        # ---------------------------------------------------------
        try:
            tower = SVGMobject("assets/tower.svg").scale(1.5).to_edge(LEFT, buff=1)
        except:
            tower = VGroup(Line(DOWN, UP), Triangle()).arrange(UP, buff=0).scale(1.5).set_color(GRAY).to_edge(LEFT, buff=1)
        
        tower_label = Text("Base Station", font_size=18).next_to(tower, DOWN)
        title = Text("The Resource Allocation Problem", font_size=32).to_edge(UP)
        
        self.add(title, tower, tower_label)

        # ---------------------------------------------------------
        # PART 1: SINGLE USER (IDEAL)
        # ---------------------------------------------------------
        user1 = Dot(color=BLUE).move_to(RIGHT * 4)
        u1_label = Text("User 1", font_size=20).next_to(user1, DOWN)
        
        spectrum_bar = Rectangle(width=6, height=0.5, color=GREEN, fill_opacity=0.3).shift(UP * 1.5)
        spec_label = Text("Full Bandwidth (B)", font_size=20).next_to(spectrum_bar, UP)
        
        shannon = MathTex(r"C = B \log_2(1 + \text{SNR})", font_size=34, color=YELLOW).to_edge(DOWN, buff=1.2)
        shannon.shift(UP*1.2)

        self.play(FadeIn(user1, u1_label, spectrum_bar, spec_label))
        self.play(Write(shannon))
        self.wait(5)

        # ---------------------------------------------------------
        # PART 2: THE MULTI-USER DILEMMA (100 Users)
        # ---------------------------------------------------------
        self.play(FadeOut(u1_label))
        
        crowd = VGroup(user1)
        for _ in range(49):
            d = Dot(color=BLUE, radius=0.08)
            d.move_to([random.uniform(2, 6), random.uniform(-2, 1), 0])
            crowd.add(d)

        self.play(LaggedStart(*[FadeIn(d) for d in crowd if d != user1], lag_ratio=0.01))
        self.wait(2)
        # --- PATH A: DIVIDING FREQUENCY ---
        path_a_text = Text("Option 1: Divide Frequency (Orthogonal)", font_size=24, color=BLUE).move_to(UP*2.5)
        self.play(Write(path_a_text))

        # Show spectrum being sliced
        N = 9
        slice_w = 6 / N
        slices = VGroup(*[
            Rectangle(
                width=slice_w - 0.04, height=0.55,
                fill_color=BLUE_E, fill_opacity=0.75,
                stroke_color=WHITE, stroke_width=0.8,
            ).move_to(spectrum_bar.get_left() + RIGHT * (slice_w * i + slice_w / 2))
            for i in range(N)
        ])

        self.play(
            spectrum_bar.animate.set_opacity(0.1),
            FadeOut(spec_label),
            LaggedStart(*[GrowFromCenter(s) for s in slices], lag_ratio=0.06),
            run_time=1.2,
        )
        self.play(Transform(shannon, MathTex(r"C = \frac{B}{N} \log_2(1 + \text{SNR})", font_size=34, color=BLUE_B).move_to(shannon.get_center())))
        self.wait(6)
        
        # --- PATH B: FULL REUSE (INTERFERENCE) ---
        self.play(FadeOut(path_a_text), FadeOut(slices))
        path_b_text = Text("Option 2: Full Bandwidth Reuse (Non-Orthogonal)", font_size=24, color=RED).move_to(UP*2.5)
        
        # Re-highlight full spectrum
        self.play(Write(path_b_text), spectrum_bar.animate.set_opacity(0.5).set_color(RED))
        
        # Update Shannon to SINR
        shannon_sinr = MathTex(r"C = B \log_2(1 + \frac{S}{I + N})", font_size=34, color=RED).move_to(shannon.get_center())
        
        # ACTION: Dots turn RED to show interference
        self.play(
            Transform(shannon, shannon_sinr),
            crowd.animate.set_color(RED)
        )
        self.wait(1.2)
        calc_interf = MathTex(r"I \uparrow \uparrow \implies \text{SINR} \downarrow \downarrow \implies C \text{ crashes!}", font_size=28, color=RED).next_to(shannon, DOWN)
        self.play(Write(calc_interf))
        
        # Jitter effect to visualize "noise/clash"
        for _ in range(5):
            self.play(crowd.animate.shift(np.array([random.uniform(-0.05, 0.05), random.uniform(-0.05, 0.05), 0])), run_time=0.1)

        self.wait(6)