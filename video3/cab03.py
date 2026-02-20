from manim import *
import numpy as np

class Phase2_DiscreteToContinuous(Scene):
    def construct(self):
        # -----------------------------------------
        # 1. SETUP (Resume from Phase 1)
        # -----------------------------------------
        title = Title("Power Delay Profile")
        self.add(title)

        axes = Axes(
            x_range=[0, 7, 1], y_range=[0, 1.2, 0.5],
            x_length=7, y_length=4,
            axis_config={"include_tip": True, "font_size": 24}
        ).move_to(DOWN*0.5)

        x_lbl = axes.get_x_axis_label(Tex("Delay $(\\tau)$"), edge=DOWN, direction=DOWN, buff=0.3)
        y_lbl = axes.get_y_axis_label(Tex("Power $P(\\tau)$").rotate(90*DEGREES), edge=LEFT, direction=LEFT, buff=0.3)
        
        # Helper to make taps
        def make_impulse(x_val, height, color, opacity=1.0):
            base = axes.c2p(x_val, 0)
            top = axes.c2p(x_val, height)
            line = Line(base, top, color=color, stroke_width=6, stroke_opacity=opacity)
            return line

        # The Original 3 Taps (Power)
        # 1.0 -> 1.0, 0.6 -> 0.36, 0.3 -> 0.09
        tap1 = make_impulse(1.5, 1.0, BLUE)
        tap2 = make_impulse(3.0, 0.36, GREEN)
        tap3 = make_impulse(5.0, 0.09, YELLOW)
        
        original_taps = VGroup(tap1, tap2, tap3)
        self.add(axes, x_lbl, y_lbl, original_taps)
        self.wait(4)

        # -----------------------------------------
        # 2. THE SCATTERING EFFECT (Discrete -> Clusters)
        # -----------------------------------------
        # Narrative: "But real reflections aren't perfect. A building is rough. 
        # One echo is actually a cluster of micro-echoes."
        
        clusters = VGroup()
        np.random.seed(42) # Fixed seed for consistent "randomness"

        # Generate mini-taps around each main tap
        for main_t, main_h, col in [(1.5, 1.0, BLUE), (3.0, 0.36, GREEN), (5.0, 0.09, YELLOW)]:
            for _ in range(15): # 15 micro-echoes per cluster
                # Random spread +/- 0.3s, Random height variation
                jit_t = main_t + np.random.normal(0, 0.15)
                jit_h = main_h * np.random.uniform(0.3, 0.9) * np.exp(-abs(jit_t - main_t)*2)
                if jit_h > 0:
                    clusters.add(make_impulse(jit_t, jit_h, col, opacity=0.6))
        
        self.play(
            FadeOut(original_taps),
            LaggedStart(*[Create(c) for c in clusters], lag_ratio=0.01),
            run_time=2
        )
        self.wait(1)

        # -----------------------------------------
        # 3. THE ENVELOPE (The Continuous Curve)
        # -----------------------------------------
        # Narrative: "When we average these clusters over time, we get a smooth curve.
        # THIS is the Average Power Delay Profile."
        
        # Create a smooth function that approximates the peaks
        # Sum of 3 Gaussians
        def pdp_curve(x):
            g1 = 1.0 * np.exp(-((x - 1.5)**2) / (2 * 0.15**2))
            g2 = 0.36 * np.exp(-((x - 3.0)**2) / (2 * 0.2**2))
            g3 = 0.09 * np.exp(-((x - 5.0)**2) / (2 * 0.25**2))
            return g1 + g2 + g3

        envelope = axes.plot(pdp_curve, x_range=[0, 7], color=WHITE, stroke_width=4)
        
        # Area under curve (optional, looks nice)
        area = axes.get_area(envelope, x_range=[0, 7], color=[BLUE, GREEN, YELLOW], opacity=0.3)

        self.play(Create(envelope), FadeIn(area))
        # Fade out the messy clusters to leave just the clean average
        self.play(FadeOut(clusters), run_time=1)
        self.wait(4)

        