from manim import *

class SpectrumGraph(Scene):
    def construct(self):
        # 1. Coordinate System
        axes = Axes(
            x_range=[0, 14, 1],
            y_range=[0, 14, 1],
            x_length=9,
            y_length=6,
            axis_config={"color": WHITE, "include_tip": True},
            tips=True
        ).shift(DOWN * 0.5)
        
        # Labels for Axes
        y_label = Text("BANDWIDTH REQUIREMENTS", font_size=20).rotate(90*DEGREES).next_to(axes.y_axis, LEFT, buff=0.2)
        x_label = Text("TIME", font_size=20).next_to(axes.x_axis, DOWN, aligned_edge=RIGHT)
        title = Text("Current Situation", color=ORANGE, font_size=32).to_corner(UL, buff=0.5)
        
        # Animate axes and labels
        self.play(Create(axes), run_time=2)
        self.play(Write(y_label), Write(x_label), run_time=1.5)
        self.play(FadeIn(title), run_time=1)
        self.wait(0.5)
        
        # 2. Define Paths for Areas
        # Demand Path (Red) - Approximating the jagged points from the image
        demand_points = [
            [0, 0, 0], [1, 2, 0], [2, 3, 0], [3, 4, 0], [4, 5.5, 0], 
            [5, 5.2, 0], [6, 6.5, 0], [7, 8, 0], [8, 9, 0], [9, 10, 0], 
            [10, 11.5, 0], [12, 13.5, 0], [13, 13.8, 0]
        ]
        demand_coords = [axes.c2p(p[0], p[1]) for p in demand_points]
        
        # Creating the shaded Demand area
        demand_area_points = [axes.c2p(0,0)] + demand_coords + [axes.c2p(13, 0)]
        demand_area = Polygon(*demand_area_points, fill_opacity=0.4, fill_color=RED, stroke_width=2, stroke_color=RED)
        
        # Animate demand area
        self.play(Create(demand_area), run_time=3)
        self.wait(0.5)
        
        # Supply Path (Blue/Purple)
        supply_points = [
            [0, 0, 0], [1, 1.5, 0], [2, 2, 0], [3, 1.5, 0], [4, 2.2, 0], 
            [5, 2.8, 0], [6, 2, 0], [7, 2.2, 0], [8, 1.2, 0], [9, 1.8, 0], 
            [10, 2.5, 0], [11, 2.8, 0], [13, 3.2, 0]
        ]
        supply_coords = [axes.c2p(p[0], p[1]) for p in supply_points]
        
        # Creating the shaded Supply area
        supply_area_points = [axes.c2p(0,0)] + supply_coords + [axes.c2p(13, 0)]
        supply_area = Polygon(*supply_area_points, fill_opacity=0.6, fill_color=BLUE_E, stroke_width=2, stroke_color=BLUE_C)
        
        # Animate supply area
        self.play(Create(supply_area), run_time=3)
        self.wait(0.5)
        
        # 3. Text inside areas
        demand_text = Text("SPECTRUM\nDEMAND", font_size=36, weight=BOLD, color=RED).move_to(axes.c2p(8, 5))
        supply_text = Text("SPECTRUM SUPPLY", font_size=18, weight=BOLD, color=BLUE_C).move_to(axes.c2p(8, 1.5))
        
        # Animate texts
        self.play(Write(demand_text), run_time=1.5)
        self.play(Write(supply_text), run_time=1.5)
        self.wait(0.5)
        
        # 4. Labels and Leader Lines
        # Demand Labels (Red dots)
        d_dots_indices = [4, 7, 10]
        d_labels = ["Growth of\nPrivate Networks", "High\nBandwidth\nApplications", "Next\nGeneration\nDevices"]
        
        demand_annotations = []
        for i, idx in enumerate(d_dots_indices):
            dot = Dot(demand_coords[idx], color=RED, radius=0.12)
            line = Line(dot.get_center(), dot.get_center() + UP*1.2 + LEFT*0.8, color=RED, stroke_width=2)
            label = Text(d_labels[i], font_size=16, weight=BOLD, color=WHITE).next_to(line, UP, buff=0.1)
            demand_annotations.append((dot, line, label))
        
        # Animate demand annotations
        for dot, line, label in demand_annotations:
            self.play(FadeIn(dot), run_time=0.3)
            self.play(Create(line), run_time=0.4)
            self.play(Write(label), run_time=0.6)
        
        self.wait(0.5)
        
        # Supply Labels (Blue dots)
        s_dots_indices = [2, 5, 10]
        s_labels = ["No New\nSpectrum\nAllocation", "Nascent\nSecondary\nMarket", "Inefficient\nUse of\nSpectrum"]
        
        supply_annotations = []
        for i, idx in enumerate(s_dots_indices):
            dot = Dot(supply_coords[idx], color=BLUE_C, radius=0.12)
            line = Line(dot.get_center(), dot.get_center() + DOWN*1.2, color=BLUE_C, stroke_width=2)
            label = Text(s_labels[i], font_size=16, weight=BOLD, color=WHITE).next_to(line, DOWN, buff=0.1)
            supply_annotations.append((dot, line, label))
        
        # Animate supply annotations
        for dot, line, label in supply_annotations:
            self.play(FadeIn(dot), run_time=0.3)
            self.play(Create(line), run_time=0.4)
            self.play(Write(label), run_time=0.6)
        
        # Final wait to show complete graph
        self.wait(2)