from manim import *
import numpy as np

class SignalEffectsSummary(Scene):
    """Standalone animation showing Path Loss, Shadowing, and Multipath preview"""
    
    def construct(self):
        # Title
        title = Text("Summary", font_size=44, color=WHITE, weight=BOLD)
        self.play(Write(title))
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3))
        
        # Three key points
        SUMP1 = VGroup(
            VGroup(
                Text("Question A:", font_size=24, color=WHITE, weight=BOLD),
                Text("   How signals reach the receiver even without a line-of-sight.", 
                    font_size=20, color=WHITE, slant=ITALIC)
            ).arrange(RIGHT, buff=0.15, aligned_edge=UP),
            
            VGroup(
                Text("Question B:", font_size=24, color=WHITE, weight=BOLD),
                Text("   Why small spatial movements cause abrupt received power variations.", 
                    font_size=20, color=WHITE, slant=ITALIC)
            ).arrange(RIGHT, buff=0.15, aligned_edge=UP),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(SUMP1[0]))
        self.wait(4.2)
        self.play(Write(SUMP1[1]))
        self.wait(7.2)
        self.play(FadeOut(SUMP1))
        
        
    

        summary_points = VGroup(

        VGroup(
            Text("1. Multipath:", font_size=24, color=WHITE, weight=BOLD),
            Text("   Multiple propagation paths via reflection, diffraction, and scattering.", 
                font_size=20, color=WHITE, slant=ITALIC)
        ).arrange(RIGHT, buff=0.15, aligned_edge=UP),
        
        VGroup(
            Text("2. Phasors:", font_size=24, color=WHITE, weight=BOLD),
            Text("   Mathematical representation of signal amplitude and phase.", 
                font_size=20, color=WHITE, slant=ITALIC)
        ).arrange(RIGHT, buff=0.15, aligned_edge=UP),

        VGroup(
            Text("3. Fading Distribution:", font_size=24, color=WHITE, weight=BOLD),
            Text("   Rayleigh (no LOS) and Rician (dominant LOS) fading models.", 
                font_size=20, color=WHITE, slant=ITALIC)
        ).arrange(RIGHT, buff=0.15, aligned_edge=UP),
        
        VGroup(
            Text("Multipath Phenomena:", font_size=24, color=YELLOW, weight=BOLD),
            Text("   Delay spread, coherence bandwidth, and intersymbol interference.", 
                font_size=20, color=YELLOW, slant=ITALIC)
        ).arrange(RIGHT, buff=0.15, aligned_edge=UP)
    ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        
        summary_points.move_to(ORIGIN)
        
        # Animate points one by one
        self.play(Write(summary_points[0]))
        self.wait(2.2)
        self.play(Write(summary_points[1]))
        self.wait(2.2)
        self.play(Write(summary_points[2]))
        self.wait(2.2)
        self.play(Write(summary_points[3]))
        self.wait(2.2)
        
        # Highlight multipath for next video
        multipath_box = SurroundingRectangle(
            summary_points[3], 
            color=YELLOW, 
            buff=0.2, 
            stroke_width=4,
            corner_radius=0.1
        )
        
        # coming_soon = Text("→ Next Video!", font_size=20, color=YELLOW, weight=BOLD)
        # coming_soon.next_to(multipath_box, RIGHT, buff=0.4)
        
        self.play(
            Create(multipath_box),
            # Write(coming_soon),
            Flash(multipath_box, color=YELLOW, line_length=0.5, num_lines=12)
        )
        self.wait(2)
        
        # Pulse animation on multipath
        self.play(
            multipath_box.animate.scale(1.05).set_stroke(width=6),
            # coming_soon.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(3)


# To render:
# manim -pql signal_effects_complete.py SignalEffectsSummary