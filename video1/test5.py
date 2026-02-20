from manim import *
import numpy as np

class DistancePowerPlot(Scene):
    """Animation 8: Distance vs Received Power plot - Memory Optimized"""
    
    def construct(self):
        # Title
        title = Text("Path Loss: Distance vs Received Power", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP, buff=0.3))
        self.wait(0.5)
        
        # Create axes
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[-120, -20, 20],
            x_length=9,
            y_length=5.5,
            axis_config={
                "color": BLUE,
                "include_numbers": True,
                "font_size": 20,
            },
            tips=False,
        )
        
        # Axis labels
        x_label = Text("Distance (meters)", font_size=24).next_to(axes.x_axis, DOWN, buff=0.4)
        y_label = Text("Received Power (dBm)", font_size=24).next_to(axes.y_axis, LEFT, buff=0.6).rotate(PI/2)
        
        # Move axes down to make room
        axes_group = VGroup(axes, x_label, y_label).shift(DOWN * 0.3)
        
        # Show axes
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            run_time=2
        )
        self.wait(1)
        
        # Path loss function
        def power_loss(d):
            if d < 1:
                d = 1
            Pt = -30
            n = 2
            d0 = 1
            return Pt - 10 * n * np.log10(d / d0)
        
        # Create the curve
        curve = axes.plot(
            power_loss,
            x_range=[1, 100],
            color=YELLOW,
            stroke_width=4
        )
        
        # Draw the curve
        self.play(Create(curve), run_time=3, rate_func=linear)
        self.wait(1)
        
        # Moving marker along the curve
        marker = Dot(color=RED, radius=0.12)
        marker.move_to(axes.c2p(1, power_loss(1)))
        
        # Static label (will update manually)
        d_label = Text("d = 1m", font_size=20, color=WHITE)
        p_label = Text(f"P = {power_loss(1):.1f} dBm", font_size=20, color=YELLOW)
        value_label = VGroup(d_label, p_label).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        value_label.next_to(marker, UR, buff=0.3)
        
        self.play(FadeIn(marker), FadeIn(value_label))
        
        # Animate marker with manual label updates at key points
        distances = [1, 25, 50, 75, 100]
        
        for i in range(len(distances) - 1):
            d_start = distances[i]
            d_end = distances[i + 1]
            
            # Move marker
            self.play(
                marker.animate.move_to(axes.c2p(d_end, power_loss(d_end))),
                run_time=1,
                rate_func=linear
            )
            
            # Update label
            new_d_label = Text(f"d = {d_end}m", font_size=20, color=WHITE)
            new_p_label = Text(f"P = {power_loss(d_end):.1f} dBm", font_size=20, color=YELLOW)
            new_value_label = VGroup(new_d_label, new_p_label).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            new_value_label.next_to(marker, UR, buff=0.3)
            
            self.play(Transform(value_label, new_value_label), run_time=0.3)
        
        self.wait(1)
        
        # Remove marker and show specific points
        self.play(FadeOut(marker), FadeOut(value_label))
        
        # Show specific points of interest
        points_of_interest = [10, 50, 100]
        dots = VGroup()
        labels = VGroup()
        
        for d in points_of_interest:
            dot = Dot(axes.c2p(d, power_loss(d)), color=GREEN, radius=0.1)
            label = VGroup(
                Text(f"{d}m", font_size=18, color=GREEN),
                Text(f"{power_loss(d):.1f}dBm", font_size=16, color=GREEN)
            ).arrange(DOWN, buff=0.05)
            label.next_to(dot, DOWN, buff=0.25)
            
            dots.add(dot)
            labels.add(label)
        
        self.play(
            LaggedStart(*[FadeIn(dot, scale=1.5) for dot in dots], lag_ratio=0.3),
            LaggedStart(*[Write(label) for label in labels], lag_ratio=0.3),
            run_time=2
        )
        self.wait(1)
        
        # Add decade line annotation
        d1, d2 = 10, 100
        p1, p2 = power_loss(d1), power_loss(d2)
        
        decade_line = Line(
            axes.c2p(d1, p1),
            axes.c2p(d2, p2),
            color=ORANGE,
            stroke_width=4
        )
        
        # Arrows showing the relationship
        h_arrow = DoubleArrow(
            axes.c2p(d1, -115),
            axes.c2p(d2, -115),
            color=ORANGE,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.1
        )
        h_text = Text("10× distance", font_size=18, color=ORANGE).next_to(h_arrow, DOWN, buff=0.2)
        
        v_arrow = DoubleArrow(
            axes.c2p(3, p2),
            axes.c2p(3, p1),
            color=ORANGE,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.1
        )
        v_text = Text("20 dB", font_size=18, color=ORANGE).next_to(v_arrow, LEFT, buff=0.2)
        
        self.play(Create(decade_line), run_time=1)
        self.play(
            GrowArrow(h_arrow),
            Write(h_text)
        )
        self.play(
            GrowArrow(v_arrow),
            Write(v_text)
        )
        self.wait(1)
        
        # Main annotation box
        slope_annotation = VGroup(
            Text("Path Loss Formula:", font_size=22, color=WHITE, weight=BOLD),
            Text("Pr ∝ -20log₁₀(d) dB/decade", font_size=20, color=YELLOW),
            Text("(Free space, n=2)", font_size=16, color=GRAY)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        annotation_box = SurroundingRectangle(
            slope_annotation,
            color=ORANGE,
            buff=0.25,
            corner_radius=0.12,
            stroke_width=3
        )
        
        annotation_group = VGroup(annotation_box, slope_annotation)
        annotation_group.to_corner(UR, buff=0.5).shift(DOWN * 1.5)
        
        self.play(
            Create(annotation_box),
            Write(slope_annotation),
            run_time=2
        )
        self.wait(1)
        
        # Highlight the decay nature
        decay_note = Text(
            "Signal decays with distance",
            font_size=24,
            color=WHITE
        ).to_edge(DOWN, buff=0.4)
        
        self.play(Write(decay_note))
        self.wait(3)