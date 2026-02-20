from manim import *
import numpy as np
import random

class Part1_Cellular_Evolution_3D(ThreeDScene):
    def construct(self):
        # Main title
        title = Text("Lecture 6: Interference and Orthogonality", font_size=40)
        subtitle = Text("From Single Cell to Cellular System", font_size=32, color=BLUE)
        subtitle.next_to(title, DOWN)
        
        self.add_fixed_in_frame_mobjects(title, subtitle)
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
        self.set_camera_orientation(phi=0, theta=-90*DEGREES)
        
        # Title
        gen_title = Text("1G Mobile Communication System", font_size=36, color=GREEN)
        gen_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(gen_title)
        self.play(Write(gen_title))
        self.wait(0.5)
        
        # Spectrum allocation
        spectrum_info = VGroup(
            Text("Available Uplink Spectrum", font_size=28, color=YELLOW),
            Text("Bandwidth: 25 MHz", font_size=32, color=BLUE, weight=BOLD)
        ).arrange(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(spectrum_info)
        self.play(Write(spectrum_info))
        self.wait(1)
        
        # Visual spectrum bar
        spectrum_bar = Rectangle(width=10, height=1, color=BLUE, fill_opacity=0.3, stroke_width=3)
        spectrum_bar.shift(DOWN * 1)
        
        bandwidth_label = Text("25 MHz", font_size=24, color=BLUE)
        bandwidth_label.next_to(spectrum_bar, DOWN, buff=0.2)
        
        self.add_fixed_in_frame_mobjects(spectrum_bar, bandwidth_label)
        self.play(Create(spectrum_bar), Write(bandwidth_label))
        self.wait(1.5)
        
        # Clear
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def voice_frequency_analysis(self):
        """Explain voice frequency requirements"""
        
        # Title
        voice_title = Text("Human Voice Spectrum Analysis", font_size=36, color=ORANGE)
        voice_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(voice_title)
        self.play(Write(voice_title))
        
        # Voice info
        voice_info = VGroup(
            Text("Intelligence-carrying speech harmonics", font_size=24, color=YELLOW),
            Text("Clear communication range:", font_size=22, color=WHITE),
            Text("300 Hz - 3,400 Hz", font_size=28, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.3)
        voice_info.shift(UP * 1)
        self.add_fixed_in_frame_mobjects(voice_info)
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
        
        self.add_fixed_in_frame_mobjects(axes, x_label, voice_range, range_label)
        self.play(Create(axes), Write(x_label))
        self.play(Create(voice_range), Write(range_label))
        self.wait(1)
        
        # Guard bands and overhead
        overhead = Text("+ Guard bands & overhead ≈ 10× factor", font_size=24, color=ORANGE)
        overhead.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(overhead)
        self.play(Write(overhead))
        self.wait(1)
        
        # Channel bandwidth calculation
        calc = VGroup(
            Text("Channel Bandwidth Required:", font_size=24, color=YELLOW),
            Text("≈ 30 kHz per user", font_size=28, color=BLUE, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        calc.to_edge(DOWN, buff=1.5)
        
        self.add_fixed_in_frame_mobjects(calc)
        self.play(FadeOut(overhead), Write(calc))
        self.wait(2)
        
        # Clear
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def single_hexagonal_cell(self):
        """Show single hexagonal cell with tower and capacity calculation"""
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)
        
        # Title
        title = Text("Single Cell System", font_size=36, color=GREEN)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # Create 3D hexagonal cell
        hexagon = self.create_3d_hexagon(radius=3, height=0.1, color=BLUE)
        
        self.play(Create(hexagon))
        self.wait(0.5)
        
        # Add tower in center
        tower = self.create_3d_tower()
        tower.shift(UP * 0.5)
        
        self.play(FadeIn(tower))
        self.wait(0.5)
        
        # Coverage dome
        coverage = Surface(
            lambda u, v: np.array([
                2.8 * np.sin(u) * np.cos(v),
                2.8 * np.sin(u) * np.sin(v),
                2 * np.cos(u)
            ]),
            u_range=[0, PI/2],
            v_range=[0, 2*PI],
            resolution=(20, 32),
            fill_color=BLUE,
            fill_opacity=0.15,
            stroke_color=BLUE,
            stroke_width=1
        )
        coverage.shift(UP * 0.5)
        
        self.play(Create(coverage))
        
        # Why hexagon note
        why_hex = Text("* Why hexagonal? Explained later in this lecture", 
                      font_size=18, color=YELLOW, slant=ITALIC)
        why_hex.to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(why_hex)
        self.play(Write(why_hex))
        self.wait(1)
        
        # Add user dots scattered in the cell
        user_dots = VGroup()
        num_users = 20  # Show sample of users
        
        for i in range(num_users):
            # Random position within hexagon (approximation using circle)
            angle = random.uniform(0, 2*PI)
            radius = random.uniform(0.3, 2.5)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            user = self.create_user_dot(color=BLUE)
            user.move_to([x, y, 0])
            user_dots.add(user)
        
        self.play(LaggedStart(*[FadeIn(dot) for dot in user_dots], lag_ratio=0.05))
        self.wait(0.5)
        
        # Rotate to show 3D
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        
        # Capacity calculation
        self.move_camera(phi=0, theta=-90*DEGREES)
        
        calc_box = VGroup(
            Text("Capacity Calculation:", font_size=28, color=YELLOW),
            MathTex(r"\text{Total Channels} = \frac{\text{Total BW}}{\text{Channel BW}}", font_size=24),
            MathTex(r"= \frac{25 \text{ MHz}}{30 \text{ kHz}}", font_size=24),
            MathTex(r"= \frac{25000 \text{ kHz}}{30 \text{ kHz}}", font_size=24),
            MathTex(r"= 833 \approx 832 \text{ users}", font_size=28, color=GREEN)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        calc_box.to_edge(RIGHT, buff=0.5).shift(UP * 0.5)
        
        self.add_fixed_in_frame_mobjects(calc_box)
        self.play(Write(calc_box), run_time=3)
        self.wait(2)
        
        # Result
        result = Text("832 users in ONE cell", font_size=32, color=GREEN, weight=BOLD)
        result.to_edge(DOWN, buff=1.5)
        
        self.add_fixed_in_frame_mobjects(result)
        self.play(Write(result))
        self.wait(2)
        
        # Clear
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def seven_cell_cluster(self):
        """Show breaking single cell into 7 cells with frequency allocation"""
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)
        
        # Title
        title = Text("Breaking Into 7 Smaller Cells", font_size=36, color=ORANGE)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # Create 7-cell cluster
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK]
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        
        # Center positions for 7 hexagons
        positions = [
            [0, 0, 0],  # Center - A
            [1.5, 0.866, 0],  # B
            [1.5, -0.866, 0],  # C
            [0, -1.732, 0],  # D
            [-1.5, -0.866, 0],  # E
            [-1.5, 0.866, 0],  # F
            [0, 1.732, 0]  # G
        ]
        
        cells = VGroup()
        towers = VGroup()
        cell_labels = VGroup()
        
        for i, (pos, color, label) in enumerate(zip(positions, colors, labels)):
            # Hexagon
            hex_cell = self.create_3d_hexagon(radius=1, height=0.05, color=color)
            hex_cell.move_to(pos)
            cells.add(hex_cell)
            
            # Tower
            tower = self.create_3d_tower(color=color)
            tower.scale(0.6)
            tower.move_to(pos)
            tower.shift(UP * 0.3)
            towers.add(tower)
            
            # Label
            text_label = Text(label, font_size=36, color=color, weight=BOLD)
            text_label.move_to(pos)
            text_label.shift(UP * 1.2)
            cell_labels.add(text_label)
        
        # Animate cells appearing
        self.play(LaggedStart(*[Create(cell) for cell in cells], lag_ratio=0.15))
        self.play(LaggedStart(*[FadeIn(tower) for tower in towers], lag_ratio=0.15))
        self.play(LaggedStart(*[Write(label) for label in cell_labels], lag_ratio=0.1))
        
        # Add user dots to each cell
        all_user_dots = VGroup()
        for i, pos in enumerate(positions):
            # Add ~10 users per cell
            for j in range(10):
                angle = random.uniform(0, 2*PI)
                radius = random.uniform(0.2, 0.8)
                x = pos[0] + radius * np.cos(angle)
                y = pos[1] + radius * np.sin(angle)
                
                user = self.create_user_dot(color=colors[i])
                user.move_to([x, y, 0])
                all_user_dots.add(user)
        
        self.play(LaggedStart(*[FadeIn(dot) for dot in all_user_dots], lag_ratio=0.02))
        self.wait(0.5)
        
        # Rotate view
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        
        # Frequency allocation explanation
        self.move_camera(phi=0, theta=-90*DEGREES)
        
        freq_info = VGroup(
            Text("Frequency Allocation Strategy:", font_size=26, color=YELLOW),
            Text("• 832 channels ÷ 7 cells = 119 channels/cell", font_size=20),
            Text("• Each cell gets different frequencies", font_size=20),
            Text("• Neighboring cells: NO overlap!", font_size=20, color=RED)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        freq_info.to_edge(RIGHT, buff=0.3).shift(UP * 1)
        
        self.add_fixed_in_frame_mobjects(freq_info)
        self.play(Write(freq_info), run_time=2)
        self.wait(2)
        
        # Total capacity still same
        capacity_note = VGroup(
            Text("Total System Capacity:", font_size=28, color=GREEN),
            Text("7 cells × 119 ≈ 833 users", font_size=24),
            Text("Same as before!", font_size=26, color=BLUE, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        capacity_note.to_edge(DOWN, buff=0.5)
        
        self.add_fixed_in_frame_mobjects(capacity_note)
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
                   if mob not in [self.seven_cells, self.seven_towers, self.seven_labels]])
        
        # New title
        title = Text("Frequency Reuse Concept", font_size=36, color=GOLD)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # Highlight cell A
        self.play(
            self.seven_cells[0].animate.set_fill(RED, opacity=0.5),
            self.seven_labels[0].animate.scale(1.5).set_color(RED)
        )
        self.wait(1)
        
        # Key insight
        insight = VGroup(
            Text("Key Insight:", font_size=28, color=YELLOW),
            Text("Frequency 'A' can be REUSED", font_size=24),
            Text("in another cluster far away!", font_size=24),
            Text("With minimal interference", font_size=22, color=GREEN)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        insight.to_edge(RIGHT, buff=0.5).shift(UP * 0.5)
        
        self.add_fixed_in_frame_mobjects(insight)
        self.play(Write(insight))
        self.wait(2)
        
        # Clear for scaling
        self.play(*[FadeOut(mob) for mob in self.mobjects 
                   if mob not in [self.seven_cells, self.seven_towers, self.seven_labels]])
    
    def scaling_multiple_clusters(self):
        """Show multiple 7-cell clusters demonstrating frequency reuse"""
        
        # Title
        title = Text("Scaling: Multiple Clusters", font_size=36, color=GREEN)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # Shift current cluster to left
        self.play(
            self.seven_cells.animate.shift(LEFT * 4),
            self.seven_towers.animate.shift(LEFT * 4),
            self.seven_labels.animate.shift(LEFT * 4)
        )
        
        # Create second cluster (center)
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK]
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        
        positions = [
            [0, 0, 0],
            [1.5, 0.866, 0],
            [1.5, -0.866, 0],
            [0, -1.732, 0],
            [-1.5, -0.866, 0],
            [-1.5, 0.866, 0],
            [0, 1.732, 0]
        ]
        
        cluster2_cells = VGroup()
        cluster2_towers = VGroup()
        cluster2_labels = VGroup()
        
        for i, (pos, color, label) in enumerate(zip(positions, colors, labels)):
            hex_cell = self.create_3d_hexagon(radius=1, height=0.05, color=color)
            hex_cell.move_to(pos)
            cluster2_cells.add(hex_cell)
            
            tower = self.create_3d_tower(color=color)
            tower.scale(0.6)
            tower.move_to(pos)
            tower.shift(UP * 0.3)
            cluster2_towers.add(tower)
            
            text_label = Text(label, font_size=36, color=color, weight=BOLD)
            text_label.move_to(pos)
            text_label.shift(UP * 1.2)
            cluster2_labels.add(text_label)
        
        self.play(
            LaggedStart(*[Create(cell) for cell in cluster2_cells], lag_ratio=0.1),
            LaggedStart(*[FadeIn(tower) for tower in cluster2_towers], lag_ratio=0.1),
            LaggedStart(*[Write(label) for label in cluster2_labels], lag_ratio=0.1)
        )
        
        # Add user dots to cluster 2
        cluster2_users = VGroup()
        for i, pos in enumerate(positions):
            for j in range(8):
                angle = random.uniform(0, 2*PI)
                radius = random.uniform(0.2, 0.8)
                x = pos[0] + radius * np.cos(angle)
                y = pos[1] + radius * np.sin(angle)
                
                user = self.create_user_dot(color=colors[i])
                user.move_to([x, y, 0])
                cluster2_users.add(user)
        
        self.play(LaggedStart(*[FadeIn(dot) for dot in cluster2_users], lag_ratio=0.02))
        self.wait(1)
        
        # Create third cluster (right)
        cluster3_cells = VGroup()
        cluster3_towers = VGroup()
        cluster3_labels = VGroup()
        
        for i, (pos, color, label) in enumerate(zip(positions, colors, labels)):
            hex_cell = self.create_3d_hexagon(radius=1, height=0.05, color=color)
            hex_cell.move_to([pos[0] + 4, pos[1], pos[2]])
            cluster3_cells.add(hex_cell)
            
            tower = self.create_3d_tower(color=color)
            tower.scale(0.6)
            tower.move_to([pos[0] + 4, pos[1], pos[2]])
            tower.shift(UP * 0.3)
            cluster3_towers.add(tower)
            
            text_label = Text(label, font_size=36, color=color, weight=BOLD)
            text_label.move_to([pos[0] + 4, pos[1], pos[2]])
            text_label.shift(UP * 1.2)
            cluster3_labels.add(text_label)
        
        self.play(
            LaggedStart(*[Create(cell) for cell in cluster3_cells], lag_ratio=0.1),
            LaggedStart(*[FadeIn(tower) for tower in cluster3_towers], lag_ratio=0.1),
            LaggedStart(*[Write(label) for label in cluster3_labels], lag_ratio=0.1)
        )
        
        # Add user dots to cluster 3
        cluster3_users = VGroup()
        for i, pos in enumerate(positions):
            for j in range(8):
                angle = random.uniform(0, 2*PI)
                radius = random.uniform(0.2, 0.8)
                x = pos[0] + 4 + radius * np.cos(angle)
                y = pos[1] + radius * np.sin(angle)
                
                user = self.create_user_dot(color=colors[i])
                user.move_to([x, y, 0])
                cluster3_users.add(user)
        
        self.play(LaggedStart(*[FadeIn(dot) for dot in cluster3_users], lag_ratio=0.02))
        self.wait(1)
        
        # Highlight all 'A' cells
        a_cells = VGroup(
            self.seven_cells[0],
            cluster2_cells[0],
            cluster3_cells[0]
        )
        
        a_labels = VGroup(
            self.seven_labels[0],
            cluster2_labels[0],
            cluster3_labels[0]
        )
        
        # Zoom and highlight
        self.play(
            *[cell.animate.set_fill(RED, opacity=0.6) for cell in a_cells],
            *[label.animate.scale(1.3).set_color(GOLD) for label in a_labels]
        )
        self.wait(1)
        
        # Draw distance indicators
        line1 = DashedLine(
            self.seven_cells[0].get_center(),
            cluster2_cells[0].get_center(),
            color=YELLOW,
            stroke_width=4
        )
        
        line2 = DashedLine(
            cluster2_cells[0].get_center(),
            cluster3_cells[0].get_center(),
            color=YELLOW,
            stroke_width=4
        )
        
        self.play(Create(line1), Create(line2))
        
        # Distance labels
        dist_label = Text("Sufficient Distance → Minimal Interference", 
                         font_size=26, color=GREEN, weight=BOLD)
        dist_label.to_edge(DOWN, buff=0.5)
        
        self.add_fixed_in_frame_mobjects(dist_label)
        self.play(Write(dist_label))
        self.wait(2)
        
        # Rotate to see full view
        self.move_camera(phi=65*DEGREES, theta=-50*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        
        # Final message
        self.move_camera(phi=0, theta=-90*DEGREES)
        
        final = VGroup(
            Text("Frequency Reuse Pattern:", font_size=32, color=YELLOW),
            Text("✓ Same frequencies in distant cells", font_size=24, color=GREEN),
            Text("✓ Maximizes spectrum efficiency", font_size=24, color=GREEN),
            Text("✓ Enables UNLIMITED scaling!", font_size=26, color=BLUE, weight=BOLD)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.add_fixed_in_frame_mobjects(final)
        self.play(Write(final))
        self.wait(3)
        
        # End
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        end_text = Text("Continue to Part 2: Orthogonal Access Methods", 
                       font_size=32, color=GREEN)
        self.add_fixed_in_frame_mobjects(end_text)
        self.play(Write(end_text))
        self.wait(2)
    
    # Helper functions
    def create_3d_hexagon(self, radius=1, height=0.1, color=BLUE):
        """Create a 3D hexagonal prism"""
        vertices = []
        for i in range(6):
            angle = i * PI / 3
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            vertices.append([x, y, 0])
        
        # Create hexagon using lines
        hexagon = VGroup()
        for i in range(6):
            start = vertices[i]
            end = vertices[(i + 1) % 6]
            line = Line3D(start=start, end=end, color=color, stroke_width=3)
            hexagon.add(line)
        
        # Add fill using polygon
        hex_fill = Polygon(*vertices, color=color, fill_opacity=0.3, stroke_width=0)
        hexagon.add(hex_fill)
        
        return hexagon
    
    def create_3d_tower(self, color=GOLD):
        """Create a tower using SVG"""
        # Load SVG and convert to 3D
        tower_svg = SVGMobject("assets/tower.svg")
        tower_svg.set_color(color)
        tower_svg.scale(0.5)
        
        # Make it face the camera by rotating
        tower_svg.rotate(PI/2, axis=RIGHT)
        tower_svg.shift(UP * 0.5)
        
        return tower_svg
    
    def create_user_dot(self, color=BLUE):
        """Create a dot to represent a user"""
        dot = Dot3D(point=ORIGIN, radius=0.08, color=color)
        return dot