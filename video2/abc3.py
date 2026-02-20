from manim import *
import numpy as np

class DiffractionScene(Scene):
    def construct(self):
        # === TITLE ===
        self.wait(0.3)
        
        # === SETUP: TOWER, BUILDING (OBSTACLE), MOBILE IN SHADOW ===
        tower = SVGMobject("tower.svg").scale(0.7)
        tower.to_edge(LEFT, buff=1.2).shift(DOWN * 1.2)
        
        # Building as hill/obstacle - positioned centrally
        building = SVGMobject("building.svg").scale(1.2)
        building.move_to(ORIGIN + DOWN * 0.5)
        
        # Mobile in shadow zone (behind building)
        mobile = SVGMobject("mobile.svg").scale(0.5)
        mobile.to_edge(RIGHT, buff=1.2).shift(DOWN * 1.2)
        
        # Labels
        tower_label = Text("Tx", font_size=24, weight=BOLD).next_to(tower, DOWN, buff=0.2)
        mobile_label = Text("Rx", font_size=24, weight=BOLD).next_to(mobile, DOWN, buff=0.2)
        
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
            FadeIn(building, scale=0.9),
            run_time=0.6
        )
        self.wait(0.3)
        
        # === GET KEY POSITIONS ===
        tower_pos = tower.get_right()
        mobile_pos = mobile.get_left()
        building_top = building.get_top()  # Peak/edge where diffraction occurs
        
        # === SHOW BLOCKED DIRECT PATH ===
        blocked_path = DashedLine(
            tower_pos, mobile_pos,
            color=RED, stroke_width=4, dash_length=0.2
        )
        
        x_mark = Cross(scale_factor=0.4, color=RED, stroke_width=6)
        x_mark.move_to(building.get_center())
        x_mark.shift(DOWN*0.5)
        
        self.play(Create(blocked_path), run_time=0.6)
        self.play(
            FadeIn(x_mark, scale=1.5),
            blocked_path.animate.set_opacity(0.3),
            run_time=0.5
        )
        self.wait(0.3)
        
        # === LABEL: ORIGINAL SIGNAL ===
        label_original = Text("Original Signal", font_size=22, color=BLUE, weight=BOLD)
        label_original.move_to(tower_pos + UP * 2.2 + RIGHT * 1.5)
        self.play(FadeIn(label_original, shift=DOWN*0.2), run_time=0.4)
        
        # === CREATE ARC WAVEFRONTS APPROACHING BUILDING ===
        # These are semi-circular arcs emanating from tower, getting larger
        # They DON'T intersect with building - stop before hitting it
        
        num_waves = 6
        original_waves = VGroup()
        
        for i in range(num_waves):
            # Arc radius increases with each wave
            radius = 1.2 + i * 0.8
            
            # Create arc centered at tower position
            # Arc spans from bottom to top, approaching building but not intersecting
            arc = Arc(
                radius=radius,
                start_angle=-10 * DEGREES,
                angle=80 * DEGREES,
                color=BLUE,
                stroke_width=3,
                stroke_opacity=0.85
            )
            arc.move_arc_center_to(tower_pos)
            original_waves.add(arc)
        
        # Animate waves propagating from tower
        self.play(
            LaggedStart(*[
                Create(wave) for wave in original_waves
            ], lag_ratio=0.25),
            run_time=2.0
        )
        self.wait(0.5)
        
        # === MARK THE DIFFRACTION EDGE ===
        edge_dot = Dot(building_top, color=YELLOW, radius=0.12)
        edge_label = Text("Edge", font_size=20, color=YELLOW, weight=BOLD)
        edge_label.next_to(building_top, UP, buff=0.2)
        
        self.play(
            Flash(building_top, color=YELLOW, line_length=0.25, num_lines=8),
            FadeIn(edge_dot, scale=0.5),
            FadeIn(edge_label, shift=DOWN*0.2),
            run_time=0.6
        )
        self.wait(0.3)
        
        # === DIFFRACTED WAVES ===
        # Label for diffracted signal
        label_diffracted = Text("Diffracted Signal", font_size=22, color=YELLOW, weight=BOLD)
        label_diffracted.move_to(mobile_pos + UP * 2.2 + LEFT * 1.5)
        self.play(FadeIn(label_diffracted, shift=DOWN*0.2), run_time=0.4)
        
        # At the top of building (edge), waves split:
        # 1. Some continue straight (same direction) - BLUE
        # 2. Some bend downward toward receiver - YELLOW
        
        diffracted_waves = VGroup()
        
        # Create waves that:
        # - Start from the building edge
        # - Some go straight continuing original direction
        # - Some bend downward toward mobile
        
        for i in range(6):
            offset = i * 0.6
            
            # STRAIGHT CONTINUATION (Blue - original direction)
            # straight_arc = Arc(
            #     radius=1.0 + offset,
            #     start_angle=10 * DEGREES,
            #     angle=70 * DEGREES,
            #     color=BLUE,
            #     stroke_width=3,
            #     stroke_opacity=0.7 - i*0.1
            # )
            # straight_arc.move_arc_center_to(building_top)
            
            # BENT DOWNWARD (Yellow - diffracted toward receiver)
            # These arcs curve downward from the edge toward mobile
            bent_arc = Arc(
                radius=1.0 + offset,
                start_angle=-65* DEGREES,
                angle=85 * DEGREES,
                color=YELLOW,
                stroke_width=3,
                stroke_opacity=0.8 - i*0.12
            )

            bent_arc.move_arc_center_to(building_top)
            
            # diffracted_waves.add(straight_arc)
            diffracted_waves.add(bent_arc)
        
        # Animate diffracted waves appearing from the edge
        self.play(
            LaggedStart(*[
                Create(wave) for wave in diffracted_waves
            ], lag_ratio=0.15),
            run_time=2.0
        )
        self.wait(0.5)



        
        
        # === SHOW SIGNAL PATH WITH ANIMATED DOT ===
        # Path: Tower -> Edge -> Mobile (bends at edge)
        signal_path = VMobject()
        signal_path.set_points_as_corners([
            tower_pos,
            building_top,
            mobile_pos
        ])
        signal_path.make_smooth()
        
        signal_dot = Dot(color=GREEN, radius=0.15).set_sheen(-0.4, DOWN)
        signal_glow = Circle(radius=0.3, color=GREEN, fill_opacity=0.25, stroke_width=0)
        
        signal_dot.move_to(tower_pos)
        signal_glow.move_to(tower_pos)
        self.add(signal_glow, signal_dot)
        
        # Animate signal traveling and bending at edge
        self.play(
            MoveAlongPath(signal_dot, signal_path),
            signal_glow.animate.move_to(mobile_pos),
            run_time=2.0,
            rate_func=smooth
        )
        
        # Flash at receiver - signal received!
        self.play(
            Flash(mobile_pos, color=GREEN, line_length=0.3, num_lines=12),
            mobile.animate.scale(1.15),
            run_time=0.5
        )
        self.play(mobile.animate.scale(1/1.15), run_time=0.2)
        self.remove(signal_dot, signal_glow)
        
        self.wait(0.5)
        
        # === KEY INSIGHT TEXT ===
        self.play(
            FadeOut(edge_label),
            FadeOut(label_original),
            FadeOut(label_diffracted),
            FadeOut(blocked_path),
            FadeOut(x_mark),
            run_time=0.5
        )
        
        key_text = VGroup(
            Text("Waves bend around edges", font_size=30, color=WHITE),
            Text("Enables NLOS communication", font_size=28, color=WHITE)
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
        
        # Emphasize the bending effect - pulse yellow waves
        yellow_waves = VGroup(*[w for w in diffracted_waves if w.get_color() == ManimColor(YELLOW)])
        self.play(
            yellow_waves.animate.set_stroke(width=5, opacity=1),
            rate_func=there_and_back,
            run_time=0.9
        )
        
        self.wait(1.2)
        
        # === FADE OUT ===
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8
        )