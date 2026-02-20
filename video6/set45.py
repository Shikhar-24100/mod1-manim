from manim import *
import numpy as np

class CellularReplication(Scene):
    def construct(self):
        # --- Configuration ---
        # SCALED DOWN VALUES
        self.R_SMALL = 0.45   # Reduced from 0.55 to fit screen better
        self.R_MACRO = 3.2    # Reduced from 3.8 to keep proportional
        self.STROKE_WIDTH = 2
        
        # --- 1. Define the Fundamental Cluster ---
        self.cluster_offsets = [
            (0, 0, BLUE, "C"),      # Top
            (0, -1, GREEN, "B"),    # Bottom Left
            (1, -1, RED, "A")       # Bottom Right
        ]
        
        # Adjust centering offset for the new smaller size
        self.centering_offset = UP * 0.65 

        # --- Scene Execution ---
        self.show_macro_cell()
        self.intro()
        self.show_base_cluster()
        self.animate_replication()
        self.capacity_summary()

    def show_macro_cell(self):
        # Big Hexagon
        title = Text("Single Cell: High Power Transmitter", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))

        self.macro_hex = RegularPolygon(n=6, radius=self.R_MACRO, color=WHITE, stroke_width=4)
        self.macro_hex.rotate(PI/2) 

        # --- TOWER REPLACEMENT ---
        # Loading the SVG from assets folder
        try:
            self.tower_group = SVGMobject("assets/tower.svg")
            
            # Styling: Set color to RED to match previous theme, and adjust size
            # self.tower_group.set_color(RED)
            self.tower_group.set(height=2) # Adjust height to fit inside the macro hex
            self.tower_group.move_to(ORIGIN)
            
        except OSError:
            # Fallback if file is missing (prevents crash during testing)
            print("Warning: assets/tower.svg not found. Using fallback circle.")
            self.tower_group = Circle(radius=0.5, color=RED, fill_opacity=1)
        
        self.macro_group = VGroup(self.macro_hex, self.tower_group)

        # Animation
        self.play(DrawBorderThenFill(self.macro_hex), FadeIn(self.tower_group))
        
        why_hex = Text("* Why hexagonal? Explained later", 
                        font_size=18, color=YELLOW, slant=ITALIC)
        why_hex.to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        self.play(Write(why_hex))
        calc_box = VGroup(
            Text("Capacity Calculation:", font_size=26, color=YELLOW),
            MathTex(r"\text{Total Channels} = \frac{25000 \text{ kHz}}{30 \text{ kHz}}", font_size=22),
            MathTex(r"= 833 \text{ channels}", font_size=24),
            MathTex(r"\approx 832 \text{ users}", font_size=26, color=GREEN)
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        calc_box.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        self.play(Write(calc_box), run_time=3)
        self.wait(5)
        self.play(
            FadeOut(self.tower_group),FadeOut(title), FadeOut(why_hex),FadeOut(calc_box),
            self.macro_hex.animate.set_stroke(opacity=0.3).set_fill(opacity=0.1, color=GREY),
            run_time=1.5
        )
        self.macro_hex.set_z_index(-1)
        self.wait(1)

    def intro(self):
        self.wait(2)
        
        # Fade out tower and dim the hex
        

    def show_base_cluster(self):
        # Create center cluster with the OFFSET applied
        self.base_cluster = self.create_cluster_group(0, 0)
        
        title = Text("The Fundamental Cluster (N=3)", font_size=32).to_edge(UP)
        self.play(Write(title))
        
        self.play(LaggedStart(*[DrawBorderThenFill(cell) for cell in self.base_cluster], lag_ratio=0.3))
        
        self.wait(1)

        freq_info = VGroup(
            Text("Frequency Allocation:", font_size=24, color=YELLOW),
            Text("• Total: 832 channels", font_size=19),
            Text("• 832 ÷ 3 = 277 channels/cell", font_size=19),
            Text("• Each cell: different frequencies", font_size=19),
            Text("• No overlap between neighbors", font_size=19, color=RED)
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        freq_info.to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        
        self.play(Write(freq_info), run_time=2.5)
        self.wait(2)

        # Capacity note (below freq_info)
        # capacity_note = VGroup(
        #     Text("Total System Capacity:", font_size=24, color=GREEN),
        #     Text("3 × 277 ≈ 831 users", font_size=21),
        #     Text("Same as single cell!", font_size=23, color=BLUE, weight=BOLD)
        # ).arrange(DOWN, buff=0.18)
        # capacity_note.next_to(freq_info, DOWN, buff=0.6)
        
        # self.play(Write(capacity_note))
        # self.wait(2)

        # Store for next scene
        self.freq_info = freq_info
        # self.capacity_note = capacity_note
        
        self.play(FadeOut(title), FadeOut(freq_info))
        
        rep_title = Text("Replicating Coverage...", font_size=32, color=BLUE).to_edge(UP)
        self.play(Write(rep_title))
        self.title = rep_title

    def animate_replication(self):
        # --- Dynamic Coordinate Generation ---
        directions = [
            (1, 1), (2, -1), (1, -2), 
            (-1, -1), (-2, 1), (-1, 2)
        ]
        
        valid_anchors = []
        visited = set()
        visited.add((0,0))
        queue = [(0,0)]
        
        # Breadth-first search to find all valid tiling spots inside the radius
        while queue:
            curr_q, curr_r = queue.pop(0)
            
            # Check neighbors
            for dq, dr in directions:
                nq, nr = curr_q + dq, curr_r + dr
                
                if (nq, nr) not in visited:
                    pixel_pos = self.hex_to_pixel(nq, nr) 
                    dist = np.linalg.norm(pixel_pos)
                    
                    if dist < self.R_MACRO - 0.2:
                        valid_anchors.append((nq, nr))
                        visited.add((nq, nr))
                        queue.append((nq, nr))

        # Sort by distance from center so they animate in a ripple
        valid_anchors.sort(key=lambda x: x[0]**2 + x[1]**2)

        self.all_clusters = VGroup(self.base_cluster)
        self.play(FadeOut(self.title))
        
        # Animation Loop
        for i, (aq, ar) in enumerate(valid_anchors):
            new_cluster = self.create_cluster_group(aq, ar)
            new_cluster.set_opacity(0.5)
            
            self.play(
                TransformFromCopy(self.base_cluster, new_cluster),
                run_time=0.15 
            )
            
            new_cluster.set_opacity(1)
            self.all_clusters.add(new_cluster)

        self.wait(1)

        calc_box = VGroup(
            Text("Capacity Calculation:", font_size=25, color=YELLOW),
            Text("Single 3-cell cluster:", font_size=19),
            MathTex(r"3 \times 277 = 831 \text{ users}", font_size=21),
            Text(f"With {len(valid_anchors)+1} clusters (frequency reuse):", font_size=19, color=GREEN),
            MathTex(f"831 \\times {len(valid_anchors)+1} = {831 * (len(valid_anchors)+1)} \\text{{ users}}", font_size=23, color=GREEN),
            Text("Coverage: Same area", font_size=17, color=BLUE),
            Text(f"Capacity: {len(valid_anchors)+1}× increase!", font_size=21, color=RED, weight=BOLD)
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        calc_box.to_edge(LEFT, buff=0.1).shift(DOWN*0.3)
        
        self.play(Write(calc_box), run_time=4)
        self.wait(6)
        self.play(FadeOut(calc_box))
        
        # Key insight
        insight = VGroup(
            Text("Key Insight:", font_size=23, color=YELLOW),
            Text("Frequency reuse enables MORE", font_size=17),
            Text("users in the SAME coverage area", font_size=17),
            Text("by tiling smaller cells!", font_size=17, color=GREEN)
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        insight.to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        
        self.play(Write(insight))
        self.wait(4)
        self.play(FadeOut(insight))

    def capacity_summary(self):
        red_cells = VGroup()
        for cluster in self.all_clusters:
            for hex_group in cluster:
                if hex_group[0].color == RED:
                    red_cells.add(hex_group)

        self.play(
            self.all_clusters.animate.set_opacity(0.2),
            red_cells.animate.set_opacity(1).set_stroke(width=3, color=YELLOW)
        )
        
        final_text = Text("Cluster Replication = Frequency Reuse", font_size=28, color=YELLOW)
        final_text.add_background_rectangle()
        final_text.move_to(ORIGIN)
        
        self.play(Write(final_text))
        self.wait(2)

    # --- Geometry Helpers ---

    def create_cluster_group(self, anchor_q, anchor_r):
        cluster_group = VGroup()
        
        for dq, dr, color, label in self.cluster_offsets:
            q = anchor_q + dq
            r = anchor_r + dr
            pos = self.hex_to_pixel(q, r)
            
            # Apply the correction offset so the whole grid is centered
            pos += self.centering_offset
            
            hex_obj = self.create_hex(pos, color, label)
            cluster_group.add(hex_obj)
            
        return cluster_group

    def create_hex(self, pos, color, label):
        hex_shape = RegularPolygon(n=6, radius=self.R_SMALL, color=color, fill_opacity=0.4, stroke_width=self.STROKE_WIDTH)
        hex_shape.rotate(PI/2) 
        hex_shape.move_to(pos)
        text = Text(label, font_size=16, weight=BOLD).move_to(pos)
        return VGroup(hex_shape, text)

    def hex_to_pixel(self, q, r):
        x = self.R_SMALL * np.sqrt(3) * (q + r/2)
        y = self.R_SMALL * 3/2 * r
        return np.array([x, y, 0])