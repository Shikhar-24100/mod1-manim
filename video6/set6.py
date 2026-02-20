from manim import *
import numpy as np

class CoChannelVisualizer(Scene):
    def construct(self):
        # --- Configuration ---
        self.R = 0.4        # Radius of hexagons
        self.i_val = 2      # i steps
        self.j_val = 1      # j steps
        self.N_val = 7      # N = i^2 + ij + j^2 = 7
        
        # Grid Size (q, r coordinates)
        self.q_range = range(-5, 6)
        self.r_range = range(-5, 6)

        # Colors for the 7 cells (A, B, C, D, E, F, G)
        self.cell_colors = {
            "A": RED, "B": GREEN, "C": BLUE, 
            "D": YELLOW, "E": PURPLE, "F": ORANGE, "G": TEAL
        }
        
        # --- 1. Setup the Hex Grid ---
        # We store hexes in a dictionary to access them by coordinate (q,r)
        self.hex_map = {} 
        self.grid_group = VGroup()
        
        # Create the grid
        for q in self.q_range:
            for r in self.r_range:
                self.create_hex(q, r)
        
        # Center the grid on screen
        self.grid_group.move_to(ORIGIN)
        self.play(FadeIn(self.grid_group, run_time=1))
        
        # --- 2. Define the Base Cluster (Center) ---
        # We define the relative positions of A-G for a standard 7-cell cluster
        # Center (0,0) is A. Neighbors are B-G.
        cluster_layout = [
            (0, 0, "A"),    # Center
            (1, 0, "B"),    # Right
            (1, -1, "C"),   # Bottom Right
            (0, -1, "D"),   # Bottom Left
            (-1, 0, "E"),   # Left
            (-1, 1, "F"),   # Top Left
            (0, 1, "G")     # Top Right
        ]
        
        # Light up the Base Cluster
        base_cluster_group = VGroup()
        for q, r, label in cluster_layout:
            if (q, r) in self.hex_map:
                hex_obj, lbl_obj = self.hex_map[(q,r)]
                
                # Animate filling
                self.play(
                    hex_obj.animate.set_fill(self.cell_colors[label], 0.6),
                    lbl_obj.animate.set_text(label).set_opacity(1),
                    run_time=0.1
                )
                base_cluster_group.add(hex_obj)
        
        self.wait(1)

        # --- 3. The Co-Channel Logic (The "Shift Vector") ---
        # Calculate the vector for i=2, j=1 in pixel space
        # This vector represents the distance to the nearest Co-Channel cell
        # Vector = i * u + j * v
        # In axial coords: (i, j) -> (2, 1) means +2q, +1r? 
        # Actually for N=7, shift is usually 2 right, 1 up-right visually.
        # In axial (q,r): Right is +q. Top-Right is +r. 
        # So we want shift (2, 1) in axial coordinates.
        
        shift_q = self.i_val
        shift_r = self.j_val
        
        # We need finding neighbors in all 6 directions (rotations of i,j)
        # But for this demo, we just show the MAIN vector first.
        
        # --- PHASE A: Reusing Frequency 'A' ---
        text_A = Text("1. Reuse Pattern for Cell A", font_size=24, color=RED).to_edge(UP)
        self.play(Write(text_A))
        
        # 1. Start at A(0,0)
        start_hex, _ = self.hex_map[(0,0)]
        
        # 2. Show the Vector (The "Procedure")
        # Calculate pixel end point for (2, 1)
        target_pos = self.hex_to_pixel(shift_q, shift_r) + self.grid_group.get_center()
        
        arrow = Arrow(start=start_hex.get_center(), end=target_pos, color=WHITE, buff=0)
        arrow_label = MathTex("D_{reuse}", font_size=20, color=WHITE).next_to(arrow, UP)
        
        self.play(GrowArrow(arrow), FadeIn(arrow_label))
        
        # 3. Light up the target A
        if (shift_q, shift_r) in self.hex_map:
            h, l = self.hex_map[(shift_q, shift_r)]
            self.play(
                h.animate.set_fill(self.cell_colors["A"], 0.6),
                l.animate.set_text("A").set_opacity(1)
            )
        
        self.wait(0.5)
        self.play(FadeOut(arrow), FadeOut(arrow_label))
        
        # 4. Fill ALL 'A's in the grid (The Iteration)
        # We assume the lattice repeats every (2,1) and its rotations
        self.fill_all_of_type("A", cluster_layout)
        self.wait(1)
        self.play(FadeOut(text_A))


        # --- PHASE B: Reusing Frequency 'B' ---
        # "Show the same procedure for B"
        text_B = Text("2. Same Shift Vector applies to Cell B!", font_size=24, color=GREEN).to_edge(UP)
        self.play(Write(text_B))
        
        # 1. Start at B(1,0) (The neighbor of A)
        start_B_q, start_B_r = 1, 0
        start_hex_B, _ = self.hex_map[(start_B_q, start_B_r)]
        
        # 2. Show the SAME Vector starting from B
        # Destination = Start + Shift
        dest_B_q = start_B_q + shift_q
        dest_B_r = start_B_r + shift_r
        
        # Pixel positions
        p1 = start_hex_B.get_center()
        # Re-calculate vector manually to ensure it's visually identical
        vec_vector = self.hex_to_pixel(shift_q, shift_r) # This is the delta
        p2 = p1 + vec_vector
        
        arrow_B = Arrow(start=p1, end=p2, color=WHITE, buff=0)
        
        self.play(GrowArrow(arrow_B))
        
        # 3. Light up the target B
        if (dest_B_q, dest_B_r) in self.hex_map:
            h, l = self.hex_map[(dest_B_q, dest_B_r)]
            self.play(
                h.animate.set_fill(self.cell_colors["B"], 0.6),
                l.animate.set_text("B").set_opacity(1)
            )
            
        self.wait(0.5)
        self.play(FadeOut(arrow_B))
        
        # 4. Fill ALL 'B's quickly
        self.fill_all_of_type("B", cluster_layout)
        self.wait(1)
        self.play(FadeOut(text_B))


        # --- PHASE C: Speedrun the rest ---
        text_Rest = Text("3. Replicating for C, D, E, F, G...", font_size=24, color=YELLOW).to_edge(UP)
        self.play(Write(text_Rest))
        
        remaining_labels = ["C", "D", "E", "F", "G"]
        
        for label in remaining_labels:
            # Very fast fill
            self.fill_all_of_type(label, cluster_layout, speed=0.1)
            
        self.wait(2)


    # --- HELPER FUNCTIONS ---

    def create_hex(self, q, r):
        """Creates a single hex and adds to map"""
        pos = self.hex_to_pixel(q, r)
        
        # Hexagon
        hex_shape = RegularPolygon(n=6, radius=self.R, color=GREY, stroke_width=1, fill_opacity=0)
        hex_shape.rotate(PI/6) # Rotate so pointy top
        hex_shape.move_to(pos)
        
        # Label (Empty initially)
        label = Text("", font_size=16, color=WHITE).move_to(pos)
        
        self.grid_group.add(hex_shape, label)
        self.hex_map[(q,r)] = (hex_shape, label)

    def hex_to_pixel(self, q, r):
        """Axial to Pixel conversion (Pointy Top)"""
        # x = R * sqrt(3) * (q + r/2)
        # y = R * 3/2 * r
        x = self.R * np.sqrt(3) * (q + r/2.0)
        y = self.R * 3/2.0 * r
        return np.array([x, y, 0])

    def fill_all_of_type(self, target_label, layout, speed=0.3):
        """Fills all cells in the grid that match the target label based on the shift pattern"""
        
        # 1. Find the offset of this label relative to center (0,0)
        base_offset_q = 0
        base_offset_r = 0
        for lq, lr, ll in layout:
            if ll == target_label:
                base_offset_q = lq
                base_offset_r = lr
                break
        
        # 2. Identify all 'replication centers' (lattice points)
        # Lattice basis vectors for N=7 are (2,1) and (-1, 3) roughly? 
        # Actually easier: iterate all grid cells, check if they map to this label
        
        cells_to_animate = []
        
        # The shift basis for N=7 (i=2, j=1)
        # A cell (q,r) is type 'A' if (q - 2r) % 7 == 0? 
        # There's a mathematical check, but let's just use the vectors
        # v1 = (2, 1), v2 = (-1, 2) [Rotated 60 deg]
        # Any linear combination of v1, v2 is a valid center.
        
        # Brute force check for grid range
        # We start from the base offset and add multiples of shifts
        shifts = [
            (2, 1), (1, -2), (-1, -3), (-2, -1), (-1, 2), (1, 3), # 6 neighbors
            (3, -3), (0, 0) # etc
        ]
        
        # A simple BFS or extensive search to find all matching spots
        # For simplicity in this script, I'll iterate the whole grid map
        # and check if the coordinate matches the lattice condition for N=7
        
        group_anim = []
        
        for (q, r), (h, l) in self.hex_map.items():
            # Check if this cell is a 'target_label' cell
            # Formula for N=7 (i=2, j=1):
            # A cell is the same type if: q relative to base == 2*m - 1*n ... etc.
            # Simplified check:
            dq = q - base_offset_q
            dr = r - base_offset_r
            
            # Use the N=7 specific modulo check
            # (dq + 2*dr) % 7 == 0 is often used for specific orientations
            # Let's verify: Shift (2,1) -> 2 + 2(1) = 4 != 0. 
            # Let's try: (dq - 2*dr) % 7 == 0? -> 2 - 2 = 0. YES.
            # Try rotated shift (-1, 2) -> -1 - 2(2) = -5 = 2 mod 7. NO.
            
            # Let's trust the vector addition.
            # Any position P = Base + a*(2,1) + b*(-1, 3) 
            # where a,b are integers.
            # Solving for a,b is cleaner. 
            # 2a - b = dq
            # 1a + 3b = dr
            # -> b = 2a - dq
            # -> a + 3(2a - dq) = dr
            # -> 7a - 3dq = dr
            # -> 7a = dr + 3dq
            # So if (dr + 3dq) is divisible by 7, it's a match!
            
            if (dr + 3*dq) % 7 == 0:
                 # Don't re-animate if already filled (opacity check is hacky, just check label)
                 if l.text != target_label:
                    group_anim.append(
                        AnimationGroup(
                            h.animate.set_fill(self.cell_colors[target_label], 0.6),
                            l.animate.set_text(target_label).set_opacity(1)
                        )
                    )

        if group_anim:
            self.play(LaggedStart(*group_anim, lag_ratio=0.1), run_time=1.5 if speed > 0.1 else 0.8)