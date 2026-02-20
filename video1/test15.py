from manim import *
import numpy as np
class RandomShadowingRealization(Scene):
    """Animation 18: Random shadowing realization with signal strength map"""
    
    def construct(self):
        # Title
        title = Text("Path Loss + Random Shadowing", font_size=42, weight=BOLD)
        subtitle = Text("Combined Effect on Received Power", font_size=26, color=BLUE)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(
            title.animate.scale(0.6).to_edge(UP, buff=0.2),
            FadeOut(subtitle)
        )
        
        # Transmitter in center
        try:
            tx = SVGMobject("tower.svg").scale(0.8)
        except:
            tx = VGroup(
                Rectangle(height=1.0, width=0.2, color=BLUE, fill_opacity=0.9),
                Triangle(color=YELLOW, fill_opacity=1).scale(0.25).rotate(PI/2).shift(UP * 0.52)
            )
        
        tx.move_to(ORIGIN)
        tx_label = Text("TX", font_size=20, color=YELLOW, weight=BOLD).next_to(tx, DOWN, buff=0.1)
        
        self.play(FadeIn(tx, scale=1.5), Write(tx_label))
        self.wait(0.5)
        
        # Create concentric circles showing distance
        circles = VGroup()
        circle_labels = VGroup()
        radii = [0.8, 1.8, 2.8, 3.5]
        distances = ["100m", "200m", "300m", "400m"]
        
        for radius, dist in zip(radii, distances):
            circle = Circle(radius=radius, color=WHITE, stroke_width=2, stroke_opacity=0.5)
            circle.move_to(ORIGIN)
            circles.add(circle)
            
            label = Text(dist, font_size=14, color=WHITE).move_to(RIGHT * radius + UP * 0.2)
            circle_labels.add(label)
        
        self.play(
            LaggedStart(*[Create(c) for c in circles], lag_ratio=0.3),
            LaggedStart(*[Write(l) for l in circle_labels], lag_ratio=0.3),
            run_time=2
        )
        self.wait(0.5)
        
        # Legend
        legend = self.create_legend()
        legend.to_corner(UR, buff=0.3)
        self.play(FadeIn(legend, shift=LEFT))
        
        # Create initial shadowing map
        realization_label = Text("Realization 1", font_size=24, color=BLUE)
        realization_label.to_edge(DOWN, buff=0.3)
        self.play(Write(realization_label))
        
        # Show multiple realizations
        for realization_num in range(1, 4):
            shadowing_map = self.create_shadowing_map(radii[-1])
            
            if realization_num == 1:
                self.play(FadeIn(shadowing_map), run_time=1.5)
            else:
                new_label = Text(f"Realization {realization_num}", font_size=24, color=BLUE)
                new_label.to_edge(DOWN, buff=0.3)
                
                new_map = self.create_shadowing_map(radii[-1])
                self.play(
                    Transform(shadowing_map, new_map),
                    Transform(realization_label, new_label),
                    run_time=2
                )
            
            self.wait(1)
        
        # Final annotation
        annotation = VGroup(
            Text("Random shadowing creates", font_size=20, color=YELLOW),
            Text("unpredictable variations", font_size=20, color=YELLOW),
            Text("in signal strength!", font_size=20, color=YELLOW, weight=BOLD)
        ).arrange(DOWN, buff=0.1)
        annotation.to_edge(LEFT, buff=0.5).shift(DOWN * 1 + LEFT * 0.2)
        
        self.play(Write(annotation))
        self.wait(10)
    
    def create_shadowing_map(self, max_radius):
        """Create a color-coded shadowing map"""
        map_group = VGroup()
        
        # Create grid of small circles/patches
        resolution = 30
        for i in range(resolution):
            for j in range(resolution):
                x = -max_radius + (2 * max_radius * i / resolution)
                y = -max_radius + (2 * max_radius * j / resolution)
                
                distance = np.sqrt(x**2 + y**2)
                
                if distance < max_radius and distance > 0.5:
                    # Path loss component (decreases with distance)
                    path_loss_factor = 1 / (distance**1.5)
                    
                    # Random shadowing component (log-normal)
                    shadowing = np.random.normal(0, 0.3)
                    
                    # Combined effect
                    total_factor = path_loss_factor * np.exp(shadowing)
                    
                    # Map to color
                    color = self.power_to_color(total_factor)
                    
                    patch = Circle(
                        radius=max_radius / resolution * 1.5,
                        color=color,
                        fill_opacity=0.7,
                        stroke_width=0
                    )
                    patch.move_to([x, y, 0])
                    map_group.add(patch)
        
        return map_group
    
    def power_to_color(self, power_factor):
        """Map power factor to color (red=weak, yellow=medium, green=strong)"""
        # Normalize power factor to 0-1 range
        normalized = np.clip(power_factor * 3, 0, 1)
        
        if normalized > 0.7:
            return GREEN
        elif normalized > 0.4:
            return YELLOW
        elif normalized > 0.2:
            return ORANGE
        else:
            return RED
    
    def create_legend(self):
        """Create color legend for signal strength"""
        legend = VGroup()
        
        legend_title = Text("Signal Strength", font_size=18, weight=BOLD)
        legend.add(legend_title)
        
        colors = [GREEN, YELLOW, ORANGE, RED]
        labels = ["Strong", "Medium", "Weak", "Very Weak"]
        
        color_guide = VGroup()
        for color, label in zip(colors, labels):
            square = Square(side_length=0.2, color=color, fill_opacity=0.8, stroke_width=1)
            text = Text(label, font_size=14).next_to(square, RIGHT, buff=0.1)
            row = VGroup(square, text)
            color_guide.add(row)
        
        color_guide.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        color_guide.next_to(legend_title, DOWN, buff=0.2)
        legend.add(color_guide)
        
        # Add background
        bg = Rectangle(
            height=legend.height + 0.3,
            width=legend.width + 0.3,
            color=BLACK,
            fill_opacity=0.7,
            stroke_color=WHITE,
            stroke_width=2
        )
        bg.move_to(legend.get_center())
        
        return VGroup(bg, legend)


# To render these animations:
# manim -pql urban_rural_shadowing.py UrbanVsRuralShadowing
# manim -pql urban_rural_shadowing.py RandomShadowingRealization