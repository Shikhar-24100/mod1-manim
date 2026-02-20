from manim import *
import numpy as np

class WirelessSignalScatteringWithSVG(Scene):
    def construct(self):
        # Set background color
        # self.camera.background_color = "#1a1a1a"
        
        # Create title
        # title = Text("Wireless Signal Scattering", font_size=40, color=WHITE)
        # title.to_edge(UP)
        # self.add(title)
        
        # Import SVG files (make sure they're in the same directory)
        tower = SVGMobject("tower.svg").scale(0.7)
        tower.to_edge(LEFT, buff=1.2)
        # tower = SVGMobject("tower.svg", height=2)
        # tower.move_to(LEFT * 5)
        
        rough_wall = ImageMobject("rough2.png").scale(0.25)
        rough_wall.move_to(ORIGIN).shift(UP*0.5)
        
        # mobile = SVGMobject("mobile.svg", height=1.5)
        # mobile.move_to(RIGHT * 5)
        mobile = SVGMobject("mobile.svg").scale(0.5)
        mobile.to_edge(RIGHT, buff=1.2)
        
        # Add labels
        tower_label = Text("TX ", font_size=16, color=WHITE).next_to(tower, DOWN, buff=0.3)
        wall_label = Text("Rough Surface", font_size=16, color=GREY_A).next_to(rough_wall, UP, buff=0.5)
        mobile_label = Text("RX ", font_size=16, color=WHITE).next_to(mobile, DOWN, buff=0.3)
        # Add SVG elements
        self.play(FadeIn(tower), FadeIn(mobile), FadeIn(rough_wall), run_time=1.5)
        self.play(Write(tower_label), Write(wall_label), Write(mobile_label))
        self.wait(1)
        
        # Wavelength explanation
        # wavelength_text = Text(
        #     "Wavelength: λ | Scatterer size comparable to λ → Strong scattering",
        #     font_size=14, color=YELLOW
        # )
        # wavelength_text.to_edge(DOWN)
        # self.play(Write(wavelength_text))
        
        self.wait(1.5)
        
        # Create incident signal ray with wave pattern
        incident_ray_start = tower.get_right() + UP * 0.4
        incident_ray_end = rough_wall.get_left() + RIGHT * 2.1 
        
        incident_ray = Line(
            start=incident_ray_start,
            end=incident_ray_end,
            color=BLUE,
            stroke_width=3
        )
        
        # Add wave pattern to incident ray
        wave_func = lambda t: 0.1 * np.sin(15 * t)
        incident_wave = ParametricFunction(
            lambda t: np.array([
                incident_ray_start[0] + t * (incident_ray_end[0] - incident_ray_start[0]),
                incident_ray_start[1] + wave_func(t),
                0
            ]),
            t_range=[0, 1],
            color=BLUE,
            stroke_width=2.5
        )
        
        self.play(Create(incident_wave), run_time=1.5)
        
        # Animate wave traveling along the ray
        self.play(
            incident_wave.animate.shift(np.array([0.1, 0, 0])),
            run_time=0.5
        )
        
        self.wait(0.5)
        
        # Flash at scattering point
        scatter_point = rough_wall.get_center()
        flash = Circle(radius=0.3, color=YELLOW, fill_opacity=0.8)
        flash.move_to(scatter_point)
        
        self.play(
            FadeIn(flash),
            flash.animate.scale(3),
            FadeOut(flash),
            run_time=1
        )
        
        # Create scattered rays - multiple directions showing diffuse scattering
        scattered_rays = VGroup()
        scattered_waves = VGroup()
        
        num_scattered = 6
        for i in range(num_scattered):
            # Scattered in various directions
            angle = (np.pi / (num_scattered - 1)) * i - np.pi / 2
            
            ray_length = 2
            end_point = scatter_point + ray_length * np.array([np.cos(angle), np.sin(angle), 0])
            
            # Create wavy scattered ray
            scattered_wave = ParametricFunction(
                lambda t, a=angle, sp=scatter_point, ep=end_point: np.array([
                    sp[0] + t * (ep[0] - sp[0]) + 0.08 * np.cos(angle + np.pi/2) * np.sin(12 * t),
                    sp[1] + t * (ep[1] - sp[1]) + 0.08 * np.sin(angle + np.pi/2) * np.sin(12 * t),
                    0
                ]),
                t_range=[0, 1],
                color=YELLOW,
                stroke_width=2
            )
            scattered_waves.add(scattered_wave)
        
        self.play(Create(scattered_waves), run_time=2)
        
        # Highlight the scattered rays traveling
        for i, wave in enumerate(scattered_waves):
            self.play(
                wave.animate.set_stroke(width=2.5, color=ORANGE),
                run_time=0.3
            )
        
        self.wait(0.5)
        
        # Ray reaching the receiver
        receiver_ray_start = scatter_point + np.array([0.5, 0, 0])
        receiver_ray_end = mobile.get_left() + UP * 0.3
        
        receiver_wave = ParametricFunction(
            lambda t: np.array([
                receiver_ray_start[0] + t * (receiver_ray_end[0] - receiver_ray_start[0]),
                receiver_ray_start[1] + t * (receiver_ray_end[1] - receiver_ray_start[1]) + 0.1 * np.sin(14 * t),
                0
            ]),
            t_range=[0, 1],
            color=GREEN,
            stroke_width=2.5,
            # stroke_dash_pattern=[5, 5]
        )
        
        self.play(Create(receiver_wave), run_time=1.5)
        
        # Reception pulse
        reception_pulse = Circle(radius=0.2, color=GREEN, fill_opacity=0.8)
        reception_pulse.move_to(mobile.get_center())
        
        self.play(
            FadeIn(reception_pulse),
            reception_pulse.animate.scale(2.5),
            FadeOut(reception_pulse),
            run_time=1
        )
        
        self.wait(0.5)
        
        # Add explanation text
        explanation = VGroup(
            Text("Rough surface size ~ wavelength → Effective scattering", font_size=25, color=WHITE),
            
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.to_edge(DOWN, buff=0.5)
        explanation.shift(UP*1.5)
        explanation.scale(0.8)
        
        self.play(Write(explanation), run_time=2)
        
        self.wait(2)