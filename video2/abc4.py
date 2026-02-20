from manim import *
import numpy as np

class ScatteringScene(Scene):
    def construct(self):
        # === TITLE ===
        self.wait(0.3)
        
        # === SETUP: TOWER, TREE (SCATTERER), MOBILE ===
        tower = SVGMobject("tower.svg").scale(0.7)
        tower.to_edge(LEFT, buff=1.5).shift(DOWN * 1)
        
        mobile = SVGMobject("mobile.svg").scale(0.5)
        mobile.to_edge(RIGHT, buff=1.5).shift(DOWN * 1)
        
        # Tree as rough/irregular scattering object
        tree = SVGMobject("tree.svg").scale(1.0)
        tree.move_to(ORIGIN + DOWN * 0.5)
        
        # Labels
        tower_label = Text("Tx", font_size=24, weight=BOLD).next_to(tower, DOWN, buff=0.2)
        mobile_label = Text("Rx", font_size=24, weight=BOLD).next_to(mobile, DOWN, buff=0.2)
        tree_label = Text("Rough Object", font_size=20, color=GREEN, weight=BOLD)
        tree_label.next_to(tree, DOWN, buff=0.3)
        
        # Show scene elements
        self.play(
            FadeIn(tower, shift=RIGHT*0.3),
            FadeIn(mobile, shift=LEFT*0.3),
            run_time=0.7
        )
        self.play(
            Write(tower_label),
            Write(mobile_label),
            run_time=0.5
        )
        self.play(
            FadeIn(tree, scale=0.9),
            FadeIn(tree_label, shift=UP*0.2),
            run_time=0.6
        )
        self.wait(0.3)
        
        # === GET KEY POSITIONS ===
        tower_pos = tower.get_right()
        mobile_pos = mobile.get_left()
        tree_center = tree.get_center()
        
        # === INCOMING SIGNAL - SINGLE STRONG ARROW ===
        incoming_arrow = Arrow(
            tower_pos,
            tree_center + LEFT * 0.8,
            color=BLUE,
            stroke_width=6,
            buff=0,
            max_tip_length_to_length_ratio=0.15
        )
        
        incoming_label = Text("Incoming Signal", font_size=20, color=BLUE, weight=BOLD)
        incoming_label.next_to(incoming_arrow, UP, buff=0.2)
        
        self.play(
            GrowArrow(incoming_arrow),
            FadeIn(incoming_label, shift=DOWN*0.2),
            run_time=0.8
        )
        
        # Signal dot traveling to tree
        signal_dot = Dot(color=BLUE, radius=0.15).set_sheen(-0.4, DOWN)
        signal_glow = Circle(radius=0.3, color=BLUE, fill_opacity=0.3, stroke_width=0)
        
        signal_dot.move_to(tower_pos)
        signal_glow.move_to(tower_pos)
        self.add(signal_glow, signal_dot)
        
        self.play(
            MoveAlongPath(signal_dot, incoming_arrow),
            signal_glow.animate.move_to(tree_center),
            run_time=1.0,
            rate_func=smooth
        )
        
        # Impact flash at tree
        self.play(
            Flash(tree_center, color=YELLOW, line_length=0.4, num_lines=16),
            tree.animate.scale(1.08),
            run_time=0.4
        )
        self.play(tree.animate.scale(1/1.08), run_time=0.2)
        self.remove(signal_dot, signal_glow)
        
        self.wait(0.3)
        
        # === SCATTERED SIGNALS - MANY SMALL ARROWS IN VARIOUS DIRECTIONS ===
        scattered_label = Text("Scattered Signals", font_size=20, color=YELLOW, weight=BOLD)
        scattered_label.move_to(tree_center + UP * 2.5)
        
        self.play(FadeIn(scattered_label, shift=DOWN*0.2), run_time=0.4)
        
        # Create multiple small arrows going in random directions
        num_scattered = 16
        scattered_arrows = VGroup()
        
        # Generate scattered arrows in various directions
        for i in range(num_scattered):
            # Random angle for scattering (360 degrees around tree)
            angle = i * (360 / num_scattered) * DEGREES + np.random.uniform(-10, 10) * DEGREES
            
            # Random length (but generally small - weak signals)
            length = np.random.uniform(0.8, 1.5)
            
            # Direction vector
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            
            # Start slightly away from tree center to avoid overlap
            start_point = tree_center + direction * 0.4
            end_point = start_point + direction * length
            
            # Create small arrow with random opacity (showing varying strengths)
            arrow = Arrow(
                start_point,
                end_point,
                color=YELLOW,
                stroke_width=3,
                buff=0,
                max_tip_length_to_length_ratio=0.2,
                stroke_opacity=np.random.uniform(0.5, 0.9)
            )
            
            scattered_arrows.add(arrow)
        
        # Animate scattered arrows appearing in all directions
        self.play(
            LaggedStart(*[
                GrowArrow(arrow) for arrow in scattered_arrows
            ], lag_ratio=0.05),
            run_time=1.5
        )
        
        self.wait(0.5)
        
        # === EXTEND SOME SCATTERED ARROWS TO REACH RECEIVER ===
        # Create 3-4 extended arrows from tree scatter points to mobile
        extended_paths = VGroup()
        
        # Select scattered arrows that point toward mobile direction
        angles_to_mobile = [
            -20 * DEGREES,  # Slightly above mobile
            0 * DEGREES,    # Directly at mobile
            20 * DEGREES,   # Slightly below mobile
        ]
        
        for angle in angles_to_mobile:
            # Find the scattered arrow closest to this angle
            target_direction = np.array([np.cos(angle), np.sin(angle), 0])
            
            # Start from edge of tree scatter
            start_point = tree_center + target_direction * 0.4
            
            # Extended arrow reaching all the way to mobile
            extended_arrow = Arrow(
                start_point,
                mobile_pos,
                color=GREEN,
                stroke_width=4,
                buff=0.1,
                max_tip_length_to_length_ratio=0.1,
                stroke_opacity=0.8
            )
            extended_paths.add(extended_arrow)
        
        # Show extended paths growing from tree to mobile
        self.play(
            LaggedStart(*[
                GrowArrow(arrow) for arrow in extended_paths
            ], lag_ratio=0.2),
            run_time=1.0
        )
        
        self.wait(0.3)
        
        # Show signal dots traveling along these extended paths to mobile
        dots = VGroup()
        for arrow in extended_paths:
            dot = Dot(color=GREEN, radius=0.1)
            dot.move_to(arrow.get_start())
            dots.add(dot)
            self.add(dot)
        
        self.play(
            *[MoveAlongPath(dot, arrow) for dot, arrow in zip(dots, extended_paths)],
            run_time=1.2,
            rate_func=smooth
        )
        
        # Flash at receiver
        self.play(
            Flash(mobile_pos, color=GREEN, line_length=0.3, num_lines=12),
            mobile.animate.scale(1.12),
            run_time=0.5
        )
        self.play(mobile.animate.scale(1/1.12), run_time=0.2)
        self.remove(dots)
        
        self.wait(0.4)
        
        # === KEY INSIGHT TEXT ===
        self.play(
            FadeOut(incoming_label),
            FadeOut(scattered_label),
            FadeOut(tree_label),
            run_time=0.5
        )
        
        key_text = VGroup(
            Text("Rough/small objects", font_size=28, color=WHITE),
            Text("Many weak scattered paths", font_size=28, color=WHITE)
        ).arrange(DOWN, buff=0.25)
        key_text.to_edge(DOWN, buff=0.5)
        
        self.play(
            FadeIn(key_text[0], shift=UP*0.2),
            run_time=0.6
        )
        self.wait(0.2)
        self.play(
            FadeIn(key_text[1], shift=UP*0.2),
            run_time=0.6
        )
        
        # Emphasize scattered arrows
        self.play(
            scattered_arrows.animate.set_stroke(width=4, opacity=1),
            rate_func=there_and_back,
            run_time=0.9
        )
        
        self.wait(1.2)
        
        # === FADE OUT ===
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8
        )