from manim import *
import numpy as np

class FrequencyReuse_MathAndFill(Scene):
    def construct(self):
        # --- Configuration ---
        self.R_LARGE = 3.6       # Radius of the Ghost City
        self.R_SMALL = 0.4       # Radius of individual hex cells
        self.STROKE_WIDTH = 1.5
        
        # Shift the city to the right to make room for math on the left
        self.CITY_OFFSET = RIGHT * 2.5 
        
        # Colors (0=White Center, 1-6=Neighbors)
        self.cell_colors = [WHITE, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

        # --- Execution ---
        self.setup_ghost_city()
        
        # 1. Pre-calculate all valid cluster positions
        self.valid_centers = self.calculate_grid_centers()
        
        # 2. Draw ONLY the first center cluster
        self.render_first_cluster()
        
        # 3. PAUSE & SHOW MATH (User Request)
        self.show_math_sequence()
        
        # 4. Resume and fill the rest
        self.render_remaining_clusters()
        
        # 5. Final Stats
        self.add_capacity_info()

    def setup_ghost_city(self):
        title = Text("Frequency Reuse: The Math & Scaling", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Ghost City Hexagon (Shifted Right)
        self.ghost_hex = RegularPolygon(n=6, radius=self.R_LARGE, color=BLUE, fill_opacity=0.1, stroke_width=2)
        self.ghost_hex.rotate(PI/2) 
        self.ghost_hex.move_to(ORIGIN + self.CITY_OFFSET)
        
        self.play(DrawBorderThenFill(self.ghost_hex))
        self.wait(0.5)

    def calculate_grid_centers(self):
        # BFS to find ALL fitting cluster centers
        cluster_shifts = []
        q, r = 2, 1
        for _ in range(6):
            cluster_shifts.append((q, r))
            q, r = -r, q + r

        queue = [(0, 0)]
        visited_centers = set([(0, 0)])
        valid_centers_sorted = []
        search_radius = self.R_LARGE + 0.5 

        while queue:
            cq, cr = queue.pop(0)
            # Check distance relative to (0,0) before shifting
            pos_local = self.hex_to_pixel_local(cq, cr)
            
            if np.linalg.norm(pos_local) <= search_radius:
                valid_centers_sorted.append((cq, cr))
                for dq, dr in cluster_shifts:
                    nq, nr = cq + dq, cr + dr
                    if (nq, nr) not in visited_centers:
                        visited_centers.add((nq, nr))
                        queue.append((nq, nr))
        
        # Sort by distance from center
        valid_centers_sorted.sort(key=lambda p: np.linalg.norm(self.hex_to_pixel_local(p[0], p[1])))
        return valid_centers_sorted

    def render_first_cluster(self):
        self.all_clusters = VGroup()
        self.red_cells = VGroup()

        # The first center in our sorted list is (0,0)
        center_q, center_r = self.valid_centers[0]
        self.base_cluster = self.create_cluster_mobject(center_q, center_r)
        
        self.play(LaggedStart(*[DrawBorderThenFill(c) for c in self.base_cluster], lag_ratio=0.05))
        self.all_clusters.add(self.base_cluster)

    def show_math_sequence(self):
        # --- The Math Sequence Requested ---
        
        # 1. Definition of S
        def_S = MathTex(r"S = \text{Total Channels}", font_size=32, color=YELLOW)
        def_S.to_edge(LEFT).shift(UP*1.5) # Adjusted slightly for layout
        self.play(Write(def_S))
        self.wait(1)

        # 2. Definition of k
        def_k = MathTex(r"k = \text{Channels/Cell}", font_size=32).next_to(def_S, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(def_k))
        self.wait(1)

        # 3. Definition of N
        def_N = MathTex(r"N = 7 \text{ (Cluster Size)}", font_size=32).next_to(def_k, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(def_N))
        self.wait(1)

        # 4. The Formula S = kN
        formula_S = MathTex(r"S = k \times N", font_size=42, color=YELLOW)
        formula_S.next_to(def_N, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(Write(formula_S))
        self.wait(1)

        # 5. Highlight Box
        surr_box = SurroundingRectangle(formula_S, color=YELLOW, buff=0.2)
        self.play(Create(surr_box))
        self.wait(2)

        desc = Text(f"M ≈ Number of Clusters", font_size=24, color=BLUE).next_to(surr_box, DOWN,buff=0.8, aligned_edge=LEFT)
        self.play(Write(desc))
        self.wait(2)
        
        # Group math elements to fade them out later if needed, or keep them
        self.math_group = VGroup(def_S, def_k, def_N, formula_S, surr_box, desc)

    def render_remaining_clusters(self):
        # Loop through the remaining centers (index 1 to end)
        for cq, cr in self.valid_centers[1:]:
            cluster_group = self.create_cluster_mobject(cq, cr)
            
            # If the cluster has cells (wasn't fully clipped), animate it
            if len(cluster_group) > 0:
                self.play(
                    TransformFromCopy(self.base_cluster, cluster_group),
                    run_time=0.2,
                    rate_func=smooth
                )
                self.all_clusters.add(cluster_group)

    def add_capacity_info(self):
        # 1. Dim Background
        self.play(self.all_clusters.animate.set_opacity(0.4))

        # 2. Highlight Red Cells
        self.play(
            self.red_cells.animate.set_opacity(1).set_stroke(color=YELLOW, width=3)
        )

        # 3. New Math for Capacity
        # Show C = M * S
        capacity_eq = MathTex(r"C_{sys} = M \times S", font_size=36, color=BLUE)
        capacity_eq.next_to(self.math_group, DOWN, buff=0.2, aligned_edge=LEFT)
        
        count = len(self.red_cells)
        
        
        self.play(Write(capacity_eq))
        self.wait(5)

    # --- Helpers ---
    
    def hex_to_pixel_local(self, q, r):
        """Calculates pixel position relative to (0,0)"""
        x = self.R_SMALL * np.sqrt(3) * (q + r/2)
        y = self.R_SMALL * 3/2 * r
        return np.array([x, y, 0])

    def create_cluster_mobject(self, cq, cr):
        """Generates the VGroup for a cluster at grid (cq, cr)"""
        cluster_group = VGroup()
        cell_offsets = [(0, 0), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        
        for i, (dq, dr) in enumerate(cell_offsets):
            abs_q = cq + dq
            abs_r = cr + dr
            
            # Get local pos then apply City Offset
            pos_local = self.hex_to_pixel_local(abs_q, abs_r)
            pos_final = pos_local + self.CITY_OFFSET
            
            # Clipping Check: Use local pos distance against R_LARGE
            if np.linalg.norm(pos_local) < self.R_LARGE:
                color = self.cell_colors[i]
                label = str(i + 1)
                
                hex_obj = self.create_hex(pos_final, color, label)
                cluster_group.add(hex_obj)
                
                if i == 1:
                    self.red_cells.add(hex_obj[0])
                    
        return cluster_group

    def create_hex(self, pos, color, label):
        h = RegularPolygon(n=6, radius=self.R_SMALL, color=color, fill_opacity=0.6, stroke_width=self.STROKE_WIDTH)
        h.rotate(PI/2)
        h.move_to(pos)
        t = Text(label, font_size=14, weight=BOLD).move_to(pos)
        return VGroup(h, t)