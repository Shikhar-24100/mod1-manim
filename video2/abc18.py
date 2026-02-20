from manim import *
import numpy as np

class RayleighToRicianScene(ThreeDScene):
    def construct(self):
        # ================================================
        # PART A: RECREATE THE RAYLEIGH DISTRIBUTION (SAME AS BEFORE)
        # ================================================
        title = Title("Rayleigh and Rician Fading").scale(0.9)
        self.add(title)
        # Position at center (same as end of previous video)
        center_pos = ORIGIN
        
        # Rayleigh Distribution (longer x-axis)
        rayleigh_axes = Axes(
            x_range=[0, 6, 1],  # Extended x-range to 6
            y_range=[0, 0.7, 0.2],
            x_length=7,  # Longer x-axis
            y_length=3,
            axis_config={"include_tip": True, "tip_width": 0.15, "tip_height": 0.15},
            tips=True
        ).move_to(center_pos)
        
        # Rayleigh PDF function
        def rayleigh_pdf(r, sigma=1):
            if r < 0:
                return 0
            return (r / sigma**2) * np.exp(-r**2 / (2 * sigma**2))
        
        rayleigh_curve = rayleigh_axes.plot(
            lambda r: rayleigh_pdf(r, sigma=1),
            x_range=[0, 6],  # Extended range
            color=BLUE,
            stroke_width=4
        )
        
        # # Labels for Rayleigh
        # rayleigh_title = MathTex(r"P_R(r)", font_size=32, color=RED)
        # rayleigh_title.next_to(rayleigh_axes, UP, buff=0.3)
        
        r_label = MathTex(r"\text{Amplitude } (r)", font_size=24, color=WHITE)
        r_label.next_to(rayleigh_axes.x_axis.get_end(), DOWN, buff=0.4)
        
        prob_label = MathTex(r"\text{Probability}", font_size=24, color=WHITE)
        prob_label.rotate(90 * DEGREES)
        prob_label.next_to(rayleigh_axes.y_axis.get_end(), LEFT, buff=0.4)
        
        # Show the Rayleigh distribution (already on screen from previous video)
        self.add(rayleigh_axes, rayleigh_curve, r_label, prob_label)
        
        self.wait(1.0)
        
        # ================================================
        # PART B: INTRODUCE THE RAYLEIGH FORMULA (SEPARATE)
        # ================================================
        
        # Create a background box for the formula
        rayleigh_formula_box = Rectangle(
            width=7,
            height=1.2,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_color=BLUE,
            stroke_width=2
        ).to_edge(UP, buff=0.3).shift(RIGHT * 2.5 + DOWN*1.2)
        
        rayleigh_formula = MathTex(
            r"P_R(r) = \frac{r}{\sigma^2} e^{-\frac{r^2}{2\sigma^2}}, \quad r \geq 0",
            font_size=32,
            color=YELLOW
        ).move_to(rayleigh_formula_box.get_center())
        
        # formula_title = Text("Rayleigh Distribution:", font_size=24, color=BLUE, weight=BOLD)
        # formula_title.next_to(rayleigh_formula, UP, buff=0.15)
        
        rayleigh_formula_group = VGroup(rayleigh_formula)
        
        self.play(
            # FadeIn(rayleigh_formula_box),
            # Write(formula_title),
            Write(rayleigh_formula),
            run_time=1.0
        )
        
        self.wait(4.5)
        
        # ================================================
        # PART C: HIGHLIGHT DEEP FADES
        # ================================================
        
        # Define deep fade region (r close to 0, e.g., r < 0.5)
        deep_fade_threshold = 0.5
        
        # Create shaded area for deep fades
        deep_fade_area = rayleigh_axes.get_area(
            rayleigh_curve,
            x_range=[0, deep_fade_threshold],
            color=RED,
            opacity=0.6
        )
        
        # "Deep fades!" text
        deep_fade_text = Text("Deep fades!", font_size=28, color=RED, weight=BOLD)
        deep_fade_text.move_to(rayleigh_axes.c2p(-2.1, 0.4))
        
        # Arrow pointing to deep fade region
        deep_fade_arrow = Arrow(
            deep_fade_text.get_right(),
            rayleigh_axes.c2p(0.25, 0.15),
            color=RED,
            stroke_width=4,
            buff=0.1
        )
        
        # Animate deep fade highlight
        self.play(
            FadeIn(deep_fade_area),
            run_time=0.8
        )
        self.play(
            Write(deep_fade_text),
            GrowArrow(deep_fade_arrow),
            run_time=0.8
        )
        
        # Hold for 3 seconds
        self.wait(6.0)
        
        # Fade out deep fade indicators
        self.play(
            FadeOut(deep_fade_area),
            FadeOut(deep_fade_text),
            FadeOut(deep_fade_arrow),
            run_time=0.6
        )
        
        self.wait(0.5)
        
        # ================================================
        # PART D: INTRODUCE RICIAN DISTRIBUTION
        # ================================================
        
        # Rician PDF function (with LOS component)
        def rician_pdf(r, K=3, sigma=1):
            """
            K: Rician K-factor (ratio of LOS to scattered power)
            Higher K means stronger LOS component
            """
            if r < 0:
                return 0
            from scipy.special import i0  # Modified Bessel function
            A = np.sqrt(K * 2)  # LOS amplitude
            return (r / sigma**2) * np.exp(-(r**2 + A**2) / (2 * sigma**2)) * i0(r * A / sigma**2)
        
        # Create Rician curve (shifted to the right, with peak around LOS strength)
        rician_curve = rayleigh_axes.plot(
            lambda r: rician_pdf(r, K=3, sigma=1),
            x_range=[0, 6],  # Extended range
            color=ORANGE,
            stroke_width=4
        )
        
        # Rician label
        rician_label = Text("Rician (LOS + scatter)", font_size=22, color=ORANGE)
        rician_label.move_to(rayleigh_axes.c2p(3.5, 0.35))
        
        # Rayleigh label (update to show it's NLOS)
        rayleigh_label = Text("Rayleigh (NLOS)", font_size=22, color=BLUE)
        rayleigh_label.move_to(rayleigh_axes.c2p(1.5, 0.5))
        
        # Animate Rician curve appearing
        self.play(Create(rician_curve), run_time=1.2)
        
        self.wait(0.5)
        
        # Add labels
        self.play(
            FadeIn(rician_label),
            FadeIn(rayleigh_label),
            run_time=0.8
        )
        
        self.wait(5.0)
        
        # Add bottom text explanations
        rayleigh_desc = Text(
            "Rayleigh: Deep fades common",
            font_size=20,
            color=BLUE
        ).to_edge(DOWN, buff=1.2).shift(LEFT * 3)
        
        rician_desc = Text(
            "Rician: More stable (LOS helps)",
            font_size=20,
            color=ORANGE
        ).to_edge(DOWN, buff=1.2).shift(RIGHT * 3)
        
        self.play(
            FadeIn(rayleigh_desc),
            FadeIn(rician_desc),
            run_time=0.8
        )
        
        self.wait(5.0)
        
        # ================================================
        # PART E: SHOW RICIAN FORMULA (SEPARATE)
        # ================================================
        
        # Fade out Rayleigh formula
        self.play(FadeOut(rayleigh_formula_group), run_time=0.5)
        
        self.wait(0.3)
        
        # Create a background box for Rician formula
        rician_formula_box = Rectangle(
            width=9,
            height=1.2,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_color=ORANGE,
            stroke_width=2
        ).to_edge(UP, buff=0.3).shift(RIGHT * 2.5 + DOWN*1.2)
        
        rician_formula = MathTex(
            r"P_R(r) = \frac{r}{\sigma^2} e^{-\frac{r^2+A^2}{2\sigma^2}} I_0\left(\frac{rA}{\sigma^2}\right), \quad r \geq 0",
            font_size=28,
            color=YELLOW
        ).move_to(rician_formula_box.get_center())
        
        # rician_formula_title = Text("Rician Distribution:", font_size=24, color=ORANGE, weight=BOLD)
        # rician_formula_title.next_to(rician_formula, UP, buff=0.15)
        
        self.play(
            # FadeIn(rician_formula_box),
            # Write(rician_formula_title),
            Write(rician_formula),
            run_time=1.0
        )
        
        self.wait(2.0)
        
        # Final fade out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.0
        )
        
        self.wait(3.5)