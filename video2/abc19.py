from manim import *
import numpy as np

class SignalStrengthMysteryIntro(Scene):
    def construct(self):
        # ================================================
        # PART A: TITLE - THE MYSTERY
        # ================================================
        
        main_title = Title("The Signal Strength Mystery").scale(0.9)
        main_title.to_edge(UP, buff=0.5)
        
        self.play(Write(main_title), run_time=1.0)
        self.wait(0.5)
        
        # ================================================
        # PART B: THE SCENARIO - PERSON WITH PHONE AND TOWER
        # ================================================
        
        # Tower on the left
        tower = SVGMobject("tower.svg").scale(0.6)
        tower.to_edge(LEFT, buff=1.5).shift(UP * 0.5)
        
        # Person with phone on the right
        person = SVGMobject("man_with_phone.svg").scale(0.8)
        person.to_edge(RIGHT, buff=2.5).shift(DOWN * 0.5)
        
        # Signal bars icon above person (starting with full signal)
        signal_bars = VGroup()
        bar_heights = [0.3, 0.4, 0.5, 0.6, 0.7]
        for i, height in enumerate(bar_heights):
            bar = Rectangle(
                height=height,
                width=0.15,
                fill_color=GREEN,
                fill_opacity=1,
                stroke_width=0
            )
            bar.shift(RIGHT * i * 0.2)
            signal_bars.add(bar)
        
        signal_bars.arrange(RIGHT, buff=0.05)
        signal_bars.next_to(person, UP, buff=0.3).shift(LEFT * 0.3)
        
        # Show the scene
        self.play(
            FadeIn(tower),
            FadeIn(person),
            FadeIn(signal_bars),
            run_time=1.0
        )
        
        self.wait(0.5)
        
        # Signal waves from tower to person
        signal_wave = Line(
            tower.get_right(),
            person.get_left(),
            color=BLUE,
            stroke_width=3
        )
        
        # Animated signal transmission
        for _ in range(3):
            self.play(
                Create(signal_wave),
                run_time=0.5
            )
            self.play(
                FadeOut(signal_wave),
                run_time=0.3
            )
        
        self.wait(5.3)
        
        # ================================================
        # PART C: TINY MOVEMENT - BIG CHANGE
        # ================================================
        
        # Text: "You move just a little..."
        move_text = Text(
            "If you move just a little...",
            font_size=32,
            color=WHITE
        ).to_edge(DOWN, buff=2.0)
        
        self.play(Write(move_text), run_time=0.8)
        
        # Show small movement distance indicator
        start_pos = person.get_center()
        end_pos = start_pos + RIGHT * 0.5
        
        movement_arrow = Arrow(
            start_pos + DOWN * 1.2,
            end_pos + DOWN * 1.2,
            color=YELLOW,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.3
        )
        
        distance_label = Text("eg: 10 cm", font_size=20, color=YELLOW)
        distance_label.next_to(movement_arrow, DOWN, buff=0.1)
        
        self.play(
            GrowArrow(movement_arrow),
            Write(distance_label),
            run_time=0.6
        )
        
        # Animate person moving slightly
        self.play(
            person.animate.shift(RIGHT * 0.5),
            signal_bars.animate.shift(RIGHT * 0.5),
            run_time=1.0
        )
        
        self.wait(0.3)
        
        # ================================================
        # PART D: SIGNAL DROPS DRAMATICALLY
        # ================================================
        
        # Fade out movement indicators
        self.play(
            FadeOut(move_text),
            FadeOut(movement_arrow),
            FadeOut(distance_label),
            run_time=0.4
        )
        
        # Show signal trying to reach
        weak_signal = DashedLine(
            tower.get_right(),
            person.get_left(),
            color=RED,
            stroke_width=3,
            dash_length=0.15
        )
        
        self.play(Create(weak_signal), run_time=0.6)
        
        # Signal bars drop dramatically (with animation)
        new_signal_bars = VGroup()
        new_bar_heights = [0.3, 0, 0, 0, 0]  # Only 1 bar remaining
        new_colors = [RED, GRAY, GRAY, GRAY, GRAY]
        
        for i, (height, color) in enumerate(zip(new_bar_heights, new_colors)):
            if height > 0:
                bar = Rectangle(
                    height=height,
                    width=0.15,
                    fill_color=color,
                    fill_opacity=1,
                    stroke_width=0
                )
            else:
                bar = Rectangle(
                    height=0.3,
                    width=0.15,
                    fill_color=color,
                    fill_opacity=0.3,
                    stroke_width=1,
                    stroke_color=color
                )
            bar.shift(RIGHT * i * 0.2)
            new_signal_bars.add(bar)
        
        new_signal_bars.arrange(RIGHT, buff=0.05)
        new_signal_bars.move_to(signal_bars.get_center())
        
        # Drop animation with shake
        self.play(
            Transform(signal_bars, new_signal_bars),
            # person.animate.scale(0.95).set_color(RED),
            run_time=0.8
        )
        # self.play(
        #     person.animate.scale(1/0.95).set_color(WHITE),
        #     run_time=0.3
        # )
        
        # Add "No Signal!" or weak signal indicator
        exclamation = Text("Signal Dropped!!", font_size=19, color=RED, weight=BOLD)
        exclamation.next_to(signal_bars, RIGHT, buff=0.3)
        
        self.play(Write(exclamation), run_time=0.5)
        
        self.wait(5.0)
        
        # ================================================
        # PART E: THE BIG QUESTION
        # ================================================
        
        # Fade out everything except title
        # self.play(
        #     FadeOut(tower),
        #     FadeOut(person),
        #     FadeOut(signal_bars),
        #     FadeOut(weak_signal),
        #     FadeOut(exclamation),
        #     run_time=0.6
        # )
        
        self.wait(5.3)
        
        # The central question
        question = VGroup(
            Text("Why does signal strength", font_size=22, color=WHITE),
            Text("change so dramatically", font_size=22, color=YELLOW, weight=BOLD),
            Text("with such small movements?", font_size=22, color=WHITE)
        ).arrange(DOWN, buff=0.3)
        question.to_edge(DOWN, buff=1.5)
        
        self.play(Write(question), run_time=2.0)
        
        self.wait(4.0)
        
        