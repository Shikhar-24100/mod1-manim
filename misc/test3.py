from manim import *
import numpy as np

class DopplerAngle(Scene):
    def construct(self):
        # Create tower from SVG on the left
        tower = SVGMobject("tower.svg").scale(1.2)
        tower.to_edge(LEFT, buff=1).shift(UP * 0.5)
        
        # Create mobile phone from SVG on the right lower position
        phone = SVGMobject("mobile.svg").scale(0.8)
        phone.shift(RIGHT * 5 + DOWN * 2.5)
        
        self.add(tower, phone)
        
        # Create horizontal dashed line showing the path
        path_start = phone.get_center()
        path_end = path_start + LEFT * 8
        dashed_path = DashedLine(path_start, path_end, color=WHITE, dash_length=0.2)
        self.play(Create(dashed_path), run_time=1.5)
        self.wait(0.3)
        
        # Create ray from tower to mobile (yellow line)
        ray = Line(tower.get_center(), phone.get_center(), color=YELLOW, stroke_width=4)
        self.play(Create(ray), run_time=1)
        self.wait(0.3)
        
        # Velocity vector (arrow pointing left from mobile)
        v_arrow = Arrow(phone.get_center(), phone.get_center() + LEFT * 1.5, 
                       color=YELLOW, buff=0, stroke_width=6)
        v_label = MathTex("v = 5", r"\text{ m/s}", font_size=36, color=YELLOW)
        v_label.next_to(phone, UP, buff=0.2)
        
        self.play(GrowArrow(v_arrow), Write(v_label), run_time=1)
        self.wait(0.5)
        
        # Mobile moves a bit to the left - ray follows together
        move_distance = LEFT * 1.2
        
        def update_ray(mob):
            new_line = Line(tower.get_center(), phone.get_center(), 
                          color=YELLOW, stroke_width=4)
            mob.become(new_line)
        
        ray.add_updater(update_ray)
        
        self.play(
            phone.animate.shift(move_distance),
            v_arrow.animate.shift(move_distance),
            v_label.animate.shift(move_distance),
            run_time=2,
            rate_func=smooth
        )
        
        ray.clear_updaters()
        self.wait(0.5)
        
        # Everything stops - fade out velocity
        self.play(FadeOut(v_arrow), FadeOut(v_label), run_time=0.5)
        self.wait(0.3)
        
        # Show angle theta at the mobile (between ray and velocity direction)
        # Velocity direction (horizontal left from mobile)
        vel_direction_line = DashedLine(phone.get_center(), 
                                       phone.get_center() + LEFT * 1.5, 
                                       color=GRAY, dash_length=0.15)
        self.play(Create(vel_direction_line), run_time=0.8)
        
        # Calculate angle at mobile between ray and velocity
        phone_pos = phone.get_center()
        tower_pos = tower.get_center()
        
        # Ray direction (from phone to tower)
        ray_direction = tower_pos - phone_pos
        ray_angle = np.arctan2(ray_direction[1], ray_direction[0])
        
        # Velocity direction (horizontal left = 180 degrees = PI)
        velocity_angle = PI
        
        # Angle between them
        angle_diff = ray_angle - velocity_angle
        
        # Create angle arc at phone position
        angle_arc = Arc(
            radius=0.6,
            start_angle=velocity_angle,
            angle=angle_diff,
            arc_center=phone_pos,
            color=GREEN,
            stroke_width=3
        )
        
        # Theta label
        theta_label = MathTex(r"\theta", font_size=40, color=GREEN)
        # Position theta at the arc
        theta_label.next_to(angle_arc, LEFT + UP, buff=0.1)
        
        self.play(Create(angle_arc), Write(theta_label), run_time=1.5)
        self.wait(1)
        
        # Show Doppler formula
        formula = MathTex(
            r"f_r = f_c \left(1 + \frac{v}{c} \cos\theta\right)",
            font_size=44
        )
        formula.to_edge(RIGHT, buff=1)
        
        # Box around formula
        formula_box = SurroundingRectangle(formula, color=BLUE, buff=0.2, corner_radius=0.1)
        
        self.play(Write(formula), Create(formula_box), run_time=2)
        self.wait(0.5)
        
        # Add labels for variables
        var_labels = VGroup(
            MathTex(r"f_r : \text{Received frequency}", font_size=28),
            MathTex(r"f_c : \text{Carrier frequency}", font_size=28),
            MathTex(r"v : \text{Velocity of mobile}", font_size=28),
            MathTex(r"c : \text{Speed of light}", font_size=28),
            MathTex(r"\theta : \text{Angle of arrival}", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        var_labels.to_corner(UR, buff=0.5)
        
        self.play(FadeIn(var_labels, shift=DOWN), run_time=2)
        self.wait(3)