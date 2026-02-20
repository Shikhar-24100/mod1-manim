from manim import *
import random
import numpy as np

class ResourceAllocationProblem(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # CONFIGURATION & ASSETS
        # ---------------------------------------------------------
        # Load Tower SVG (Gray)
        try:
            tower_svg = SVGMobject("assets/tower.svg").scale(2)
        except:
            # Fallback if file is missing
            tower_svg = VGroup(Line(DOWN, UP), Triangle()).arrange(UP, buff=0).scale(2).set_color(GRAY)

        # ---------------------------------------------------------
        # Part 1: Single User - The Ideal Case
        # ---------------------------------------------------------
        
        # 1. Title
        title = Text("The Resource Allocation Problem").to_edge(UP)
        self.play(Write(title), run_time=1)

        # 2. Layout (Tower Left, User Right)
        tower = tower_svg.copy().to_edge(LEFT, buff=1.5).shift(DOWN * 0.5)
        tower_label = Text("Base Station", font_size=20).next_to(tower, DOWN)

        # Use a Dot for the user
        user_dot = Dot(radius=0.15, color=BLUE).move_to(RIGHT * 3 + DOWN * 0.5)
        user_label = Text("User 1", font_size=24).next_to(user_dot, DOWN)

        self.play(
            FadeIn(tower), 
            Write(tower_label),
            FadeIn(user_dot), 
            Write(user_label)
        )

        # 3. Spectrum Visualization (Top Center)
        # Create the bar slightly lower than the title
        spectrum_bar = Rectangle(width=6, height=0.6, color=GREEN, fill_opacity=0.5, stroke_width=2)
        spectrum_bar.next_to(title, DOWN, buff=0.5)
        
        spectrum_label = Text("Available Spectrum: 25 MHz", font_size=24).next_to(spectrum_bar, UP, buff=0.1)

        self.play(
            Create(spectrum_bar),
            Write(spectrum_label)
        )

        # 4. Ideal Allocation Animation
        # Draw arrow from Spectrum to User
        arrow_1 = Arrow(start=spectrum_bar.get_bottom(), end=user_dot.get_top(), color=GREEN, buff=0.1)
        data_text = Text("Full Bandwidth (High Speed)", color=GREEN, font_size=20).next_to(arrow_1, RIGHT, buff=0.1)

        self.play(GrowArrow(arrow_1), FadeIn(data_text))
        self.wait(1.5)

        # ---------------------------------------------------------
        # Part 2: Multiple Users - The Scaling Problem
        # ---------------------------------------------------------

        # 1. STRICT CLEANUP: Remove Part 1 specific indicators
        self.play(
            FadeOut(arrow_1),
            FadeOut(data_text),
            FadeOut(user_label)
        )
        self.wait(0.2) # Breath to ensure screen is clean

        # 2. Create the Crowd
        # Generate random dots around the original user position
        crowd = VGroup()
        crowd.add(user_dot) # Add the original dot to the group
        
        for _ in range(25):
            d = Dot(color=BLUE, radius=0.12)
            # Random spread around the center point (RIGHT * 3)
            offset = [random.uniform(-2, 2), random.uniform(-1.5, 1.5), 0]
            d.move_to(user_dot.get_center() + np.array(offset))
            crowd.add(d)

        crowd_label = Text("~100 Users", font_size=24).next_to(crowd, DOWN, buff=0.5)

        # Animate the single dot exploding into a crowd
        self.play(
            LaggedStart(*[FadeIn(d) for d in crowd if d is not user_dot], lag_ratio=0.02),
            Write(crowd_label),
            run_time=2
        )

        # 3. Show the Resource Constraint (The Math)
        math_eq = MathTex(r"\frac{25 \text{ MHz}}{100 \text{ Users}} = 250 \text{ kHz}", font_size=32)
        math_eq.next_to(spectrum_bar, DOWN, buff=1.0) # More buffer to avoid overlap with crowd
        math_eq.shift(LEFT*1)

        self.play(Write(math_eq))

        # 4. Visualizing the Slice (Green -> Red Slice)
        # Create a tiny slice
        slice_width = spectrum_bar.width / 25 
        red_slice = Rectangle(width=slice_width, height=0.6, color=RED, fill_opacity=0.9, stroke_width=0)
        # Align it strictly to the left of the bar for visual comparison
        red_slice.align_to(spectrum_bar, LEFT).align_to(spectrum_bar, UP)

        # bad_arrow = Arrow(start=red_slice.get_bottom(), end=crowd.get_top(), color=RED, buff=0.1)
        bad_text = Text("Bandwidth drops!", color=RED, font_size=20).next_to(spectrum_bar, RIGHT)

        self.play(
            spectrum_bar.animate.set_opacity(0.1), # Dim the main bar
            FadeIn(red_slice),
            Write(bad_text)
        )
        self.wait(2)

        # ---------------------------------------------------------
        # Part 3: The Fundamental Question
        # ---------------------------------------------------------

        # 1. TOTAL CLEANUP: Remove everything except the spectrum bar
        # Grouping explicitly to avoid missing anything
        cleanup_items = VGroup(
            tower, tower_label, 
            crowd, crowd_label, 
            math_eq, 
            red_slice, bad_text,
            title, spectrum_label
        )

        self.play(FadeOut(cleanup_items))
        
        # 2. Re-center the Spectrum Bar for the finale
        self.play(
            spectrum_bar.animate.set_opacity(0.5).move_to(ORIGIN)
        )

        # 3. Create the "Box" (Constraint)
        box = SurroundingRectangle(spectrum_bar, color=YELLOW, buff=0.2, stroke_width=4)
        box_label = Text("LIMITED RESOURCE", color=YELLOW, font_size=32).next_to(box, UP)

        self.play(
            Create(box),
            Write(box_label)
        )
        self.wait(1)

        # 4. Final Text
        question = Text(
            "How can we serve millions of users with limited spectrum?", 
            font_size=34, 
            line_spacing=1.2
        ).next_to(box, DOWN, buff=1)

        self.play(Write(question))
        self.wait(3)