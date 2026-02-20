from manim import *
import numpy as np

class ClusterSizeRestrictions(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # CONFIGURATION
        # ---------------------------------------------------------
        # Hexagon Geometry
        R = 0.35  # Radius of individual hexagon
        # Distance between centers of adjacent hexagons = sqrt(3) * R
        d_center = np.sqrt(3) * R 
        
        # Grid visual style
        grid_color = GRAY_B
        stroke_width = 2
        
        # ---------------------------------------------------------
        # SCENE 1: THE FORMULA & CONSTRAINT
        # ---------------------------------------------------------
        
        title = Text("Geometry of Frequency Reuse", font_size=40).to_edge(UP)
        self.play(Write(title))

        # 1. State the restriction
        restriction_text = VGroup(
            Text("Hexagons must tile perfectly without gaps.", font_size=24),
            Text("This restricts the possible values of Cluster Size (N).", font_size=24)
        ).arrange(DOWN).next_to(title, DOWN, buff=0.5)

        self.play(Write(restriction_text))
        self.wait(1)

        # 2. The Formula
        formula = MathTex(
            r"N = i^2 + ij + j^2",
            font_size=60, color=YELLOW
        ).next_to(restriction_text, DOWN, buff=0.5)
        
        params = MathTex(
            r"\text{where } i, j \text{ are non-negative integers}",
            font_size=28, color=GRAY_A
        ).next_to(formula, DOWN)

        self.play(Write(formula), FadeIn(params))
        self.wait(2)

        # ---------------------------------------------------------
        # SCENE 2: FINDING CO-CHANNEL CELLS (ANIMATION)
        # ---------------------------------------------------------
        
        # 1. Clear text, keep title, prepare grid
        self.play(
            FadeOut(restriction_text),
            FadeOut(params),
            formula.animate.scale(0.6).to_corner(UL).set_color(WHITE)
        )
        
        # Show current i, j values for the demo
        val_text = MathTex(r"N = 19 \quad (i=3, j=2)", font_size=36, color=YELLOW)
        val_text.next_to(formula, DOWN, aligned_edge=LEFT)
        self.play(Write(val_text))

        # 2. Generate Large Hex Grid
        # We use axial coordinates (q, r)
        hex_group = VGroup()
        center_hex = None
        grid_radius = 6 

        for q in range(-grid_radius, grid_radius + 1):
            for r in range(-grid_radius, grid_radius + 1):
                if abs(q + r) <= grid_radius:
                    # Axial to Pixel conversion (Pointy-Topped Logic)
                    x = d_center * (q + r/2)
                    y = d_center * (np.sqrt(3)/2 * r)
                    
                    # CORRECTION: Rotate 30 degrees to match Pointy-Topped math
                    h = RegularPolygon(n=6, color=grid_color, stroke_width=stroke_width)
                    h.scale(R).rotate(30*DEGREES) 
                    h.move_to([x, y, 0])
                    
                    hex_group.add(h)
                    
                    if q == 0 and r == 0:
                        center_hex = h

        # Center the grid on screen
        hex_group.move_to(DOWN * 0.5)
        
        self.play(Create(hex_group), run_time=2)
        
        # 3. Mark Center "A"
        center_label = Text("A", font_size=20, color=RED, weight=BOLD).move_to(center_hex)
        self.play(
            center_hex.animate.set_fill(color=RED, opacity=0.3).set_stroke(color=RED, width=4),
            Write(center_label)
        )
        
        # 4. Animate the Path (i=3, j=2)
        # We recalculate origin based on the moved group
        origin_point = center_hex.get_center()
        
        # Define basis vectors (Aligned with grid axes)
        # i direction: 0 degrees (Right)
        # j direction: 60 degrees (Up-Right)
        vec_i = np.array([d_center, 0, 0])
        vec_j = np.array([d_center * np.cos(60*DEGREES), d_center * np.sin(60*DEGREES), 0])

        # --- STEP 1: Move i = 3 ---
        point_interim = origin_point + (vec_i * 3)
        
        line_i = DashedLine(start=origin_point, end=point_interim, color=RED, stroke_width=4)
        dot_moving = Dot(color=RED).move_to(origin_point)
        i_label = MathTex("i=3", color=RED, font_size=24).next_to(line_i, DOWN)

        self.play(FadeIn(dot_moving))
        self.play(
            Create(line_i),
            dot_moving.animate.move_to(point_interim),
            Write(i_label),
            run_time=1.5
        )

        # --- STEP 2: Turn 60 Degrees ---
        arc = Arc(radius=0.4, start_angle=0, angle=60*DEGREES, arc_center=point_interim, color=YELLOW)
        angle_label = MathTex("60^\circ", font_size=20, color=YELLOW).next_to(arc, RIGHT, buff=0.1)
        
        self.play(Create(arc), Write(angle_label))
        
        # --- STEP 3: Move j = 2 ---
        point_final = point_interim + (vec_j * 2)
        
        line_j = DashedLine(start=point_interim, end=point_final, color=RED, stroke_width=4)
        j_label = MathTex("j=2", color=RED, font_size=24).next_to(line_j, UP)
        
        self.play(
            Create(line_j),
            dot_moving.animate.move_to(point_final),
            Write(j_label),
            run_time=1.5
        )

        # --- STEP 4: Mark the Co-channel Cell ---
        target_A = Text("A", font_size=20, color=RED, weight=BOLD).move_to(point_final)
        
        # Note: We create a new hex for highlight, remember to rotate it too!
        target_hex_highlight = RegularPolygon(n=6, color=RED, fill_color=RED, fill_opacity=0.3)
        target_hex_highlight.scale(R).rotate(30*DEGREES).move_to(point_final)

        self.play(
            FadeIn(target_hex_highlight),
            Write(target_A)
        )
        self.wait(1)

        # 5. Populate ALL other 'A's (Rotation)
        self.play(
            FadeOut(line_i), FadeOut(line_j), FadeOut(arc), FadeOut(angle_label), 
            FadeOut(i_label), FadeOut(j_label), FadeOut(dot_moving)
        )

        new_As = VGroup()
        vector_to_A = point_final - origin_point

        for k in range(1, 6): 
            # Rotate vector by k * 60 degrees
            angle = k * 60 * DEGREES
            vx, vy = vector_to_A[0], vector_to_A[1]
            rx = vx * np.cos(angle) - vy * np.sin(angle)
            ry = vx * np.sin(angle) + vy * np.cos(angle)
            
            pos = origin_point + np.array([rx, ry, 0])
            
            lbl = Text("A", font_size=20, color=RED, weight=BOLD).move_to(pos)
            hgh = RegularPolygon(n=6, color=RED, fill_color=RED, fill_opacity=0.3).scale(R).rotate(30*DEGREES).move_to(pos)
            
            new_As.add(VGroup(lbl, hgh))

        self.play(LaggedStart(*[FadeIn(g) for g in new_As], lag_ratio=0.1))
        
        # Connect centers
        all_A_points = [point_final] + [g[1].get_center() for g in new_As]
        connector = Polygon(*all_A_points, color=RED, stroke_width=2, stroke_opacity=0.5)
        self.play(Create(connector))
        self.wait(2)

        # ---------------------------------------------------------
        # SCENE 3: THE TABLE
        # ---------------------------------------------------------
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        table_title = Text("Valid Cluster Sizes (N)", font_size=36, color=BLUE).to_edge(UP)
        
        data = [
            ["1", "0", "1 + 0 + 0", "1"],
            ["1", "1", "1 + 1 + 1", "3"],
            ["2", "0", "4 + 0 + 0", "4"],
            ["2", "1", "4 + 2 + 1", "7"],
            ["3", "0", "9 + 0 + 0", "9"],
            ["2", "2", "4 + 4 + 4", "12"],
            ["3", "2", "9 + 6 + 4", "19"],
        ]

        t = Table(
            data,
            col_labels=[Text("i"), Text("j"), MathTex("i^2 + ij + j^2"), Text("N")],
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": GRAY}
        )
        
        t.scale(0.5).move_to(DOWN * 0.5)
        
        t.get_col_labels()[3].set_color(YELLOW)
        for i in range(len(data)):
            t.get_entries((i+1, 4)).set_color(YELLOW)

        self.play(Write(table_title))
        self.play(Create(t))
        self.wait(3)