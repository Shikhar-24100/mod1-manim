from manim import *
import numpy as np

class PulseRateMotivation(Scene):
    def construct(self):
        # 1. Setup the Timeline
        timeline = NumberLine(
            x_range=[0, 10, 1],
            length=10,
            color=WHITE,
            include_numbers=False,
            label_direction=DOWN
        ).shift(DOWN * 0.5)
        
        time_label = Text("Time", font_size=20).next_to(timeline, RIGHT)

        # 2. Function to create a clean rectangular pulse
        def get_rect_pulse(x_pos, width, color=BLUE):
            return Rectangle(
                width=width, 
                height=1.2, 
                fill_opacity=0.5, 
                fill_color=color, 
                stroke_width=2, 
                stroke_color=color
            ).move_to(timeline.n2p(x_pos)).shift(UP * 0.6) # Perfectly aligned above line

        # 3. Initial State: Low Data Rate (Wide pulses, far apart)
        # We start with 4 pulses spread out
        width_slow = 0.8
        positions_slow = [1.5, 4.0, 6.5, 9.0]
        pulses_slow = VGroup(*[get_rect_pulse(pos, width_slow) for pos in positions_slow])
        
        title = Text("Increasing the Data Rate...", font_size=32).to_edge(UP)

        self.add(timeline, time_label)
        self.play(FadeIn(pulses_slow, shift=UP))
        self.wait(2)
        self.play(Write(title))
        self.wait(1)

        # 4. Animate to High Data Rate (Thin pulses, packed tightly)
        # To pack them, we make them thinner (higher BW) and decrease spacing
        width_fast = 0.2
        # We increase the number of pulses to 15 to show the speed increase
        positions_fast = np.linspace(1, 9, 15)
        pulses_fast = VGroup(*[get_rect_pulse(pos, width_fast, color=YELLOW) for pos in positions_fast])
        
        # This text reflects your thought process
        quicker_text = Text("Transmission is quicker!", font_size=32).to_edge(UP)

        self.play(
            ReplacementTransform(pulses_slow, pulses_fast),
            ReplacementTransform(title, quicker_text),
            run_time=2.5
        )
        self.wait(1)

        # 5. The Doubt / The Question
        # As they are packed to the limit, we pose the question
        question = VGroup(
            Text("Then why can't we achieve", font_size=32),
            Text("INFINITE DATA RATE?", font_size=44, weight=BOLD, color=PINK)
        ).arrange(DOWN).to_edge(UP, buff=1.0)

        self.play(
            FadeOut(quicker_text),
            # Move the whole diagram down to give the question space
            VGroup(timeline, time_label, pulses_fast).animate.shift(DOWN * 1)
        )
        
        self.play(Write(question[0]))
        self.play(Write(question[1]), run_time=0.8)
        
        # Make the pulses "flicker" or turn red to show stress at the limit
        self.play(pulses_fast.animate.set_color(PINK), run_time=1)
        
        self.wait(4)