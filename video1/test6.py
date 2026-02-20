from manim import *
import numpy as np

class InteractiveDistanceSlider(Scene):
    """Animation 9: Interactive distance slider - Memory Optimized"""
    
    def construct(self):
        # Title
        title = Text("Signal Strength vs Distance", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP, buff=0.3))
        
        # ===== SETUP TRANSMITTER AND RECEIVER =====
        # Transmitter (fixed position)
        transmitter = SVGMobject("tower.svg").scale(0.6)
        transmitter.move_to(LEFT * 5 + DOWN * 1)
        
        # Receiver (will move)
        receiver = SVGMobject("mobile.svg").scale(0.5)
        initial_distance = 2  # Start at 2 units
        receiver.move_to(LEFT * 5 + RIGHT * initial_distance + DOWN * 1)
        
        self.play(
            FadeIn(transmitter, scale=1.5),
            FadeIn(receiver, scale=1.5)
        )
        self.wait(0.5)
        
        # ===== STATIC DISPLAYS (Update manually) =====
        def get_distance():
            return np.linalg.norm(receiver.get_center() - transmitter.get_center())
        
        def calculate_received_power(distance):
            if distance < 0.1:
                distance = 0.1
            Pt = -30
            n = 2
            d0 = 1
            return Pt - 10 * n * np.log10(distance / d0)
        
        # Distance display
        distance_label = Text("Distance:", font_size=24, color=WHITE)
        distance_value = Text(f"{get_distance():.1f}m", font_size=28, color=BLUE, weight=BOLD)
        distance_display = VGroup(distance_label, distance_value).arrange(RIGHT, buff=0.2)
        distance_display.to_corner(UL, buff=0.8)
        
        # Power display
        power_label = Text("Power:", font_size=24, color=WHITE)
        power_value = Text(f"{calculate_received_power(get_distance()):.1f} dBm", 
                          font_size=28, color=YELLOW, weight=BOLD)
        power_display = VGroup(power_label, power_value).arrange(RIGHT, buff=0.2)
        power_display.to_corner(UR, buff=0.8)
        
        self.play(Write(distance_display), Write(power_display))
        
        # Signal bars (static, will update manually)
        bars = VGroup()
        for i in range(5):
            height = 0.3 + i * 0.15
            bar = Rectangle(width=0.2, height=height, stroke_width=2)
            bars.add(bar)
        bars.arrange(RIGHT, buff=0.1)
        bars.next_to(receiver, UP, buff=0.5)
        
        # Initial bar colors
        for i, bar in enumerate(bars):
            if i < 4:  # 4 bars at start (2m distance)
                bar.set_fill(GREEN, opacity=1).set_stroke(GREEN, width=2)
            else:
                bar.set_fill(GRAY, opacity=0.3).set_stroke(GRAY, width=2)
        
        self.play(FadeIn(bars))
        self.wait(1)
        
        # Helper function to update displays
        def update_displays():
            dist = get_distance()
            new_dist_value = Text(f"{dist:.1f}m", font_size=28, color=BLUE, weight=BOLD)
            new_power_value = Text(f"{calculate_received_power(dist):.1f} dBm", 
                                   font_size=28, color=YELLOW, weight=BOLD)
            new_dist_value.move_to(distance_value)
            new_power_value.move_to(power_value)
            
            # Update bars
            filled_bars = max(0, int((1 - dist/10) * 5))
            bar_anims = []
            for i, bar in enumerate(bars):
                if i < filled_bars:
                    bar_anims.append(bar.animate.set_fill(GREEN, opacity=1).set_stroke(GREEN, width=2))
                else:
                    bar_anims.append(bar.animate.set_fill(GRAY, opacity=0.3).set_stroke(GRAY, width=2))
            
            return new_dist_value, new_power_value, bar_anims
        
        # ===== ANIMATION SEQUENCE =====
        instruction = Text("Moving receiver away from transmitter...", 
                          font_size=22, color=WHITE).to_edge(DOWN, buff=0.5)
        self.play(Write(instruction))
        self.wait(0.5)
        
        # Move receiver away in stages
        distances = [4, 6, 8, 10]
        
        for target_distance in distances:
            target_pos = transmitter.get_center() + RIGHT * target_distance
            
            # Move receiver
            self.play(receiver.animate.move_to(target_pos), run_time=1.5)
            
            # Update all displays
            new_dist, new_power, bar_anims = update_displays()
            self.play(
                Transform(distance_value, new_dist),
                Transform(power_value, new_power),
                *bar_anims,
                run_time=0.5
            )
            
            # Move bars with receiver
            bars.next_to(receiver, UP, buff=0.5)
            self.wait(0.3)
        
        self.play(FadeOut(instruction))
        self.wait(1)
        
        # ===== SLIDER DEMONSTRATION =====
        conclusion = Text("Distance Control Slider", font_size=26, color=WHITE)
        conclusion.to_edge(DOWN, buff=1.8)
        
        # Slider track
        slider_track = Line(LEFT * 3, RIGHT * 3, color=GRAY, stroke_width=6)
        slider_track.next_to(conclusion, DOWN, buff=0.4)
        
        # Slider knob
        slider_knob = Circle(radius=0.15, color=BLUE, fill_opacity=1)
        slider_knob.move_to(slider_track.get_right())
        
        # Labels
        label_min = Text("2m", font_size=16, color=GRAY).next_to(slider_track.get_left(), DOWN, buff=0.2)
        label_max = Text("10m", font_size=16, color=GRAY).next_to(slider_track.get_right(), DOWN, buff=0.2)
        
        slider_group = VGroup(conclusion, slider_track, slider_knob, label_min, label_max)
        self.play(FadeIn(slider_group))
        self.wait(0.5)
        
        # Animate slider with receiver
        def move_to_distance(target_dist, run_time=2):
            target_pos = transmitter.get_center() + RIGHT * target_dist
            alpha = (target_dist - 2) / 8
            knob_target = slider_track.point_from_proportion(alpha)
            
            self.play(
                receiver.animate.move_to(target_pos),
                slider_knob.animate.move_to(knob_target),
                run_time=run_time
            )
            
            # Update displays
            new_dist, new_power, bar_anims = update_displays()
            bars.next_to(receiver, UP, buff=0.5)
            self.play(
                Transform(distance_value, new_dist),
                Transform(power_value, new_power),
                *bar_anims,
                run_time=0.3
            )
        
        # Sweep backward
        move_to_distance(2, run_time=2.5)
        self.wait(0.3)
        
        # Sweep forward
        move_to_distance(10, run_time=2.5)
        self.wait(0.3)
        
        # Final position
        move_to_distance(5, run_time=1.5)
        self.wait(1)
        self.play(FadeOut(bars))
        # Final summary
        summary = VGroup(
            Text("Key Observations:", font_size=24, color=WHITE, weight=BOLD),
            Text("• 2× distance → -6 dB loss", font_size=20, color=YELLOW),
            Text("• 10× distance → -20 dB loss", font_size=20, color=YELLOW),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        
        summary_box = SurroundingRectangle(summary, color=BLUE, buff=0.25, corner_radius=0.1)
        summary_group = VGroup(summary_box, summary)
        summary_group.scale(0.9).next_to(power_display, DOWN, buff=0.5).shift(LEFT * 0.5)
        
        self.play(FadeIn(summary_group, shift=UP * 0.3))
        self.wait(3)