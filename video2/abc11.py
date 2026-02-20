from manim import *
import numpy as np

class SummaryScene(Scene):
    def construct(self):
        # === TITLE ===
        title = Text("Summary", font_size=48, weight=BOLD, color=BLUE)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=0.8)
        self.wait(0.5)
        
        # ============================================
        # PART 1: THREE MECHANISMS
        # ============================================
        
        mechanisms_title = Text("Three Multipath Mechanisms:", font_size=32, color=YELLOW)
        mechanisms_title.next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(mechanisms_title, shift=DOWN*0.2), run_time=0.6)
        self.wait(0.4)
        
        # Create three icons with labels
        # Reflection
        reflection_group = VGroup()
        building = SVGMobject("building.svg").scale(0.5)
        car = SVGMobject("car2.svg").scale(0.4)
        car.next_to(building.get_top(), UP, buff=0.3)
        
        # Simple reflection arrow
        ref_arrow_in = Arrow(ORIGIN + LEFT*0.6 + DOWN*0.2, car.get_left(), 
                            color=YELLOW, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        ref_arrow_out = Arrow(car.get_right(), ORIGIN + RIGHT*0.6 + DOWN*0.2, 
                             color=BLUE, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        
        reflection_group.add(building, car, ref_arrow_in, ref_arrow_out)
        reflection_label = Text("Reflection", font_size=24, color=GREEN, weight=BOLD)
        reflection_label.next_to(reflection_group, DOWN, buff=0.3)
        reflection_group.add(reflection_label)
        
        reflection_group.move_to(LEFT * 4 + DOWN * 0.5)
        
        # Diffraction
        diffraction_group = VGroup()
        building2 = SVGMobject("building.svg").scale(0.5)
        building_edge = building2.get_top()
        
        # Waves bending around edge
        diff_arc1 = Arc(radius=0.5, start_angle=PI, angle=-PI/2, 
                       color=YELLOW, stroke_width=3).move_arc_center_to(building_edge)
        diff_arc2 = Arc(radius=0.7, start_angle=PI, angle=-PI/2, 
                       color=BLUE, stroke_width=3).move_arc_center_to(building_edge)
        
        diffraction_group.add(building2, diff_arc1, diff_arc2)
        diffraction_label = Text("Diffraction", font_size=24, color=GREEN, weight=BOLD)
        diffraction_label.next_to(diffraction_group, DOWN, buff=0.3)
        diffraction_group.add(diffraction_label)
        
        diffraction_group.move_to(ORIGIN + DOWN * 0.5)
        
        # Scattering
        scattering_group = VGroup()
        tree = SVGMobject("tree.svg").scale(0.6)
        
        # Multiple scattered arrows
        scatter_arrows = VGroup()
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            arrow = Arrow(ORIGIN, ORIGIN + 0.4*np.array([np.cos(angle*DEGREES), 
                         np.sin(angle*DEGREES), 0]),
                         color=YELLOW, stroke_width=2, max_tip_length_to_length_ratio=0.2)
            scatter_arrows.add(arrow)
        scatter_arrows.move_to(tree.get_center())
        
        scattering_group.add(tree, scatter_arrows)
        scattering_label = Text("Scattering", font_size=24, color=GREEN, weight=BOLD)
        scattering_label.next_to(scattering_group, DOWN, buff=0.3)
        scattering_group.add(scattering_label)
        
        scattering_group.move_to(RIGHT * 4 + DOWN * 0.5)
        
        # Animate all three
        self.play(
            FadeIn(reflection_group, shift=RIGHT*0.3),
            FadeIn(diffraction_group, scale=0.8),
            FadeIn(scattering_group, shift=LEFT*0.3),
            run_time=1.2
        )
        self.wait(0.8)
        
        # ============================================
        # TRANSITION TO PHASOR SUMMARY
        # ============================================
        
        self.play(
            FadeOut(mechanisms_title),
            FadeOut(reflection_group),
            FadeOut(diffraction_group),
            FadeOut(scattering_group),
            run_time=0.6
        )
        
        # ============================================
        # PART 2: PHASOR CONCEPT
        # ============================================
        
        phasor_title = Text("Phasor Analysis:", font_size=32, color=YELLOW)
        phasor_title.next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(phasor_title, shift=DOWN*0.2), run_time=0.6)
        self.wait(0.3)
        
        # Create phasor diagram on the left
        circle_center = LEFT * 3.5 + DOWN * 0.8
        circle_radius = 1.2
        
        circle = Circle(radius=circle_radius, color=WHITE, stroke_width=3)
        circle.move_to(circle_center)
        
        # Three phasors
        phasor1 = Arrow(circle_center, circle_center + RIGHT * circle_radius,
                       color=GREEN, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.12)
        phasor2 = Arrow(circle_center, circle_center + np.array([0.8*np.cos(60*DEGREES), 
                       0.8*np.sin(60*DEGREES), 0]),
                       color=BLUE, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.12)
        phasor3 = Arrow(circle_center, circle_center + np.array([0.5*np.cos(150*DEGREES), 
                       0.5*np.sin(150*DEGREES), 0]),
                       color=RED, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.12)
        
        # Resultant (tip-to-tail addition visual)
        phasor1_tip = phasor1.get_end()
        vec2 = phasor2.get_end() - circle_center
        phasor2_trans = Arrow(phasor1_tip, phasor1_tip + vec2,
                             color=BLUE, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.12)
        
        vec3 = phasor3.get_end() - circle_center
        phasor3_trans = Arrow(phasor2_trans.get_end(), phasor2_trans.get_end() + vec3,
                             color=RED, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.12)
        
        resultant = Arrow(circle_center, phasor3_trans.get_end(),
                         color=YELLOW, buff=0, stroke_width=7, max_tip_length_to_length_ratio=0.15)
        
        self.play(Create(circle), run_time=0.5)
        self.play(
            LaggedStart(
                GrowArrow(phasor1),
                GrowArrow(phasor2),
                GrowArrow(phasor3),
                lag_ratio=0.2
            ),
            run_time=1.0
        )
        self.wait(0.3)
        
        # Transform to tip-to-tail
        self.play(
            Transform(phasor2, phasor2_trans),
            Transform(phasor3, phasor3_trans),
            run_time=0.8
        )
        self.play(GrowArrow(resultant), run_time=0.6)
        self.wait(0.4)
        
        # Key points on the right
        key_points = VGroup(
            Text("• Phasor = Amplitude + Phase", font_size=24, color=WHITE),
            Text("• Multiple paths add as vectors", font_size=24, color=WHITE),
            Text("• Phase difference controls result", font_size=24, color=BLUE, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        key_points.move_to(RIGHT * 2.5 + DOWN * 0.5)
        
        for point in key_points:
            self.play(FadeIn(point, shift=RIGHT*0.2), run_time=0.5)
            self.wait(0.2)
        
        self.wait(0.8)
        
        # ============================================
        # PART 3: INTERFERENCE
        # ============================================
        
        self.play(
            FadeOut(phasor_title),
            FadeOut(circle),
            FadeOut(phasor1),
            FadeOut(phasor2),
            FadeOut(phasor3),
            FadeOut(resultant),
            FadeOut(key_points),
            run_time=0.6
        )
        
        interference_title = Text("Interference:", font_size=32, color=YELLOW)
        interference_title.next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(interference_title, shift=DOWN*0.2), run_time=0.6)
        self.wait(0.3)
        
        # Constructive on left
        construct_label = Text("Constructive", font_size=26, color=GREEN, weight=BOLD)
        construct_label.move_to(LEFT * 3 + UP * 0.5)
        
        # Two phasors in same direction
        c_center = LEFT * 3 + DOWN * 0.5
        c_radius = 0.8
        c_circle = Circle(radius=c_radius, color=WHITE, stroke_width=2).move_to(c_center)
        c_phasor1 = Arrow(c_center, c_center + RIGHT * c_radius,
                         color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        c_phasor2 = Arrow(c_center, c_center + RIGHT * c_radius * 0.9,
                         color=RED, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        
        c_text = Text("Same phase\n→ Strong signal", font_size=20, color=GREEN)
        c_text.next_to(c_center, DOWN, buff=1.0)
        
        # Destructive on right
        destruct_label = Text("Destructive", font_size=26, color=RED, weight=BOLD)
        destruct_label.move_to(RIGHT * 3 + UP * 0.5)
        
        # Two phasors opposite direction
        d_center = RIGHT * 3 + DOWN * 0.5
        d_radius = 0.8
        d_circle = Circle(radius=d_radius, color=WHITE, stroke_width=2).move_to(d_center)
        d_phasor1 = Arrow(d_center, d_center + RIGHT * d_radius,
                         color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        d_phasor2 = Arrow(d_center, d_center + LEFT * d_radius,
                         color=RED, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        
        d_text = Text("Opposite phase\n→ Weak/no signal", font_size=20, color=RED)
        d_text.next_to(d_center, DOWN, buff=1.0)
        
        self.play(
            Write(construct_label),
            Create(c_circle),
            GrowArrow(c_phasor1),
            GrowArrow(c_phasor2),
            FadeIn(c_text, shift=UP*0.2),
            run_time=1.0
        )
        self.wait(0.3)
        
        self.play(
            Write(destruct_label),
            Create(d_circle),
            GrowArrow(d_phasor1),
            GrowArrow(d_phasor2),
            FadeIn(d_text, shift=UP*0.2),
            run_time=1.0
        )
        self.wait(0.8)
        
        # ============================================
        # CLEAR FOR FINAL SUMMARY
        # ============================================
        
        self.play(
            *[FadeOut(mob) for mob in [
                interference_title, construct_label, c_circle, c_phasor1, c_phasor2, c_text,
                destruct_label, d_circle, d_phasor1, d_phasor2, d_text
            ]],
            run_time=0.6
        )
        
        # ============================================
        # FINAL KEY TAKEAWAYS
        # ============================================
        
        takeaway_title = Text("Key Takeaways:", font_size=36, color=YELLOW, weight=BOLD)
        takeaway_title.next_to(title, DOWN, buff=0.6)
        
        self.play(Write(takeaway_title), run_time=0.6)
        self.wait(0.3)
        
        takeaways = VGroup(
            Text("✓ 3 mechanisms create multipath", font_size=28, color=GREEN),
            Text("✓ Phasor = amplitude + phase", font_size=28, color=BLUE),
            Text("✓ Phase difference → interference", font_size=28, color=ORANGE),
            Text("✓ Random phases cause fading", font_size=28, color=RED, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        takeaways.move_to(DOWN * 0.5)
        
        for takeaway in takeaways:
            self.play(FadeIn(takeaway, shift=RIGHT*0.3), run_time=0.6)
            self.wait(0.3)
        
        self.wait(1.0)
        
        # ============================================
        # TEASER FOR NEXT VIDEO
        # ============================================
        
        self.play(
            FadeOut(takeaway_title),
            FadeOut(takeaways),
            run_time=0.6
        )
        
        next_title = Text("Coming Up Next:", font_size=38, color=ORANGE, weight=BOLD)
        next_title.next_to(title, DOWN, buff=0.7)
        
        self.play(Write(next_title), run_time=0.7)
        self.wait(0.3)
        
        # Teaser content
        teaser = VGroup(
            Text("Fading Models", font_size=36, color=YELLOW, weight=BOLD),
            Text("Rayleigh & Rician Distributions", font_size=30, color=BLUE),
            Text("When does your signal disappear?", font_size=26, color=WHITE, slant=ITALIC),
        ).arrange(DOWN, buff=0.4)
        teaser.move_to(DOWN * 0.3)
        
        teaser_box = SurroundingRectangle(teaser, color=YELLOW, buff=0.4, corner_radius=0.2, stroke_width=3)
        
        self.play(
            FadeIn(teaser_box),
            Write(teaser[0]),
            run_time=0.8
        )
        self.wait(0.3)
        self.play(Write(teaser[1]), run_time=0.7)
        self.wait(0.3)
        self.play(FadeIn(teaser[2], shift=UP*0.2), run_time=0.6)
        
        # Pulse the teaser
        self.play(
            teaser_box.animate.set_color(ORANGE).set_stroke(width=5),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(1.5)
        
        # ============================================
        # FINAL FADE OUT
        # ============================================
        
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.0
        )
        self.wait(0.5)