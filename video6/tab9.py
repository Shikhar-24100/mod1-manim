from manim import *

class FDMA_Cuboids(ThreeDScene):
    def construct(self):
        # --- CONFIGURATION ---
        # 1. Colors from your chart
        fdma_colors = [LIGHT_GRAY, LIGHT_GRAY, LIGHT_GRAY, LIGHT_GRAY, LIGHT_GRAY, LIGHT_GRAY, LIGHT_GRAY]
        tdma_colors = [TEAL_C, MAROON_D, GREEN, YELLOW, GRAY, RED]
        # 2. Schedule Data: (Freq_Index, Start_Time, End_Time)
        # Note: In FDMA, they occupy the whole time frame usually, or distinct slots.
        # This matches the "staggered" look of your reference image.
        tdma_title = Text("2. TIME Domain (TDMA)", font_size=32, color=BLUE, weight=BOLD)
        self.play(Write(tdma_title))
        self.wait(1.5)
        self.play(FadeOut(tdma_title))
        schedule = [
            (1, 0.5, 6.5), # User 1 (Freq 1)
            (2, 0.5, 6.5), # User 2 (Freq 2)
            (3, 0.5, 6.5), # User 3 (Freq 3)
            (4, 0.5, 6.5), # User 4 (Freq 4)
            (5, 0.5, 6.5), 
            (6, 0.5, 6.5),
            (7, 0.5, 6.5),
        ]

        # --- SETUP AXES ---
        axes_3d = ThreeDAxes(
            x_range=[0, 7, 1],
            y_range=[-4, 8, 1],
            z_range=[0, 2, 1],
            x_length=5.5,
            y_length=9,
            z_length=1.5
        )
        axes_3d.shift(DOWN * 1.5)
        
        # Fixed labels (Static)
        labels = VGroup(
            Text("Time", color=RED, font_size=20).move_to(axes_3d.c2p(7, 0, 0) + RIGHT * 0.5),
            Text("Frequency", color=BLUE, font_size=20).move_to(axes_3d.c2p(0, -4, 0) + UP * 0.1),
            Text("Power", color=BLACK, font_size=20).rotate(90*DEGREES, axis=RIGHT).move_to(axes_3d.c2p(0, 0, 2) + UP * 0.5)
        )

        # --- CREATE CUBOIDS ---
        blocks = VGroup()
        target_gray_block = None
        for i, (freq_idx, start, end) in enumerate(schedule):
            c = fdma_colors[i % len(fdma_colors)]
            
            # Dimensions
            time_duration = end - start
            freq_width = 0.8  # Width of the frequency band
            power_height = 1.5 # Constant power
            
            # Create the Prism (Cuboid)
            # Prism dimensions are [width, height, depth] -> mapped to x, y, z usually
            # But Prism defaults can be tricky, so we use a Cube and scale it.
            
            block = Cube(fill_color=c, fill_opacity=0.8, stroke_width=1, stroke_color=WHITE)
            
            # Scale to correct dimensions: (Time, Frequency, Power)
            # Note: We need to scale relative to axis units.
            
            # Get unit size from axes
            x_unit = axes_3d.x_axis.unit_size
            y_unit = axes_3d.y_axis.unit_size
            z_unit = axes_3d.z_axis.unit_size
            
            block.scale([
                (time_duration * x_unit) / 2, # Scale X (Time)
                (freq_width * y_unit) / 2,    # Scale Y (Freq)
                (power_height * z_unit) / 2   # Scale Z (Power)
            ])
            
            # Move to position
            # X: Center of time slot
            # Y: Exact Frequency Index
            # Z: Half of height (so it sits ON the grid, not cutting through it)
            
            pos = axes_3d.c2p(
                (start + end) / 2, 
                freq_idx, 
                power_height / 2
            )
            block.move_to(pos)
            
            blocks.add(block)

            if freq_idx == 2:
                target_gray_block = block

        # --- ANIMATION ---
        
        # 1. Set specific Isometric view (Static, no rotation)
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        # 2. Draw Axes
        self.play(Create(axes_3d), Write(labels))
        
        # 3. Grow the blocks (Simple FadeIn or GrowFromBottom)
        # GrowFromPoint looks nice for 3D bar charts
        self.play(
            AnimationGroup(
                *[GrowFromPoint(b, b.get_bottom()) for b in blocks],
                lag_ratio=0.2
            )
        )
        
        # 4. HOLD (No spinning)
        self.wait(3)


        schedule1 = [
            (1.95, 0.5, 1.5), # User 1 (Freq 1)
            (1.95, 1.5, 2.5), # User 2 (Freq 2)
            (1.95, 2.5, 3.5), # User 3 (Freq 3)
            (1.95, 3.5, 4.5), # User 4 (Freq 4)
            (1.95, 4.5, 5.5), 
            (1.95, 5.5, 6.5),
        ]


        blocks1 = VGroup()
        
        for i, (freq_idx, start, end) in enumerate(schedule1):
            c = tdma_colors[i % len(tdma_colors)]
            
            # Dimensions
            time_duration = end - start
            time_width = 0.8  # Width of the frequency band
            power_height = 1.6 # Constant power
            
            # Create the Prism (Cuboid)
            # Prism dimensions are [width, height, depth] -> mapped to x, y, z usually
            # But Prism defaults can be tricky, so we use a Cube and scale it.
            
            block = Cube(fill_color=c, fill_opacity=0.8, stroke_width=1, stroke_color=WHITE)
            
            # Scale to correct dimensions: (Time, Frequency, Power)
            # Note: We need to scale relative to axis units.
            
            # Get unit size from axes
            x_unit = axes_3d.x_axis.unit_size
            y_unit = axes_3d.y_axis.unit_size
            z_unit = axes_3d.z_axis.unit_size
            
            block.scale([
                (time_duration * x_unit) / 2, # Scale X (Time)
                (time_width * y_unit) / 2,    # Scale Y (Freq)
                (power_height * z_unit) / 2   # Scale Z (Power)
            ])
            
            # Move to position
            # X: Center of time slot
            # Y: Exact Frequency Index
            # Z: Half of height (so it sits ON the grid, not cutting through it)
            
            pos = axes_3d.c2p(
                (start + end) / 2, 
                freq_idx, 
                power_height / 2
            )
            block.move_to(pos)
            
            blocks1.add(block)

        if target_gray_block:
            self.play(FadeOut(target_gray_block))
        self.play(
            AnimationGroup(
                *[GrowFromPoint(b, b.get_bottom()) for b in blocks1],
                lag_ratio=0.2
            )
        )

        self.wait(3)