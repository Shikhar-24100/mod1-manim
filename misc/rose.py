from manim import *
import numpy as np

class RoseBouquet(ThreeDScene):
    def construct(self):
        # 1. Camera & Scene Setup
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # 2. The Core Rose Surface Formula (Ported from your reference)
        def rose_formula(u, v):
            # u (x in JS) range [0, 1]
            # v (t in JS) range [4*PI, 24*PI]
            p = (np.pi / 2) * np.exp(-v / (8 * np.pi))
            c = np.sin(15 * v) / 150
            
            # The petal shaping logic
            mod_term = (3.6 * v) % (2 * np.pi)
            u_inner = 1 - (1 - mod_term / np.pi)**4 / 2 + c
            y_inner = 2 * (u**2 - u)**2 * np.sin(p)
            
            r = u_inner * (u * np.sin(p) + y_inner * np.cos(p))
            h = u_inner * (u * np.cos(p) - y_inner * np.sin(p))
            
            # Convert to Cartesian for Manim
            return np.array([
                r * np.cos(v),
                r * np.sin(v),
                h + 0.35 # Slightly lifted
            ])

        # 3. Create a Single Rose Function
        def create_rose(pos, color_base, scale_val=0.8):
            rose = Surface(
                rose_formula,
                u_range=[0, 1],
                v_range=[4 * np.pi, 24 * np.pi],
                resolution=(15, 60), # Higher resolution = smoother petals
                should_make_jagged=False
            )
            # Apply a gradient from center to edge
            rose.set_fill_by_value(axes=Z_AXIS, colors=[color_base.darken(0.5), color_base, color_base.lighten(0.3)])
            rose.scale(scale_val)
            rose.move_to(pos)
            
            # Simple stem
            stem = Line(pos + [0, 0, -0.1], pos + [0, 0, -2.5], color=DARK_GREEN, stroke_width=4)
            return VGroup(rose, stem)

        # 4. Assemble the Bouquet
        # Using the same layout logic as your reference code
        rose_positions = [
            [0, 0, 0],         # Center
            [1.2, 0.5, -0.2],  # Right-ish
            [-1.2, -0.3, -0.1],# Left-ish
            [0.5, 1.2, -0.3],  # Back-right
            [-0.4, 1.3, -0.2], # Back-left
            [0.6, -1.2, -0.4], # Front-right
            [-0.7, -1.1, -0.3] # Front-left
        ]
        
        bouquet = VGroup()
        colors = [RED_D, RED_C, PINK, MAROON_B, RED_E, PINK, RED_D]
        
        for i, pos in enumerate(rose_positions):
            rose_unit = create_rose(np.array(pos), colors[i])
            bouquet.add(rose_unit)

        # 5. The Reveal
        title = Text("For You, Harshita", font_size=40, color=RED_A)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP)

        self.play(Create(bouquet), run_time=6, rate_func=ease_in_out_sine)
        self.begin_ambient_camera_rotation(rate=0.2) # Rotate to show off the 3D depth
        self.wait(5)
        self.stop_ambient_camera_rotation()