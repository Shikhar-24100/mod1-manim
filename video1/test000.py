from manim import *
import numpy as np




class ShadowingAnswer(Scene):
    """The Answer - Showing reflection and shadowing effects"""
    
    def construct(self):
        # Simple title
        title = Text("The Answer", font_size=36, color=WHITE, weight=BOLD)
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
        self.play(FadeIn(tx))
        self.wait(0.5)
        
        # Two mobiles on outer circle
        mobile_radius = 3.0
        mobile1_angle = 45 * DEGREES
        mobile2_angle = 225 * DEGREES
        
        # Mobile 1 (top-right)
        try:
            mobile1 = SVGMobject("mobile.svg").scale(0.35)
        except:
            mobile1 = Rectangle(height=0.4, width=0.2, color=GREEN, fill_opacity=1)
        
        x1 = mobile_radius * np.cos(mobile1_angle)
        y1 = mobile_radius * np.sin(mobile1_angle)
        mobile1.move_to([x1, y1, 0])
        
        bars1 = self.create_signal_bars(4, GREEN)
        bars1.next_to(mobile1, UP, buff=0.2)
        mobile1_group = VGroup(mobile1, bars1)
        
        # Mobile 2 (bottom-left)
        try:
            mobile2 = SVGMobject("mobile.svg").scale(0.35)
        except:
            mobile2 = Rectangle(height=0.4, width=0.2, color=RED, fill_opacity=1)
        
        x2 = mobile_radius * np.cos(mobile2_angle)
        y2 = mobile_radius * np.sin(mobile2_angle)
        mobile2.move_to([x2, y2, 0])
        
        bars2 = self.create_signal_bars(1, RED)
        bars2.next_to(mobile2, DOWN, buff=0.2)
        mobile2_group = VGroup(mobile2, bars2)
        
        self.play(FadeIn(mobile1_group), FadeIn(mobile2_group))
        self.wait(1)
        
        # Draw signal paths (dashed lines)
        path1 = DashedLine(tx.get_center(), mobile1.get_center(), color=GREEN, stroke_width=2)
        path2 = DashedLine(tx.get_center(), mobile2.get_center(), color=RED, stroke_width=2)
        
        self.play(Create(path1), Create(path2))
        self.wait(1)
        
        # ========== EFFECT 1: REFLECTION (Car for mobile 1) ==========
        effect_label = Text("1. Reflection", font_size=24, color=BLUE)
        effect_label.to_edge(DOWN, buff=0.5)
        self.play(Write(effect_label))
        
        # Add car on path to mobile 1 (slightly off to side)
        try:
            car = SVGMobject("car.svg").scale(0.28)
        except:
            car = Rectangle(height=0.3, width=0.6, color=GRAY, fill_opacity=0.8)
        
        # Position car between tower and mobile1, slightly offset
        car_pos = (tx.get_center() + mobile1.get_center()) / 2 + UP * 0.5
        car.move_to(car_pos)
        
        self.play(FadeIn(car, scale=1.3))
        self.wait(0.5)
        
        # Show reflection path
        reflection_path = VGroup(
            Line(tx.get_center(), car.get_center(), color=BLUE, stroke_width=2),
            Arrow(car.get_center(), mobile1.get_center(), color=BLUE, stroke_width=2, 
                  max_tip_length_to_length_ratio=0.2)
        )
        
        self.play(
            path1.animate.set_opacity(0.3),
            Create(reflection_path)
        )
        self.wait(1.5)
        
        # ========== EFFECT 2: SHADOWING (Building for mobile 2) ==========
        self.play(FadeOut(effect_label))
        effect_label = Text("2. Shadowing", font_size=24, color=RED, weight=BOLD)
        effect_label.to_edge(DOWN, buff=0.5)
        self.play(Write(effect_label))
        
        # Add building blocking path to mobile 2
        try:
            building = SVGMobject("building.svg").scale(0.5)
        except:
            building = Rectangle(height=1.0, width=0.4, color=GRAY, fill_opacity=0.8)
        
        # Position building between tower and mobile2
        building_pos = (tx.get_center() + mobile2.get_center()) / 2
        building.move_to(building_pos)
        
        self.play(FadeIn(building, scale=1.3))
        self.wait(0.5)
        
        # Show blocked signal (X mark)
        x_mark = VGroup(
            Line(UL * 0.3, DR * 0.3, color=RED, stroke_width=4),
            Line(UR * 0.3, DL * 0.3, color=RED, stroke_width=4)
        )
        x_mark.move_to(building_pos)
        
        self.play(
            path2.animate.set_stroke(RED, width=3, opacity=1),
            Create(x_mark),
            Flash(x_mark, color=RED, line_length=0.4, num_lines=8)
        )
        self.wait(1)
        
        # Shadow zone behind building
        shadow = Polygon(
            building.get_top(),
            building.get_top() + (mobile2.get_center() - building.get_center()) * 1.5,
            building.get_bottom() + (mobile2.get_center() - building.get_center()) * 1.5,
            building.get_bottom(),
            color=BLACK,
            fill_opacity=0.5,
            stroke_width=0
        )
        
        self.play(FadeIn(shadow))
        self.wait(1.5)
        
        # ========== FINAL SUMMARY ==========
        self.play(FadeOut(effect_label))
        
        summary = VGroup(
            Text("Mobile 1: Reflection → Strong signal", font_size=18, color=GREEN),
            Text("Mobile 2: Shadowing → Weak signal", font_size=18, color=RED, weight=BOLD)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.to_edge(DOWN, buff=0.5)
        summary.shift(RIGHT* 0.8)
        
        self.play(Write(summary))
        self.wait(3)
    
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


# To render:
# manim -pql shadowing_intro_payoff.py ShadowingIntroduction
# manim -pql shadowing_intro_payoff.py ShadowingAnswer