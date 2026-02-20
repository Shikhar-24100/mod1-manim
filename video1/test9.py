from manim import *
import numpy as np

class ObstacleBlockingAnimation(Scene):
    """Animation 12: Obstacle Blocking with Shadow Casting - Improved Version"""
    
    def construct(self):
        # Title
        title = Text("Shadowing: Large-Scale Fading", font_size=42, weight=BOLD)
        subtitle = Text("What happens when obstacles block the signal?", font_size=26, color=BLUE)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(
            title.animate.scale(0.7).to_edge(UP, buff=0.3),
            FadeOut(subtitle)
        )
        
        # ========== SETUP SCENE ==========
        # Ground
        ground = Line(LEFT * 7, RIGHT * 7, color="#654321", stroke_width=3)
        ground.shift(DOWN * 2.5)
        self.play(Create(ground))
        
        # Transmitter (use SVG or fallback)
        try:
            tx = SVGMobject("tower.svg").scale(0.8)
        except:
            tx = VGroup(
                Rectangle(height=1.8, width=0.35, color=BLUE, fill_opacity=0.9),
                Triangle(color=YELLOW, fill_opacity=1).scale(0.35).rotate(PI/2).shift(UP * 0.95)
            )
        tx.shift(LEFT * 5.5 + DOWN * 1.9)
        
        # Receiver (use SVG or fallback)
        try:
            rx = SVGMobject("mobile.svg").scale(0.6)
        except:
            rx = VGroup(
                Rectangle(height=1.2, width=0.3, color=RED, fill_opacity=0.9),
                Triangle(color=ORANGE, fill_opacity=1).scale(0.3).rotate(-PI/2).shift(UP * 0.65)
            )
        rx.shift(RIGHT * 5.5 + DOWN * 1.9)
        
        tx_label = Text("Transmitter", font_size=18).next_to(tx, DOWN, buff=0.15)
        rx_label = Text("Receiver", font_size=18).next_to(rx, DOWN, buff=0.15)
        
        self.play(
            FadeIn(tx, scale=1.2),
            FadeIn(rx, scale=1.2),
            Write(tx_label),
            Write(rx_label)
        )
        self.wait(0.5)
        
        # Signal waves (multiple expanding arcs from transmitter)
        self.signal_waves = VGroup()
        self.create_signal_waves(tx)
        
        # LOS (Line of Sight) indicator
        los_line = DashedLine(
            tx.get_right() + RIGHT * 0.2,
            rx.get_left() + LEFT * 0.2,
            color=GREEN,
            stroke_width=2,
            dash_length=0.1
        )
        los_label = Text("LOS", font_size=16, color=GREEN).next_to(los_line, UP, buff=0.1)
        
        self.play(Create(los_line), Write(los_label))
        self.wait(0.5)
        
        # Signal strength meter
        strength_label = Text("Signal Strength:", font_size=22, color=WHITE)
        strength_label.to_corner(UR, buff=0.5).shift(DOWN * 0.3)
        
        strength_bar_bg = Rectangle(height=0.4, width=3.5, color=WHITE, stroke_width=3, fill_opacity=0)
        strength_bar_bg.next_to(strength_label, DOWN, buff=0.2)
        
        self.strength_bar = Rectangle(height=0.4, width=3.5, color=GREEN, fill_opacity=0.8, stroke_width=0)
        self.strength_bar.move_to(strength_bar_bg.get_center())
        self.strength_bar.align_to(strength_bar_bg, LEFT)
        
        self.strength_value = DecimalNumber(
            100, num_decimal_places=0, font_size=24, color=GREEN
        )
        self.strength_value.next_to(strength_bar_bg, RIGHT, buff=0.2)
        self.percent = Text("%", font_size=24, color=GREEN).next_to(self.strength_value, RIGHT, buff=0.1)
        
        self.play(
            Write(strength_label),
            Create(strength_bar_bg),
            FadeIn(self.strength_bar),
            Write(self.strength_value),
            Write(self.percent)
        )
        self.wait(1)
        
        # Store for later reference
        self.strength_bar_bg = strength_bar_bg
        self.los_line = los_line
        self.los_label = los_label
        
        # ========== INTRODUCE OBSTACLES ==========
        intro_text = Text("Obstacles enter the path...", font_size=28, color=YELLOW, slant=ITALIC)
        intro_text.move_to(ORIGIN).shift(UP * 2)
        self.play(Write(intro_text))
        self.wait(1)
        self.play(FadeOut(intro_text))
        
        # Create obstacles using SVG with fallbacks
        # Building
        try:
            building = SVGMobject("building.svg").scale(1.2)
            building.move_to(LEFT * 2 + DOWN * 0.9)
        except:
            building = Rectangle(height=2.2, width=0.7, color=GRAY, fill_opacity=0.9, stroke_color=WHITE)
            building.move_to(LEFT * 2 + DOWN * 1.4)
            windows = VGroup(*[
                Rectangle(height=0.12, width=0.12, color=YELLOW, fill_opacity=0.6)
                for _ in range(8)
            ]).arrange_in_grid(rows=4, cols=2, buff=0.12)
            windows.scale(0.65).move_to(building.get_center())
            building.add(windows)
        
        # Tree
        try:
            tree = SVGMobject("tree.svg").scale(1.0)
            tree.move_to(RIGHT * 1.2 + DOWN * 1.3)
        except:
            tree = VGroup(
                Rectangle(height=0.5, width=0.18, color="#8B4513", fill_opacity=1),
                Circle(radius=0.4, color=GREEN, fill_opacity=0.85),
                Circle(radius=0.32, color="#228B22", fill_opacity=0.7).shift(UL * 0.15),
            )
            tree[1].next_to(tree[0], UP, buff=-0.15)
            tree[2].move_to(tree[1].get_center())
            tree.move_to(RIGHT * 1.2 + DOWN * 2.05)
        
        # Person (instead of hill)
        try:
            person = SVGMobject("person.svg").scale(0.8)
            person.move_to(RIGHT * 3.8 + DOWN * 1.8)
        except:
            # Simple person silhouette
            person = VGroup(
                Circle(radius=0.15, color=BLUE, fill_opacity=0.9),  # Head
                Rectangle(height=0.6, width=0.3, color=BLUE, fill_opacity=0.9),  # Body
                Rectangle(height=0.5, width=0.08, color=BLUE, fill_opacity=0.9).shift(DOWN * 0.5 + LEFT * 0.15),  # Left leg
                Rectangle(height=0.5, width=0.08, color=BLUE, fill_opacity=0.9).shift(DOWN * 0.5 + RIGHT * 0.15),  # Right leg
            )
            person[0].next_to(person[1], UP, buff=0.05)
            person.move_to(RIGHT * 3.8 + DOWN * 1.8)
        
        # Animate obstacles with improved shadowing
        self.introduce_obstacle(building, tx, rx, "Building", 60, YELLOW)
        self.wait(1)
        
        self.introduce_obstacle(tree, tx, rx, "Tree", 30, ORANGE)
        self.wait(1)
        
        self.introduce_obstacle(person, tx, rx, "Person", 10, RED)
        
        # Warning message
        warning = VGroup(
            # Text("⚠️ Signal Severely Blocked!", font_size=32, color=RED, weight=BOLD),
            Text("This is SHADOWING - Non-Line-of-Sight (NLOS)", font_size=28, color=WHITE)
        ).arrange(DOWN, buff=0.2)
        warning.to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(warning, shift=UP))
        self.wait(2)
        
        # Show X mark on blocked LOS
        x_mark = VGroup(
            Line(UL * 0.3, DR * 0.3, color=RED, stroke_width=5),
            Line(UR * 0.3, DL * 0.3, color=RED, stroke_width=5)
        )
        x_mark.move_to(self.los_line.get_center())
        self.play(Create(x_mark), self.los_line.animate.set_color(RED), self.los_label.animate.set_color(RED))
        
        self.wait(10)
    
    def create_signal_waves(self, transmitter):
        """Create animated signal waves emanating from transmitter"""
        for i in range(3):
            arc = Arc(
                radius=0.5 + i * 0.3,
                angle=PI,
                color=YELLOW,
                stroke_width=2,
                stroke_opacity=0.7
            )
            arc.rotate(-PI/2)
            arc.move_arc_center_to(transmitter.get_right() + RIGHT * 0.2)
            self.signal_waves.add(arc)
        
        # Animate waves expanding
        self.play(
            *[
                Succession(
                    Wait(i * 0.3),
                    arc.animate.scale(2).set_stroke(opacity=0.1),
                    run_time=2
                )
                for i, arc in enumerate(self.signal_waves)
            ]
        )
    
    def introduce_obstacle(self, obstacle, tx, rx, name, strength_percent, color):
        """Introduce an obstacle with shadowing effect"""
        # Slide in from bottom
        original_pos = obstacle.get_center()
        obstacle.shift(DOWN * 4)
        
        self.play(
            obstacle.animate.move_to(original_pos),
            run_time=1.5,
            rate_func=smooth
        )
        
        # Create shadow zone (visual representation)
        shadow = self.create_shadow_zone(obstacle, tx, rx)
        
        self.play(
            FadeIn(shadow, scale=0.8),
            run_time=0.8
        )
        
        # Add obstacle label
        label = Text(name, font_size=16, color=WHITE).next_to(obstacle, UP, buff=0.2)
        self.play(Write(label))
        
        # Update signal strength
        new_width = 3.5 * (strength_percent / 100)
        new_strength = Rectangle(
            height=0.4, 
            width=new_width, 
            color=color, 
            fill_opacity=0.8, 
            stroke_width=0
        )
        new_strength.move_to(self.strength_bar_bg.get_center())
        new_strength.align_to(self.strength_bar_bg, LEFT)
        
        # Animate signal reduction with visual feedback
        self.play(
            Transform(self.strength_bar, new_strength),
            self.strength_value.animate.set_value(strength_percent).set_color(color),
            self.percent.animate.set_color(color),
            Flash(self.strength_value, color=color, flash_radius=0.5),
            run_time=1.5
        )
        
        # Add blocked signal indicator
        if strength_percent <= 30:
            blocked_text = Text("BLOCKED!", font_size=20, color=RED, weight=BOLD)
            blocked_text.next_to(obstacle, DOWN, buff=0.1)
            self.play(Write(blocked_text))
    
    def create_shadow_zone(self, obstacle, tx, rx):
        """Create a visual shadow zone behind the obstacle"""
        # Get obstacle boundaries
        obstacle_left = obstacle.get_left()
        obstacle_right = obstacle.get_right()
        obstacle_top = obstacle.get_top()
        obstacle_bottom = obstacle.get_bottom()
        
        tx_pos = tx.get_right()
        
        # Calculate shadow projection
        # Project rays from transmitter through obstacle edges
        def project_point(obstacle_point, distance=5):
            direction = normalize(obstacle_point - tx_pos)
            return obstacle_point + direction * distance
        
        # Create shadow polygon
        shadow = Polygon(
            obstacle_top,
            project_point(obstacle_top, 4),
            project_point(obstacle_bottom, 4),
            obstacle_bottom,
            color=BLACK,
            fill_opacity=0.6,
            stroke_width=0
        )
        
        # Add hatching pattern to make shadow more visible
        hatches = VGroup()
        for i in range(10):
            t = i / 9
            start = obstacle_top + t * (obstacle_bottom - obstacle_top)
            end = project_point(obstacle_top, 4) + t * (project_point(obstacle_bottom, 4) - project_point(obstacle_top, 4))
            hatch = Line(start, end, color=RED, stroke_width=1, stroke_opacity=0.4)
            hatches.add(hatch)
        
        return VGroup(shadow, hatches)


# To render this animation:
# manim -pql improved_shadowing.py ObstacleBlockingAnimation
#
# Make sure tower.svg, mobile.svg, building.svg, tree.svg, and person.svg 
# are in the same directory, or the code will use fallback graphics