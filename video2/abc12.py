from manim import *
import numpy as np

class RayleighFadingSceneV2(ThreeDScene):
    def construct(self):
        # === TITLE ===
        title = Title("Fading Distribution - Mathematical Intuition").scale(0.9)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)
        
        # ================================================
        # PART A: NLOS SCENARIO - MANY SCATTERED PATHS
        # ================================================
        
        left_center = LEFT * 4.2
        
        # Tower and Mobile
        tower = SVGMobject("tower.svg").scale(0.45)
        tower.move_to(left_center + UP * 1.8 + LEFT * 0.3)
        
        mobile = SVGMobject("mobile.svg").scale(0.3)
        mobile.move_to(left_center + DOWN * 1.8 + RIGHT * 0.8)
        
        # Buildings blocking LOS (using SVG)
        building1 = SVGMobject("building.svg").scale(0.6)
        building1.move_to(left_center + UP * 0.2 + LEFT * 0.2)
        
        building2 = SVGMobject("building.svg").scale(0.45)
        building2.move_to(left_center + DOWN * 0.4 + RIGHT * 0.6)
        
        # Blocked direct path
        blocked_line = DashedLine(
            tower.get_bottom(), mobile.get_top(),
            color=RED, stroke_width=2
        )
        x_mark = Cross(scale_factor=0.2, color=RED).move_to(left_center)
        
        nlos_label = Text("NLOS", font_size=20, color=RED, weight=BOLD)
        nlos_label.next_to(x_mark, DOWN, buff=0.15)
        
        # Show scene
        self.play(
            FadeIn(tower), FadeIn(mobile),
            # FadeIn(building1), FadeIn(building2),
            run_time=0.8
        )
        # self.play(
        #     Create(blocked_line), FadeIn(x_mark), Write(nlos_label),
        #     run_time=0.6
        # )
        
        self.wait(0.3)
        
        # --- MANY SCATTERED PATHS ---
        scatter_text = Text("Many scattered paths exists (multipath)", font_size=22, color=YELLOW)
        scatter_text.move_to(left_center + DOWN * 2.9)
        self.play(FadeIn(scatter_text), run_time=0.4)
        
        # Scatter points (8 paths bouncing off various surfaces)
        scatter_points = [
            left_center + UP * 2.2 + RIGHT * 0.5,
            left_center + UP * 1.2 + RIGHT * 1.6,
            left_center + UP * 0.6 + LEFT * 1.0,
            left_center + DOWN * 0.3 + RIGHT * 1.9,
            left_center + UP * 1.9 + LEFT * 0.6,
            left_center + DOWN * 0.9 + LEFT * 0.8,
            left_center + UP * 0.3 + RIGHT * 2.1,
            left_center + DOWN * 1.2 + RIGHT * 1.4,
        ]
        
        path_colors = [BLUE, GREEN, ORANGE, PURPLE, TEAL, MAROON, GOLD, PINK]
        scattered_paths = VGroup()
        
        for sp, col in zip(scatter_points, path_colors):
            path = VGroup(
                Line(tower.get_bottom(), sp, color=col, stroke_width=2, stroke_opacity=0.6),
                Line(sp, mobile.get_top(), color=col, stroke_width=2, stroke_opacity=0.6)
            )
            scattered_paths.add(path)
        
        # Animate paths appearing
        for path in scattered_paths:
            self.play(Create(path), run_time=0.12)
        
        self.wait(0.5)
        
        # ================================================
        # PART B: PHASOR ADDITION - MANY RANDOM PHASORS
        # ================================================
        
        right_center = RIGHT * 2.5 + UP * 0.3
        phasor_radius = 1.6
        
        phasor_circle = Circle(radius=phasor_radius, color=WHITE, stroke_width=2, stroke_opacity=0.3)
        phasor_circle.move_to(right_center)
        
        phasor_title = Text("Adding all phasors:", font_size=24, color=WHITE)
        phasor_title.next_to(phasor_circle, UP, buff=0.25)
        
        self.play(Create(phasor_circle), Write(phasor_title), run_time=0.6)
        
        # Random phasor data
        num_phasors = 8
        np.random.seed(42)
        random_phases = np.random.uniform(0, 2 * PI, num_phasors)
        random_amplitudes = np.random.uniform(0.45, 0.75, num_phasors)
        
        # Show phasors as starburst first
        phasors_starburst = VGroup()
        for i in range(num_phasors):
            amp, phase = random_amplitudes[i], random_phases[i]
            end = right_center + np.array([amp * np.cos(phase), amp * np.sin(phase), 0])
            arrow = Arrow(right_center, end, color=path_colors[i], buff=0, stroke_width=4,
                         max_tip_length_to_length_ratio=0.25)
            phasors_starburst.add(arrow)
        
        self.play(*[GrowArrow(p) for p in phasors_starburst], run_time=0.8)
        
        random_text = Text("We receive random phases at the receiver!", font_size=20, color=YELLOW)
        random_text.next_to(phasor_circle, DOWN, buff=0.25)
        self.play(FadeIn(random_text), run_time=0.4)
        
        self.wait(0.6)
        
        # --- TIP-TO-TAIL ADDITION ---
        self.play(FadeOut(random_text), run_time=0.2)
        
        adding_text = Text("Add tip-to-tail...(vector addition)", font_size=22, color=YELLOW)
        adding_text.next_to(phasor_circle, DOWN, buff=0.25)
        self.play(FadeIn(adding_text), run_time=0.3)
        
        # Build tip-to-tail phasors
        def build_tip_to_tail(phases, amplitudes, center):
            """Returns VGroup of tip-to-tail arrows and final tip position"""
            arrows = VGroup()
            tip = center.copy()
            for i, (amp, phase) in enumerate(zip(amplitudes, phases)):
                delta = np.array([amp * np.cos(phase), amp * np.sin(phase), 0])
                new_tip = tip + delta
                arrow = Arrow(tip, new_tip, color=path_colors[i], buff=0, stroke_width=4,
                             max_tip_length_to_length_ratio=0.3)
                arrows.add(arrow)
                tip = new_tip
            return arrows, tip
        
        tip_to_tail, final_tip = build_tip_to_tail(random_phases, random_amplitudes, right_center)
        
        # Transform starburst to tip-to-tail
        self.play(
            *[Transform(phasors_starburst[i], tip_to_tail[i]) for i in range(num_phasors)],
            run_time=1.2
        )
        
        self.wait(0.3)
        
        # Resultant
        resultant = Arrow(right_center, final_tip, color=RED, buff=0, stroke_width=6,
                         max_tip_length_to_length_ratio=0.2)
        resultant_label = Text("Resultant", font_size=18, color=RED, weight=BOLD)
        resultant_label.next_to(resultant.get_center(), RIGHT, buff=0.15)
        
        self.play(GrowArrow(resultant), FadeIn(resultant_label), FadeOut(adding_text), run_time=0.6)
        
        self.wait(0.5)
        
        # ================================================
        # PART C: FLUCTUATION - ALL PHASORS SHIFT TOGETHER
        # ================================================
        
        fluct_text = Text("As you move, phases shift...", font_size=22, color=YELLOW)
        fluct_text.next_to(phasor_circle, DOWN, buff=0.25)
        self.play(FadeIn(fluct_text), run_time=0.4)
        
        # Also move the mobile slightly to show connection
        mobile_original_pos = mobile.get_center()
        
        phase_shifts = [0.4, -0.6, 0.9, -0.4, 0.7]
        mobile_shifts = [RIGHT * 0.15, LEFT * 0.1, RIGHT * 0.12, LEFT * 0.08, RIGHT * 0.1]
        
        for shift, mob_shift in zip(phase_shifts, mobile_shifts):
            new_phases = random_phases + shift
            new_tip_to_tail, new_final_tip = build_tip_to_tail(new_phases, random_amplitudes, right_center)
            
            new_resultant = Arrow(right_center, new_final_tip, color=RED, buff=0, stroke_width=6,
                                 max_tip_length_to_length_ratio=0.2)
            new_label = Text("Resultant", font_size=18, color=RED, weight=BOLD)
            new_label.next_to(new_resultant.get_center(), RIGHT, buff=0.15)
            
            # Animate ALL phasors + resultant + mobile moving together
            self.play(
                *[Transform(phasors_starburst[i], new_tip_to_tail[i]) for i in range(num_phasors)],
                Transform(resultant, new_resultant),
                Transform(resultant_label, new_label),
                mobile.animate.shift(mob_shift),
                run_time=0.5
            )
        
        self.wait(0.3)
        
        # Reset mobile position
        self.play(mobile.animate.move_to(mobile_original_pos), run_time=0.3)
        
        # Key insight
        self.play(FadeOut(fluct_text), run_time=0.2)
        
        insight = Text("Amplitude fluctuates randomly!", font_size=22, color=RED, weight=BOLD)
        insight.next_to(phasor_circle, DOWN, buff=0.25)
        self.play(FadeIn(insight), run_time=0.5)
        
        self.wait(4.8)
        
        # ================================================
        # PART D: RAYLEIGH DISTRIBUTION
        # ================================================
        
        # Clear scene
        self.play(FadeIn(building1), FadeIn(building2))
        self.wait(1)
        self.add(x_mark)
        self.wait(5)
        left_group = VGroup(tower, mobile, blocked_line, 
                           x_mark, nlos_label, scattered_paths, scatter_text, phasor_title, insight, building1, building2)
        right_group = VGroup(phasor_circle, phasors_starburst, resultant, 
                            resultant_label)
        
        self.play(FadeOut(left_group), run_time=0.5)

        self.play(right_group.animate.shift(LEFT * 6.5), run_time=0.7)
        self.wait(3)
        # Remove circle and smaller phasor components, keep only resultant
        self.play(FadeOut(phasor_circle), FadeOut(phasors_starburst), run_time=0.4)
        
        # Calculate new center after shift
        axes_center = right_center + LEFT * 6.5
        self.wait(3)
        # Add dotted x and y axes
        axis_length = 2.9
        dotted_x_axis = DashedLine(
            axes_center + LEFT * axis_length, 
            axes_center + RIGHT * axis_length,
            stroke_width=2, color=GRAY
        )
        dotted_y_axis = DashedLine(
            axes_center + DOWN * axis_length,
            axes_center + UP * axis_length,
            stroke_width=2, color=GRAY
        )
        
        # Add axis labels
        x_label = Text("Real", font_size=14, color=GRAY).next_to(axes_center + RIGHT * axis_length, RIGHT, buff=0.15)
        y_label = Text("Imag", font_size=14, color=GRAY).next_to(axes_center + UP * axis_length, UP, buff=0.1)
        
        self.play(Create(dotted_x_axis), Create(dotted_y_axis), run_time=0.5)
        
        
        # Replace resultant_label with the complex form
        resultant_complex = Text(
            "Resultant = x + iy",
            font_size=18, color=RED, weight=BOLD
        )
        resultant_complex.next_to(resultant.get_center(), RIGHT, buff=0.15)
        self.play(Write(x_label), Write(y_label), run_time=0.3)
        
        self.play(Transform(resultant_label, resultant_complex), run_time=0.5)
        self.wait(5)
        self.play(Write(x_label), Write(y_label), run_time=0.3)
        self.wait(2)


        # Calculate x and y components based on current resultant position
        resultant_start = resultant.get_start()
        resultant_end = resultant.get_end()
        
        # Calculate the displacement from origin
        x_displacement = resultant_end[0] - resultant_start[0]
        y_displacement = resultant_end[1] - resultant_start[1]
        
        # X component (along x-axis from origin)
        x_component = Arrow(
            axes_center,
            axes_center + np.array([x_displacement, 0, 0]),
            color=BLUE,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.25
        )
        
        # Y component (along y-axis from origin)
        y_component = Arrow(
            axes_center,
            axes_center + np.array([0, y_displacement, 0]),
            color=GREEN,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.25
        )
        
        # Labels for components
        x_label_comp = MathTex("x", font_size=24, color=BLUE).next_to(x_component.get_end(), DOWN, buff=0.15)
        y_label_comp = MathTex("iy", font_size=24, color=GREEN).next_to(y_component.get_end(), RIGHT, buff=0.15)
        
        # Dotted lines showing the projection from resultant tip to axes
        proj_line_to_x = DashedLine(
            resultant_end,
            axes_center + np.array([x_displacement, 0, 0]),
            stroke_width=1.5,
            color=BLUE_D,
            stroke_opacity=0.5
        )
        proj_line_to_y = DashedLine(
            resultant_end,
            axes_center + np.array([0, y_displacement, 0]),
            stroke_width=1.5,
            color=GREEN_D,
            stroke_opacity=0.5
        )
        
        # Show projection lines first
        self.play(Create(proj_line_to_x), Create(proj_line_to_y), run_time=0.5)
        
        # Then show the component arrows on the axes
        self.play(
            GrowArrow(x_component),
            GrowArrow(y_component),
            run_time=0.8
        )
        
        # Add labels
        self.play(Write(x_label_comp), Write(y_label_comp), run_time=0.5)
        
        self.wait(0.8)
        
        # Fade out the original resultant to emphasize components
        self.play(
            resultant.animate.set_opacity(0),
            resultant_label.animate.set_opacity(0),
            run_time=0.5
        )
        
        self.wait(1.0)
        
        self.wait(5)
        # Position for the distribution plots (right side)
        dist_center = RIGHT * 3.5
        
        # Create two axes for distributions
        x_dist_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 0.5, 0.1],
            x_length=2.5,
            y_length=2.0,
            axis_config={"include_tip": True, "tip_width": 0.15, "tip_height": 0.15, "include_ticks": False},
            tips=True
        ).move_to(dist_center + UP * 1.4)
        
        y_dist_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 0.5, 0.1],
            x_length=2.5,
            y_length=2.0,
            axis_config={"include_tip": True, "tip_width": 0.15, "tip_height": 0.15, "include_ticks": False},
            tips=True
        ).move_to(dist_center + DOWN * 1.6)
        
        # Labels for axes
        x_axis_label = MathTex("x", font_size=28, color=BLUE).next_to(x_dist_axes.x_axis.get_end(), RIGHT, buff=0.1)
        y_axis_label = MathTex("y", font_size=28, color=GREEN).next_to(y_dist_axes.x_axis.get_end(), RIGHT, buff=0.1)
        
        # Gaussian/Normal distribution function
        def gaussian(x, mu=0, sigma=1):
            return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        
        # Create Gaussian curves (Normal distribution for x and y)
        x_gaussian = x_dist_axes.plot(
            lambda x: gaussian(x, mu=0, sigma=1),
            x_range=[-3, 3],
            color=BLUE,
            stroke_width=3
        )
        
        y_gaussian = y_dist_axes.plot(
            lambda y: gaussian(y, mu=0, sigma=1),
            x_range=[-3, 3],
            color=GREEN,
            stroke_width=3
        )
        
        # Labels for distributions
        px_label = MathTex("P_X(x)", font_size=24, color=BLUE).next_to(x_dist_axes, UP, buff=0.2)
        py_label = MathTex("P_Y(y)", font_size=24, color=GREEN).next_to(y_dist_axes, UP, buff=0.2)
        
        # Vertical line at mean (x=0, y=0)
        x_mean_line = x_dist_axes.get_vertical_line(
            x_dist_axes.c2p(0, gaussian(0, 0, 1)),
            color=BLUE,
            stroke_width=2,
            line_func=DashedLine
        )
        
        y_mean_line = y_dist_axes.get_vertical_line(
            y_dist_axes.c2p(0, gaussian(0, 0, 1)),
            color=GREEN,
            stroke_width=2,
            line_func=DashedLine
        )
        
        # Animate the creation of axes and distributions
        self.play(
            Create(x_dist_axes),
            Create(y_dist_axes),
            run_time=0.6
        )
        
        self.play(
            Write(x_axis_label),
            Write(y_axis_label),
            Write(px_label),
            Write(py_label),
            run_time=0.5
        )
        
        # Draw the Gaussian curves
        self.play(
            Create(x_gaussian),
            Create(y_gaussian),
            run_time=1.0
        )
        
        # Show mean lines
        self.play(
            Create(x_mean_line),
            Create(y_mean_line),
            run_time=0.5
        )
        
        self.wait(0.5)
        
        # Add text explanation
        gaussian_text = Text(
            "x and y follow Gaussian distribution (Central Limit Theorem)",
            font_size=20,
            color=YELLOW
        ).to_edge(DOWN, buff=0.4)
        
        self.play(FadeIn(gaussian_text), run_time=0.6)
        
        self.wait(6)



        # Fade out the two separate distributions
        self.play(
            FadeOut(x_dist_axes),
            FadeOut(y_dist_axes),
            FadeOut(x_gaussian),
            FadeOut(y_gaussian),
            FadeOut(x_mean_line),
            FadeOut(y_mean_line),
            FadeOut(x_axis_label),
            FadeOut(y_axis_label),
            FadeOut(px_label),
            FadeOut(py_label),
            FadeOut(gaussian_text),
            # Fade out left side elements
            FadeOut(dotted_x_axis),
            FadeOut(dotted_y_axis),
            FadeOut(x_component),
            FadeOut(y_component),
            FadeOut(x_label_comp),
            FadeOut(y_label_comp),
            FadeOut(proj_line_to_x),
            FadeOut(proj_line_to_y),
            FadeOut(resultant),
            FadeOut(resultant_label),
            FadeOut(title),
            run_time=0.6
        )
        
        self.wait(4)
        
        # Create 3D axes (centered on screen)
        axes_3d = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 0.2, 0.05],
            x_length=4,
            y_length=4,
            z_length=2.5,
            axis_config={"include_tip": True, "tip_width": 0.15, "tip_height": 0.15},
        ).move_to(ORIGIN)  # Centered on screen
        
        # Add axis labels
        x_label_3d = MathTex("x", font_size=28, color=BLUE).next_to(axes_3d.x_axis.get_end(), RIGHT, buff=0.1)
        y_label_3d = MathTex("y", font_size=28, color=GREEN).next_to(axes_3d.y_axis.get_end(), UP, buff=0.1)
        z_label_3d = MathTex("P(x,y)", font_size=24, color=WHITE).next_to(axes_3d.z_axis.get_end(), UP, buff=0.1)
        
        # 2D Gaussian function (joint distribution)
        def gaussian_2d(x, y, sigma=1):
            return (1 / (2 * np.pi * sigma**2)) * np.exp(-(x**2 + y**2) / (2 * sigma**2))
        
        # Create the 3D surface
        surface = Surface(
            lambda u, v: axes_3d.c2p(u, v, gaussian_2d(u, v, sigma=1)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_width=0.5,
            stroke_color=BLUE
        )
        
        # Start with camera at 2D angle (top-down view)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        
        # Animate creation of 3D axes
        self.play(Create(axes_3d), run_time=0.8)
        self.play(
            Write(x_label_3d),
            Write(y_label_3d),
            Write(z_label_3d),
            run_time=0.5
        )
        
        # Create the 3D surface (will appear flat initially)
        self.play(Create(surface), run_time=2.5)
        
        self.wait(4.5)
        
        # Add contour lines on the base
        contours = VGroup()
        for r in [0.5, 1.0, 1.5, 2.0, 2.5]:
            circle = Circle(radius=r * 0.6, color=GRAY, stroke_width=1, stroke_opacity=0.4)
            circle.move_to(axes_3d.c2p(0, 0, 0))
            contours.add(circle)
        
        self.play(Create(contours), run_time=0.6)
        
        self.wait(0.5)
        
        # Smooth transition from 2D (flat) to 3D view
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2.0)
        
        self.wait(0.5)
        
        # Add explanation text
        joint_text = Text(
            "Joint distribution: P(x,y) - product of two Gaussians",
            font_size=20,
            color=YELLOW
        )
        joint_text.to_edge(DOWN, buff=0.4)
        
        self.add_fixed_in_frame_mobjects(joint_text)
        self.play(FadeIn(joint_text), run_time=0.6)
        
        self.wait(1.0)
        
        # Rotate the camera around the surface
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        
        self.wait(5.0)



        # Fade out 3D surface and related elements
        self.play(
            FadeOut(surface),
            FadeOut(axes_3d),
            FadeOut(x_label_3d),
            FadeOut(y_label_3d),
            FadeOut(z_label_3d),
            FadeOut(contours),
            FadeOut(joint_text),
            run_time=0.8
        )
        
        # Reset camera to 2D view
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        
        self.wait(3.3)
        
        # Show transformation equations
        transform_title = Text("Transformation to Polar Coordinates", font_size=32, color=YELLOW, weight=BOLD)
        transform_title.to_edge(UP, buff=0.5)
        
        # Cartesian to Polar transformation
        eq1 = MathTex(r"r = \sqrt{x^2 + y^2}", font_size=36, color=WHITE)
        eq2 = MathTex(r"\theta = \tan^{-1}\left(\frac{y}{x}\right)", font_size=36, color=WHITE)
        
        eq1.move_to(UP * 1.5)
        eq2.next_to(eq1, DOWN, buff=0.5)
        
        self.play(Write(transform_title), run_time=0.6)
        self.play(Write(eq1), run_time=0.8)
        self.play(Write(eq2), run_time=0.8)
        
        self.wait(1.5)
        
        # Show the resulting distributions
        result_eq = MathTex(
            r"P_{R,\Theta}(r,\theta) = |J| \cdot P_{X,Y}(x,y)",
            font_size=32,
            color=BLUE
        )
        result_eq.next_to(eq2, DOWN, buff=0.8)
        
        self.play(Write(result_eq), run_time=0.8)
        
        self.wait(1.5)
        
        # Fade out equations to make space for graphs
        self.play(
            FadeOut(transform_title),
            FadeOut(eq1),
            FadeOut(eq2),
            FadeOut(result_eq),
            run_time=0.6
        )
        
        self.wait(0.3)
        
        # ================================================
        # PART H: SHOW RAYLEIGH AND PHASE DISTRIBUTIONS
        # ================================================
        title1 = Title("Rayleigh and Rician Fading").scale(0.9)
        self.add(title1)
        # Create two plots side by side
        left_pos = LEFT * 3.5
        right_pos = RIGHT * 3.5
        
        # Rayleigh Distribution (left)
        rayleigh_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 0.7, 0.2],
            x_length=4.5,
            y_length=3,
            axis_config={"include_tip": True, "tip_width": 0.15, "tip_height": 0.15},
            tips=True
        ).move_to(left_pos)
        
        # Rayleigh PDF function
        def rayleigh_pdf(r, sigma=1):
            if r < 0:
                return 0
            return (r / sigma**2) * np.exp(-r**2 / (2 * sigma**2))
        
        rayleigh_curve = rayleigh_axes.plot(
            lambda r: rayleigh_pdf(r, sigma=1),
            x_range=[0, 4],
            color=BLUE,
            stroke_width=4
        )
        
        # Labels for Rayleigh
        rayleigh_title = MathTex(r"P_R(r)", font_size=32, color=RED)
        rayleigh_title.next_to(rayleigh_axes, UP, buff=0.3)
        
        r_label = MathTex("r", font_size=28, color=WHITE).next_to(rayleigh_axes.x_axis.get_end(), RIGHT, buff=0.1)
        
        # Phase/Theta Distribution (right) - Uniform
        theta_axes = Axes(
            x_range=[0, 2*PI, PI/2],
            y_range=[0, 0.25, 0.1],
            x_length=4.5,
            y_length=3,
            axis_config={"include_tip": True, "tip_width": 0.15, "tip_height": 0.15},
            tips=True
        ).move_to(right_pos)


        # Uniform distribution for phase
        uniform_height = 1 / (2 * PI)
        uniform_line = theta_axes.plot(
            lambda x: uniform_height,
            x_range=[0, 2*PI],
            color=PURPLE,
            stroke_width=4
        )
        
        # Labels for Phase
        theta_title = MathTex(r"P_\Theta(\theta)", font_size=32, color=PURPLE)
        theta_title.next_to(theta_axes, UP, buff=0.3)
        
        theta_label = MathTex(r"\theta", font_size=28, color=WHITE).next_to(theta_axes.x_axis.get_end(), RIGHT, buff=0.1)
        
        # Custom x-axis labels for theta
        theta_x_labels = VGroup(
            MathTex("0", font_size=20).next_to(theta_axes.c2p(0, 0), DOWN, buff=0.15),
            MathTex(r"\pi", font_size=20).next_to(theta_axes.c2p(PI, 0), DOWN, buff=0.15),
            MathTex(r"2\pi", font_size=20).next_to(theta_axes.c2p(2*PI, 0), DOWN, buff=0.15)
        )
        
        # Animate Rayleigh distribution
        self.play(Create(rayleigh_axes), run_time=0.6)
        self.play(Write(rayleigh_title), Write(r_label), run_time=0.5)
        self.play(Create(rayleigh_curve), run_time=1.0)
        
        self.wait(0.5)
        
        # Animate Phase distribution
        self.play(Create(theta_axes), run_time=0.6)
        self.play(Write(theta_title), Write(theta_label), Write(theta_x_labels), run_time=0.5)
        self.play(Create(uniform_line), run_time=1.0)
        
        self.wait(1.5)
        
        # ================================================
        # PART I: FADE OUT PHASE, CENTER RAYLEIGH
        # ================================================
        
        # Fade out the phase distribution
        self.play(
            FadeOut(theta_axes),
            FadeOut(theta_title),
            FadeOut(theta_label),
            FadeOut(theta_x_labels),
            FadeOut(uniform_line),
            run_time=0.6
        )
        
        self.wait(0.3)
        
        # Move Rayleigh to center
        rayleigh_group = VGroup(rayleigh_axes, rayleigh_curve, rayleigh_title, r_label)
        
        self.play(
            rayleigh_group.animate.move_to(ORIGIN),
            run_time=0.8
        )
        
        self.wait(1.0)
        
        # Add emphasis text
        emphasis_text = Text(
            "Rayleigh Fading: Amplitude follows Rayleigh Distribution",
            font_size=24,
            color=YELLOW
        ).to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(emphasis_text), run_time=0.6)
        
        self.wait(4.0)


        # Distribution title
        # dist_title = Text("Signal Amplitude Distribution", font_size=30, color=WHITE)
        # dist_title.next_to(title, DOWN, buff=0.5)
        # self.play(Write(dist_title), run_time=0.5)
        
        # # Axes
        # axes = Axes(
        #     x_range=[0, 4, 1],
        #     y_range=[0, 0.7, 0.2],
        #     x_length=9,
        #     y_length=3.5,
        #     tips=False,
        #     axis_config={"color": WHITE}
        # ).move_to(ORIGIN + DOWN * 0.5)
        
        # x_label = Text("Amplitude (r)", font_size=20).next_to(axes.x_axis, DOWN, buff=0.25)
        # y_label = Text("Probability", font_size=20).next_to(axes.y_axis, LEFT, buff=0.2).rotate(PI/2)
        
        # self.play(Create(axes), Write(x_label), Write(y_label), run_time=0.7)
        
        # # Rayleigh PDF
        # sigma = 1.0
        # rayleigh_curve = axes.plot(
        #     lambda r: (r / sigma**2) * np.exp(-r**2 / (2 * sigma**2)) if r > 0 else 0,
        #     x_range=[0.01, 4], color=BLUE, stroke_width=4
        # )
        
        # rayleigh_formula = MathTex(
        #     r"f(r) = \frac{r}{\sigma^2} e^{-r^2/2\sigma^2}",
        #     font_size=30, color=BLUE
        # ).to_corner(UR, buff=0.6)
        
        # self.play(Create(rayleigh_curve), Write(rayleigh_formula), run_time=1.0)
        
        # self.wait(0.4)
        
        # # Highlight deep fades
        # fade_region = axes.get_area(rayleigh_curve, x_range=[0.01, 0.35], color=RED, opacity=0.5)
        # fade_text = Text("Deep fades!", font_size=20, color=RED, weight=BOLD)
        # fade_text.move_to(axes.c2p(0.8, 0.12))
        # fade_arrow = Arrow(fade_text.get_left(), axes.c2p(0.18, 0.06), color=RED, stroke_width=3)
        
        # self.play(FadeIn(fade_region), Write(fade_text), GrowArrow(fade_arrow), run_time=0.6)
        
        # self.wait(0.8)
        
        # # ================================================
        # # PART E: RAYLEIGH VS RICIAN
        # # ================================================
        
        # self.play(FadeOut(VGroup(fade_region, fade_text, fade_arrow)), run_time=0.3)
        
        # # Rician curve (Gaussian-like, shifted right)
        # rician_curve = axes.plot(
        #     lambda r: 0.65 * np.exp(-((r - 1.9)**2) / 0.4) if r > 0 else 0,
        #     x_range=[0.01, 4], color=ORANGE, stroke_width=4
        # )
        
        # rician_label = Text("Rician (LOS + scatter)", font_size=18, color=ORANGE)
        # rician_label.move_to(axes.c2p(3.0, 0.5))
        
        # rayleigh_label2 = Text("Rayleigh (NLOS)", font_size=18, color=BLUE)
        # rayleigh_label2.move_to(axes.c2p(2.8, 0.22))
        
        # self.play(
        #     Create(rician_curve),
        #     Write(rician_label), Write(rayleigh_label2),
        #     run_time=0.8
        # )
        
        # # Comparison text
        # compare = VGroup(
        #     Text("Rayleigh: Deep fades common", font_size=22, color=BLUE),
        #     Text("Rician: More stable (LOS helps)", font_size=22, color=ORANGE)
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        # compare.to_edge(DOWN, buff=0.4)
        
        # self.play(FadeIn(compare, shift=UP * 0.2), run_time=0.5)
        
        # self.wait(1.2)
        
        # # ================================================
        # # PART F: KEY TAKEAWAY
        # # ================================================
        
        # self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)
        
        # final_title = Text("Rayleigh Fading", font_size=44, weight=BOLD, color=BLUE)
        # final_title.to_edge(UP, buff=0.5)
        
        # takeaway = VGroup(
        #     Text("✓ Many scattered paths + No LOS", font_size=26, color=WHITE),
        #     Text("✓ Random phases → Random amplitude", font_size=26, color=WHITE),
        #     Text("✓ Amplitude follows Rayleigh distribution", font_size=26, color=YELLOW),
        #     Text("✓ Deep fades happen frequently", font_size=26, color=RED),
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        # takeaway.move_to(ORIGIN + UP * 0.3)
        
        # formula_box = VGroup(
        #     MathTex(r"f(r) = \frac{r}{\sigma^2} e^{-r^2/2\sigma^2}", font_size=34, color=BLUE),
        #     Text("NLOS Multipath Model", font_size=18, color=GRAY)
        # ).arrange(DOWN, buff=0.15)
        # formula_box.to_edge(DOWN, buff=0.5)
        
        # self.play(Write(final_title), run_time=0.5)
        # for line in takeaway:
        #     self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.4)
        # self.play(FadeIn(formula_box, shift=UP * 0.2), run_time=0.5)
        
        # self.wait(2.0)
        
        # self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.7)