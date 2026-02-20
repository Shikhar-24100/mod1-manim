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
        
        # Color scheme for A-G
        cell_colors = {
            "A": RED,
            "B": BLUE,
            "C": GREEN,
            "D": ORANGE,
            "E": PURPLE,
            "F": PINK,
            "G": TEAL
        }
        
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
        
        # Show current i, j values for the demo (N=7)
        val_text = MathTex(r"N = 7 \quad (i=2, j=1)", font_size=36, color=YELLOW)
        val_text.next_to(formula, DOWN, aligned_edge=LEFT)
        self.play(Write(val_text))

        # 2. Generate Large Hex Grid
        # We use axial coordinates (q, r)
        hex_group = VGroup()
        hex_dict = {}  # Store hexagons by (q, r) coordinates
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
                    hex_dict[(q, r)] = h
                    
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
        
        # 4. Calculate co-channel positions for N=7 (i=2, j=1)
        origin_point = center_hex.get_center()
        
        # Define basis vectors (Aligned with grid axes)
        vec_i = np.array([d_center, 0, 0])
        vec_j = np.array([d_center * np.cos(60*DEGREES), d_center * np.sin(60*DEGREES), 0])

        # Helper function to get all 6 co-channel positions
        def get_cochannel_positions(origin, i_val, j_val):
            base_vector = origin + (vec_i * i_val) + (vec_j * j_val)
            positions = [base_vector]
            
            vector_to_first = base_vector - origin
            for k in range(1, 6):
                angle = k * 60 * DEGREES
                vx, vy = vector_to_first[0], vector_to_first[1]
                rx = vx * np.cos(angle) - vy * np.sin(angle)
                ry = vx * np.sin(angle) + vy * np.cos(angle)
                positions.append(origin + np.array([rx, ry, 0]))
            
            return positions

        # Show the path for A (i=2, j=1)
        point_interim = origin_point + (vec_i * 2)
        point_final = point_interim + (vec_j * 1)
        
        line_i = DashedLine(start=origin_point, end=point_interim, color=RED, stroke_width=4)
        dot_moving = Dot(color=RED).move_to(origin_point)
        i_label = MathTex("i=2", color=RED, font_size=24).next_to(line_i, DOWN)

        self.play(FadeIn(dot_moving))
        self.play(
            Create(line_i),
            dot_moving.animate.move_to(point_interim),
            Write(i_label),
            run_time=1.5
        )

        arc = Arc(radius=0.4, start_angle=0, angle=60*DEGREES, arc_center=point_interim, color=YELLOW)
        angle_label = MathTex("60^\circ", font_size=20, color=YELLOW).next_to(arc, RIGHT, buff=0.1)
        
        self.play(Create(arc), Write(angle_label))
        
        line_j = DashedLine(start=point_interim, end=point_final, color=RED, stroke_width=4)
        j_label = MathTex("j=1", color=RED, font_size=24).next_to(line_j, UP)
        
        self.play(
            Create(line_j),
            dot_moving.animate.move_to(point_final),
            Write(j_label),
            run_time=1.5
        )

        # Mark the first co-channel A cell
        target_A = Text("A", font_size=20, color=RED, weight=BOLD).move_to(point_final)
        target_hex_highlight = RegularPolygon(n=6, color=RED, fill_color=RED, fill_opacity=0.3)
        target_hex_highlight.scale(R).rotate(30*DEGREES).move_to(point_final)

        self.play(
            FadeIn(target_hex_highlight),
            Write(target_A)
        )
        self.wait(1)

        # 5. Populate ALL other A co-channel cells quickly
        self.play(
            FadeOut(line_i), FadeOut(line_j), FadeOut(arc), FadeOut(angle_label), 
            FadeOut(i_label), FadeOut(j_label), FadeOut(dot_moving)
        )

        a_positions = get_cochannel_positions(origin_point, 2, 1)
        all_As = VGroup()
        
        for pos in a_positions[1:]:  # Skip first one as it's already shown
            lbl = Text("A", font_size=20, color=RED, weight=BOLD).move_to(pos)
            hgh = RegularPolygon(n=6, color=RED, fill_color=RED, fill_opacity=0.3).scale(R).rotate(30*DEGREES).move_to(pos)
            all_As.add(VGroup(lbl, hgh))

        self.play(LaggedStart(*[FadeIn(g) for g in all_As], lag_ratio=0.1))
        self.wait(1)

        # ---------------------------------------------------------
        # SCENE 3: CALCULATE FOR B (Adjacent to A)
        # ---------------------------------------------------------
        
        # Find B cell - adjacent to center A (one cell to the right)
        b_origin = origin_point + vec_i
        b_label_temp = Text("B", font_size=20, color=BLUE, weight=BOLD).move_to(b_origin)
        
        # Highlight B
        b_hex_highlight = RegularPolygon(n=6, color=BLUE, fill_color=BLUE, fill_opacity=0.3)
        b_hex_highlight.scale(R).rotate(30*DEGREES).move_to(b_origin)
        
        self.play(
            FadeIn(b_hex_highlight),
            Write(b_label_temp)
        )
        self.wait(0.5)

        # Show path from B to its first co-channel cell
        b_point_interim = b_origin + (vec_i * 2)
        b_point_final = b_point_interim + (vec_j * 1)
        
        b_line_i = DashedLine(start=b_origin, end=b_point_interim, color=BLUE, stroke_width=4)
        b_dot = Dot(color=BLUE).move_to(b_origin)
        b_i_label = MathTex("i=2", color=BLUE, font_size=24).next_to(b_line_i, DOWN)

        self.play(FadeIn(b_dot))
        self.play(
            Create(b_line_i),
            b_dot.animate.move_to(b_point_interim),
            Write(b_i_label),
            run_time=1
        )

        b_arc = Arc(radius=0.4, start_angle=0, angle=60*DEGREES, arc_center=b_point_interim, color=YELLOW)
        b_angle_label = MathTex("60^\circ", font_size=20, color=YELLOW).next_to(b_arc, RIGHT, buff=0.1)
        
        self.play(Create(b_arc), Write(b_angle_label), run_time=0.5)
        
        b_line_j = DashedLine(start=b_point_interim, end=b_point_final, color=BLUE, stroke_width=4)
        b_j_label = MathTex("j=1", color=BLUE, font_size=24).next_to(b_line_j, UP)
        
        self.play(
            Create(b_line_j),
            b_dot.animate.move_to(b_point_final),
            Write(b_j_label),
            run_time=1
        )

        # Mark first B co-channel cell
        target_B = Text("B", font_size=20, color=BLUE, weight=BOLD).move_to(b_point_final)
        target_B_highlight = RegularPolygon(n=6, color=BLUE, fill_color=BLUE, fill_opacity=0.3)
        target_B_highlight.scale(R).rotate(30*DEGREES).move_to(b_point_final)

        self.play(
            FadeIn(target_B_highlight),
            Write(target_B)
        )
        self.wait(0.5)

        # Quickly populate all other B co-channel cells
        self.play(
            FadeOut(b_line_i), FadeOut(b_line_j), FadeOut(b_arc), FadeOut(b_angle_label),
            FadeOut(b_i_label), FadeOut(b_j_label), FadeOut(b_dot)
        )

        b_positions = get_cochannel_positions(b_origin, 2, 1)
        all_Bs = VGroup()
        
        for pos in b_positions[1:]:
            lbl = Text("B", font_size=20, color=BLUE, weight=BOLD).move_to(pos)
            hgh = RegularPolygon(n=6, color=BLUE, fill_color=BLUE, fill_opacity=0.3).scale(R).rotate(30*DEGREES).move_to(pos)
            all_Bs.add(VGroup(lbl, hgh))

        self.play(LaggedStart(*[FadeIn(g) for g in all_Bs], lag_ratio=0.05), run_time=1)
        self.wait(1)

        # ---------------------------------------------------------
        # SCENE 4: FILL IN C, D, E, F, G (First Level Cluster)
        # ---------------------------------------------------------
        
        # Define the first cluster around center A using axial coordinates
        # For N=7, the 6 neighbors around (0,0) in axial coordinates are:
        # (1,0), (0,1), (-1,1), (-1,0), (0,-1), (1,-1)
        
        # Helper function to convert axial to pixel coordinates
        def axial_to_pixel(q, r):
            x = d_center * (q + r/2)
            y = d_center * (np.sqrt(3)/2 * r)
            return hex_group[0].get_center() + np.array([x, y, 0]) - hex_group[0].get_center() + origin_point
        
        first_level_coords = [
            # ("C", 0, 1, GREEN),      # Top-right
            ("D", -1, 1, ORANGE),    # Top-left
            ("E", -1, 0, PURPLE),    # Left
            ("F", 0, -1, PINK),      # Bottom-left
            ("G", 1, -1, TEAL),      # Bottom-right
            ("C", 1, 0, GREEN),      # Right (this is actually where B should be, so skip)
        ]
        
        # Actually, for N=7 cluster, the pattern is:
        #       C
        #    D     (B is here at 1,0)
        #  E   A   B
        #    F   G
        
        # Correct positions for N=7:
        first_level_coords = [
            ("C", 0, 1, GREEN),      # Top
            ("D", -1, 1, ORANGE),    # Top-left  
            ("E", -1, 0, PURPLE),    # Left
            ("F", 0, -1, PINK),      # Bottom-left
            ("G", 1, -1, TEAL),      # Bottom-right
        ]

        first_level_group = VGroup()
        
        for letter, q, r, color in first_level_coords:
            # Calculate position using axial coordinates
            x = d_center * (q + r/2)
            y = d_center * (np.sqrt(3)/2 * r)
            pos = origin_point + np.array([x, y, 0])
            
            lbl = Text(letter, font_size=20, color=color, weight=BOLD).move_to(pos)
            hgh = RegularPolygon(n=6, color=color, fill_color=color, fill_opacity=0.3)
            hgh.scale(R).rotate(30*DEGREES).move_to(pos)
            first_level_group.add(VGroup(hgh, lbl))

        self.play(LaggedStart(*[FadeIn(g) for g in first_level_group], lag_ratio=0.1), run_time=1.5)
        self.wait(1)

        # ---------------------------------------------------------
        # SCENE 5: FILL REMAINING LEVELS WITH A-G PATTERN
        # ---------------------------------------------------------
        
        # Define the complete base cluster for N=7
        base_cluster = {
            (0, 0): ("A", RED),
            (1, 0): ("B", BLUE),
            (0, 1): ("C", GREEN),
            (-1, 1): ("D", ORANGE),
            (-1, 0): ("E", PURPLE),
            (0, -1): ("F", PINK),
            (1, -1): ("G", TEAL),
        }
        
        # Track already filled positions
        filled_positions = set(base_cluster.keys())
        
        # The key insight: for N=7 with i=2, j=1, cluster centers repeat at
        # positions that are linear combinations of two basis vectors in axial coords
        # Basis 1: (2, 1) - the shift we calculated
        # Basis 2: rotation of (2,1) by 60° in axial coords
        
        # In axial coordinates, 60° rotation: (q,r) -> (-r, q+r)
        # But for our shift vector, we need to rotate (2,1):
        # After 60° rotation: (-1, 3)? Let's calculate properly.
        
        # Actually, easier approach: rotate the shift vector in all 6 directions
        # and these give us all cluster center offsets
        
        # Calculate all 6 rotations of the (2,1) shift vector
        def rotate_axial_vector(q, r, times):
            """Rotate a vector in axial coordinates by 60° * times"""
            for _ in range(times % 6):
                # 60° CCW rotation in axial: (q, r) -> (-r-q, q)
                q, r = -r-q, q
            return q, r
        
        # Get all 6 shift directions
        shift_vectors = []
        for rot in range(6):
            shift_vectors.append(rotate_axial_vector(2, 1, rot))
        
        # Now we'll fill the grid by finding which cluster each cell belongs to
        all_patterns = VGroup()
        
        for q in range(-grid_radius, grid_radius + 1):
            for r in range(-grid_radius, grid_radius + 1):
                if abs(q + r) <= grid_radius:
                    # Skip already filled positions
                    if (q, r) in filled_positions:
                        continue
                    
                    # Find which cluster this cell belongs to
                    # Try to express (q,r) as cluster_center + offset
                    # where offset is one of the 7 base cluster positions
                    # and cluster_center is a combination of shift vectors
                    
                    found = False
                    
                    # Search through possible cluster centers
                    # A cluster center can be at any combination: n1*v1 + n2*v2
                    # where v1 and v2 are two of our shift vectors
                    # We'll use v1 = (2,1) and v2 = rotate(2,1) by 60° = (-3, 2)
                    
                    v1 = (2, 1)
                    v2 = rotate_axial_vector(2, 1, 1)  # (-3, 2)
                    
                    # Try different combinations
                    for n1 in range(-5, 6):
                        for n2 in range(-5, 6):
                            center_q = n1 * v1[0] + n2 * v2[0]
                            center_r = n1 * v1[1] + n2 * v2[1]
                            
                            # Check if (q,r) is in the cluster centered here
                            offset_q = q - center_q
                            offset_r = r - center_r
                            
                            if (offset_q, offset_r) in base_cluster:
                                letter, color = base_cluster[(offset_q, offset_r)]
                                
                                # Calculate pixel position
                                x = d_center * (q + r/2)
                                y = d_center * (np.sqrt(3)/2 * r)
                                pos = origin_point + np.array([x, y, 0])
                                
                                lbl = Text(letter, font_size=20, color=color, weight=BOLD).move_to(pos)
                                hgh = RegularPolygon(n=6, color=color, fill_color=color, fill_opacity=0.3)
                                hgh.scale(R).rotate(30*DEGREES).move_to(pos)
                                all_patterns.add(VGroup(hgh, lbl))
                                filled_positions.add((q, r))
                                found = True
                                break
                        
                        if found:
                            break

        self.play(LaggedStart(*[FadeIn(g) for g in all_patterns], lag_ratio=0.005), run_time=4)
        self.wait(2)

        # ---------------------------------------------------------
        # SCENE 6: THE TABLE
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