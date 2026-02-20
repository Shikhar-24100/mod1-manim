from manim import *
import numpy as np
import random

class Part1_Cellular_Evolution_2D(Scene):
    def construct(self):
        # Main title
        title = Text("Lecture 6: Interference and Orthogonality", font_size=40)
        subtitle = Text("From Single Cell to Cellular System", font_size=32, color=BLUE)
        subtitle.next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Scene 1: 1G System Introduction
        self.first_generation_intro()
        
        # Scene 2: Voice frequency requirements
        self.voice_frequency_analysis()
        
        
        
        self.wait(2)

    def first_generation_intro(self):
        """Introduce 1G communication system"""
        # Title
        gen_title = Text("1G Mobile Communication System", font_size=36, color=WHITE)
        gen_title.to_edge(UP)
        self.play(Write(gen_title))
        self.wait(0.5)

        # CHANGE 2: Emphasize focus on voice transmission only
        focus_text = Text("Focus: Voice Transmission Only", font_size=28, color=YELLOW)
        focus_text.next_to(gen_title, DOWN, buff=0.4)
        self.play(Write(focus_text))
        self.wait(0.8)

        # Spectrum allocation
        spectrum_info = VGroup(
            Text("Available Uplink Spectrum", font_size=28, color=YELLOW),
            Text("Bandwidth: 25 MHz", font_size=32, color=BLUE, weight=BOLD)
        ).arrange(DOWN, buff=0.3)
        spectrum_info.shift(UP * 0.5)
        self.play(Write(spectrum_info))
        self.wait(1)

        # CHANGE 1: Visual spectrum bar with frequency range labels
        spectrum_bar = Rectangle(width=10, height=1, color=BLUE, fill_opacity=0.3, stroke_width=3)
        spectrum_bar.shift(DOWN * 1.5)
        
        # Add frequency range labels (825-849 MHz, around 824 MHz)
        freq_start = Text("825 MHz", font_size=22, color=WHITE)
        freq_start.next_to(spectrum_bar, LEFT, buff=0.2)
        
        freq_end = Text("849 MHz", font_size=22, color=WHITE)
        freq_end.next_to(spectrum_bar, RIGHT, buff=0.2)
        
        # Bandwidth label
        bandwidth_label = Text("25 MHz", font_size=24, color=BLUE, weight=BOLD)
        bandwidth_label.next_to(spectrum_bar, DOWN, buff=0.3)
        
        self.play(Create(spectrum_bar))
        self.play(Write(freq_start), Write(freq_end))
        self.play(Write(bandwidth_label))
        self.wait(1.5)

        # Clear
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def voice_frequency_analysis(self):
        """Explain voice frequency requirements"""
        # Title
        voice_title = Text("Human Voice Spectrum Analysis", font_size=36, color=WHITE)
        voice_title.to_edge(UP)
        self.play(Write(voice_title))

        # Voice info
        voice_info = VGroup(
            Text("Intelligence-carrying speech harmonics", font_size=24, color=YELLOW),
            Text("Clear communication range:", font_size=22, color=WHITE),
            Text("300 Hz - 3,400 Hz", font_size=28, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.3)
        voice_info.shift(UP * 1)
        self.play(Write(voice_info))
        self.wait(1)

        # Frequency spectrum visualization
        axes = Axes(
            x_range=[0, 4000, 500],
            y_range=[0, 1.2, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"color": BLUE},
            tips=False
        )
        axes.shift(DOWN * 1.5)
        x_label = Text("Frequency (Hz)", font_size=20)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)

        # Voice range box
        voice_range = Rectangle(
            width=axes.x_axis.get_length() * (3100/4000),
            height=2,
            color=GREEN,
            fill_opacity=0.3,
            stroke_width=2
        )
        voice_range.move_to(axes.c2p(1850, 0.5))
        range_label = Text("Voice Range", font_size=18, color=GREEN)
        range_label.next_to(voice_range, UP, buff=0.1)

        self.play(Create(axes), Write(x_label))
        self.play(Create(voice_range), Write(range_label))
        self.wait(1)

        # CHANGE 3: Explain guard bands and overhead due to inefficient filters
        overhead = VGroup(
            Text("Guard bands & overhead ≈ 10× factor", font_size=24, color=ORANGE),
            Text("(Due to inefficient filters available at that time)", font_size=20, color=GRAY)
        ).arrange(DOWN, buff=0.2)
        overhead.next_to(voice_title, DOWN, buff=0.5)
        self.play(Write(overhead))
        self.wait(2.5)

        # Channel bandwidth calculation
        calc = VGroup(
            Text("Channel Bandwidth Required:", font_size=24, color=YELLOW),
            Text("≈ 30 kHz per user", font_size=28, color=BLUE, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        calc.to_edge(DOWN, buff=1.5)
        self.play(FadeOut(overhead), Write(calc))
        self.wait(2)

        # Clear
        self.play(*[FadeOut(mob) for mob in self.mobjects])