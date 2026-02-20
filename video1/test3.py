from manim import *
import numpy as np

class FriisEquation(ThreeDScene):
    def construct(self):
        # Animation 5: Transmitter-Receiver Setup
        title2 = Text("Friis equation", font_size=48, weight=BOLD)
        subtitle = Text("Free‑space path loss and antenna gains", font_size=32)
        subtitle.next_to(title2, DOWN)
        
        self.play(Write(title2))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title2), FadeOut(subtitle))


        

        # -----------------------------
        self.show_transmitter_receiver_setup()
        self.wait(2)
        
        # Transition to 3D view
        self.transition_to_3d()
        
        # Animation 6: Expanding Spherical Wavefront
        self.show_expanding_wavefront()
        self.wait(2)

    def show_transmitter_receiver_setup(self):
        """Animation 5: 2D Transmitter-Receiver setup"""
        # Title
        # title = Text("Friis Free-Space Equation", font_size=48)
        # title.to_edge(UP)
        # self.play(Write(title))
        # self.wait()


        title = Text("Inverse square law", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        
        self.wait(1)
        
        # Transmitter (tower/antenna on left) - using SVG
        try:
            transmitter = SVGMobject("tower.svg")
            transmitter.scale(1.5)
        except:
            # Fallback if SVG not found
            transmitter_base = Rectangle(width=0.3, height=1, fill_opacity=0.8, color=BLUE)
            transmitter_top = Triangle(fill_opacity=0.8, color=YELLOW).scale(0.3)
            transmitter_top.next_to(transmitter_base, UP, buff=0)
            transmitter = VGroup(transmitter_base, transmitter_top)
        
        transmitter.shift(LEFT * 4 + DOWN * 1)
        
        tx_label = Text("Transmitter", font_size=24).next_to(transmitter, DOWN)
        # Fix labels in frame
        self.add_fixed_in_frame_mobjects(tx_label)
        
        # Receiver (phone/antenna on right) - using SVG
        try:
            receiver = SVGMobject("mobile.svg")
            receiver.scale(1.0)
        except:
            # Fallback if SVG not found
            receiver_body = Rectangle(width=0.4, height=0.8, fill_opacity=0.8, color=GREEN)
            receiver_antenna = Line(ORIGIN, UP * 0.4, color=YELLOW).set_stroke(width=3)
            receiver_antenna.next_to(receiver_body, UP, buff=0)
            receiver = VGroup(receiver_body, receiver_antenna)
        
        receiver.shift(RIGHT * 4 + DOWN * 1)
        
        rx_label = Text("Receiver", font_size=24).next_to(receiver, DOWN)
        # Fix labels in frame
        self.add_fixed_in_frame_mobjects(rx_label)
        
        # Animate transmitter and receiver appearance
        self.play(
            FadeIn(transmitter),
            Write(tx_label),
            FadeIn(receiver),
            Write(rx_label)
        )
        self.wait()
        
        # Distance line with label
        distance_line = DashedLine(
            transmitter.get_right() + UP * 0.5,
            receiver.get_left() + UP * 0.5,
            color=WHITE
        )
        distance_label = MathTex("d", font_size=36)
        distance_label.next_to(distance_line, UP)
        
        self.play(
            Create(distance_line),
            Write(distance_label)
        )
        self.wait()
        
        # Antenna gain patterns (petal shapes)
        # Transmitter gain pattern
        tx_pattern = self.create_gain_pattern(4, color=BLUE)
        tx_pattern.scale(0.8).move_to(transmitter.get_center())
        
        # Receiver gain pattern
        rx_pattern = self.create_gain_pattern(4, color=GREEN)
        rx_pattern.scale(0.6).move_to(receiver.get_center()).rotate(PI)
        
        self.play(
            FadeIn(tx_pattern, scale=0.5),
            FadeIn(rx_pattern, scale=0.5)
        )
        self.wait()
        
        # Store objects for later use
        self.transmitter = transmitter
        self.receiver = receiver
        self.tx_label = tx_label
        self.rx_label = rx_label
        self.distance_line = distance_line
        self.distance_label = distance_label
        self.tx_pattern = tx_pattern
        self.rx_pattern = rx_pattern
        self.title = title

    def create_gain_pattern(self, num_petals=4, color=BLUE):
        """Create a petal-shaped antenna gain pattern"""
        petals = VGroup()
        for i in range(num_petals):
            angle = i * 2 * PI / num_petals
            petal = Ellipse(width=0.6, height=1.2, color=color, fill_opacity=0.3)
            petal.rotate(angle)
            petals.add(petal)
        return petals

    def transition_to_3d(self):
        """Transition from 2D to 3D view"""
        # subtitle = Text("Expanding Wavefront (Inverse Square Law)", font_size=36)
        # subtitle.next_to(self.title, DOWN)
        
        # Fix title and subtitle in frame so they don't move
        self.add_fixed_in_frame_mobjects(self.title)
        
        self.play(
            FadeOut(self.tx_pattern),
            FadeOut(self.rx_pattern),
            FadeOut(self.distance_line),
            FadeOut(self.distance_label),
            # Write(subtitle)
        )
        
        # Move camera to 3D view - this will only affect 3D objects
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2)
        self.wait()
        
        # self.subtitle = subtitle

    def show_expanding_wavefront(self):
        """Animation 6: Expanding spherical wavefront with power spreading"""
        # Create equation for power density
        equation = MathTex(
            r"P = \frac{P_t}{4\pi d^2}",
            font_size=36
        )
        equation.to_corner(UL).shift(DOWN * 0.5)
        self.add_fixed_in_frame_mobjects(equation)
        
        self.play(Write(equation))
        box1 = SurroundingRectangle(equation, color=YELLOW, buff=0.2)
        self.add_fixed_in_frame_mobjects(box1)
        self.play(Create(box1))
        
        # Create multiple expanding spheres with decreasing opacity
        max_radius = 5
        num_spheres = 8
        
        for i in range(num_spheres):
            # Calculate sphere properties
            delay = i * 0.3
            start_radius = 0.1
            end_radius = max_radius
            
            # Calculate color intensity (decreases with radius)
            start_color = YELLOW
            end_color = RED
            
            # Create sphere
            sphere = Surface(
                lambda u, v: np.array([
                    start_radius * np.cos(u) * np.cos(v),
                    start_radius * np.cos(u) * np.sin(v),
                    start_radius * np.sin(u)
                ]),
                u_range=[-PI/2, PI/2],
                v_range=[0, 2*PI],
                resolution=(20, 20),
                fill_opacity=0.6,
                stroke_width=0.5
            )
            sphere.set_color(start_color)
            sphere.move_to(self.transmitter.get_center())
            
            # Animate sphere expansion with fading
            self.play(
                sphere.animate.apply_function(
                    lambda p: (p - self.transmitter.get_center()) * (end_radius / start_radius) + self.transmitter.get_center()
                ).set_opacity(0.05),
                rate_func=linear,
                run_time=2.5
            )
            
            if i < num_spheres - 1:
                self.remove(sphere)
        
        self.wait()
        
        # Highlight receiver patch on final sphere
        self.highlight_receiver_patch()

    def highlight_receiver_patch(self):
        """Highlight the small patch where receiver catches signal"""
        # Create a small patch (circular area) at receiver location
        patch_radius = 0.4
        patch = Circle(
            radius=patch_radius,
            color=GREEN,
            fill_opacity=0.7,
            stroke_width=3
        )
        patch.move_to(self.receiver.get_center())
        
        # Create annotation
        annotation = Text("Receiver\nCatch Area", font_size=24, color=GREEN)
        annotation.next_to(patch, RIGHT, buff=0.5)
        self.add_fixed_in_frame_mobjects(annotation)
        
        self.play(
            FadeIn(patch),
            Write(annotation)
        )
        self.wait()
        
        # Show power intensity visualization
        power_label = MathTex(
            r"\text{Power } \propto \frac{1}{d^2}",
            font_size=32,
            color=YELLOW
        )
        power_label.to_corner(DR)
        self.add_fixed_in_frame_mobjects(power_label)
        
        self.play(Write(power_label))
        self.wait(2)
        
        # Restore camera to normal upright view
        self.play(
            FadeOut(patch),
            FadeOut(annotation),
        )
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=2)
        self.wait()


# To render this animation, save it as friis_equation.py and run:
# manim -pql friis_equation.py FriisEquation
# 
# Quality options:
# -ql : Low quality (fastest)
# -qm : Medium quality
# -qh : High quality
# -qk : 4K quality (slowest)
# 
# Add -p flag to preview after rendering