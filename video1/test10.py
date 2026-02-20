from manim import *

class PathLossVsShadowing(Scene):
    """Animation 13: Path Loss vs Shadowing Comparison - Side by Side"""
    
    def construct(self):
        # Title
        title = Tex("Path Loss vs Shadowing", font_size=42)
        subtitle = Tex("Understanding the difference", font_size=32, color=BLUE)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(
            title.animate.scale(0.78).to_edge(UP, buff=0.2),
            FadeOut(subtitle)
        )
        
        # ========== CREATE SIDE-BY-SIDE PLOTS ==========
        
        # Left plot - Path Loss Only
        axes_left = Axes(
            x_range=[0, 10, 2],
            y_range=[-90, -30, 15],
            x_length=5,
            y_length=4,
            axis_config={
                "color": BLUE, 
                "include_numbers": True, 
                "font_size": 18,
                "include_ticks": True
            },
            tips=False
        ).shift(LEFT * 3.5 + DOWN * 0.5)
        
        left_label = Tex("Path Loss Only", font_size=28, color=GREEN)
        left_label.next_to(axes_left, UP, buff=0.4)
        
        left_subtitle = Tex("(Deterministic)", font_size=20, color=GREEN)
        left_subtitle.next_to(left_label, DOWN, buff=0.1)
        
        x_label_left = Tex("Distance (km)", font_size=16).next_to(axes_left, DOWN, buff=0.4)
        y_label_left = Tex("Power (dBm)", font_size=16).rotate(PI/2).next_to(axes_left, LEFT, buff=0.5)
        
        # Right plot - Path Loss + Shadowing
        axes_right = Axes(
            x_range=[0, 10, 2],
            y_range=[-90, -30, 15],
            x_length=5,
            y_length=4,
            axis_config={
                "color": BLUE, 
                "include_numbers": True, 
                "font_size": 18,
                "include_ticks": True
            },
            tips=False
        ).shift(RIGHT * 3.5 + DOWN * 0.5)
        
        right_label = Tex("Path Loss + Shadowing", font_size=28, color=ORANGE)
        right_label.next_to(axes_right, UP, buff=0.4)
        
        right_subtitle = Tex("(Stochastic)", font_size=20, color=ORANGE)
        right_subtitle.next_to(right_label, DOWN, buff=0.1)
        
        x_label_right = Tex("Distance (km)", font_size=16).next_to(axes_right, DOWN, buff=0.4)
        y_label_right = Tex("Power (dBm)", font_size=16).rotate(PI/2).next_to(axes_right, LEFT, buff=0.5)
        
        # Display axes
        self.play(
            Create(axes_left),
            Create(axes_right),
        )
        self.play(
            Write(left_label),
            Write(left_subtitle),
            Write(right_label),
            Write(right_subtitle),
            Write(x_label_left),
            Write(y_label_left),
            Write(x_label_right),
            Write(y_label_right),
            run_time=2
        )
        self.wait(1)
        
        # ========== PATH LOSS MODEL ==========
        P0 = -40  # Reference power at 1m
        n = 2     # Path loss exponent
        
        def path_loss(d):
            if d < 0.1:
                d = 0.1
            return P0 - 10 * n * np.log10(d) - 15
        
        # ========== LEFT SIDE: SMOOTH PATH LOSS ==========
        
        path_loss_curve_left = axes_left.plot(
            path_loss,
            x_range=[0.1, 10],
            color=GREEN,
            stroke_width=4
        )
        
        equation_left = MathTex(
            r"P_r(d) = P_0 - 10n\log_{10}(d)",
            font_size=24,
            color=WHITE
        ).next_to(axes_left, UP, buff=0.8)
        
        # Animate curve drawing
        self.play(
            Create(path_loss_curve_left),
            run_time=2
        )
        self.play(Write(equation_left))
        rect1 = SurroundingRectangle(equation_left, color=YELLOW)
        self.play(Create(rect1))
        self.wait(0.5)
        
        # Add smooth indicator
        # smooth_indicator = VGroup(
        #     Tex("Smooth", font_size=18, color=GREEN),
        #     Tex("Predictable", font_size=18, color=GREEN),
        #     Tex("No randomness", font_size=18, color=GREEN)
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        # smooth_indicator.next_to(equation_left, DOWN, buff=0.3)
        
        # self.play(FadeIn(smooth_indicator, shift=UP))
        self.wait(1)
        
        # ========== RIGHT SIDE: PATH LOSS + SHADOWING ==========
        
        # First show the smooth curve (reference)
        path_loss_curve_right_reference = axes_right.plot(
            path_loss,
            x_range=[0.1, 10],
            color=GREEN,
            stroke_width=2,
            stroke_opacity=0.4
        )
        
        self.play(Create(path_loss_curve_right_reference), run_time=1)
        
        reference_label = Tex("Reference", font_size=14, color=GREEN)
        reference_label.next_to(path_loss_curve_right_reference, RIGHT, buff=0.1).shift(UP * 0.5)
        self.play(FadeIn(reference_label, scale=0.5))
        
        self.wait(0.5)
        
        # Generate shadowing values (FIXED SEED FOR CONSISTENCY)
        np.random.seed(42)
        num_points = 200
        distances = np.linspace(0.1, 10, num_points)
        sigma = 6  # Standard deviation in dB
        
        # Generate correlated shadowing (more realistic - smoother variations)
        shadowing = np.zeros(num_points)
        shadowing[0] = np.random.normal(0, sigma)
        
        # Use autocorrelation for smoother shadowing
        correlation = 0.95  # High correlation between adjacent points
        for i in range(1, num_points):
            shadowing[i] = correlation * shadowing[i-1] + np.sqrt(1 - correlation**2) * np.random.normal(0, sigma)
        
        # Create shadowed path loss curve
        points_shadowed = [
            axes_right.c2p(d, path_loss(d) + s)
            for d, s in zip(distances, shadowing)
        ]
        
        path_loss_shadowed = VMobject(color=ORANGE, stroke_width=4)
        path_loss_shadowed.set_points_smoothly(points_shadowed)
        
        equation_right = MathTex(
            r"P_r(d) = P_0 - 10n\log_{10}(d) + ",
            r"X_\sigma",
            font_size=24,
            color=WHITE
        ).next_to(axes_right, UP, buff=0.8)
        
        # Draw shadowed curve
        self.play(
            Create(path_loss_shadowed),
            run_time=3,
            rate_func=linear
        )
        self.play(Write(equation_right))
        rect2 = SurroundingRectangle(equation_right, color=YELLOW)
        self.play(Create(rect2))
        self.wait(0.5)
        
        # Highlight shadowing term
        shadow_box = SurroundingRectangle(equation_right[1], color=RED, buff=0.05)
        shadow_term_label = Tex(r"Random\\Variation", font_size=16, color=RED)
        shadow_term_label.next_to(shadow_box, RIGHT, buff=0.2)
        
        self.play(
            Create(shadow_box),
            Write(shadow_term_label)
        )
        self.wait(1.5)
        
        # Add fluctuation indicator
        # fluctuation_indicator = VGroup(
        #     Tex("Fluctuates", font_size=18, color=ORANGE),
        #     Tex("Unpredictable", font_size=18, color=ORANGE),
        #     Tex(r"Random $\pm\sigma$ dB", font_size=18, color=ORANGE)
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        # fluctuation_indicator.next_to(equation_right, DOWN, buff=0.6)
        
        # self.play(FadeIn(fluctuation_indicator, shift=UP))
        # self.wait(1)
        
        # ========== COMPARISON HIGHLIGHTS ==========
        
        # Show sample points with variations
        sample_distances = [2, 5, 8]
        comparison_dots = VGroup()
        comparison_lines = VGroup()
        
        for d in sample_distances:
            # Left side (deterministic)
            dot_left = Dot(
                axes_left.c2p(d, path_loss(d)),
                color=YELLOW,
                radius=0.08
            )
            
            # Right side (with shadowing) - find closest point
            idx = np.argmin(np.abs(distances - d))
            actual_power = path_loss(d) + shadowing[idx]
            dot_right = Dot(
                axes_right.c2p(d, actual_power),
                color=YELLOW,
                radius=0.08
            )
            
            # Show deviation
            deviation_line = DashedLine(
                axes_right.c2p(d, path_loss(d)),
                axes_right.c2p(d, actual_power),
                color=RED,
                stroke_width=2
            )
            
            comparison_dots.add(dot_left, dot_right)
            comparison_lines.add(deviation_line)
        
        self.play(
            LaggedStart(*[FadeIn(dot, scale=1.5) for dot in comparison_dots], lag_ratio=0.2),
            run_time=1.5
        )
        self.play(
            LaggedStart(*[Create(line) for line in comparison_lines], lag_ratio=0.2),
            run_time=1.5
        )
        
        # Final comparison text
        comparison_text = Tex(
            "Same average trend, but shadowing adds random variations around it!",
            font_size=26,
            color=YELLOW
        )
        comparison_text.to_edge(DOWN, buff=0.3)
        comparison_text.shift(UP*0.5)
        
        self.play(Write(comparison_text))
        
        self.wait(3)
        
        # ========== OPTIONAL: Show distribution ==========
        
        # Fade out comparison elements
        self.play(
            FadeOut(comparison_dots),
            FadeOut(comparison_lines),
            FadeOut(comparison_text)
        )
        
        # Show shadowing distribution
        # distribution = MathTex(
        #     r"X_\sigma \sim \mathcal{N}(0, \sigma^2)",
        #     font_size=28,
        #     color=PURPLE
        # ).to_edge(DOWN, buff=0.5)
        
        # sigma_value = MathTex(
        #     r"\sigma = 6 \text{ dB (typical)}",
        #     font_size=24,
        #     color=PURPLE
        # ).next_to(distribution, DOWN, buff=0.2)
        
        # self.play(
        #     Write(distribution),
        #     Write(sigma_value)
        # )
        
        self.wait(3)