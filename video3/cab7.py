from manim import *
import numpy as np

class Phase4_Frequency_Ripple(Scene):
    def construct(self):
        # 0. SETUP: Two Views
        title = Title("Bandwidth and Delay spread", color=WHITE).scale(0.9)
        
        eqn = MathTex(r"\sigma_\tau < T_{retrans}", font_size=40, color=RED).next_to(title, DOWN, buff=0.5)
        self.add(eqn)
        
        self.wait(2)
        
        # --- NEW ANIMATION SEQUENCE ---
        # 1. Add vertical arrows showing τ and T_retrans relationship
        arrow_tau = Arrow(eqn.get_left() + LEFT*0.2 + DOWN*0.34, eqn.get_left() + LEFT*0.2 + UP*0.34, color=BLUE, buff=0.1, stroke_width=3)
        arrow_tretrans = Arrow(eqn.get_right() + RIGHT*0.2 + DOWN*0.34, eqn.get_right() + RIGHT*0.2 + UP*0.34, color=BLUE, buff=0.1, stroke_width=3)
        # lbl_tau_arrow = Text("τ ↑", font_size=20, color=BLUE).next_to(arrow_tau, LEFT, buff=0.1)
        # lbl_tretrans_arrow = Text("T ↑", font_size=20, color=BLUE).next_to(arrow_tretrans, RIGHT, buff=0.1)
        
        self.play(Create(arrow_tau), Create(arrow_tretrans))
        self.wait(3)
        
        # 2. Fade out arrows and transform equation to show proportionality
        self.play(FadeOut(arrow_tau), FadeOut(arrow_tretrans))
        
        eqn2 = MathTex(r"\sigma_\tau \propto T_{retrans}", font_size=40, color=RED).next_to(title, DOWN, buff=0.5)
        self.play(Transform(eqn, eqn2))
        self.wait(3)
        
        # 3. New formula appears below showing T_retrans ∝ 1/Bch
        eqn3 = MathTex(r"T_{retrans} \propto \frac{1}{B_{ch}}", font_size=40, color=GREEN).next_to(eqn, DOWN, buff=0.5)
        self.play(FadeIn(eqn3, shift=DOWN))
        self.wait(3)
        
        # 4. Lower formula disappears, upper becomes the combined relationship
        self.play(FadeOut(eqn3))
        
        eqn4 = MathTex(r"\sigma_\tau \propto T_{retrans} \propto \frac{1}{B_{ch}}", font_size=40, color=RED).next_to(title, DOWN, buff=0.5)
        self.play(Transform(eqn, eqn4))
        self.wait(3)
        
        # 5. Transform to final simplified form
        eqn5 = MathTex(r"\sigma_\tau \propto \frac{1}{B_{ch}}", font_size=40, color=RED).next_to(title, DOWN, buff=0.5)
        self.play(Transform(eqn, eqn5))
        self.wait(3)
        
        # 6. Transform to show inverse perspective: B_w ∝ 1/σ_τ
        eqn6 = MathTex(r"B_{ch} \propto \frac{1}{\sigma_\tau}", font_size=40, color=RED).next_to(title, DOWN, buff=0.5)
        self.play(Transform(eqn, eqn6))
        self.wait(3)
        self.add(title)

        ax_t = Axes(x_range=[0, 5, 1], y_range=[0, 1.5, 1], x_length=5, y_length=3,
                    axis_config={"include_tip": True}).to_edge(LEFT, buff=0.5).shift(DOWN*1)
        ax_f = Axes(x_range=[0, 10, 1], y_range=[0, 2.2, 1], x_length=5, y_length=3,
                    axis_config={"include_tip": True}).to_edge(RIGHT, buff=0.5).shift(DOWN*1)

        lbl_t = Text("Impulse Response h(t)", font_size=20).next_to(ax_t, DOWN)
        lbl_f = Text("Frequency Response |H(f)|", font_size=20).next_to(ax_f, DOWN)
        self.add(ax_t, ax_f, lbl_t, lbl_f)

        # Value tracker for the Delay (Tau)
        tau_tracker = ValueTracker(0.2) # Start very close

        # 1. TIME DOMAIN: Redrawing Taps
        def get_taps():
            tau = tau_tracker.get_value()
            main = Arrow(ax_t.c2p(0,0), ax_t.c2p(0,1), color=YELLOW, buff=0)
            echo = Arrow(ax_t.c2p(tau,0), ax_t.c2p(tau,0.7), color=YELLOW, buff=0)
            return VGroup(main, echo)
        
        taps = always_redraw(get_taps)

        # 2. FREQUENCY DOMAIN: The Ripple (Magnitude Response)
        # Based on H(f) = 1 + a*exp(-j2pi*f*tau)
        def get_ripple():
            tau = tau_tracker.get_value()
            # a = 0.7 for echo amplitude
            return ax_f.plot(
                lambda f: np.sqrt(1 + 0.49 + 1.4 * np.cos(2 * PI * f * tau * 0.5)), 
                color=YELLOW, x_range=[0, 10]
            )

        ripple = always_redraw(get_ripple)

        # 3. COHERENCE BANDWIDTH (Bch) INDICATOR with dotted lines and flickering arrow
        # Add time tracker for flickering effect
        flicker_time = ValueTracker(0)
        
        def get_bc():
            tau = tau_tracker.get_value()
            # Conceptual Bc is inversely proportional to Tau
            width = 1.2 / (tau + 0.05)
            if width > 4: width = 4
            
            # Left vertical dotted line
            left_line = DashedLine(ax_f.c2p(0, 1.8), ax_f.c2p(0, 2.2), dash_length=0.1, color=BLUE, stroke_width=2)
            
            # Right vertical dotted line
            right_line = DashedLine(ax_f.c2p(width, 1.8), ax_f.c2p(width, 2.2), dash_length=0.1, color=BLUE, stroke_width=2)
            
            # Double-sided arrow with flickering opacity
            arrow = DoubleArrow(ax_f.c2p(0.05, 2), ax_f.c2p(width-0.05, 2), color=BLUE, stroke_width=2, buff=0.05)
            t = flicker_time.get_value()
            flicker_opacity = 0.3 + 0.7 * (0.5 + 0.5 * np.sin(t * 8))  # Flickers between 0.3 and 1.0
            arrow.set_opacity(flicker_opacity)
            
            # Label
            label = MathTex("B_{ch}", color=BLUE, font_size=28).next_to(arrow, UP, buff=0.15).shift(UP*0.5)
            
            return VGroup(left_line, right_line, arrow, label)

        bc_marker = always_redraw(get_bc)

        self.add(taps, ripple, bc_marker)
        self.wait(1)

        # THE MORPH: Move delay from 0.2 to 1.5 (capped to prevent ripples from getting too close)
        # Watch the frequency response go from "Flat" to "Many Notches"
        self.play(tau_tracker.animate.set_value(1.5), run_time=9, rate_func=linear)
        self.wait(2)