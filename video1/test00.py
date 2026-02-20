from manim import *
import numpy as np

class ShadowingIntroduction(Scene):
    """Introduction - The Question (2D view, no camera changes)"""
    
    def construct(self):
        # Title
        title = Text("Same Distance, Different Signal Strength?", font_size=36, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(1)
        
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
        
        # Concentric circles (distance rings)
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
        
        # Animated signal waves (expanding circles)
        self.emit_signal_waves(tx, radii[-1])
        
        # Place two mobiles on the SAME circle (200m - middle circle)
        mobile1_angle = 45 * DEGREES
        mobile2_angle = 225 * DEGREES
        mobile_radius = radii[2]  # 300m (outer circle)
        
        # Mobile 1 - Strong signal
        try:
            mobile1 = SVGMobject("mobile.svg").scale(0.4)
        except:
            mobile1 = Rectangle(height=0.4, width=0.2, color=GREEN, fill_opacity=1)
        
        x1 = mobile_radius * np.cos(mobile1_angle)
        y1 = mobile_radius * np.sin(mobile1_angle)
        mobile1.move_to([x1, y1, 0])
        
        # Signal bars for mobile 1 (4 bars - strong)
        bars1 = self.create_signal_bars(4, GREEN)
        bars1.next_to(mobile1, UP)
        mobile1_group = VGroup(mobile1, bars1)
        
        # Mobile 2 - Weak signal
        try:
            mobile2 = SVGMobject("mobile.svg").scale(0.4)
        except:
            mobile2 = Rectangle(height=0.4, width=0.2, color=RED, fill_opacity=1)
        
        x2 = mobile_radius * np.cos(mobile2_angle)
        y2 = mobile_radius * np.sin(mobile2_angle)
        mobile2.move_to([x2, y2, 0])
        
        # Signal bars for mobile 2 (1 bar - weak)
        bars2 = self.create_signal_bars(1, RED)
        bars2.next_to(mobile2, UP)
        mobile2_group = VGroup(mobile2, bars2)
        
        self.play(FadeIn(mobile1_group, scale=1.5), FadeIn(mobile2_group, scale=1.5))
        self.wait(1)
        
        # Highlight the circle they're both on
        highlight_circle = Circle(radius=mobile_radius, color=YELLOW, stroke_width=4)
        self.play(Create(highlight_circle))
        self.wait(0.5)
        
        # Distance label
        dist_label = Text("Both at 300m", font_size=20, color=YELLOW, weight=BOLD)
        dist_label.move_to(RIGHT * (mobile_radius + 1.8) + UP * 0.3)
        self.play(Write(dist_label))
        self.wait(1)
        
        # Pulse the highlight to emphasize
        self.play(
            highlight_circle.animate.set_stroke(width=6).set_color(RED),
            Flash(highlight_circle, color=RED, line_length=0.4, num_lines=12)
        )
        self.wait(0.5)

    
    def emit_signal_waves(self, tx, max_radius):
        """Create expanding wave animation"""
        waves = VGroup()
        
        for i in range(3):
            wave = Circle(radius=0.3, color=BLUE, stroke_width=2, stroke_opacity=0.7)
            wave.move_to(tx.get_center())
            waves.add(wave)
        
        # Animate waves expanding one after another
        for i, wave in enumerate(waves):
            self.play(
                wave.animate.scale(max_radius / 0.3).set_stroke(opacity=0.1),
                run_time=1.5,
                rate_func=linear
            )
            if i < len(waves) - 1:
                self.wait(0.3)
    
    def create_signal_bars(self, num_filled, color):
        """Create signal strength bars"""
        bars = VGroup()
        for i in range(4):
            height = 0.15 + i * 0.08
            bar = Rectangle(width=0.08, height=height, stroke_width=1)
            
            if i < num_filled:
                bar.set_fill(color, opacity=1).set_stroke(color, width=1)
            else:
                bar.set_fill(GRAY, opacity=0.3).set_stroke(GRAY, width=1)
            
            bars.add(bar)
        
        bars.arrange(RIGHT, buff=0.04)
        return bars

