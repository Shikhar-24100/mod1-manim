from manim import *
import numpy as np

class MultipathPhasorsScene(Scene):
    def construct(self):
        # === TITLE ===
        title = Text("Multipath Through Phasor Lens", font_size=40, weight=BOLD, color=BLUE)
        title.to_edge(UP, buff=0.4)
        
        self.play(Write(title), run_time=0.8)
        self.wait(0.4)
        
        # ============================================
        # SCENE 1: SHOW PHYSICAL SETUP WITH 3 PATHS
        # ============================================
        
        # # Transmitter
        # tower = SVGMobject("tower.svg").scale(0.6)
        # tower.to_edge(LEFT, buff=1.0).shift(DOWN * 1.0)
        # tower_label = Text("Tx", font_size=22, weight=BOLD).next_to(tower, DOWN, buff=0.2)
        # tower_pos = tower.get_right()
        
        # # Receiver
        # mobile = SVGMobject("mobile.svg").scale(0.5)
        # mobile.to_edge(RIGHT, buff=1.0).shift(DOWN * 1.0)
        # mobile_label = Text("Rx", font_size=22, weight=BOLD).next_to(mobile, DOWN, buff=0.2)
        # mobile_pos = mobile.get_left()
        
        # # Obstacles for reflection/diffraction
        # building = SVGMobject("building.svg").scale(0.8)
        # building.move_to(ORIGIN + DOWN * 0.3 + LEFT * 1.0)
        
        # car = SVGMobject("car2.svg").scale(0.5)
        # car.move_to(ORIGIN + UP * 1.5 + RIGHT * 0.5)
        
        # self.play(
        #     FadeIn(tower, shift=RIGHT*0.3),
        #     Write(tower_label),
        #     FadeIn(mobile, shift=LEFT*0.3),
        #     Write(mobile_label),
        #     run_time=0.7
        # )
        # self.play(
        #     FadeIn(building, scale=0.9),
        #     FadeIn(car, scale=0.9),
        #     run_time=0.6
        # )
        # self.wait(0.4)
        
        # === SHOW 3 PATHS ===
        # path_text = Text("Three different paths:", font_size=26, color=YELLOW)
        # path_text.next_to(title, DOWN, buff=0.3)
        # self.play(FadeIn(path_text, shift=DOWN*0.2), run_time=0.5)
        # self.wait(0.3)
        
        # # Path 1: Direct (LOS)
        # path1 = Line(tower_pos, mobile_pos, color=GREEN, stroke_width=3)
        # path1_label = Text("Path 1: Direct", font_size=18, color=GREEN)
        # path1_label.next_to(path1, DOWN, buff=0.1)
        
        # self.play(
        #     Create(path1),
        #     FadeIn(path1_label, shift=UP*0.2),
        #     run_time=0.7
        # )
        # self.wait(0.3)
        
        # # Path 2: Reflected from building
        # building_reflect = building.get_corner(UR)
        # path2_part1 = Line(tower_pos, building_reflect, color=BLUE, stroke_width=3)
        # path2_part2 = Line(building_reflect, mobile_pos, color=BLUE, stroke_width=3)
        # path2_label = Text("Path 2: Reflected", font_size=18, color=BLUE)
        # path2_label.next_to(building, UP, buff=0.2)
        
        # self.play(
        #     Create(path2_part1),
        #     Create(path2_part2),
        #     FadeIn(path2_label, shift=DOWN*0.2),
        #     run_time=0.7
        # )
        # self.wait(0.3)
        
        # # Path 3: Scattered from car
        # car_pos = car.get_center()
        # path3_part1 = Line(tower_pos, car_pos, color=RED, stroke_width=3)
        # path3_part2 = Line(car_pos, mobile_pos, color=RED, stroke_width=3)
        # path3_label = Text("Path 3: Scattered", font_size=18, color=RED)
        # path3_label.next_to(car, UP, buff=0.2)
        
        # self.play(
        #     Create(path3_part1),
        #     Create(path3_part2),
        #     FadeIn(path3_label, shift=DOWN*0.2),
        #     run_time=0.7
        # )
        # self.wait(0.8)
        
        # ============================================
        # SCENE 2: SHOW PHASORS FOR EACH PATH
        # ============================================
        
        # self.play(
        #     FadeOut(path_text),
        #     run_time=0.4
        # )
        
        # phasor_text = Text("Each path → Different phase & amplitude", font_size=26, color=BLUE)
        # phasor_text.next_to(title, DOWN, buff=0.3)
        # self.play(FadeIn(phasor_text, shift=DOWN*0.2), run_time=0.6)
        # self.wait(0.5)
        
        # Fade physical scene slightly
        # self.play(
        #     VGroup(tower, mobile, building, car, tower_label, mobile_label,
        #            path1, path2_part1, path2_part2, path3_part1, path3_part2,
        #            path1_label, path2_label, path3_label).animate.set_opacity(0.15),
        #     run_time=0.5
        # )
        
        # Create phasor diagram
        circle_center = ORIGIN + DOWN * 0.5
        circle_radius = 1.5
        
        circle = Circle(radius=circle_radius, color=WHITE, stroke_width=3)
        circle.move_to(circle_center)
        
        self.play(Create(circle), run_time=0.6)
        
        # Phasor 1: Direct path (strongest, 0°)
        phasor1_length = circle_radius * 0.9
        phasor1_angle = 0 * DEGREES
        phasor1_end = circle_center + np.array([
            phasor1_length * np.cos(phasor1_angle),
            phasor1_length * np.sin(phasor1_angle),
            0
        ])
        phasor1 = Arrow(
            circle_center,
            phasor1_end,
            color=GREEN,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.12
        )
        # dot1 = Dot(phasor1.get_end(), color=GREEN, radius=0.08)
        label1 = Text("Path 1", font_size=20, color=GREEN, weight=BOLD)
        label1.next_to(phasor1, DOWN, buff=0.2).shift(RIGHT * 0.3)
        
        self.play(
            GrowArrow(phasor1),
            # FadeIn(dot1),
            Write(label1),
            run_time=0.7
        )
        self.wait(0.3)
        
        # Phasor 2: Reflected (medium strength, 60°)
        phasor2_length = circle_radius * 0.65
        phasor2_angle = 60 * DEGREES
        phasor2_end = circle_center + np.array([
            phasor2_length * np.cos(phasor2_angle),
            phasor2_length * np.sin(phasor2_angle),
            0
        ])
        phasor2 = Arrow(
            circle_center,
            phasor2_end,
            color=BLUE,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.12
        )
        # dot2 = Dot(phasor2.get_end(), color=BLUE, radius=0.08)
        label2 = Text("Path 2", font_size=20, color=BLUE, weight=BOLD)
        label2.next_to(phasor2, UP, buff=0.2).shift(RIGHT * 0.2)
        
        self.play(
            GrowArrow(phasor2),
            # FadeIn(dot2),
            Write(label2),
            run_time=0.7
        )
        self.wait(0.3)
        
        # Phasor 3: Scattered (weakest, 150°)
        phasor3_length = circle_radius * 0.4
        phasor3_angle = 150 * DEGREES
        phasor3_end = circle_center + np.array([
            phasor3_length * np.cos(phasor3_angle),
            phasor3_length * np.sin(phasor3_angle),
            0
        ])
        phasor3 = Arrow(
            circle_center,
            phasor3_end,
            color=RED,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.12
        )
        # dot3 = Dot(phasor3.get_end(), color=RED, radius=0.08)
        label3 = Text("Path 3", font_size=20, color=RED, weight=BOLD)
        label3.next_to(phasor3, LEFT, buff=0.2)
        
        self.play(
            GrowArrow(phasor3),
            # FadeIn(dot3),
            Write(label3),
            run_time=0.7
        )
        self.wait(0.8)
        
        # ============================================
        # SCENE 3: TIP-TO-TAIL ADDITION
        # ============================================
        
        # self.play(
        #     FadeOut(phasor_text),
        #     run_time=0.4
        # )
        
        add_text = Text("Add tip-to-tail:", font_size=28, color=YELLOW, weight=BOLD)
        add_text.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(add_text, shift=DOWN*0.2), run_time=0.6)
        self.wait(0.4)
        
        # Remove labels to declutter
        self.play(
            FadeOut(label1),
            FadeOut(label2),
            FadeOut(label3),
            run_time=0.3
        )
        
        # Move phasor 2 to tip of phasor 1
        phasor1_tip = phasor1.get_end()
        phasor2_vector = phasor2.get_end() - phasor2.get_start()
        phasor2_translated = Arrow(
            phasor1_tip,
            phasor1_tip + phasor2_vector,
            color=BLUE,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.12
        )
        
        self.play(
            Transform(phasor2, phasor2_translated),
            # dot2.animate.move_to(phasor2_translated.get_end()),
            run_time=1.0
        )
        self.wait(0.4)
        
        # Move phasor 3 to tip of phasor 2
        phasor2_tip = phasor2_translated.get_end()
        phasor3_vector = phasor3.get_end() - phasor3.get_start()
        phasor3_translated = Arrow(
            phasor2_tip,
            phasor2_tip + phasor3_vector,
            color=RED,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.12
        )
        
        self.play(
            Transform(phasor3, phasor3_translated),
            # dot3.animate.move_to(phasor3_translated.get_end()),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Show resultant
        resultant_end = phasor3_translated.get_end()
        resultant = Arrow(
            circle_center,
            resultant_end,
            color=YELLOW,
            buff=0,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15
        )
        # dot_resultant = Dot(resultant.get_end(), color=YELLOW, radius=0.12)
        
        result_label = Text("Total Signal", font_size=24, color=YELLOW, weight=BOLD)
        result_label.next_to(resultant, RIGHT, buff=0.3)
        
        self.play(
            GrowArrow(resultant),
            # FadeIn(dot_resultant),
            Write(result_label),
            run_time=1.0
        )
        
        # Emphasize
        self.play(
            resultant.animate.set_stroke(width=12),
            # dot_resultant.animate.scale(1.4),
            rate_func=there_and_back,
            run_time=0.9
        )
        
        self.wait(0.8)
        
        # ============================================
        # SCENE 4: RECEIVER MOVES - PHASES CHANGE
        # ============================================
        
        self.play(
            FadeOut(add_text),
            run_time=0.4
        )
        
        move_text = Text("Receiver moves slightly...", font_size=28, color=ORANGE)
        move_text.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(move_text, shift=DOWN*0.2), run_time=0.6)
        self.wait(0.4)
        
        # Reset phasors to original positions for animation
        self.play(
            FadeOut(phasor2),
            FadeOut(phasor3),
            # FadeOut(dot2),
            # FadeOut(dot3),
            FadeOut(resultant),
            # FadeOut(dot_resultant),
            FadeOut(result_label),
            run_time=0.5
        )
        
        # Recreate initial phasors
        phasor2 = Arrow(circle_center, phasor2_end, color=BLUE, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.12)
        phasor3 = Arrow(circle_center, phasor3_end, color=RED, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.12)
        # dot2 = Dot(phasor2.get_end(), color=BLUE, radius=0.08)
        # dot3 = Dot(phasor3.get_end(), color=RED, radius=0.08)
        
        self.play(
            GrowArrow(phasor2),
            GrowArrow(phasor3),
            # FadeIn(dot2),
            # FadeIn(dot3),
            run_time=0.5
        )
        
        # Animate phases changing (simulating movement)
        angle2_tracker = ValueTracker(phasor2_angle)
        angle3_tracker = ValueTracker(phasor3_angle)
        
        # Create tip-to-tail versions that update
        def get_phasor2_translated():
            angle = angle2_tracker.get_value()
            vec = np.array([
                phasor2_length * np.cos(angle),
                phasor2_length * np.sin(angle),
                0
            ])
            return Arrow(phasor1_tip, phasor1_tip + vec, color=BLUE, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.12)
        
        def get_phasor3_translated():
            angle2 = angle2_tracker.get_value()
            angle3 = angle3_tracker.get_value()
            
            vec2 = np.array([phasor2_length * np.cos(angle2), phasor2_length * np.sin(angle2), 0])
            tip2 = phasor1_tip + vec2
            
            vec3 = np.array([phasor3_length * np.cos(angle3), phasor3_length * np.sin(angle3), 0])
            return Arrow(tip2, tip2 + vec3, color=RED, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.12)
        
        def get_resultant():
            angle2 = angle2_tracker.get_value()
            angle3 = angle3_tracker.get_value()
            
            vec1 = np.array([phasor1_length, 0, 0])
            vec2 = np.array([phasor2_length * np.cos(angle2), phasor2_length * np.sin(angle2), 0])
            vec3 = np.array([phasor3_length * np.cos(angle3), phasor3_length * np.sin(angle3), 0])
            
            final = circle_center + vec1 + vec2 + vec3
            return Arrow(circle_center, final, color=YELLOW, buff=0, stroke_width=8, max_tip_length_to_length_ratio=0.15)
        
        # Transform to tip-to-tail and create resultant
        phasor2_trans = get_phasor2_translated()
        phasor3_trans = get_phasor3_translated()
        resultant_dynamic = get_resultant()
        
        self.play(
            Transform(phasor2, phasor2_trans),
            # dot2.animate.move_to(phasor2_trans.get_end()),
            run_time=0.6
        )
        self.play(
            Transform(phasor3, phasor3_trans),
            # dot3.animate.move_to(phasor3_trans.get_end()),
            run_time=0.6
        )
        self.play(
            GrowArrow(resultant_dynamic),
            run_time=0.6
        )
        
        # Animate phase changes
        for _ in range(3):
            new_angle2 = angle2_tracker.get_value() + 50 * DEGREES
            new_angle3 = angle3_tracker.get_value() + 70 * DEGREES
            
            new_phasor2 = get_phasor2_translated()
            new_phasor3 = get_phasor3_translated()
            new_resultant = get_resultant()
            
            self.play(
                angle2_tracker.animate.set_value(new_angle2),
                angle3_tracker.animate.set_value(new_angle3),
                Transform(phasor2, Arrow(phasor1_tip, phasor1_tip + np.array([phasor2_length * np.cos(new_angle2), phasor2_length * np.sin(new_angle2), 0]), color=BLUE, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.12)),
                run_time=1.2,
                rate_func=smooth
            )
            
            # Update phasor3 and resultant based on new angle2
            angle2_now = new_angle2
            vec2 = np.array([phasor2_length * np.cos(angle2_now), phasor2_length * np.sin(angle2_now), 0])
            tip2_now = phasor1_tip + vec2
            
            vec3 = np.array([phasor3_length * np.cos(new_angle3), phasor3_length * np.sin(new_angle3), 0])
            
            vec1 = np.array([phasor1_length, 0, 0])
            self.play(
                Transform(
                    phasor3,
                    Arrow(
                        tip2_now,
                        tip2_now + vec3,
                        color=RED,
                        buff=0,
                        stroke_width=6,
                        max_tip_length_to_length_ratio=0.12,
                    ),
                ),
                Transform(
                    resultant_dynamic,
                    Arrow(
                        circle_center,
                        circle_center + vec1 + vec2 + vec3,
                        color=YELLOW,
                        buff=0,
                        stroke_width=8,
                        max_tip_length_to_length_ratio=0.15,
                    ),
                ),
                run_time=0.8,
            )
            
            self.wait(0.3)
        
        self.wait(0.6)
        
        # ============================================
        # FINAL MESSAGE
        # ============================================
        
        self.play(
            FadeOut(move_text),
            run_time=0.4
        )
        
        final_message = VGroup(
            Text("Multipath = Adding phasors", font_size=30, color=WHITE, weight=BOLD),
            Text("with random phases", font_size=28, color=BLUE)
        ).arrange(DOWN, buff=0.2)
        final_message.to_edge(DOWN, buff=0.7)
        
        self.play(
            FadeIn(final_message, shift=UP*0.2),
            run_time=0.8
        )
        
        self.wait(1.5)
        
        # === FADE OUT ===
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8
        )