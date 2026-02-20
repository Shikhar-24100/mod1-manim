from manim import *
import numpy as np

class FriisVsShadowingComparison(Scene):
    """Animation 19: Side-by-side model comparison"""
    
    def construct(self):
        # Title
        title = Text("Friis Equation vs Shadowing Model", font_size=44, weight=BOLD)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.75).to_edge(UP, buff=0.2))
        
        # Create split screen divider
        divider = Line(UP * 3.5, DOWN * 3.1, color=WHITE, stroke_width=3)
        self.play(Create(divider))
        
        # Labels
        friis_label = Text("Friis Equation", font_size=28, color=BLUE, weight=BOLD)
        friis_label.move_to(LEFT * 3.5 + UP * 2.8)
        friis_sublabel = Text("(Deterministic)", font_size=20, color=BLUE, slant=ITALIC)
        friis_sublabel.next_to(friis_label, DOWN, buff=0.1)
        
        shadowing_label = Text("Shadowing Model", font_size=28, color=RED, weight=BOLD)
        shadowing_label.move_to(RIGHT * 3.5 + UP * 2.8)
        shadowing_sublabel = Text("(Stochastic)", font_size=20, color=RED, slant=ITALIC)
        shadowing_sublabel.next_to(shadowing_label, DOWN, buff=0.1)
        
        self.play(
            Write(friis_label), Write(friis_sublabel),
            Write(shadowing_label), Write(shadowing_sublabel)
        )
        self.wait(0.5)
        
        # ========== FRIIS SIDE (LEFT) - Deterministic ==========
        # Setup scene
        friis_tx, friis_rx = self.create_tx_rx_pair(LEFT * 3.5)
        self.play(FadeIn(friis_tx), FadeIn(friis_rx))
        
        # Create axes for signal strength vs distance
        friis_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 100, 25],
            x_length=4,
            y_length=3,
            axis_config={"color": GRAY, "include_numbers": False},
            tips=False
        ).shift(LEFT * 3.5 + DOWN * 0.8)
        
        friis_x_label = Text("Distance", font_size=14).next_to(friis_axes.x_axis, DOWN, buff=0.1)
        friis_y_label = Text("Power (dBm)", font_size=14).next_to(friis_axes.y_axis, LEFT, buff=0.1)
        
        self.play(
            Create(friis_axes),
            Write(friis_x_label),
            Write(friis_y_label)
        )
        
        # ========== SHADOWING SIDE (RIGHT) - Stochastic ==========
        # Setup scene
        shadow_tx, shadow_rx = self.create_tx_rx_pair(RIGHT * 3.5)
        
        # Add obstacles on shadowing side
        obstacles = self.create_obstacles(RIGHT * 3.5)
        
        self.play(FadeIn(shadow_tx), FadeIn(shadow_rx), FadeIn(obstacles))
        
        # Create axes
        shadow_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 100, 25],
            x_length=4,
            y_length=3,
            axis_config={"color": GRAY, "include_numbers": False},
            tips=False
        ).shift(RIGHT * 3.5 + DOWN * 0.8)
        
        shadow_x_label = Text("Distance", font_size=14).next_to(shadow_axes.x_axis, DOWN, buff=0.1)
        shadow_y_label = Text("Power (dBm)", font_size=14).next_to(shadow_axes.y_axis, LEFT, buff=0.1)
        
        self.play(
            Create(shadow_axes),
            Write(shadow_x_label),
            Write(shadow_y_label)
        )
        self.wait(0.5)
        
        # ========== DRAW CURVES SIMULTANEOUSLY ==========
        # Friis curve (smooth, predictable)
        friis_curve = friis_axes.plot(
            lambda x: 90 * np.exp(-0.5 * x),
            x_range=[0.2, 4.8],
            color=BLUE,
            stroke_width=4
        )
        
        # Shadowing curve (fluctuating around trend)
        def shadowing_function(x):
            base = 90 * np.exp(-0.5 * x)
            noise = 10 * np.sin(5 * x) + 5 * np.cos(7 * x) + 3 * np.sin(11 * x)
            return base + noise
        
        shadowing_curve = shadow_axes.plot(
            shadowing_function,
            x_range=[0.2, 4.8],
            color=RED,
            stroke_width=4
        )
        
        # Draw both curves simultaneously
        self.play(
            Create(friis_curve, run_time=3),
            Create(shadowing_curve, run_time=3)
        )
        self.wait(1)
        
        # ========== ANNOTATIONS ==========
        friis_annotation = VGroup(
            Text("✓ Smooth curve", font_size=16, color=GREEN),
            Text("✓ Predictable", font_size=16, color=GREEN),
            Text("✗ Unrealistic", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        friis_annotation.next_to(friis_axes, DOWN, buff=0.3)
        
        shadow_annotation = VGroup(
            Text("✓ Fluctuates", font_size=16, color=GREEN),
            Text("✓ Realistic", font_size=16, color=GREEN),
            Text("✓ Accounts for obstacles", font_size=16, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        shadow_annotation.next_to(shadow_axes, DOWN, buff=0.3)
        
        self.play(
            Write(friis_annotation),
            Write(shadow_annotation)
        )
        self.wait(10)
    
    def create_tx_rx_pair(self, center):
        """Create transmitter and receiver pair"""
        try:
            tx = SVGMobject("tower.svg").scale(0.4)
        except:
            tx = Triangle(color=BLUE, fill_opacity=1).scale(0.15).rotate(-PI/2)
        
        try:
            rx = SVGMobject("mobile.svg").scale(0.3)
        except:
            rx = Rectangle(height=0.2, width=0.1, color=RED, fill_opacity=1)
        
        tx.move_to(center + LEFT * 1.8 + UP * 1.5)
        rx.move_to(center + RIGHT * 1.8 + UP * 1.5)
        
        return VGroup(tx, rx)
    
    def create_obstacles(self, center):
        """Create small obstacles for shadowing side"""
        obstacles = VGroup()
        
        positions = [
            center + LEFT * 0.8 + UP * 1.5,
            center + RIGHT * 0.3 + UP * 1.5,
            center + RIGHT * 1.2 + UP * 1.5
        ]
        
        for i, pos in enumerate(positions):
            if i == 0:
                try:
                    obs = SVGMobject("building.svg").scale(0.3)
                except:
                    obs = Rectangle(height=0.4, width=0.15, color=GRAY, fill_opacity=0.7)
            elif i == 1:
                try:
                    obs = SVGMobject("tree.svg").scale(0.25)
                except:
                    obs = Circle(radius=0.15, color=GREEN, fill_opacity=0.7)
            else:
                try:
                    obs = SVGMobject("person.svg").scale(0.2)
                except:
                    obs = Rectangle(height=0.25, width=0.08, color=BLUE, fill_opacity=0.7)
            
            obs.move_to(pos)
            obstacles.add(obs)
        
        return obstacles