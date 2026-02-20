from manim import *
import numpy as np

class DopplerEffect(Scene):
    def construct(self):
        # Create tower from SVG
        tower = SVGMobject("tower.svg").scale(0.8)
        tower.to_edge(LEFT, buff=1)
        
        # Create mobile phone from SVG
        phone = SVGMobject("mobile.svg").scale(0.5)
        phone.shift(RIGHT * 5)
        
        # Add to scene
        self.add(tower, phone)
        
        # Velocity label
        v_label = MathTex("v = 0", font_size=40).next_to(phone, UP)
        self.add(v_label)
        
        # Create continuous sine wave that fills the space
        # The wave is emitted from tower and travels toward phone
        time = ValueTracker(0)
        wavelength_at_phone = ValueTracker(1.0)  # Controls compression/expansion
        
        def make_wave():
            tower_x = tower.get_right()[0]
            phone_x = phone.get_left()[0]
            
            # Base wavelength (constant from tower)
            base_wavelength = 1.0
            
            # Create the wave
            x_range = np.linspace(tower_x, phone_x, 500)
            points = []
            
            for x in x_range:
                # Distance from phone
                d = phone_x - x
                
                # Only modify wavelength close to phone (within 2 units)
                if d < 2.0:
                    # Smooth transition from base to modified wavelength
                    blend = (2.0 - d) / 2.0
                    local_wavelength = base_wavelength + blend * (wavelength_at_phone.get_value() - base_wavelength)
                else:
                    local_wavelength = base_wavelength
                
                # Wave equation with local wavelength
                k = 2 * PI / local_wavelength
                y = 0.5 * np.sin(k * x - time.get_value())
                points.append([x, y, 0])
            
            wave = VMobject(stroke_color=YELLOW, stroke_width=3)
            wave.set_points_smoothly(points)
            return wave
        
        wave = always_redraw(make_wave)
        self.add(wave)
        
        # Animate initial wave propagation
        self.play(time.animate.increment_value(10), run_time=3, rate_func=linear)
        self.wait(0.3)
        
        # ===== PHASE 1: Move toward tower (waves compress near phone) =====
        arrow = Arrow(ORIGIN, LEFT * 1, color=GREEN, stroke_width=8)
        arrow.next_to(phone, UP, buff=0.2)
        v_moving = MathTex("v", font_size=40, color=GREEN).next_to(arrow, UP, buff=0.1)
        
        self.play(FadeOut(v_label), FadeIn(arrow), FadeIn(v_moving))
        
        # Move phone LEFT and compress wavelength near phone
        self.play(
            phone.animate.shift(LEFT * 3),
            arrow.animate.shift(LEFT * 3),
            v_moving.animate.shift(LEFT * 3),
            wavelength_at_phone.animate.set_value(0.5),  # Compress
            time.animate.increment_value(15),
            run_time=5,
            rate_func=smooth
        )
        
        # Stop moving
        v_stop = MathTex("v = 0", font_size=40).next_to(phone, UP)
        self.play(
            FadeOut(arrow), 
            FadeOut(v_moving), 
            FadeIn(v_stop),
            wavelength_at_phone.animate.set_value(1.0)
        )
        self.play(time.animate.increment_value(10), run_time=2, rate_func=linear)
        self.wait(0.3)
        
        # ===== PHASE 2: Move away from tower (waves expand near phone) =====
        arrow2 = Arrow(ORIGIN, RIGHT * 1, color=RED, stroke_width=8)
        arrow2.next_to(phone, UP, buff=0.2)
        v_moving2 = MathTex("v", font_size=40, color=RED).next_to(arrow2, UP, buff=0.1)
        
        self.play(FadeOut(v_stop), FadeIn(arrow2), FadeIn(v_moving2))
        
        # Move phone RIGHT and expand wavelength near phone
        self.play(
            phone.animate.shift(RIGHT * 2.5),
            arrow2.animate.shift(RIGHT * 2.5),
            v_moving2.animate.shift(RIGHT * 2.5),
            wavelength_at_phone.animate.set_value(1.5),  # Expand
            time.animate.increment_value(15),
            run_time=5,
            rate_func=smooth
        )
        
        # Final stop
        v_final = MathTex("v = 0", font_size=40).next_to(phone, UP)
        self.play(
            FadeOut(arrow2), 
            FadeOut(v_moving2), 
            FadeIn(v_final),
            wavelength_at_phone.animate.set_value(1.0)
        )
        self.play(time.animate.increment_value(10), run_time=2, rate_func=linear)
        self.wait(1)