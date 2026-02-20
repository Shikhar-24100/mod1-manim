from manim import *
import numpy as np
import random

class Part1_Cellular_Evolution_2D(Scene):
    def construct(self):
        # Main title
        title = Text("Lecture 6: Interference and Orthogonality", font_size=40)
        subtitle = Text("From Single Cell to Cellular System", font_size=32, color=BLUE)
        subtitle.next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Scene 1: 1G System Introduction
        self.first_generation_intro()
        
        # Scene 2: Voice frequency requirements
        self.voice_frequency_analysis()
        
        # Scene 3: Single hexagonal cell with capacity calculation
        self.single_hexagonal_cell()
        
        # Scene 4: Breaking into 7 cells
        self.seven_cell_cluster()
        
        # Scene 5: Frequency reuse demonstration
        self.frequency_reuse_concept()
        
        # Scene 6: Scaling - multiple clusters
        self.scaling_multiple_clusters()
        
        self.wait(2)

    def first_generation_intro(self):
        """Introduce 1G communication system"""
        # Title
        gen_title = Text("1G Mobile Communication System", font_size=36, color=WHITE)
        gen_title.to_edge(UP)
        self.play(Write(gen_title))
        self.wait(0.5)

        # Spectrum allocation
        spectrum_info = VGroup(
            Text("Available Uplink Spectrum", font_size=28, color=YELLOW),
            Text("Bandwidth: 25 MHz", font_size=32, color=BLUE, weight=BOLD)
        ).arrange(DOWN, buff=0.3)
        self.play(Write(spectrum_info))
        self.wait(1)

        # Visual spectrum bar
        spectrum_bar = Rectangle(width=10, height=1, color=BLUE, fill_opacity=0.3, stroke_width=3)
        spectrum_bar.shift(DOWN * 2)
        # bandwidth_label = Text("25 MHz", font_size=24, color=BLUE)
        # bandwidth_label.next_to(spectrum_bar, DOWN, buff=0.2)
        
        self.play(Create(spectrum_bar))
        self.wait(1.5)

        # Clear
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def voice_frequency_analysis(self):
        """Explain voice frequency requirements"""
        # Title
        voice_title = Text("Human Voice Spectrum Analysis", font_size=36, color=WHITE)
        voice_title.to_edge(UP)
        self.play(Write(voice_title))

        # Voice info
        voice_info = VGroup(
            Text("Intelligence-carrying speech harmonics", font_size=24, color=YELLOW),
            Text("Clear communication range:", font_size=22, color=WHITE),
            Text("300 Hz - 3,400 Hz", font_size=28, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.3)
        voice_info.shift(UP * 1)
        self.play(Write(voice_info))
        self.wait(1)

        # Frequency spectrum visualization
        axes = Axes(
            x_range=[0, 4000, 500],
            y_range=[0, 1.2, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"color": BLUE},
            tips=False
        )
        axes.shift(DOWN * 1.5)
        x_label = Text("Frequency (Hz)", font_size=20)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)

        # Voice range box
        voice_range = Rectangle(
            width=axes.x_axis.get_length() * (3100/4000),
            height=2,
            color=GREEN,
            fill_opacity=0.3,
            stroke_width=2
        )
        voice_range.move_to(axes.c2p(1850, 0.5))
        range_label = Text("Voice Range", font_size=18, color=GREEN)
        range_label.next_to(voice_range, UP, buff=0.1)

        self.play(Create(axes), Write(x_label))
        self.play(Create(voice_range), Write(range_label))
        self.wait(1)

        # Guard bands and overhead
        overhead = Text("(+ Guard bands & overhead ≈ 10× factor)", font_size=24, color=GREEN)
        overhead.next_to(voice_title, DOWN, buff=0.5)
        self.play(Write(overhead))
        self.wait(2)

        # self.play(FadeOut(overhead))

        # Channel bandwidth calculation
        calc = VGroup(
            Text("Channel Bandwidth Required:", font_size=24, color=YELLOW),
            Text("≈ 30 kHz per user", font_size=28, color=BLUE, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        calc.to_edge(DOWN, buff=1.5)
        self.play(FadeOut(overhead), Write(calc))
        self.wait(2)

        # Clear
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def single_hexagonal_cell(self):
        """Show single hexagonal cell with tower and capacity calculation"""
        # Title
        title = Text("Single Cell with high power transmitter", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))

        # Create hexagonal cell
        hexagon = self.create_hexagon(radius=2.5, color=BLUE)
        hexagon.shift(LEFT * 3)
        self.play(Create(hexagon))
        self.wait(0.5)

        # Add tower in center
        tower = SVGMobject("assets/tower.svg").scale(0.35)
        tower.move_to(hexagon.get_center())
        self.play(FadeIn(tower))
        self.wait(0.5)

        # Coverage circle
        # coverage = Circle(radius=2.3, color=BLUE, stroke_width=2, stroke_opacity=0.5)
        # coverage.set_fill(BLUE, opacity=0.1)
        # coverage.move_to(hexagon.get_center())
        # self.play(Create(coverage))

        # Why hexagon note
        why_hex = Text("* Why hexagonal? Explained later in this lecture", 
                       font_size=18, color=YELLOW, slant=ITALIC)
        why_hex.to_edge(DOWN, buff=0.3)
        self.play(Write(why_hex))
        self.wait(1)

        # Add user dots scattered in the cell
        user_dots = VGroup()
        num_users = 20
        for i in range(num_users):
            angle = random.uniform(0, 2*PI)
            radius = random.uniform(0.3, 2.0)
            x = hexagon.get_center()[0] + radius * np.cos(angle)
            y = hexagon.get_center()[1] + radius * np.sin(angle)
            user = Dot(point=[x, y, 0], radius=0.05, color=YELLOW)
            user_dots.add(user)

        self.play(LaggedStart(*[FadeIn(dot) for dot in user_dots], lag_ratio=0.05))
        self.wait(0.5)

        # Capacity calculation
        calc_box = VGroup(
            Text("Capacity Calculation:", font_size=28, color=YELLOW),
            MathTex(r"\text{Total Channels} = \frac{\text{Total BW}}{\text{Channel BW}}", font_size=24),
            MathTex(r"= \frac{25 \text{ MHz}}{30 \text{ kHz}}", font_size=24),
            MathTex(r"= \frac{25000 \text{ kHz}}{30 \text{ kHz}}", font_size=24),
            MathTex(r"= 833 \approx 832 \text{ users}", font_size=28, color=GREEN)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        calc_box.to_edge(RIGHT, buff=0.5).shift(UP * 0.5 + LEFT*2)
        
        self.play(Write(calc_box), run_time=3)
        self.wait(2)

        # Result
        result = Text("832 users in ONE cell", font_size=32, color=GREEN, weight=BOLD)
        result.next_to(why_hex, UP, buff=0.5)
        self.play(Write(result))
        self.wait(2)

        # Clear
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def seven_cell_cluster(self):
        """Show breaking single cell into 7 cells with frequency allocation"""
        # Title
        title = Text("7 Smaller Cells will less power transmitters", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))

        # Create 7-cell cluster
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK]
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        
        # Center positions for 7 hexagons (scaled for 2D)
        hex_radius = 1.0
        positions = [
            [0, 0],  # Center - A
            [1.5*hex_radius, 0.866*hex_radius],  # B
            [1.5*hex_radius, -0.866*hex_radius],  # C
            [0, -1.732*hex_radius],  # D
            [-1.5*hex_radius, -0.866*hex_radius],  # E
            [-1.5*hex_radius, 0.866*hex_radius],  # F
            [0, 1.732*hex_radius]  # G
        ]

        cells = VGroup()
        towers = VGroup()
        cell_labels = VGroup()

        for i, (pos, color, label) in enumerate(zip(positions, colors, labels)):
            # Hexagon
            hex_cell = self.create_hexagon(radius=hex_radius, color=color)
            hex_cell.move_to([pos[0]-1.5, pos[1], 0])
            cells.add(hex_cell)

            # Tower
            # tower = self.create_tower(color=color)
            # tower.scale(0.4)
            # tower.move_to([pos[0], pos[1], 0])
            # towers.add(tower)

            # Label
            text_label = Text(label, font_size=36, color=color, weight=BOLD)
            text_label.move_to([pos[0]-1.5, pos[1], 0])
            cell_labels.add(text_label)

        # Animate cells appearing
        self.play(LaggedStart(*[Create(cell) for cell in cells], lag_ratio=0.15))
        # self.play(LaggedStart(*[FadeIn(tower) for tower in towers], lag_ratio=0.15))
        self.play(LaggedStart(*[Write(label) for label in cell_labels], lag_ratio=0.1))
        self.wait(2)
        # Add user dots to each cell
        # all_user_dots = VGroup()
        # for i, pos in enumerate(positions):
        #     for j in range(10):
        #         angle = random.uniform(0, 2*PI)
        #         radius = random.uniform(0.2, 0.7)
        #         x = pos[0] + radius * np.cos(angle)
        #         y = pos[1] + radius * np.sin(angle)
        #         user = Dot(point=[x, y, 0], radius=0.04, color=colors[i])
        #         all_user_dots.add(user)

        # self.play(LaggedStart(*[FadeIn(dot) for dot in all_user_dots], lag_ratio=0.02))
        self.wait(0.5)

        # Frequency allocation explanation
        freq_info = VGroup(
            Text("Frequency Allocation Strategy:", font_size=26, color=YELLOW),
            Text("• 832 channels ÷ 7 cells = 119 channels/cell", font_size=20),
            Text("• Each cell gets different frequencies", font_size=20),
            Text("• Neighboring cells: NO overlap!", font_size=20, color=RED)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        freq_info.to_edge(RIGHT, buff=0.3).shift(UP * 1)
        
        self.play(Write(freq_info), run_time=2)
        self.wait(2)

        # Total capacity still same
        capacity_note = VGroup(
            Text("Total System Capacity:", font_size=28, color=GREEN),
            Text("7 cells × 119 ≈ 833 users", font_size=24),
            Text("Same as before!", font_size=26, color=BLUE, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        capacity_note.next_to(freq_info, DOWN, buff=1.0)
        
        self.play(Write(capacity_note))
        self.wait(2)

        # Store for next scene
        self.seven_cells = cells
        self.seven_towers = towers
        self.seven_labels = cell_labels

    def frequency_reuse_concept(self):
        """Explain frequency reuse concept"""
        # Clear previous notes
        self.play(*[FadeOut(mob) for mob in self.mobjects 
                   if mob not in [self.seven_cells, self.seven_towers, 
                                 self.seven_labels]])

        # New title
        title = Text("Frequency Reuse Concept", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))

        # Highlight cell A
        self.play(
            self.seven_cells[0].animate.set_fill(RED, opacity=0.5),
            self.seven_labels[0].animate.scale(1.5).set_color(RED)
        )
        self.wait(3)

        # Key insight
        insight = VGroup(
            Text("Key Insight:", font_size=28, color=YELLOW),
            Text("Frequency 'A' can be REUSED", font_size=24),
            Text("in another cluster far away!", font_size=24),
            Text("With minimal interference", font_size=22, color=GREEN)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        insight.to_edge(RIGHT, buff=0.5).shift(UP * 0.5)
        
        self.play(Write(insight))
        self.wait(2)

        # Clear for scaling
        self.play(*[FadeOut(mob) for mob in self.mobjects 
                   if mob not in [self.seven_cells, self.seven_towers, 
                                 self.seven_labels]])

    def scaling_multiple_clusters(self):
        """Show multiple 7-cell clusters tessellating perfectly"""
        
        # 1. Setup & Title
        title = Text("Scaling: Frequency Reuse", font_size=36, color=WHITE).to_edge(UP)
        self.play(FadeIn(title))

        # 2. Geometry Constants
        R = 0.6  # Radius of a single hexagon
        
        # Shift vector for tessellation
        # This vector calculates the position of the next cluster center relative to the previous one
        cluster_shift_vector = np.array([4.5 * R, np.sqrt(3)/2 * R, 0])

        # 3. Define the Relative Centers (Center, Left, Right)
        # We define them relative to (0,0,0) first, then shift the whole group later.
        center_mid = ORIGIN
        center_left = -1 * cluster_shift_vector
        center_right = cluster_shift_vector
        
        cluster_centers = [center_left, center_mid, center_right]

        # 4. Define Hexagon Offsets for a single cluster
        # Angles: Center (0), then 30, 90, 150, 210, 270, 330
        hex_offsets = [ORIGIN] 
        for i in range(6):
            angle_deg = 30 + (60 * i)
            rad = angle_deg * DEGREES
            dist = np.sqrt(3) * R
            hex_offsets.append(np.array([dist * np.cos(rad), dist * np.sin(rad), 0]))

        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK]
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

        all_clusters_groups = [] 

        # 5. Create the Objects (At Origin)
        for center_pos in cluster_centers:
            c_cells = VGroup()
            c_towers = VGroup()
            c_labels = VGroup()
            # c_users = VGroup()

            for i, (offset, color, label) in enumerate(zip(hex_offsets, colors, labels)):
                # Calculate absolute position relative to the cluster center
                abs_pos = center_pos + offset
                
                # A. Hexagon
                # Note: Using self.create_hexagon if available, else standard Polygon
                try:
                    hex_cell = self.create_hexagon(radius=R, color=color) # Your helper function
                except:
                    hex_cell = RegularPolygon(n=6, color=WHITE, fill_color=color, fill_opacity=0.3).scale(R)
                
                hex_cell.move_to(abs_pos)
                c_cells.add(hex_cell)

                # B. Tower (Uncommented and fixed)
                try:
                    # Assuming you have a tower creation method or SVG
                    tower = SVGMobject("assets/tower.svg").set_color(GRAY).scale(0.4)
                except:
                    tower = Triangle(color=GRAY).scale(0.2) # Fallback
                
                tower.move_to(abs_pos)
                c_towers.add(tower)

                # C. Label
                text_label = Text(label, font_size=20, color=WHITE, weight=BOLD)
                text_label.add_background_rectangle(color=BLACK, opacity=0.2, buff=0.05)
                text_label.move_to(abs_pos + UP*0.3) # Slightly above center
                c_labels.add(text_label)

                # D. Users (Uncommented and fixed)
                # for _ in range(3): 
                #     angle = random.uniform(0, 2*PI)
                #     u_rad = random.uniform(0.1, 0.4 * R) 
                #     u_x = abs_pos[0] + u_rad * np.cos(angle)
                #     u_y = abs_pos[1] + u_rad * np.sin(angle)
                #     user = Dot(point=[u_x, u_y, 0], radius=0.04, color=color)
                #     c_users.add(user)

            # Combine into one cluster group
            cluster_obj = VGroup(c_cells, c_towers, c_labels)
            all_clusters_groups.append(cluster_obj)

        # ---------------------------------------------------------
        # GLOBAL SHIFT FIX
        # ---------------------------------------------------------
        # Combine all clusters into one massive group
        whole_system = VGroup(*all_clusters_groups)
        
        # Center vertically, then shift LEFT by 1.5 (or 1.15) as requested
        whole_system.move_to(ORIGIN).shift(LEFT * 1.5)

        # ---------------------------------------------------------
        # ANIMATION SEQUENCE
        # ---------------------------------------------------------
        
        # 1. Animate Appearance
        # Extract sub-groups from the shifted system for ordered animation
        total_cells = VGroup(*[g[0] for g in all_clusters_groups])
        total_towers = VGroup(*[g[1] for g in all_clusters_groups])
        total_labels = VGroup(*[g[2] for g in all_clusters_groups])
        # total_users = VGroup(*[g[3] for g in all_clusters_groups])

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP*0.5) for c in total_cells], lag_ratio=0.02),
            run_time=2
        )
        self.play(FadeIn(total_towers), Write(total_labels))
        # self.play(FadeIn(total_users, lag_ratio=0.01))

        # 2. Highlight "A" Cells
        # Access the shifted objects directly
        cells_A = VGroup(
            all_clusters_groups[0][0][0], # Cluster 1 -> Cells -> Index 0
            all_clusters_groups[1][0][0], # Cluster 2 -> Cells -> Index 0
            all_clusters_groups[2][0][0]  # Cluster 3 -> Cells -> Index 0
        )

        self.play(
            *[c.animate.set_fill(color=RED, opacity=0.8).set_stroke(width=4, color=YELLOW) for c in cells_A],
            run_time=1.5
        )

        # 3. Distance Indicator
        # Get centers of the "A" cells (Index 0 is Center "A")
        center_A_left = all_clusters_groups[0][0][0].get_center()
        center_A_mid  = all_clusters_groups[1][0][0].get_center()

        arrow_reuse = DoubleArrow(
            start=center_A_left, end=center_A_mid, color=WHITE, buff=0.1, tip_length=0.2
        )
        
        self.play(Create(arrow_reuse))

        # 4. Explanation Text (Positioned relative to the shifted arrow)
        explanation = Text("Sufficient distance = No Interference", font_size=24, color=WHITE)
        explanation.next_to(arrow_reuse, DOWN, buff=0.2) # Close to arrow
        explanation.shift(DOWN * 1.5) # Shift left to avoid overlap with arrow
        
        # 5. Math / Capacity Note
        capacity_note2 = VGroup(
            Text("Total System Capacity:", font_size=24),
            Text("7 cells × 119 users × 3 clusters", font_size=24),
            Text("≈ 2500 users (Increased 3x!)", font_size=26, color=BLUE, weight=BOLD)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        # Position the text in the empty space on the right
        # Since we shifted clusters LEFT, we have space on RIGHT.
        capacity_note2.to_edge(RIGHT, buff=1.0).shift(DOWN * 1)
        capacity_note2.shift(DOWN*0.9)

        self.play(Write(explanation))
        self.play(Write(capacity_note2))
        
        self.wait(7)
        title1 = Text("N- cell Frequency Reuse", font_size=36, color=WHITE).to_edge(UP)
        self.play(Transform(title, title1))
        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # Helper functions
    def create_hexagon(self, radius=1, color=BLUE):
        """Create a hexagon"""
        vertices = []
        for i in range(6):
            angle = i * PI / 3
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            vertices.append([x, y, 0])
        
        hexagon = Polygon(*vertices, color=color, fill_opacity=0.3, stroke_width=3)
        return hexagon

    def create_tower(self, color=GOLD):
        """Create a simple tower representation"""
        # Triangle on top of rectangle
        base = Rectangle(height=0.4, width=0.15, color=color, fill_opacity=1)
        top = Triangle(color=color, fill_opacity=1).scale(0.2)
        top.next_to(base, UP, buff=0)
        
        tower = VGroup(base, top)
        return tower