from manim import *
import numpy as np

class ReflectionScene(Scene):
    def construct(self):
        # === TITLE ===
        # title = Text("Reflection", font_size=48, weight=BOLD, color=BLUE)
        # title.to_edge(UP, buff=0.5)
        
        # self.play(Write(title), run_time=0.8)
        self.wait(0.3)
        
        # === SETUP: TOWER, MOBILE, BUILDING (OBSTACLE), CAR (REFLECTOR) ===
        tower = SVGMobject("tower.svg").scale(0.7)
        tower.to_edge(LEFT, buff=1.5).shift(DOWN * 1)
        
        mobile = SVGMobject("mobile.svg").scale(0.5)
        mobile.to_edge(RIGHT, buff=1.5).shift(DOWN * 1)
        
        # Building blocks direct path
        building = SVGMobject("building.svg").scale(1.0)
        building.move_to(ORIGIN + DOWN * 0.8)
        
        # Car on top of the building (acts as reflector)
        car = SVGMobject("car2.svg").scale(0.6)
        car.move_to(building.get_top() + UP * 2.4)
        
        # Labels
        tower_label = Text("Tx", font_size=24, weight=BOLD).next_to(tower, DOWN, buff=0.2)
        mobile_label = Text("Rx", font_size=24, weight=BOLD).next_to(mobile, DOWN, buff=0.2)
        car_label = Text("Car (Reflector)", font_size=18, color=YELLOW).next_to(car, UP, buff=0.2)
        
        # Show scene elements
        self.play(
            FadeIn(tower, shift=RIGHT*0.3),
            FadeIn(mobile, shift=LEFT*0.3),
            run_time=0.7
        )
        self.play(
            Write(tower_label),
            Write(mobile_label),
            run_time=0.5
        )
        self.play(
            FadeIn(building, scale=0.9),
            run_time=0.6
        )
        self.wait(0.3)
        
        # === BLOCKED DIRECT PATH ===
        tower_pos = tower.get_right()
        mobile_pos = mobile.get_left()
        
        blocked_path = DashedLine(
            tower_pos, mobile_pos,
            color=RED, stroke_width=4, dash_length=0.2
        )
        
        x_mark = Cross(scale_factor=0.35, color=RED, stroke_width=6)
        x_mark.move_to(building.get_center())
        
        nlos_text = Text("LOS Blocked!", font_size=22, color=RED, weight=BOLD)
        nlos_text.next_to(x_mark, UP, buff=0.3)
        nlos_text.shift(UP*0.5)
        
        self.play(Create(blocked_path), run_time=0.8)
        self.play(
            FadeIn(x_mark, scale=1.5),
            blocked_path.animate.set_opacity(0.4),
            run_time=0.5
        )
        self.play(FadeIn(nlos_text, shift=DOWN*0.2), run_time=0.4)
        self.wait(0.5)
        
        # === INTRODUCE CAR AS REFLECTOR ===
        self.play(
            FadeIn(car, scale=0.8),
            run_time=0.7
        )
        
        # Dotted line across car to show reflecting surface
        car_left = car.get_left()
        car_right = car.get_right()
        reflection_surface = DashedLine(
            car_left,
            car_right,
            color=WHITE,
            stroke_width=4,
            dash_length=0.15
        )
        
        self.play(Create(reflection_surface), run_time=0.5)
        self.play(FadeIn(car_label, shift=DOWN*0.2), run_time=0.4)
        self.wait(0.3)
        
        # === REFLECTION PATH ===
        car_reflection_point = car.get_center()
        
        # Incident path: Tower to Car
        incident_path = Line(
            tower_pos,
            car_reflection_point,
            color=YELLOW,
            stroke_width=5
        )
        
        # Reflected path: Car to Mobile
        reflected_path = Line(
            car_reflection_point,
            mobile_pos,
            color=BLUE,
            stroke_width=5
        )
        
        # === ANIMATE INCIDENT WAVE ===
        self.play(Create(incident_path), run_time=0.8)
        
        # Signal dot traveling to car
        incident_dot = Dot(color=YELLOW, radius=0.12).set_sheen(-0.4, DOWN)
        incident_glow = Circle(radius=0.25, color=YELLOW, fill_opacity=0.3, stroke_width=0)
        incident_glow.move_to(tower_pos)
        
        incident_dot.move_to(tower_pos)
        self.add(incident_glow, incident_dot)
        
        self.play(
            MoveAlongPath(incident_dot, incident_path),
            incident_glow.animate.move_to(car_reflection_point),
            run_time=1.0,
            rate_func=smooth
        )
        
        # Flash at reflection point
        self.play(
            Flash(car_reflection_point, color=YELLOW, line_length=0.3, num_lines=12),
            car.animate.scale(1.1),
            run_time=0.4
        )
        self.play(car.animate.scale(1/1.1), run_time=0.2)
        self.remove(incident_dot)
        
        self.wait(0.2)
        
        # === ANIMATE REFLECTED WAVE ===
        self.play(Create(reflected_path), run_time=0.8)
        
        # Signal dot traveling to mobile
        reflected_dot = Dot(color=BLUE, radius=0.12).set_sheen(-0.4, DOWN)
        reflected_glow = Circle(radius=0.25, color=BLUE, fill_opacity=0.3, stroke_width=0)
        reflected_glow.move_to(car_reflection_point)
        
        reflected_dot.move_to(car_reflection_point)
        self.add(reflected_glow, reflected_dot)
        
        self.play(
            MoveAlongPath(reflected_dot, reflected_path),
            incident_glow.animate.move_to(mobile_pos).set_color(BLUE),
            run_time=1.0,
            rate_func=smooth
        )
        
        # Success flash at mobile
        self.play(
            Flash(mobile_pos, color=GREEN, line_length=0.3, num_lines=12),
            mobile.animate.scale(1.15),
            run_time=0.5
        )
        self.play(mobile.animate.scale(1/1.15), run_time=0.2)
        self.remove(reflected_dot, incident_glow)
        
        self.wait(0.4)
        
        # === ANGLE LABELS ===
        # Normal line at car (perpendicular to reflecting surface - pointing UP)
        normal = DashedLine(
            car_reflection_point + DOWN * 1.0,
            car_reflection_point + UP * 1.0,
            color=GRAY,
            stroke_width=2,
            dash_length=0.08
        )
        
        self.play(Create(normal), run_time=0.4)
        
        # Calculate proper angles from the normal (vertical line)
        # Incident ray comes from bottom-left, reflected goes to bottom-right
        
        # Incident angle (measured from normal)
        incident_vec = car_reflection_point - tower_pos  # Direction TO the surface
        incident_angle_from_vertical = np.arctan2(incident_vec[0], incident_vec[1])
        
        incident_arc = Arc(
            radius=0.6,
            start_angle=incident_angle_from_vertical-1.1*PI,
            angle=incident_angle_from_vertical,
            color=YELLOW,
            stroke_width=3
        ).move_arc_center_to(car_reflection_point)
        
        theta_i = MathTex(r"\theta_i", color=YELLOW, font_size=26)
        theta_i.next_to(car_reflection_point + LEFT*0.4 + DOWN*0.5, buff=0.1)
        
        # Reflected angle (measured from normal - should be equal to incident)
        reflected_vec = mobile_pos - car_reflection_point  # Direction AWAY from surface
        reflected_angle_from_vertical = np.arctan2(reflected_vec[0], reflected_vec[1])
        
        reflected_arc = Arc(
            radius=0.6,
            start_angle=-PI/2,
            angle=reflected_angle_from_vertical - PI/2,
            color=BLUE,
            stroke_width=3
        ).move_arc_center_to(car_reflection_point)
        
        theta_r = MathTex(r"\theta_r", color=BLUE, font_size=26)
        theta_r.next_to(car_reflection_point + RIGHT*0.4 + DOWN*0.5, buff=0.1)
        
        self.play(
            Create(incident_arc),
            FadeIn(theta_i, scale=0.8),
            run_time=0.5
        )
        self.play(
            Create(reflected_arc),
            FadeIn(theta_r, scale=0.8),
            run_time=0.5
        )
        
        self.wait(0.4)
        
        # === EQUATION ===
        equation = MathTex(
            r"\theta_i", r"=", r"\theta_r",
            font_size=36
        )
        equation.set_color_by_tex(r"\theta_i", YELLOW)
        equation.set_color_by_tex(r"\theta_r", BLUE)
        equation.next_to(car_reflection_point, RIGHT, buff=1.5)
        
        eq_box = SurroundingRectangle(
            equation,
            color=GREEN,
            buff=0.2,
            stroke_width=2
        )
        
        self.play(
            Write(equation),
            Create(eq_box),
            run_time=0.7
        )
        
        # Emphasize equation
        self.play(
            VGroup(equation, eq_box).animate.scale(1.15),
            rate_func=there_and_back,
            run_time=0.7
        )
        
        self.wait(0.5)
        
        # === KEY INSIGHT TEXT ===
        # Fade out some elements
        self.play(
            FadeOut(nlos_text),
            FadeOut(equation),
            FadeOut(eq_box),
            FadeOut(normal),
            FadeOut(incident_arc),
            FadeOut(reflected_arc),
            FadeOut(theta_i),
            FadeOut(theta_r),
            run_time=0.5
        )
        
        key_text = VGroup(
            Text("Source: Smooth large surfaces", font_size=28),
            Text("Strongest multipath component", font_size=28, color=BLUE)
        ).arrange(DOWN, buff=0.2)
        key_text.to_edge(DOWN, buff=0.4)
        
        self.play(
            FadeIn(key_text[0], shift=UP*0.2),
            run_time=0.6
        )
        self.wait(0.2)
        self.play(
            FadeIn(key_text[1], shift=UP*0.2),
            run_time=0.6
        )
        
        # Highlight the reflection path
        self.play(
            incident_path.animate.set_stroke(width=7, color=YELLOW),
            reflected_path.animate.set_stroke(width=7, color=BLUE),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(1.2)
        
        # === FADE OUT ===
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8
        )