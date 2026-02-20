from manim import *
import numpy as np
import random

class ConclusionCallback(Scene):
    def construct(self):
        # --- 1. RECALL THE QUESTION ---
        question = Text("Why do we experience large signal variation?", font_size=32, color=YELLOW).to_edge(UP)
        self.play(Write(question))

        # --- 2. BRING BACK THE GRAPH (The Problem) ---
        axes = Axes(
            x_range=[0, 6, 1], y_range=[-3, 3, 1],
            x_length=6, y_length=3,
            axis_config={"color": GRAY}
        ).shift(DOWN * 0.5)
        
        # Create a static chaotic path to represent the fading signal
        path = VGroup()
        points = [axes.c2p(0, 0)]
        for x in np.arange(0.1, 6.1, 0.1):
            y = np.sin(x * 3) + random.uniform(-1.5, 1.5)
            points.append(axes.c2p(x, y))
            
        signal_line = VMobject(color=RED, stroke_width=2)
        signal_line.set_points_smoothly(points)
        
        self.play(Create(axes), Create(signal_line), run_time=2)

        # --- 3. OVERLAY THE PHYSICS (The Answer) ---
        # Show tiny coherence windows over the chaotic graph
        self.wait(5)
        windows = VGroup()
        for i in range(1, 6):
            # A tiny box representing the small Tc
            window = Rectangle(width=0.4, height=3, color=BLUE, fill_opacity=0.3)
            window.move_to(axes.c2p(i, 0))
            windows.add(window)
            
        self.play(FadeIn(windows, lag_ratio=0.4))
        self.wait(4)
        
        # Add the explanatory text pointing to the windows
        # FIXED: Using MathTex with \text{} blocks to render the arrow correctly
        answer_text = VGroup(
            Text("High Speed = High Doppler", font_size=20),
            Text("Tiny Coherence Window (Tc)", font_size=20, color=BLUE),
            MathTex(r"\text{Computation Fails } \rightarrow \text{ Signal Drops}", font_size=22, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT, buff=0.5).shift(UP * 1)
        
        # Arrow pointing from text to one of the windows
        # arrow = Arrow(start=answer_text.get_right(), end=windows[1].get_top(), color=WHITE)
        
        self.play(Write(answer_text), run_time=2)
        self.wait(4)

        # --- 4. THE FINAL WRAP-UP ---
        # A clean fade out, leaving only the core takeaway
        self.play(FadeOut(axes), FadeOut(signal_line), FadeOut(windows), FadeOut(question))
        
        final_takeaway = Text("Motion dictates the math.", font_size=36, color=GREEN)
        final_takeaway2 = Text("The math dictates the network.", font_size=36, color=GREEN).next_to(final_takeaway, DOWN)
        
        self.play(
            Transform(answer_text, VGroup(final_takeaway, final_takeaway2).arrange(DOWN).move_to(ORIGIN))
        )
        self.wait(4)