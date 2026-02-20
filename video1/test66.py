from manim import *
import numpy as np

class InteractiveDistanceSlider(Scene):
    """Simpler: stationary signal bars under title, moving device + slider"""

    def construct(self):
        # Title
        title = Text("Signal Strength vs Distance", font_size=36)
        self.play(Write(title))
        self.wait(0.3)
        self.play(title.animate.to_edge(UP, buff=0.3))

        # ===== STATIONARY SIGNAL BARS (below title) =====
        bars = VGroup()
        for i in range(5):
            height = 0.25 + i * 0.12
            bar = Rectangle(width=0.18, height=height, stroke_width=2)
            bars.add(bar)
        bars.arrange(RIGHT, buff=0.08)
        # place bars under title and centered horizontally
        bars.next_to(title, DOWN, buff=0.18)
        # initial fill
        for i, bar in enumerate(bars):
            if i < 4:
                bar.set_fill(GREEN, opacity=1).set_stroke(GREEN, width=2)
            else:
                bar.set_fill(GRAY, opacity=0.3).set_stroke(GRAY, width=2)
        self.play(FadeIn(bars))
        self.wait(0.2)

        # ===== TRANSMITTER (left) =====
        try:
            transmitter = SVGMobject("tower.svg").scale(0.5)
        except Exception:
            transmitter = Triangle(color=BLUE, fill_opacity=1).scale(0.35).rotate(-PI/2)
        transmitter.move_to(LEFT * 5 + DOWN * 1)
        self.play(FadeIn(transmitter))
        self.wait(0.1)

        # ===== RECEIVER (mobile) - moves left->right =====
        try:
            receiver = SVGMobject("mobile.svg").scale(0.45)
        except Exception:
            receiver = Rectangle(height=0.45, width=0.22, color=RED, fill_opacity=1)
        initial_distance = 2
        receiver.move_to(LEFT * 5 + RIGHT * initial_distance + DOWN * 1)
        self.play(FadeIn(receiver))
        self.wait(0.2)

        # ===== DISPLAYS =====
        def get_distance():
            return np.linalg.norm(receiver.get_center() - transmitter.get_center())

        def calculate_received_power(distance):
            distance = max(distance, 0.1)
            Pt = -30
            n = 2
            d0 = 1
            return Pt - 10 * n * np.log10(distance / d0)

        distance_label = Text("Distance:", font_size=20)
        distance_value = Text(f"{get_distance():.1f}m", font_size=24, color=BLUE, weight=BOLD)
        distance_display = VGroup(distance_label, distance_value).arrange(RIGHT, buff=0.15)
        distance_display.to_corner(UL, buff=0.6)

        power_label = Text("Power:", font_size=20)
        power_value = Text(f"{calculate_received_power(get_distance()):.1f} dBm", font_size=24, color=YELLOW, weight=BOLD)
        power_display = VGroup(power_label, power_value).arrange(RIGHT, buff=0.15)
        power_display.to_corner(UR, buff=0.6)

        self.play(Write(distance_display), Write(power_display))
        self.wait(0.2)

        # ===== ANIMATE RECEIVER & UPDATE BARS (bars stay stationary) =====
        def set_bar_anims_for_distance(dist):
            filled_bars = int(np.clip((1 - dist / 10) * 5, 0, 5))
            anims = []
            for i, bar in enumerate(bars):
                if i < filled_bars:
                    anims.append(bar.animate.set_fill(GREEN, opacity=1).set_stroke(GREEN, width=2))
                else:
                    anims.append(bar.animate.set_fill(GRAY, opacity=0.3).set_stroke(GRAY, width=2))
            return anims

        def move_receiver_to_distance(target_distance, run_time=1.2):
            target_pos = transmitter.get_center() + RIGHT * target_distance
            # create updated text objects
            new_dist = Text(f"{target_distance:.1f}m", font_size=24, color=BLUE, weight=BOLD).move_to(distance_value.get_center())
            power = calculate_received_power(target_distance)
            new_pow = Text(f"{power:.1f} dBm", font_size=24, color=YELLOW, weight=BOLD).move_to(power_value.get_center())
            # bar fill animations (no movement)
            bar_anims = set_bar_anims_for_distance(target_distance)
            # animate receiver and displays and bar fills together
            self.play(
                receiver.animate.move_to(target_pos),
                Transform(distance_value, new_dist),
                Transform(power_value, new_pow),
                *bar_anims,
                run_time=run_time
            )

        # simple left->right demo
        sequence = [2, 4, 6, 8, 10]
        for d in sequence:
            move_receiver_to_distance(d, run_time=1)
            self.wait(0.15)

        # ===== SLIDER (controls same motion) =====
        slider_label = Text("Distance Control", font_size=22).to_edge(DOWN, buff=0.8)
        slider_track = Line(LEFT * 3, RIGHT * 3, color=GRAY, stroke_width=6).next_to(slider_label, DOWN, buff=0.25)
        slider_knob = Circle(radius=0.14, color=BLUE, fill_opacity=1).move_to(slider_track.get_right())
        label_min = Text("2m", font_size=14, color=GRAY).next_to(slider_track.get_left(), DOWN, buff=0.15)
        label_max = Text("10m", font_size=14, color=GRAY).next_to(slider_track.get_right(), DOWN, buff=0.15)
        self.play(FadeIn(slider_label, slider_track, slider_knob, label_min, label_max))
        self.wait(0.2)

        def slider_move_to(target_dist, run_time=1.5):
            # clamp and compute knob position
            target_dist = float(np.clip(target_dist, 2.0, 10.0))
            alpha = (target_dist - 2) / 8
            knob_target = slider_track.point_from_proportion(alpha)
            # prepare transforms & bar fills
            new_dist = Text(f"{target_dist:.1f}m", font_size=24, color=BLUE, weight=BOLD).move_to(distance_value.get_center())
            pow_val = calculate_received_power(target_dist)
            new_pow = Text(f"{pow_val:.1f} dBm", font_size=24, color=YELLOW, weight=BOLD).move_to(power_value.get_center())
            bar_anims = set_bar_anims_for_distance(target_dist)
            # animate receiver (only), knob, texts and fills together for exact synchronization
            target_pos = transmitter.get_center() + RIGHT * target_dist
            self.play(
                receiver.animate.move_to(target_pos),
                slider_knob.animate.move_to(knob_target),
                Transform(distance_value, new_dist),
                Transform(power_value, new_pow),
                *bar_anims,
                run_time=run_time
            )

        slider_move_to(2, run_time=1.2)
        self.wait(0.2)
        slider_move_to(10, run_time=1.6)
        self.wait(0.2)
        slider_move_to(5, run_time=1.0)
        self.wait(0.6)

        # summary
        summary = VGroup(
            Text("Key Observations:", font_size=20, weight=BOLD),
            Text("• 2× distance → −6 dB (approx.)", font_size=18, color=YELLOW),
            Text("• 10× distance → −20 dB (approx.)", font_size=18, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        summary.next_to(power_display, DOWN, buff=0.4).shift(LEFT * 0.2)
        self.play(FadeIn(summary))
        self.wait(2)