from manim import *
import numpy as np

class AddingSignalsScene(Scene):
    def construct(self):
        # ============================================
        # SCENE 0: TX, RX, JET, and PATHS (LHS)
        # ============================================
        
        # Load SVGs (make sure files are in the same directory)
        tx_tower = SVGMobject("tower.svg").scale(0.6)
        rx_mobile = SVGMobject("mobile.svg").scale(0.4)
        jet = SVGMobject("jet.svg").scale(0.27)
        
        # Position on left side
        tx_tower.move_to(LEFT * 5+DOWN*1.1 )
        rx_mobile.move_to(LEFT * 1+DOWN*1.1 )
        jet.move_to(LEFT * 3.5 + UP * 1.5)
        
        # Appear TX, RX, and Jet
        self.play(
            FadeIn(tx_tower, shift=UP*0.3),
            FadeIn(rx_mobile, shift=DOWN*0.3),
            run_time=0.8
        )
        self.wait(0.3)
        self.play(FadeIn(jet, shift=RIGHT*0.3), run_time=0.6)
        self.wait(0.4)
        
        # Create paths
        # LOS path (green, direct)
        los_path = Line(
            tx_tower.get_top()+DOWN*0.3,
            rx_mobile.get_center(),
            color=GREEN,
            stroke_width=4
        )
        
        # Reflected path (blue, via jet)
        reflection_path1 = Line(
            tx_tower.get_top(),
            jet.get_center(),
            color=BLUE,
            stroke_width=4
        )
        reflection_path2 = Line(
            jet.get_center(),
            rx_mobile.get_center(),
            color=BLUE,
            stroke_width=4
        )
        
        # Animate paths appearing
        self.play(Create(los_path), run_time=0.8)
        self.wait(0.3)
        self.play(
            Create(reflection_path1),
            Create(reflection_path2),
            run_time=1.0
        )
        self.wait(0.6)
        
        # Group LHS elements
        lhs_group = VGroup(tx_tower, rx_mobile, jet, los_path, reflection_path1, reflection_path2)
        
        # ============================================
        # NOW TITLE APPEARS
        # ============================================
        
        title = Text("Adding Signals", font_size=38)
        title.to_edge(UP, buff=0.4)
        
        self.play(Write(title), run_time=0.8)
        self.wait(0.4)
        
        # ============================================
        # MOVE LHS TO LEFT, RHS CONTENT ON RIGHT
        # ============================================
        
        # Scale down and reposition LHS
        # self.play(
        #     lhs_group.animate.scale(0.7).shift(LEFT * 0.5),
        #     run_time=0.8
        # )
        
        intro_text = Text("Multiple paths arrive at receiver", font_size=24, color=YELLOW)
        intro_text.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(intro_text, shift=DOWN*0.2), run_time=0.6)
        self.wait(0.5)
        
        # ============================================
        # RHS: PHASOR DIAGRAM (shifted right)
        # ============================================
        
        circle_center = RIGHT * 2.5 + DOWN * 0.5
        circle_radius = 1.0
        
        circle = Circle(radius=circle_radius, color=WHITE, stroke_width=3)
        circle.move_to(circle_center)
        
        # Phasor 1 - horizontal (0 degrees) - GREEN (LOS)
        phasor1 = Arrow(
            circle_center,
            circle_center + RIGHT * circle_radius,
            color=GREEN,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        label1 = Text("LOS", font_size=20, color=GREEN, weight=BOLD)
        label1.next_to(phasor1, DOWN, buff=0.2)
        
        # Phasor 2 - at 60 degrees - BLUE (Reflected)
        angle2 = 60 * DEGREES
        phasor2_end = circle_center + np.array([
            circle_radius * np.cos(angle2),
            circle_radius * np.sin(angle2),
            0
        ])
        phasor2 = Arrow(
            circle_center,
            phasor2_end,
            color=BLUE,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        label2 = Text("Reflected", font_size=20, color=BLUE, weight=BOLD)
        label2.next_to(phasor2, UP, buff=0.2).shift(RIGHT * 0.3)
        
        self.play(Create(circle), run_time=0.6)
        self.play(
            GrowArrow(phasor1),
            Write(label1),
            run_time=0.7
        )
        self.play(
            GrowArrow(phasor2),
            Write(label2),
            run_time=0.7
        )
        self.wait(0.6)
        
        # ============================================
        # SCENE 2: TIP-TO-TAIL VECTOR ADDITION
        # ============================================
        
        self.play(FadeOut(intro_text), run_time=0.4)
        
        addition_text = Text("Add tip-to-tail:", font_size=24, color=YELLOW)
        addition_text.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(addition_text, shift=DOWN*0.2), run_time=0.6)
        self.wait(0.4)
        
        phasor1_tip = phasor1.get_end()
        phasor2_vector = phasor2.get_end() - phasor2.get_start()
        phasor2_translated = Arrow(
            phasor1_tip,
            phasor1_tip + phasor2_vector,
            color=BLUE,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        
        self.play(
            FadeOut(label1),
            FadeOut(label2),
            Transform(phasor2, phasor2_translated),
            run_time=1.2
        )
        self.wait(0.5)
        
        # ============================================
        # SCENE 3: SHOW RESULTANT
        # ============================================
        
        result_text = Text("Resultant:", font_size=24, color=YELLOW)
        result_text.next_to(title, DOWN, buff=0.4)
        self.play(
            FadeOut(addition_text),
            FadeIn(result_text, shift=DOWN*0.2),
            run_time=0.5
        )
        
        resultant_end = phasor2_translated.get_end()
        resultant = Arrow(
            circle_center,
            resultant_end,
            color=RED,
            buff=0,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15
        )
        
        resultant_label = Text("Result", font_size=22, color=RED, weight=BOLD)
        resultant_label.next_to(resultant, RIGHT, buff=0.3)
        
        self.play(
            GrowArrow(resultant),
            Write(resultant_label),
            run_time=1.0
        )
        
        self.play(
            resultant.animate.set_stroke(width=10),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(0.8)
        
        # ============================================
        # SCENE 4: VARYING PHASE DIFFERENCES
        # ============================================
        
        self.play(FadeOut(result_text), run_time=0.4)
        
        vary_text = Text("Different phases → Different results", font_size=24, color=BLUE, weight=BOLD)
        vary_text.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(vary_text, shift=DOWN*0.2), run_time=0.6)
        self.wait(0.5)
        
        self.play(
            FadeOut(phasor2),
            FadeOut(resultant),
            FadeOut(resultant_label),
            run_time=0.5
        )
        
        phasor2 = Arrow(
            circle_center,
            phasor2_end,
            color=BLUE,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        
        self.play(GrowArrow(phasor2), run_time=0.5)
        
        angle_tracker = ValueTracker(angle2)
        
        def update_phasor2_translated(mob):
            angle = angle_tracker.get_value()
            phasor2_vec = np.array([
                circle_radius * np.cos(angle),
                circle_radius * np.sin(angle),
                0
            ])
            new_end = phasor1_tip + phasor2_vec
            mob.put_start_and_end_on(phasor1_tip, new_end)
        
        def update_resultant(mob):
            angle = angle_tracker.get_value()
            phasor2_vec = np.array([
                circle_radius * np.cos(angle),
                circle_radius * np.sin(angle),
                0
            ])
            final_end = phasor1_tip + phasor2_vec
            mob.put_start_and_end_on(circle_center, final_end)
        
        phasor2_trans = Arrow(
            phasor1_tip,
            phasor1_tip + phasor2_vector,
            color=BLUE,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        
        resultant_dynamic = Arrow(
            circle_center,
            phasor1_tip + phasor2_vector,
            color=RED,
            buff=0,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15
        )
        
        self.play(
            Transform(phasor2, phasor2_trans),
            run_time=0.8
        )
        
        self.play(GrowArrow(resultant_dynamic), run_time=0.6)
        
        phasor2.add_updater(update_phasor2_translated)
        resultant_dynamic.add_updater(update_resultant)
        
        self.play(
            angle_tracker.animate.set_value(120 * DEGREES),
            run_time=1.5,
            rate_func=smooth
        )
        self.play(
            angle_tracker.animate.set_value(180 * DEGREES),
            run_time=1.5,
            rate_func=smooth
        )
        self.play(
            angle_tracker.animate.set_value(270 * DEGREES),
            run_time=1.5,
            rate_func=smooth
        )
        
        phasor2.clear_updaters()
        resultant_dynamic.clear_updaters()
        
        self.wait(0.8)
        
        # ============================================
        # FINAL MESSAGE
        # ============================================
        
        self.play(FadeOut(vary_text), run_time=0.4)
        
        final_message = VGroup(
            Text("Phase difference controls", font_size=26, color=WHITE),
            Text("signal strength!", font_size=28, color=YELLOW, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        final_message.to_edge(DOWN, buff=0.7)
        
        self.play(
            FadeIn(final_message, shift=UP*0.2),
            run_time=0.8
        )
        
        self.play(
            resultant_dynamic.animate.set_stroke(width=12, color=YELLOW),
            rate_func=there_and_back,
            run_time=1.0
        )
        
        self.wait(1.5)
        
        # === FADE OUT ===
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8
        )