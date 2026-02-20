from manim import *
import numpy as np

class MultipathToIQ(Scene):
    def construct(self):
        # ==========================================
        # SCENE 1: The Physical Setup & Multipath
        # ==========================================
        
        # 1. Load Assets (Uncomment the lines below if you have the SVGs)
        # tower = SVGMobject("tower.svg").scale(0.5).to_edge(LEFT, buff=1)
        # mobile = SVGMobject("mobile.svg").scale(0.3).to_edge(RIGHT, buff=1)
        
        # --- Fallback Shapes (Delete these if using SVGs) ---
        tower = Rectangle(height=2, width=0.5, color=BLUE, fill_opacity=0.5).to_edge(LEFT, buff=1)
        tower_label = Text("Tx", font_size=24).next_to(tower, UP)
        mobile = Dot(color=BLUE).to_edge(RIGHT, buff=2)
        mobile_label = Text("Rx", font_size=24).next_to(mobile, UP)
        # ----------------------------------------------------

        self.play(FadeIn(tower), FadeIn(mobile), Write(tower_label), Write(mobile_label))
        self.wait(1)

        # 2. Visualize Multipath Rays (The "Mess")
        # We create jagged lines to represent bouncing off buildings
        path_colors = [YELLOW, GREEN, TEAL, MAROON, GOLD]
        paths = VGroup()
        
        # Create 5 random paths
        for i in range(5):
            p1 = tower.get_right()
            # Random intermediate bounce point
            bounce = [np.random.uniform(-3, 3), np.random.uniform(-2, 2), 0] 
            p2 = mobile.get_left()
            
            # Create a path: Tx -> Bounce -> Rx
            path = Line(p1, bounce).append_points(Line(bounce, p2).points)
            path.set_color(path_colors[i])
            path.set_stroke(width=2)
            paths.add(path)

        # Animate the waves traveling
        self.play(Create(paths, run_time=3, lag_ratio=0.5))
        
        narrative_text = Text("Multipath: Many copies arrive with different phases.", font_size=24).to_edge(UP)
        self.play(Write(narrative_text))
        self.wait(2)

        # ==========================================
        # SCENE 2: Converting to Phasors (Tip-to-Tail)
        # ==========================================

        # 3. Transform Paths into Vectors (Phasors)
        # We move the camera focus or clear the physical objects to focus on Math
        self.play(
            FadeOut(tower), FadeOut(tower_label), 
            FadeOut(paths), FadeOut(narrative_text),
            mobile.animate.move_to(ORIGIN).set_opacity(0) # Hide mobile but keep center ref
        )
        
        # Create small random vectors representing the arriving paths
        # In reality, these are the complex baseband equivalents of the paths
        vectors = VGroup()
        start_point = ORIGIN
        
        # Generate random phases and small amplitudes
        np.random.seed(42) # Fixed seed for reproducibility in class
        current_tip = start_point
        
        for i in range(5):
            angle = np.random.uniform(0, 2*PI)
            length = np.random.uniform(0.5, 1.5)
            
            vec = Arrow(
                start=ORIGIN, 
                end=[length*np.cos(angle), length*np.sin(angle), 0], 
                buff=0, 
                color=path_colors[i]
            )
            
            # Shift the vector to start at the tip of the previous one
            vec.shift(current_tip)
            current_tip = vec.get_end()
            vectors.add(vec)

        explanation = Text("Vector Addition (Tip-to-Tail)", font_size=32).to_edge(UP)
        self.play(Write(explanation))

        # Animate vectors appearing one by one
        for vec in vectors:
            self.play(GrowArrow(vec), run_time=0.5)
        
        self.wait(1)

        # 4. The Resultant Vector (h)
        # This is the sum of all small paths
        resultant_h = Arrow(start=ORIGIN, end=current_tip, buff=0, color=RED, stroke_width=6)
        label_h = MathTex("h").next_to(resultant_h.get_end(), UP + RIGHT)

        self.play(GrowArrow(resultant_h))
        self.play(Write(label_h))
        self.wait(1)

        # Narrative: "We don't care about the small arrows anymore. We only care about the Sum."
        self.play(FadeOut(vectors), FadeOut(explanation))

        # ==========================================
        # SCENE 3: The I/Q Projection (The Formulas)
        # ==========================================

        # 5. Bring in the Coordinate System
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
            tips=False,
            axis_config={"include_numbers": False}
        ).set_color(GRAY)
        
        # Labels for I and Q
        label_I = Text("In-Phase (I)", font_size=24).next_to(axes.x_axis, RIGHT)
        label_Q = Text("Quadrature (Q)", font_size=24).next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(label_I), Write(label_Q))

        # 6. Projections (The 'Math' part)
        h_end = resultant_h.get_end()
        
        # Dashed line to I axis
        proj_line_I = DashedLine(start=h_end, end=[h_end[0], 0, 0], color=RED_A)
        # Dashed line to Q axis
        proj_line_Q = DashedLine(start=h_end, end=[0, h_end[1], 0], color=RED_A)

        self.play(Create(proj_line_I), Create(proj_line_Q))

        # Display the Components
        # Use braces to show magnitude
        brace_I = Brace(Line(ORIGIN, [h_end[0], 0, 0]), DOWN)
        text_I = brace_I.get_text("$I$")
        
        brace_Q = Brace(Line(ORIGIN, [0, h_end[1], 0]), LEFT)
        text_Q = brace_Q.get_text("$Q$")

        self.play(GrowFromCenter(brace_I), Write(text_I))
        self.play(GrowFromCenter(brace_Q), Write(text_Q))

        # 7. Final Formula Reveal
        formula = MathTex(r"h = I + jQ").to_corner(UL).scale(1.2)
        formula_mag = MathTex(r"|h| = \sqrt{I^2 + Q^2}").next_to(formula, DOWN)
        
        # Background box for formulas so they pop
        box = SurroundingRectangle(VGroup(formula, formula_mag), color=WHITE, buff=0.2, fill_opacity=0.1)

        self.play(Write(formula))
        self.play(Write(formula_mag), Create(box))

        self.wait(3)