from manim import *
import numpy as np

class SimpleShadowingDemo(Scene):
    """Minimal shadowing demonstration - just the essentials"""
    
    def construct(self):
        # Title
        title = Text("Shadowing + Path Loss realization", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)
        
        # Tower at center
        try:
            tx = SVGMobject("tower.svg").scale(0.7)
        except:
            tx = VGroup(
                Rectangle(height=0.8, width=0.15, color=BLUE, fill_opacity=0.9),
                Triangle(color=YELLOW, fill_opacity=1).scale(0.2).rotate(PI/2).shift(UP * 0.42)
            )
        tx.move_to(ORIGIN)
        
        self.play(FadeIn(tx, scale=1.3))
        self.wait(0.5)
        
        # Distance circles
        circles = VGroup()
        radii = [1.0, 2.0, 3.0]
        distances = ["100m", "200m", "300m"]
        
        for radius, dist in zip(radii, distances):
            circle = Circle(radius=radius, color=WHITE, stroke_width=2, stroke_opacity=0.4)
            label = Text(dist, font_size=14, color=WHITE)
            label.move_to(RIGHT * radius + UP * 0.15)
            
            circles.add(VGroup(circle, label))
        
        self.play(
            LaggedStart(*[FadeIn(c) for c in circles], lag_ratio=0.3),
            run_time=2
        )
        self.wait(0.5)
        
        # Legend
        legend = self.create_simple_legend()
        legend.to_corner(UR, buff=0.4)
        self.play(FadeIn(legend))
        
        # Heat map
        heat_map = self.create_heat_map(radii[-1])
        self.play(FadeIn(heat_map, lag_ratio=0.01), run_time=2)
        self.wait(1)
        
        # Arrow
        arrow = Arrow(
            ORIGIN, 
            RIGHT * radii[1],
            buff=0,
            color=WHITE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        
        self.play(Create(arrow))
        self.wait(0.5)
        
        # Rotate arrow slowly (2 full rotations)
        self.play(
            Rotate(arrow, 2 * TAU, about_point=ORIGIN),
            run_time=8,
            rate_func=linear
        )
        
        self.wait(2)
    
    def create_heat_map(self, max_radius):
        """Create color-coded heat map"""
        map_group = VGroup()
        
        resolution = 35
        patch_size = max_radius / resolution * 1.9
        
        for i in range(resolution):
            for j in range(resolution):
                x = -max_radius + (2 * max_radius * i / resolution)
                y = -max_radius + (2 * max_radius * j / resolution)
                
                distance = np.sqrt(x**2 + y**2)
                
                if distance < max_radius and distance > 0.5:
                    path_loss = 1 / (distance**1.5)
                    shadowing = np.random.normal(0, 0.4)
                    signal_strength = path_loss * np.exp(shadowing)
                    
                    color = self.strength_to_color(signal_strength)
                    
                    patch = Circle(
                        radius=patch_size,
                        color=color,
                        fill_opacity=0.8,
                        stroke_width=0
                    )
                    patch.move_to([x, y, 0])
                    map_group.add(patch)
        
        return map_group
    
    def strength_to_color(self, strength):
        """Map signal strength to 4 colors"""
        normalized = np.clip(strength * 3, 0, 1)
        
        if normalized > 0.75:
            return GREEN
        elif normalized > 0.5:
            return YELLOW
        elif normalized > 0.25:
            return ORANGE
        else:
            return RED
    
    def create_simple_legend(self):
        """Create simple legend"""
        legend = VGroup()
        
        title = Text("Signal", font_size=14, weight=BOLD)
        
        colors = [GREEN, YELLOW, ORANGE, RED]
        labels = ["Strong", "Medium", "Weak", "V.Weak"]
        
        items = VGroup()
        for color, label in zip(colors, labels):
            square = Square(side_length=0.15, color=color, fill_opacity=0.8, stroke_width=1)
            text = Text(label, font_size=11).next_to(square, RIGHT, buff=0.06)
            items.add(VGroup(square, text))
        
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        items.next_to(title, DOWN, buff=0.12)
        
        legend.add(title, items)
        
        bg = Rectangle(
            height=legend.height + 0.2,
            width=legend.width + 0.2,
            color=BLACK,
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2
        )
        bg.move_to(legend.get_center())
        
        return VGroup(bg, legend)