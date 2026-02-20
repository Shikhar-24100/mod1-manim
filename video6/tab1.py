from manim import *
import numpy as np
import random

class Scene3_MultiUserReality(Scene):
    def construct(self):
        # Sub-scenes
        self.transition_single_to_multiple()
        self.wait(0.5)
        self.scenario_cellular_network()
        self.wait(0.5)
        self.scenario_dense_urban()
        self.wait(0.5)
        self.fundamental_problem_statement()
        self.wait(0.5)
        # self.scaling_problem_visualization()
        # self.wait(1)



    def transition_single_to_multiple(self):
    # """
    # Animation: Single user duplicates into multiple users
    # Duration: ~20 seconds
    # """
    
    # ============================================
    # STEP 1: Initial Single Link (3:25 - 3:30)
    # ============================================
    
    # Load SVGs (replace with your actual SVG paths)
        tower = SVGMobject("assets/tower.svg").scale(0.8)
        tower.move_to(ORIGIN)
        
        phone_original = SVGMobject("assets/mobile.svg").scale(0.4)
        phone_original.move_to(RIGHT * 3)
        
        # Connection line
        connection = DashedLine(
            tower.get_right(), 
            phone_original.get_left(),
            color=BLUE,
            dash_length=0.1
        )
        
        # Signal indicator on phone
        signal_icon = Triangle(color=GREEN, fill_opacity=0.8).scale(0.15)
        signal_icon.next_to(phone_original, UP, buff=0.1)
        
        # Animate initial setup
        self.play(
            FadeIn(tower, shift=DOWN * 0.5),
            FadeIn(phone_original, shift=UP * 0.5),
            run_time=1
        )
        self.play(Create(connection), run_time=0.8)
        self.play(FadeIn(signal_icon, scale=0.5), run_time=0.5)
        
        # Label
        label_single = Text("Single User - Dedicated Channel", 
                            font_size=24, color=WHITE)
        label_single.to_edge(UP)
        self.play(Write(label_single), run_time=1)
        self.wait(0.5)
        
        # ============================================
        # STEP 2: Start User Duplication (3:30 - 3:40)
        # ============================================
        
        # Remove single user label
        self.play(FadeOut(label_single, connection, signal_icon), run_time=0.5)
        
        # User counter
        user_count = Variable(1, Text("N Users", font_size=28), num_decimal_places=0)
        user_count.to_corner(UL)
        self.play(Write(user_count), run_time=0.8)
        
        # Store all phones for later manipulation
        # IMPORTANT: Start with empty VGroup, we'll add phone_original properly
        all_phones = VGroup()
        all_connections = VGroup()
        all_signals = VGroup()
        
        # Duplication sequence: 1 -> 2 -> 4 -> 8 -> 16
        duplication_stages = [2, 4, 8, 16]
        
        for stage_idx, target_count in enumerate(duplication_stages):
            current_count = len(all_phones)
            
            # For first stage, we need to include the original phone
            if stage_idx == 0:
                # Include original phone in first duplication
                phones_to_add = target_count - 1  # -1 because we have phone_original
                
                # Create new phones (excluding original)
                new_phones = VGroup()
                for i in range(phones_to_add):
                    new_phone = phone_original.copy()
                    new_phones.add(new_phone)
                
                # Combine original with new phones
                all_phones_temp = VGroup(phone_original, *new_phones)
            else:
                # Subsequent stages: just add new phones
                phones_to_add = target_count - current_count
                
                # Create new phones
                new_phones = VGroup()
                for i in range(phones_to_add):
                    # Copy from existing phones (not from original)
                    new_phone = all_phones[0].copy()
                    new_phones.add(new_phone)
                
                # Combine existing with new phones
                all_phones_temp = VGroup(*all_phones, *new_phones)
            
            # Position phones in circular pattern
            radius = 3.5
            for idx, phone in enumerate(all_phones_temp):
                angle = (idx / target_count) * 2 * PI
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                phone.target_position = np.array([x, y, 0])
            
            # Animation: Replicate and rearrange
            animations = []
            
            if stage_idx == 0:
                # First stage: move original phone to its position
                animations.append(
                    phone_original.animate.move_to(phone_original.target_position)
                )
                
                # Add new phones with growth effect
                for phone in new_phones:
                    phone.move_to(tower.get_center())
                    phone.scale(0.46)
                    animations.append(
                        AnimationGroup(
                            phone.animate.scale(10).move_to(phone.target_position),
                            FadeIn(phone)
                        )
                    )
            else:
                # Subsequent stages: move existing phones
                for phone in all_phones:
                    animations.append(phone.animate.move_to(phone.target_position))
                
                # Add new phones with growth effect
                for phone in new_phones:
                    phone.move_to(tower.get_center())
                    phone.scale(0.46)
                    animations.append(
                        AnimationGroup(
                            phone.animate.scale(10).move_to(phone.target_position),
                            FadeIn(phone)
                        )
                    )
            
            self.play(
                AnimationGroup(*animations, lag_ratio=0.05),
                user_count.tracker.animate.set_value(target_count),
                run_time=1.2
            )
            
            # Update VGroup for next iteration
            all_phones = all_phones_temp
            self.wait(0.2)
        
        # ============================================
        # STEP 3: Show Simultaneous Communication Attempt (3:40 - 3:45)
        # ============================================
        
        # Create signal waves from each phone to tower
        signal_animations = []
        
        for phone in all_phones:
            # Create wavy line from phone to tower
            start = phone.get_center()
            end = tower.get_center()
            
            # Curved path for signal
            control1 = start + (end - start) * 0.3 + UP * 0.3
            control2 = start + (end - start) * 0.7 + DOWN * 0.2
            
            signal_wave = VMobject()
            signal_wave.set_points_as_corners([start, control1, control2, end])
            signal_wave.make_smooth()
            signal_wave.set_color(random.choice([RED, BLUE, YELLOW, GREEN, PURPLE]))
            signal_wave.set_stroke(width=2)
            
            all_signals.add(signal_wave)
        
        # Animate all signals simultaneously
        self.play(
            LaggedStart(
                *[Create(sig) for sig in all_signals],
                lag_ratio=0.03,
                run_time=2
            )
        )
        
        # Pulsing effect on phones (attempting to transmit)
        self.play(
            LaggedStart(
                *[Indicate(phone, color=YELLOW, scale_factor=1.2) for phone in all_phones],
                lag_ratio=0.02
            ),
            run_time=1.5
        )
        
        # Question text
        question = Text("How do we manage N simultaneous users?", 
                    font_size=28, color=YELLOW)
        question.to_edge(DOWN)
        self.play(Write(question), run_time=1.5)
        
        self.wait(1)
        
        # Store for next scene
        self.tower = tower
        self.all_phones = all_phones
        self.all_signals = all_signals
        self.user_count = user_count
        self.question = question


    def scenario_cellular_network(self):
        """
        Professional cellular network visualization
        Duration: ~30 seconds
        """
        
        # ============================================
        # STEP 1: Clear previous scene and setup (3:45 - 3:48)
        # ============================================
        
        self.play(
            FadeOut(self.all_signals),
            FadeOut(self.question),
            FadeOut(self.user_count),
            run_time=0.8
        )
        
        # Shrink and reposition tower and phones for cell view
        self.play(
            self.tower.animate.scale(0.6).move_to(ORIGIN),
            self.all_phones.animate.scale(0.5).move_to(ORIGIN),
            run_time=1
        )
        
        # ============================================
        # STEP 2: Create Cell Coverage Area (3:48 - 3:53)
        # ============================================
        
        # Hexagonal cell (you can use Circle if preferred)
        cell_coverage = RegularPolygon(n=6, color=BLUE, fill_opacity=0.1)
        cell_coverage.scale(3.5)
        cell_coverage.move_to(ORIGIN)
        
        self.play(
            Create(cell_coverage),
            self.tower.animate.move_to(ORIGIN),
            run_time=1.5
        )
        
        # ============================================
        # STEP 3: Distribute Users Within Cell (3:53 - 4:00)
        # ============================================
        
        # Clear old phones
        self.play(FadeOut(self.all_phones), run_time=0.5)
        
        # Create realistic user distribution (clustered, not uniform)
        num_users = 50
        user_phones = VGroup()
        
        # Generate random positions within hexagon
        for i in range(num_users):
            phone = SVGMobject("assets/mobile.svg").scale(0.15)
            
            # Random position within cell (hexagon approximated as circle)
            radius = np.random.uniform(0.3, 3.2)
            angle = np.random.uniform(0, 2 * PI)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            phone.move_to([x, y, 0])
            user_phones.add(phone)
        
        # Animate users appearing
        self.play(
            LaggedStart(
                *[FadeIn(phone, scale=0.3) for phone in user_phones],
                lag_ratio=0.02,
                run_time=2.5
            )
        )
        
        # ============================================
        # STEP 4: Data Flow Visualization (4:00 - 4:10)
        # ============================================
        
        # Create data streams (uplink and downlink)
        def create_data_stream(start, end, color, is_uplink=True):
            """Create animated data stream with moving dots"""
            line = Line(start, end, color=color, stroke_width=1, stroke_opacity=0.3)
            
            # Moving dot along the line
            dot = Dot(radius=0.03, color=color, fill_opacity=0.8)
            dot.move_to(start)
            
            return line, dot
        
        # Select subset of phones for visible data streams (too many = visual clutter)
        active_phones = user_phones[::3]  # Every 3rd phone
        
        uplink_streams = VGroup()
        downlink_streams = VGroup()
        uplink_dots = VGroup()
        downlink_dots = VGroup()
        
        for phone in active_phones:
            # Uplink (phone -> tower)
            ul_line, ul_dot = create_data_stream(
                phone.get_center(), 
                self.tower.get_center(),
                RED,
                is_uplink=True
            )
            uplink_streams.add(ul_line)
            uplink_dots.add(ul_dot)
            
            # Downlink (tower -> phone)
            dl_line, dl_dot = create_data_stream(
                self.tower.get_center(),
                phone.get_center(),
                BLUE,
                is_uplink=False
            )
            downlink_streams.add(dl_line)
            downlink_dots.add(dl_dot)
        
        # Show stream lines
        self.play(
            LaggedStart(
                *[Create(line) for line in uplink_streams],
                *[Create(line) for line in downlink_streams],
                lag_ratio=0.01,
                run_time=2.5
            )
        )
        
        # Animate dots moving along streams
        def move_dot_along_line(dot, line):
            return dot.animate.move_to(line.get_end())
        
        # Continuous data flow animation
        for _ in range(2):  # Repeat twice for emphasis
            # Uplink
            self.play(
                *[FadeIn(dot, scale=0.5) for dot in uplink_dots],
                run_time=0.3
            )
            self.play(
                *[move_dot_along_line(uplink_dots[i], uplink_streams[i]) 
                for i in range(len(uplink_dots))],
                run_time=1
            )
            self.play(
                *[FadeOut(dot, scale=0.5) for dot in uplink_dots],
                run_time=0.3
            )
            
            # Downlink
            self.play(
                *[FadeIn(dot, scale=0.5) for dot in downlink_dots],
                run_time=0.3
            )
            self.play(
                *[move_dot_along_line(downlink_dots[i], downlink_streams[i]) 
                for i in range(len(downlink_dots))],
                run_time=1
            )
            self.play(
                *[FadeOut(dot, scale=0.5) for dot in downlink_dots],
                run_time=0.3
            )
        
        # ============================================
        # STEP 5: Statistics Panel (4:10 - 4:15)
        # ============================================
        
        # Stats box
        stats_bg = Rectangle(
            width=3.5, 
            height=1.8, 
            fill_color=BLACK, 
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2
        )
        stats_bg.to_corner(UR, buff=0.3)
        
        stats_title = Text("Cellular Network", font_size=20, color=YELLOW)
        stats_title.next_to(stats_bg.get_top(), DOWN, buff=0.15)
        
        stat1 = Text("• Users per cell: in 100s", font_size=16, color=WHITE)
        stat1.next_to(stats_title, DOWN, buff=0.15, aligned_edge=LEFT)
        stat1.shift(RIGHT * 0.3)
        
        stat2 = Text("• Same frequency band", font_size=16, color=WHITE)
        stat2.next_to(stat1, DOWN, buff=0.1, aligned_edge=LEFT)
        
        stat3 = Text("• Interference challenge!", font_size=16, color=RED)
        stat3.next_to(stat2, DOWN, buff=0.1, aligned_edge=LEFT)
        
        stats_group = VGroup(stats_bg, stats_title, stat1, stat2, stat3)
        
        self.play(
            FadeIn(stats_bg),
            Write(stats_title),
            run_time=0.8
        )
        self.play(
            Write(stat1),
            Write(stat2),
            Write(stat3),
            run_time=1.5
        )
        
        self.wait(1)
        
        # Store for next scene
        self.cell_coverage = cell_coverage
        self.user_phones = user_phones
        self.uplink_streams = uplink_streams
        self.downlink_streams = downlink_streams
        self.stats_group = stats_group


    def scenario_dense_urban(self):
        """
        Multi-cell deployment showing inter-cell interference
        Duration: ~30 seconds
        """
        
        # ============================================
        # STEP 1: Transition to Multi-Cell View (4:15 - 4:20)
        # ============================================
        
        # Fade out streams and stats
        self.play(
            FadeOut(self.uplink_streams),
            FadeOut(self.downlink_streams),
            FadeOut(self.stats_group),
            run_time=0.8
        )
        
        # Zoom out camera to fit multiple cells
        self.play(
            self.cell_coverage.animate.scale(0.75),
            self.tower.animate.scale(0.75),
            self.user_phones.animate.scale(0.75),
            run_time=2.5
        )
        
        # ============================================
        # STEP 2: Create 7-Cell Cluster (4:20 - 4:28)
        # ============================================
        
        # Standard 7-cell hexagonal cluster pattern
        # Center cell at origin, 6 surrounding cells
        
        hex_cells = VGroup()
        towers_group = VGroup()
        
        # Center cell (already exists)
        center_cell = self.cell_coverage
        center_cell.set_fill(BLUE, opacity=0.15)
        hex_cells.add(center_cell)
        towers_group.add(self.tower)
        
        # Surrounding 6 cells
        # Hexagon center positions for 7-cell cluster
        positions = [
            np.array([6, 0, 0]),           # Right
            np.array([3, 5.2, 0]),         # Top-right
            np.array([-3, 5.2, 0]),        # Top-left
            np.array([-6, 0, 0]),          # Left
            np.array([-3, -5.2, 0]),       # Bottom-left
            np.array([3, -5.2, 0])         # Bottom-right
        ]
        
        colors = [RED, GREEN, YELLOW, PURPLE, ORANGE, TEAL]
        
        for i, (pos, color) in enumerate(zip(positions, colors)):
            # Create hexagonal cell
            cell = RegularPolygon(n=6, color=color, fill_opacity=0.12, stroke_width=2)
            cell.scale(1.925)
            cell.move_to(pos)
            hex_cells.add(cell)
            
            # Create tower
            tower = SVGMobject("assets/tower.svg").scale(0.48)
            tower.move_to(pos)
            towers_group.add(tower)
        
        # Animate appearance of surrounding cells
        self.play(
            LaggedStart(
                *[Create(cell) for cell in hex_cells[1:]],
                *[FadeIn(tower, shift=DOWN * 0.3) for tower in towers_group[1:]],
                lag_ratio=0.15,
                run_time=2.5
            )
        )
        
        # ============================================
        # STEP 3: Distribute Users Across All Cells (4:28 - 4:33)
        # ============================================
        
        # Fade out center cell users (will recreate for all cells)
        self.play(FadeOut(self.user_phones), run_time=0.5)
        
        # Create users for all cells
        all_users = VGroup()
        users_per_cell = 20  # Reduced for visual clarity
        
        for cell in hex_cells:
            cell_center = cell.get_center()
            
            for _ in range(users_per_cell):
                phone = SVGMobject("assets/mobile.svg").scale(0.12)
                
                # Random position within this cell
                radius = np.random.uniform(0.5, 3.0)
                angle = np.random.uniform(0, 2 * PI)
                x = cell_center[0] + radius * np.cos(angle)
                y = cell_center[1] + radius * np.sin(angle)
                
                phone.move_to([x, y, 0])
                all_users.add(phone)
        
        # Animate users appearing
        self.play(
            LaggedStart(
                *[FadeIn(phone, scale=0.2) for phone in all_users],
                lag_ratio=0.005,
                run_time=2.5
            )
        )
        
        # ============================================
        # STEP 4: Show Inter-Cell Interference (4:33 - 4:40)
        # ============================================
        
        # Highlight cell boundaries (edge users suffer most)
        # Create interference zones at cell edges
        
        interference_zones = VGroup()
        
        # For each pair of adjacent cells, create overlap zone
        for i in range(len(hex_cells)):
            for j in range(i+1, len(hex_cells)):
                cell1_center = hex_cells[i].get_center()
                cell2_center = hex_cells[j].get_center()
                
                # Check if cells are adjacent (distance ~ 6)
                distance = np.linalg.norm(cell1_center - cell2_center)
                if distance < 6.5:
                    # Create interference ellipse at midpoint
                    midpoint = (cell1_center + cell2_center) / 2
                    
                    interference_zone = Ellipse(
                        width=2, 
                        height=3.5,
                        color=RED,
                        fill_opacity=0.18,
                        stroke_width=0
                    )
                    interference_zone.move_to(midpoint)
                    
                    # Rotate to align with cell boundary
                    angle = np.arctan2(
                        cell2_center[1] - cell1_center[1],
                        cell2_center[0] - cell1_center[0]
                    )
                    interference_zone.rotate(angle + PI/2)
                    
                    interference_zones.add(interference_zone)
        
        # Animate interference zones appearing
        self.play(
            LaggedStart(
                *[FadeIn(zone) for zone in interference_zones],
                lag_ratio=0.1,
                run_time=2
            )
        )
        
        # Label
        ici_label = Text("Inter-Cell Interference (ICI)", 
                        font_size=24, color=WHITE, weight=BOLD)
        ici_label.to_edge(UP)
        self.play(Write(ici_label), run_time=1)
        
        # ============================================
        # STEP 5: Spectrum Allocation Bar (4:40 - 4:45)
        # ============================================
        
        
        
        # Store for next scene
        self.hex_cells = hex_cells
        self.towers_group = towers_group
        self.all_users = all_users
        self.interference_zones = interference_zones
        self.ici_label = ici_label
        



    def fundamental_problem_statement(self):
        """
        Split screen: Constraint vs Demand
        Duration: ~25 seconds
        """
        
        # ============================================
        # STEP 1: Clear Previous Scene (4:45 - 4:48)
        # ============================================
        
        self.play(
            FadeOut(self.hex_cells),
            FadeOut(self.towers_group),
            FadeOut(self.all_users),
            FadeOut(self.interference_zones),
            FadeOut(self.ici_label),
            
            run_time=1
        )

        # Show limited spectrum
        spectrum_title = Text("Available Spectrum", font_size=20, color=WHITE)
        spectrum_title.move_to(ORIGIN)
        
        spectrum_bar = Rectangle(
            width=8,
            height=0.5,
            fill_color=BLUE,
            fill_opacity=0.6,
            stroke_color=WHITE,
            stroke_width=2
        )
        spectrum_bar.next_to(spectrum_title, DOWN, buff=0.3)
        
        # Demand arrow exceeding spectrum
        demand_label = Text("Demand →", font_size=18, color=RED)
        demand_label.next_to(spectrum_bar, RIGHT, buff=0.2)
        
        demand_arrow = Arrow(
            demand_label.get_right(),
            demand_label.get_right() + RIGHT * 1.8,
            color=RED,
            stroke_width=6
        )
        
        overflow_text = Text("Limited Spectrum, Unlimited Demand",
                            font_size=22, color=YELLOW, weight=BOLD)
        overflow_text.next_to(spectrum_bar, DOWN, buff=0.5)
        self.spectrum_elements = VGroup(
            spectrum_title, spectrum_bar, demand_label, 
            demand_arrow, overflow_text
        )
        self.play(
            Write(spectrum_title),
            Create(spectrum_bar),
            run_time=1
        )
        self.play(
            Write(demand_label),
            GrowArrow(demand_arrow),
            run_time=1
        )
        self.play(Write(overflow_text), run_time=1)
        
        self.wait(1.5)
        self.play(FadeOut(self.spectrum_elements), run_time=1)
        # Reset camera
    #     self.play(
    #     self.hex_cells.animate.scale(1/1.8),
    #     self.towers_group.animate.scale(1/1.8),
    #     self.all_users.animate.scale(1/1.8),
    #     self.interference_zones.animate.scale(1/1.8),
    #     run_time=1
    # )
        
        