from manim import *

class CoherenceWindow(Scene):
    def construct(self):
        # --- TITLE ---
        title = Text("The Implication: The Coherence Window", font_size=32, color=BLUE_A).to_edge(UP)
        self.play(Write(title))

        # --- SCENARIO 1: LOW SPEED (PEDESTRIAN) ---
        scene1_text = Text("Low Speed = Large Coherence Window", font_size=24).shift(UP * 2 + LEFT * 2)
        self.play(Write(scene1_text))

        # Timeline axis
        axis1 = Line(LEFT * 5, RIGHT * 5, color=GRAY).shift(UP * 0.5)
        self.play(Create(axis1))

        # Large Coherence Time Box (The Window)
        tc_large = Rectangle(width=6, height=1, color=GREEN, fill_opacity=0.3).next_to(axis1, DOWN, buff=0)
        tc_large.align_to(axis1, LEFT)
        tc_label_1 = MathTex(r"T_c \text{ (Channel is constant)}", font_size=20).move_to(tc_large)
        
        self.play(DrawBorderThenFill(tc_large), Write(tc_label_1))

        # Computation Blocks (Channel Est, Precoding, Beamforming)
        comp_time = Rectangle(width=4, height=0.6, color=YELLOW, fill_opacity=0.8)
        comp_time.align_to(tc_large, LEFT).shift(RIGHT * 0.2 + DOWN * 0.5)
        comp_label = Text("Channel Est. + Precoding + Beamforming", font_size=14, color=BLACK).move_to(comp_time)
        
        self.play(FadeIn(comp_time), Write(comp_label))
        
        # Success indicator
        success = Text("✔ Computations finish in time!", color=GREEN, font_size=18).next_to(comp_time, RIGHT, buff=0.2)
        success.shift(DOWN*0.4)
        self.play(Write(success))
        self.wait(2)

        # --- SCENARIO 2: HIGH SPEED (TRAIN/CAR) ---
        # Fade out Scenario 1 text and success indicator
        self.play(FadeOut(scene1_text), FadeOut(success))
        
        scene2_text = Text("High Speed = Small Coherence Window", font_size=24, color=RED).shift(UP * 2 + LEFT * 2)
        self.play(Write(scene2_text))

        # Shrink the Coherence Time due to Doppler!
        tc_small = Rectangle(width=1.5, height=1, color=RED, fill_opacity=0.3).next_to(axis1, DOWN, buff=0)
        tc_small.align_to(axis1, LEFT)
        tc_label_2 = MathTex(r"T_c \text{ (Shrinks!)}", font_size=18).move_to(tc_small).shift(UP * 0.2)

        # Animate the shrinking window (Doppler effect in action)
        self.play(
            Transform(tc_large, tc_small),
            Transform(tc_label_1, tc_label_2),
            run_time=1.5
        )

        # The computation block now overflows the coherence window
        fail_arrow = Arrow(start=tc_small.get_right() + UP*0.5, end=tc_small.get_right() + DOWN*1.5, color=RED)
        fail_text = VGroup(
            Text("Channel Changes Here!", font_size=16, color=RED, weight=BOLD),
            Text("Computations are now useless.", font_size=14, color=GRAY)
        ).arrange(DOWN).next_to(fail_arrow, DOWN, buff=0.2)

        self.play(GrowArrow(fail_arrow), Write(fail_text))
        
        # Highlight that the computation block is stuck outside the safe window
        self.play(Wiggle(comp_time))
        self.wait(3)