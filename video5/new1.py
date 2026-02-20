from manim import *

class FadingSummary(Scene):
    def construct(self):
        # --- TITLE ---
        title = Text("Channel Fading Classification", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title))

        # --- HEADERS ---
        # We will create a 2x2 grid structure
        
        # Left Side: Time Domain (Fast vs Slow)
        time_header = Text("Time Domain (Doppler)", font_size=24, color=YELLOW).move_to(LEFT * 3.5 + UP * 2)
        
        # Right Side: Frequency Domain (Delay)
        freq_header = Text("Freq. Domain (Delay)", font_size=24, color=GREEN).move_to(RIGHT * 3.5 + UP * 2)
        
        self.play(FadeIn(time_header), FadeIn(freq_header))
        self.play(Create(Line(UP*1.5, DOWN*3, color=GRAY))) # Vertical separator

        # --- LEFT SIDE: FAST VS SLOW ---
        # Condition 1: Fast Fading
        fast_cond = MathTex(r"T_s > T_c", color=RED, font_size=32).move_to(LEFT * 3.5 + UP * 0.5)
        fast_label = Text("Fast Fading", font_size=20, color=RED).next_to(fast_cond, DOWN)
        fast_desc = Text("(Channel changes during symbol)", font_size=16, color=GRAY).next_to(fast_label, DOWN)

        # Condition 2: Slow Fading
        slow_cond = MathTex(r"T_s < T_c", color=BLUE, font_size=32).move_to(LEFT * 3.5 + DOWN * 1.5)
        slow_label = Text("Slow Fading", font_size=20, color=BLUE).next_to(slow_cond, DOWN)
        slow_desc = Text("(Channel constant over symbol)", font_size=16, color=GRAY).next_to(slow_label, DOWN)
        self.wait(5)
        self.play(Write(fast_cond), FadeIn(fast_label), FadeIn(fast_desc))
        self.wait(4)
        self.play(Write(slow_cond), FadeIn(slow_label), FadeIn(slow_desc))

        # --- RIGHT SIDE: FLAT VS SELECTIVE ---
        # Condition 3: Freq Selective
        sel_cond = MathTex(r"B_s > B_c", color=RED, font_size=32).move_to(RIGHT * 3.5 + UP * 0.5)
        sel_label = Text("Frequency Selective", font_size=20, color=RED).next_to(sel_cond, DOWN)
        sel_desc = Text("(ISI occurs)", font_size=16, color=GRAY).next_to(sel_label, DOWN)

        # Condition 4: Flat Fading
        flat_cond = MathTex(r"B_s < B_c", color=BLUE, font_size=32).move_to(RIGHT * 3.5 + DOWN * 1.5)
        flat_label = Text("Flat Fading", font_size=20, color=BLUE).next_to(flat_cond, DOWN)
        flat_desc = Text("(Uniform gain)", font_size=16, color=GRAY).next_to(flat_label, DOWN)
        self.wait(4)
        self.play(Write(sel_cond), FadeIn(sel_label), FadeIn(sel_desc))
        self.wait(4)
        self.play(Write(flat_cond), FadeIn(flat_label), FadeIn(flat_desc))

        # --- FINAL HIGHLIGHT ---
        # Highlighting that high mobility (Doppler) usually pushes us to Fast Fading
        box = SurroundingRectangle(VGroup(fast_cond, fast_label), color=YELLOW, buff=0.15)
        implication = Text("High Mobility Issues", font_size=18, color=YELLOW).next_to(box, UP)
        
        self.play(Create(box), Write(implication))
        self.wait(3)