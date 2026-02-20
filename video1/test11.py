from manim import *
import numpy as np

class LogNormalDistribution(Scene):
    """Animation 14: Log-Normal Distribution Visualization"""
    
    def construct(self):
        # Title
        title = Text("Statistical Model of Shadowing", font_size=42, weight=BOLD)
        subtitle = Text("Log-Normal Distribution", font_size=26, color=WHITE)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(
            title.animate.scale(0.7).to_edge(UP, buff=0.3),
            FadeOut(subtitle)
        )
        
        # ========== HISTOGRAM SETUP ==========
        
        # Generate shadow fading data (log-normal in dB)
        np.random.seed(42)
        sigma = 6  # dB
        num_samples = 1000
        shadow_values = np.random.normal(0, sigma, num_samples)
        
        # Create histogram
        hist_range = (-20, 20)
        num_bins = 20
        hist, bin_edges = np.histogram(shadow_values, bins=num_bins, range=hist_range, density=True)
        bin_width = bin_edges[1] - bin_edges[0]
        
        # Axes for histogram
        axes = Axes(
            x_range=[-20, 20, 5],
            y_range=[0, 0.08, 0.02],
            x_length=10,
            y_length=5,
            axis_config={"color": WHITE, "include_numbers": True, "font_size": 24},
            tips=False
        ).shift(DOWN * 0.5)
        
        x_label = MathTex(r"X_\sigma \text{ (dB)}", font_size=28).next_to(axes.x_axis, DOWN, buff=0.4)
        y_label = Text("Probability Density", font_size=24).next_to(axes.y_axis, UP, buff=0.4)

        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label)
        )
        self.wait(0.5)
        
        # ========== ANIMATE HISTOGRAM BARS ==========
        bars = VGroup()
        
        for i in range(len(hist)):
            bin_center = (bin_edges[i] + bin_edges[i+1]) / 2
            bar_height = hist[i]
            
            bar = Rectangle(
                height=axes.y_axis.n2p(bar_height)[1] - axes.y_axis.n2p(0)[1],
                width=axes.x_axis.n2p(bin_center + bin_width/2)[0] - axes.x_axis.n2p(bin_center - bin_width/2)[0],
                stroke_color=WHITE,
                stroke_width=1,
                fill_opacity=0
            )
            bar.move_to(axes.c2p(bin_center, bar_height / 2))
            bars.add(bar)
        
        self.play(
            LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.05),
            run_time=3
        )
        self.wait(1)
        
        # ========== OVERLAY NORMAL CURVE ==========
        
        def normal_pdf(x, mu=0, sig=6):
            return (1 / (sig * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sig) ** 2)
        
        normal_curve = axes.plot(
            lambda x: normal_pdf(x, 0, sigma),
            x_range=[-20, 20],
            color=RED,
            stroke_width=4
        )
        
        curve_label = MathTex(
            r"f(X_\sigma) = \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{X_\sigma^2}{2\sigma^2}}",
            font_size=32,
            color=YELLOW
        ).to_corner(UR, buff=0.5)
        
        self.play(
            Create(normal_curve),
            Write(curve_label),
            run_time=2
        )
        self.wait(1)
        
        # ========== STANDARD DEVIATION PARAMETER ==========
        sigma_label = MathTex(r"\sigma = 6 \text{ dB}", font_size=32, color=YELLOW)
        sigma_label.next_to(curve_label, DOWN, buff=0.3, aligned_edge=LEFT)
        sigma_box = SurroundingRectangle(sigma_label, color=YELLOW, buff=0.15)
        
        self.play(
            Write(sigma_label),
            Create(sigma_box)
        )
        self.wait(1)
        
        # ========== 68-95-99.7 RULE ==========
        
        # Create regions
        # 68% region (-σ to +σ)
        region_68 = axes.get_area(
            normal_curve,
            x_range=[-sigma, sigma],
            color=GREEN,
            opacity=0.3
        )
        
        
        # 95% region (-2σ to +2σ)
        region_95 = axes.get_area(
            normal_curve,
            x_range=[-2*sigma, 2*sigma],
            color=YELLOW,
            opacity=0.3
        )
        
        # 99.7% region (-3σ to +3σ)
        region_997 = axes.get_area(
            normal_curve,
            x_range=[-3*sigma, 3*sigma],
            color=ORANGE,
            opacity=0.15
        )
        
        rule_title = Text("68-95-99.7 Rule:", font_size=28, color=WHITE, weight=BOLD)
        rule_title.to_corner(UL, buff=0.5).shift(DOWN * 0.5)
        
        rule_text = VGroup(
            Text("68% within ±σ (±6 dB)", font_size=20, color=GREEN),
            Text("95% within ±2σ (±12 dB)", font_size=20, color=YELLOW),
            Text("99.7% within ±3σ (±18 dB)", font_size=20, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rule_text.next_to(rule_title, DOWN, buff=0.2, aligned_edge=LEFT)
        
        self.play(Write(rule_title))
        self.wait(0.5)
        
        # Animate 68% region
        self.play(
            FadeIn(region_68),
            Write(rule_text[0])
        )
        
        # Add markers
        marker_left_1 = DashedLine(
            axes.c2p(-sigma, 0),
            axes.c2p(-sigma, normal_pdf(-sigma, 0, sigma)),
            color=GREEN,
            dash_length=0.1
        )
        marker_right_1 = DashedLine(
            axes.c2p(sigma, 0),
            axes.c2p(sigma, normal_pdf(sigma, 0, sigma)),
            color=GREEN,
            dash_length=0.1
        )
        label_left_1 = MathTex(r"-\sigma", font_size=20, color=GREEN).next_to(marker_left_1, DOWN, buff=0.1)
        label_right_1 = MathTex(r"+\sigma", font_size=20, color=GREEN).next_to(marker_right_1, DOWN, buff=0.1)
        
        self.play(
            Create(marker_left_1),
            Create(marker_right_1),
            Write(label_left_1),
            Write(label_right_1)
        )
        self.wait(1)
        self.play(FadeOut(region_68))
        self.wait(0.5)
        # Animate 95% region
        self.play(
            FadeIn(region_95),
            Write(rule_text[1])
        )
        
        marker_left_2 = DashedLine(
            axes.c2p(-2*sigma, 0),
            axes.c2p(-2*sigma, normal_pdf(-2*sigma, 0, sigma)),
            color=YELLOW,
            dash_length=0.1
        )
        marker_right_2 = DashedLine(
            axes.c2p(2*sigma, 0),
            axes.c2p(2*sigma, normal_pdf(2*sigma, 0, sigma)),
            color=YELLOW,
            dash_length=0.1
        )
        
        self.play(
            Create(marker_left_2),
            Create(marker_right_2)
        )
        self.wait(1)
        self.play(FadeOut(region_95))
        self.wait(1.5)
        # Animate 99.7% region
        self.play(
            FadeIn(region_997),
            Write(rule_text[2])
        )
        
        marker_left_3 = DashedLine(
            axes.c2p(-3*sigma, 0),
            axes.c2p(-3*sigma, normal_pdf(-3*sigma, 0, sigma)),
            color=ORANGE,
            dash_length=0.1
        )
        marker_right_3 = DashedLine(
            axes.c2p(3*sigma, 0),
            axes.c2p(3*sigma, normal_pdf(3*sigma, 0, sigma)),
            color=ORANGE,
            dash_length=0.1
        )
        
        self.play(
            Create(marker_left_3),
            Create(marker_right_3)
        )
        self.wait(1)
        self.play(FadeOut(region_997))
        self.wait(0.5)
        self.play(FadeOut(rule_title), FadeOut(rule_text))
        # ========== FINAL SUMMARY ==========
        summary_box = VGroup(
            Text("Key Takeaway:", font_size=24, color=YELLOW, weight=BOLD),
            Text("Shadowing follows a log-normal distribution", font_size=20),
            Text("with zero mean and standard deviation σ", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        summary_box.to_edge(RIGHT, buff=0.4)
        summary_box.shift(UP*0.5)
        
        # summary_rect = SurroundingRectangle(summary_box, color=BLUE, buff=0.25)
        
        self.play(
            FadeIn(summary_box, shift=UP),
            # Create(summary_rect)
        )
        
        self.wait(4)