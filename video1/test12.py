from manim import *
import numpy as np

class ReceivedPowerEquation(Scene):
    """Animation 15: Received Power Equation Build-up"""
    
    def construct(self):
        # Title
        title = Text("Received Power Model", font_size=44, weight=BOLD )
        subtitle = Text("Building the complete equation", font_size=28, color=BLUE)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(
            title.animate.scale(0.7).to_edge(UP, buff=0.3),
            FadeOut(subtitle)
        )
        
        # ========== PART 1: REFERENCE POWER ==========
        step1_label = Text("Step 1: Reference Power", font_size=28, color=GREEN)
        step1_label.to_edge(UP, buff=1.2)
        
        self.play(Write(step1_label))
        self.wait(0.5)
        
        # Reference power term
        pr_d0 = MathTex(
            r"P_r(d_0)",
            font_size=60,
            color=GREEN
        ).move_to(ORIGIN)
        
        pr_d0_box = SurroundingRectangle(pr_d0, color=GREEN, buff=0.2)
        
        self.play(
            Write(pr_d0),
            Create(pr_d0_box)
        )
        self.wait(0.5)
        
        # Explanation
        explanation1 = VGroup(
            Text("Power measured at", font_size=22),
            Text("reference distance d₀", font_size=22, color=GREEN, weight=BOLD),
            Text("(typically 1m or 1km)", font_size=18, color=GRAY, slant=ITALIC)
        ).arrange(DOWN, buff=0.15)
        explanation1.to_edge(DOWN, buff=0.8)
        
        self.play(FadeIn(explanation1, shift=UP, lag_ratio=0.2))
        self.wait(2)
        
        # Move to left to make room
        self.play(
            FadeOut(step1_label),
            FadeOut(explanation1),
            FadeOut(pr_d0_box),
            pr_d0.animate.shift(LEFT * 3.5).scale(0.8)
        )
        
        # ========== PART 2: PATH LOSS TERM ==========
        step2_label = Text("Step 2: Add Path Loss", font_size=28, color=YELLOW)
        step2_label.to_edge(UP, buff=1.2)
        
        self.play(Write(step2_label))
        self.wait(0.5)
        
        # Path loss term - slides in from left
        path_loss_term = MathTex(
            r"- 10n \log_{10}\left(\frac{d}{d_0}\right)",
            font_size=48,
            color=YELLOW
        )
        path_loss_term.next_to(pr_d0, RIGHT, buff=0.3)
        path_loss_term.shift(LEFT * 8)  # Start off-screen
        
        self.play(
            path_loss_term.animate.shift(RIGHT * 8),
            run_time=1.5,
            rate_func=smooth
        )
        
        # Highlight the term
        path_loss_box = SurroundingRectangle(path_loss_term, color=YELLOW, buff=0.15)
        self.play(Create(path_loss_box))
        self.wait(0.5)
        
        # Explanation
        explanation2 = VGroup(
            Text("Path Loss Component:", font_size=22, color=YELLOW, weight=BOLD),
            Text("• n = path loss exponent", font_size=20),
            Text("• d = distance from transmitter", font_size=20),
            Text("• Deterministic (predictable)", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        explanation2.to_edge(DOWN, buff=0.6)
        
        self.play(FadeIn(explanation2, shift=UP, lag_ratio=0.15))
        self.wait(2)
        
        # Clean up
        self.play(
            FadeOut(step2_label),
            FadeOut(explanation2),
            FadeOut(path_loss_box)
        )
        
        # ========== PART 3: SHADOWING TERM ==========
        step3_label = Text("Step 3: Add Shadowing", font_size=28, color=ORANGE)
        step3_label.to_edge(UP, buff=1.2)
        
        self.play(Write(step3_label))
        self.wait(0.5)
        
        # Shadowing term - slides in from right
        shadowing_term = MathTex(
            r"+ X_\sigma",
            font_size=48,
            color=ORANGE
        )
        shadowing_term.next_to(path_loss_term, RIGHT, buff=0.3)
        shadowing_term.shift(RIGHT * 8)  # Start off-screen
        
        self.play(
            shadowing_term.animate.shift(LEFT * 8),
            run_time=1.5,
            rate_func=smooth
        )
        
        # Highlight with ± symbol to show randomness
        plus_minus = MathTex(r"\pm", font_size=40, color=RED)
        plus_minus.next_to(shadowing_term, LEFT, buff=0.1)
        
        shadowing_box = SurroundingRectangle(
            VGroup(plus_minus, shadowing_term), 
            color=ORANGE, 
            buff=0.15
        )
        
        self.play(
            Write(plus_minus),
            Create(shadowing_box),
            run_time=1
        )
        self.wait(0.5)
        
        # Explanation
        explanation3 = VGroup(
            Text("Shadowing Component:", font_size=22, color=ORANGE, weight=BOLD),
            Text("• Xσ ~ N(0, σ²) in dB", font_size=20),
            Text("• Random variation (log-normal)", font_size=20),
            Text("• Models obstacle effects", font_size=20, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        explanation3.to_edge(DOWN, buff=0.6)
        
        self.play(FadeIn(explanation3, shift=UP, lag_ratio=0.15))
        self.wait(2)
        
        # Clean up
        self.play(
            FadeOut(step3_label),
            FadeOut(explanation3),
            FadeOut(shadowing_box),
            FadeOut(plus_minus)
        )
        
        # ========== COMPLETE EQUATION ==========
        complete_label = Text("Complete Shadowing Model", font_size=32, color=BLUE, weight=BOLD)
        complete_label.to_edge(UP, buff=1.2)
        
        self.play(Write(complete_label))
        self.wait(0.5)
        
        # Group the equation
        complete_equation = VGroup(pr_d0, path_loss_term, shadowing_term)
        
        # Add equals sign at the beginning
        pr_label = MathTex(r"P_r(d) =", font_size=48, color=WHITE)
        pr_label.next_to(complete_equation, LEFT, buff=0.3)
        
        self.play(Write(pr_label))
        
        # Center everything
        full_equation = VGroup(pr_label, complete_equation)
        self.play(full_equation.animate.move_to(ORIGIN).shift(UP * 0.5))
        self.wait(0.5)
        
        # Create box around complete equation
        final_box = SurroundingRectangle(full_equation, color=BLUE, buff=0.3, stroke_width=4)
        
        self.play(Create(final_box))
        
        # Make it glow
        glow_copies = VGroup(*[
            SurroundingRectangle(
                full_equation, 
                color=BLUE, 
                buff=0.3 + i*0.1, 
                stroke_width=4,
                stroke_opacity=0.3 - i*0.1
            ) for i in range(3)
        ])
        
        self.play(
            LaggedStart(*[Create(glow) for glow in glow_copies], lag_ratio=0.2),
            run_time=1.5
        )
        self.wait(1)
        
        # Add detailed breakdown below
        breakdown = VGroup(
            MathTex(r"P_r(d_0)", font_size=24, color=GREEN),
            Text("Reference power", font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.1)
        
        breakdown2 = VGroup(
            MathTex(r"-10n\log_{10}(d/d_0)", font_size=24, color=YELLOW),
            Text("Path loss (deterministic)", font_size=18, color=YELLOW)
        ).arrange(DOWN, buff=0.1)
        
        breakdown3 = VGroup(
            MathTex(r"X_\sigma", font_size=24, color=ORANGE),
            Text("Shadowing (random)", font_size=18, color=ORANGE)
        ).arrange(DOWN, buff=0.1)
        
        all_breakdown = VGroup(breakdown, breakdown2, breakdown3).arrange(RIGHT, buff=0.8)
        all_breakdown.to_edge(DOWN, buff=0.5)
        all_breakdown.shift(UP*1.5)
        
        self.play(
            FadeIn(all_breakdown, shift=UP, lag_ratio=0.2),
            run_time=2
        )
        
        # Final emphasis
        emphasis = Text(
            "Used for cellular network planning and coverage prediction",
            font_size=20,
            color=BLUE,
            slant=ITALIC
        ).next_to(all_breakdown, DOWN, buff=0.4)
        
        self.play(Write(emphasis))
        
        self.wait(4)


