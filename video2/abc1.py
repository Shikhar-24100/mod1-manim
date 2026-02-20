from manim import *

class MultipathConcept(Scene):
    def construct(self):
        # ================================================
        # SETUP: Scene with Tx, Rx, and obstacles
        # ================================================
        
        tower = SVGMobject("tower.svg").scale(0.8).to_edge(LEFT, buff=1.5)
        mobile = SVGMobject("mobile.svg").scale(0.5).to_edge(RIGHT, buff=1.5)
        
        # Car for diffraction (center)
        car = SVGMobject("car2.svg").scale(0.6).move_to(ORIGIN + DOWN * 2.1+RIGHT*1.2)
        
        # Wall for scattering (top-right)
        wall = ImageMobject("image.png").scale(0.4).move_to(UP * 1.9+ RIGHT * 0.9)
        building = SVGMobject("building.svg").scale(0.7).move_to(ORIGIN+DOWN*0.1)
        # Labels
        tower_label = Text("Tx", font_size=24).next_to(tower, DOWN)
        mobile_label = Text("Rx", font_size=24).next_to(mobile, DOWN)
        
        # Key positions
        tower_pos = tower.get_right()
        mobile_pos = mobile.get_left()
        car_top = car.get_top()
        car_right = car.get_right() + LEFT * 0.8

        wall_pos = wall.get_center()
        building_pos = building.get_top()
        
        # ================================================
        # SHOW BASE SCENE
        # ================================================
        
        self.play(
            FadeIn(tower), 
            FadeIn(mobile), 
            FadeIn(car), 
            FadeIn(wall),
            Write(tower_label), 
            Write(mobile_label),
            FadeIn(building),
            run_time=2.0
        )
        
        self.wait(0.5)
        
        # Blocked direct path (dashed red with X)
        blocked_path = DashedLine(
            tower_pos, mobile_pos,
            color=RED, 
            stroke_width=3, 
            dash_length=0.15
        )
        x_mark = Cross(scale_factor=0.25, color=RED).move_to(ORIGIN)
        
        self.play(
            Create(blocked_path), 
            FadeIn(x_mark), 
            run_time=0.8
        )
        
        self.wait(0.5)
        
        # ================================================
        # PATH 1: REFLECTION (off car side)
        # ================================================
        
        reflect_point = car_right + UP * 0.6
        
        reflection_path = VGroup(
            Line(tower_pos, reflect_point, color=BLUE, stroke_width=4),
            Line(reflect_point, mobile_pos, color=BLUE, stroke_width=4)
        )
        
        reflect_label = Text("Reflected", font_size=20, color=BLUE)
        reflect_label.next_to(reflect_point, RIGHT, buff=0.3)
        reflect_label.shift(RIGHT*0.5)
        
        # Show reflection path
        self.play(Create(reflection_path[0]), run_time=0.6)
        self.play(Create(reflection_path[1]), run_time=0.6)
        self.play(FadeIn(reflect_label), run_time=0.4)
        
        # Animate signal traveling reflected path
        reflect_dot = Dot(color=BLUE, radius=0.08).move_to(tower_pos)
        self.play(
            MoveAlongPath(reflect_dot, reflection_path[0]),
            run_time=0.4, 
            rate_func=linear
        )
        self.play(
            MoveAlongPath(reflect_dot, reflection_path[1]),
            run_time=0.4, 
            rate_func=linear
        )
        self.remove(reflect_dot)
        
        self.wait(0.3)
        
        # ================================================
        # PATH 2: DIFFRACTION (over BUILDING top)
        # ================================================
        
        diffract_point = building_pos
        
        diffraction_path = VGroup(
            Line(tower_pos, diffract_point, color=ORANGE, stroke_width=4),
            Line(diffract_point, mobile_pos, color=ORANGE, stroke_width=4)
        )
        
        diffract_label = Text("Diffracted", font_size=20, color=ORANGE)
        diffract_label.next_to(diffract_point, UP, buff=0.2)
        
        # Show diffraction path
        self.play(Create(diffraction_path[0]), run_time=0.6)
        self.play(Create(diffraction_path[1]), run_time=0.6)
        self.play(FadeIn(diffract_label), run_time=0.4)
        
        # Animate signal traveling diffracted path
        diffract_dot = Dot(color=ORANGE, radius=0.08).move_to(tower_pos)
        self.play(
            MoveAlongPath(diffract_dot, diffraction_path[0]),
            run_time=0.4, 
            rate_func=linear
        )
        self.play(
            MoveAlongPath(diffract_dot, diffraction_path[1]),
            run_time=0.4, 
            rate_func=linear
        )
        self.remove(diffract_dot)
        
        self.wait(0.3)
        
        # ================================================
        # PATH 3: SCATTERING (off wall)
        # ================================================
        
        scatter_point = wall_pos
        
        scattering_path = VGroup(
            Line(tower_pos, scatter_point, color=GREEN, stroke_width=4),
            Line(scatter_point, mobile_pos, color=GREEN, stroke_width=4)
        )
        
        scatter_label = Text("Scattered", font_size=20, color=GREEN)
        scatter_label.next_to(scatter_point, RIGHT, buff=0.3)
        scatter_label.shift(RIGHT*0.7)
        
        # Show scattering path
        self.play(Create(scattering_path[0]), run_time=0.6)
        self.play(Create(scattering_path[1]), run_time=0.6)
        self.play(FadeIn(scatter_label), run_time=0.4)
        
        # Animate signal traveling scattered path
        scatter_dot = Dot(color=GREEN, radius=0.08).move_to(tower_pos)
        self.play(
            MoveAlongPath(scatter_dot, scattering_path[0]),
            run_time=0.4, 
            rate_func=linear
        )
        self.play(
            MoveAlongPath(scatter_dot, scattering_path[1]),
            run_time=0.4, 
            rate_func=linear
        )
        self.remove(scatter_dot)
        
        self.wait(0.5)
        
        # ================================================
        # HIGHLIGHT: All paths converge at receiver
        # ================================================
        
        receiver_circle = Circle(
            radius=0.4, 
            color=YELLOW, 
            stroke_width=4
        ).move_to(mobile_pos)
        
        self.play(Create(receiver_circle), run_time=0.5)
        self.play(
            receiver_circle.animate.scale(1.3),
            rate_func=there_and_back,
            run_time=0.6
        )
        
        self.wait(0.3)
        
        # ================================================
        # SHOW ALL SIGNALS ARRIVING TOGETHER
        # ================================================
        
        # Three dots traveling simultaneously on different paths
        dot1 = Dot(color=BLUE, radius=0.08).move_to(tower_pos)
        dot2 = Dot(color=ORANGE, radius=0.08).move_to(tower_pos)
        dot3 = Dot(color=GREEN, radius=0.08).move_to(tower_pos)
        
        self.add(dot1, dot2, dot3)
        
        # First leg of each path
        self.play(
            MoveAlongPath(dot1, reflection_path[0]),
            MoveAlongPath(dot2, diffraction_path[0]),
            MoveAlongPath(dot3, scattering_path[0]),
            run_time=0.5, 
            rate_func=linear
        )
        
        # Second leg of each path
        self.play(
            MoveAlongPath(dot1, reflection_path[1]),
            MoveAlongPath(dot2, diffraction_path[1]),
            MoveAlongPath(dot3, scattering_path[1]),
            run_time=0.5, 
            rate_func=linear
        )
        
        self.remove(dot1, dot2, dot3)
        self.wait(0.3)
        
        # ================================================
        # KEY INSIGHT
        # ================================================
        
        # Fade out labels and circle
        self.play(
            FadeOut(reflect_label),
            FadeOut(diffract_label),
            FadeOut(scatter_label),
            FadeOut(receiver_circle),
            run_time=0.5
        )
        
        # Key insight text
        insight_text = VGroup(
            Text("Different paths", font_size=28, color=WHITE),
            Text("→", font_size=28, color=WHITE),
            Text("Different delays", font_size=28, color=WHITE),
            Text("→", font_size=28, color=WHITE),
            Text("Different phases", font_size=28, color=YELLOW, weight=BOLD)
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.6)
        
        self.play(Write(insight_text), run_time=1.5)
        
        self.wait(1.0)
        
        # ================================================
        # EMPHASIZE "MULTIPATH"
        # ================================================
        
        multipath_text = Title(
            "This phenomenon is called MULTIPATH").scale(0.9)
        
        self.play(Write(multipath_text), run_time=1.0)
        
        self.wait(1.5)
        
        # ================================================
        # FADE OUT FOR NEXT SCENE
        # ================================================
        
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8
        )
        
        self.wait(0.5)