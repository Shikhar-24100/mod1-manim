from manim import *
from manim.utils.rate_functions import ease_out_expo
import numpy as np

class Phase1_Impulse_Snapshot_Centered(Scene):
    def construct(self):
        # -----------------------------------------
        # 0. LAYOUT & TITLE
        # -----------------------------------------
        title = Title("The Impulse Response Model of A Wireless Channel")
        # self.add(title)

        separator = DashedLine(UP*2.8, DOWN*3.4).shift(RIGHT*0.5)
        self.add(separator)

        # -----------------------------------------
        # 1. LEFT SIDE: PHYSICAL WORLD
        # -----------------------------------------
        # Create a VGroup for easy fading later
        physical_world = VGroup()

        tx = SVGMobject("tower.svg").scale(0.6).move_to(LEFT*5.5)
        rx = SVGMobject("mobile.svg").scale(0.35).move_to(LEFT*1.5 + UP*0)
        bldg = SVGMobject("building.svg").scale(0.6).move_to(LEFT*3.5 + DOWN*2.5)
        car = SVGMobject("jet.svg").scale(0.3).move_to(LEFT*3.0 + UP*1.5)
        
        lbl_tx = Text("Tx", font_size=16).next_to(tx, DOWN)
        lbl_rx = Text("Rx", font_size=16).next_to(rx, DOWN)

        physical_world.add(tx, rx, bldg, car, lbl_tx, lbl_rx, separator)
        self.play(FadeIn(physical_world))
        
        # Define Paths 
        path_direct = Line(tx.get_center(), rx.get_center())
        
        path_car = VMobject()
        path_car.set_points_as_corners([tx.get_center(), car.get_center(), rx.get_center()])
        
        path_bldg = VMobject()
        path_bldg.set_points_as_corners([tx.get_center(), bldg.get_center(), rx.get_center()])

        # -----------------------------------------
        # 2. RIGHT SIDE: MATH WORLD
        # -----------------------------------------
        math_world = VGroup()

        axes = Axes(
            x_range=[0, 7, 1], y_range=[0, 1.2, 0.5],
            x_length=5.5, y_length=3,
            axis_config={"include_tip": False, "font_size": 24}
        ).move_to(RIGHT*4 + DOWN*0.5)
        
        x_lbl = axes.get_x_axis_label(Tex("Delay $(\\tau)$", font_size=24), edge=DOWN, direction=DOWN, buff=0.3)
        y_lbl = axes.get_y_axis_label(Tex("Amplitude $|h(\\tau)|$", font_size=24).rotate(90*DEGREES), edge=LEFT, direction=LEFT, buff=0.3)
        
        math_world.add(axes, x_lbl, y_lbl)

        time_cursor = Triangle(fill_opacity=1, color=YELLOW).scale(0.1).rotate(PI)
        time_cursor.move_to(axes.c2p(0, 0)).shift(UP*0.2)
        
        self.play(Create(axes), Write(x_lbl), Write(y_lbl), FadeIn(time_cursor))
        
        # -----------------------------------------
        # 3. CONTINUOUS WAVE EXPANSION (10-12 seconds)
        # -----------------------------------------
        wave_time = ValueTracker(0)
        
        def get_expanding_waves():
            t = wave_time.get_value()
            waves = VGroup()
            
            # Create multiple wave rings at different phases (slower speed)
            for phase_offset in np.linspace(0, 2*PI, 6):
                for ring_idx in range(8):
                    radius = 0.3 + (t * 1.2 + ring_idx * 0.4 + phase_offset) % 5
                    radius = 0.3 + (t * 0.5 + ring_idx * 0.4 + phase_offset) % 5
                    circle = Circle(
                        radius=radius,
                        color=BLUE,
                        stroke_width=2,
                        fill_opacity=0
                    ).move_to(tx.get_center())
                    
                    # Fade opacity as radius grows
                    opacity = max(0, 1 - (radius / 5))
                    circle.set_stroke(opacity=opacity)
                    waves.add(circle)
            
            return waves
        
        expanding_waves = always_redraw(get_expanding_waves)
        physical_world.add(expanding_waves)
        self.add(expanding_waves)
        
        # Animate the continuous wave expansion for 10 seconds
        self.play(wave_time.animate.set_value(10), run_time=10, rate_func=linear)
        self.wait(2)

        # -----------------------------------------
        # 3.5 SHOW PROPAGATION PATHS (DOTTED LINES)
        # -----------------------------------------
        # Create dotted versions of the three paths
        dotted_direct = DashedLine(
            path_direct.get_start(),
            path_direct.get_end(),
            color=BLUE,
            stroke_width=2,
            dash_length=0.15
        )
        
        def make_dotted_path(path, color, n=32, dot_radius=0.024):
            return VGroup(*[
                Dot(point=path.point_from_proportion(i/(n-1)), radius=dot_radius, color=color)
                for i in range(n)
            ])

        dotted_car = make_dotted_path(path_car, GREEN, n=28, dot_radius=0.024)
        dotted_bldg = make_dotted_path(path_bldg, YELLOW, n=28, dot_radius=0.024)
        
        # Add dotted paths to physical_world so they fade out together
        physical_world.add(dotted_direct, dotted_car, dotted_bldg)
        
        # Fade in the dotted paths
        self.play(
            Create(dotted_direct),
            Create(dotted_car),
            Create(dotted_bldg),
            run_time=1.2
        )
        self.wait(1)
        self.play(FadeIn(title))
        self.wait(2)
        # -----------------------------------------
        # 3. WAVE PACKET LOGIC
        # -----------------------------------------
        def get_wave_packet(path, tracker, color):
            alpha = tracker.get_value()
            if alpha > 1: alpha = 1
            if alpha < 0: alpha = 0
            
            point = path.point_from_proportion(alpha)
            
            delta = 0.01
            p_back = path.point_from_proportion(max(0, alpha - delta))
            p_fwd = path.point_from_proportion(min(1, alpha + delta))
            tangent = p_fwd - p_back
            angle = np.arctan2(tangent[1], tangent[0])
            
            wave = FunctionGraph(
                lambda x: np.exp(-3*x**2) * np.sin(15*x),
                x_range=[-1, 1],
                color=color
            ).scale(0.2)
            
            wave.rotate(angle).move_to(point)
            
            if alpha <= 0.01 or alpha >= 0.99:
                wave.set_opacity(0)
            return wave

        t_d, t_c, t_b = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        
        packet_d = always_redraw(lambda: get_wave_packet(path_direct, t_d, BLUE))
        packet_c = always_redraw(lambda: get_wave_packet(path_car, t_c, GREEN))
        packet_b = always_redraw(lambda: get_wave_packet(path_bldg, t_b, YELLOW))
        
        # Add packets to scene (not group, as they disappear naturally)
        self.add(packet_d, packet_c, packet_b)

        # -----------------------------------------
        # 4. ANIMATION SEQUENCE
        # -----------------------------------------
        T1, T2, T3 = 1.5, 3.0, 5.0
        
        def make_impulse(x_val, height, color):
            base = axes.c2p(x_val, 0)
            top = axes.c2p(x_val, height)
            line = Line(base, top, color=color, stroke_width=6)
            tip = Triangle(fill_color=color, fill_opacity=1, stroke_color=color, stroke_width=1)
            tip.scale(0.15).move_to(top + UP * 0.08) 
            return VGroup(line, tip)

        tap1 = make_impulse(T1, 1.0, BLUE)
        tap2 = make_impulse(T2, 0.6, GREEN)
        tap3 = make_impulse(T3, 0.3, YELLOW)

        timer = ValueTracker(0)
        time_cursor.add_updater(lambda m: m.move_to(axes.c2p(timer.get_value(), 0)).shift(UP*0.2))

        # --- Propagation Animations ---
        self.play(
            timer.animate.set_value(T1), t_d.animate.set_value(1), 
            t_c.animate.set_value(T1/T2), t_b.animate.set_value(T1/T3),
            run_time=T1, rate_func=linear
        )
        self.play(Create(tap1), Flash(rx, color=BLUE, flash_radius=0.3), run_time=0.2)
        math_world.add(tap1) # Add tap to math group so it moves later

        self.play(
            timer.animate.set_value(T2), t_c.animate.set_value(1), 
            t_b.animate.set_value(T2/T3),
            run_time=(T2-T1), rate_func=linear
        )
        self.play(Create(tap2), Flash(rx, color=GREEN, flash_radius=0.3), run_time=0.2)
        math_world.add(tap2)

        self.play(
            timer.animate.set_value(T3), t_b.animate.set_value(1),
            run_time=(T3-T2), rate_func=linear
        )
        self.play(Create(tap3), Flash(rx, color=YELLOW, flash_radius=0.3), run_time=0.2)
        math_world.add(tap3)

        # Cleanup Cursor
        time_cursor.clear_updaters()
        self.play(FadeOut(time_cursor))

        # -----------------------------------------
        # 5. TRANSITION: FOCUS ON THE MATH
        # -----------------------------------------
        # Clean up any leftover packets just in case
        self.remove(packet_d, packet_c, packet_b)

        self.play(
            # 1. Fade out the physical world
            FadeOut(physical_world),
            # 2. Move the Math World to Center and Scale Up
            math_world.animate.scale(1.3).move_to(ORIGIN).shift(DOWN*1)
        )

        # -----------------------------------------
        # 6. EQUATION REVEAL
        # -----------------------------------------
        # Now define equation relative to the NEW position of axes
        equation = MathTex(
            r"h(\tau) = \sum a_i \delta(\tau - \tau_i)",
            font_size=36
        ).next_to(title, DOWN)

        self.play(Write(equation))

        assumption = Tex(
            "(Static / Time-Invariant Assumption)",
            font_size=20,
            color=YELLOW,
        ).next_to(equation, DOWN, buff=0.3)
       
        self.play(Write(assumption))
        
        # Final highlight of the terms
        self.play(
            Indicate(tap1, color=BLUE),
            Indicate(tap2, color=GREEN),
            Indicate(tap3, color=YELLOW), 
            Indicate(equation[0][6:8], color=WHITE) # Indicates 'a_i'
        )
        
        self.wait(2)