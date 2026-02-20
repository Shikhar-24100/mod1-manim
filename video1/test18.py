from manim import *
import numpy as np

class RealMeasurementOverlay(Scene):
    """Animation 21: Real measurement overlay showing model comparison"""
    
    def construct(self):
        # Title
        title = Text("Model Validation: Real Measurements", font_size=44)
        subtitle = Text("Which model fits reality better?", font_size=26, color=BLUE)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(
            title.animate.scale(0.75).to_edge(UP, buff=0.2),
            FadeOut(subtitle)
        )
        
        # Create axes
        axes = Axes(
            x_range=[0, 500, 100],
            y_range=[-100, -40, 20],
            x_length=10,
            y_length=5,
            axis_config={"color": GRAY, "include_tip": True},
            x_axis_config={"numbers_to_include": np.arange(0, 500, 100)},
            y_axis_config={"numbers_to_include": np.arange(-100, -40, 20)}
        ).shift(DOWN * 0.5)
        
        x_label = Text("Distance (m)", font_size=20).next_to(axes.x_axis, DOWN)
        y_label = Text("Received Power (dBm)", font_size=20).next_to(axes.y_axis, LEFT).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)
        
        # ========== GENERATE MEASURED DATA POINTS ==========
        np.random.seed(42)
        num_points = 30
        distances = np.linspace(50, 450, num_points)
        
        # Realistic measured data with shadowing
        def path_loss_with_shadowing(d):
            # Path loss component
            pl = -60 - 30 * np.log10(d / 100)
            # Shadowing component (log-normal with σ = 8 dB)
            shadowing = np.random.normal(0, 8)
            return pl + shadowing
        
        measured_powers = [path_loss_with_shadowing(d) for d in distances]
        
        # Create scatter plot points
        scatter_points = VGroup()
        for d, p in zip(distances, measured_powers):
            point = Dot(
                axes.c2p(d, p),
                color=WHITE,
                radius=0.06
            )
            scatter_points.add(point)
        
        measurement_label = Text("Measured Data", font_size=18, color=WHITE, weight=BOLD)
        measurement_label.to_corner(UR, buff=0.5).shift(DOWN * 1)
        measurement_dot = Dot(color=WHITE, radius=0.08).next_to(measurement_label, LEFT, buff=0.1)
        
        self.play(
            LaggedStart(*[FadeIn(point, scale=1.5) for point in scatter_points], lag_ratio=0.03),
            run_time=2
        )
        self.play(Write(measurement_label), FadeIn(measurement_dot))
        self.wait(1)
        
        # ========== OVERLAY FRIIS CURVE ==========
        friis_label = Text("Friis Equation", font_size=18, color=RED, weight=BOLD)
        friis_label.next_to(measurement_label, DOWN, buff=0.2, aligned_edge=LEFT)
        friis_line = Line(LEFT * 0.3, RIGHT * 0.3, color=BLUE, stroke_width=4)
        friis_line.next_to(friis_label, LEFT, buff=0.1)
        
        self.play(Write(friis_label), Create(friis_line))
        
        # Friis curve (deterministic path loss)
        friis_curve = axes.plot(
            lambda x: -60 - 30 * np.log10(x / 100),
            x_range=[50, 450],
            color=BLUE,
            stroke_width=4
        )
        
        self.play(Create(friis_curve, run_time=2))
        self.wait(1)
        
        # Show misfit
        misfit_text = Text("X Misses most points!", font_size=20, color=RED, slant=ITALIC)
        misfit_text.next_to(friis_label, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(misfit_text))
        self.wait(1)
        
        # ========== OVERLAY SHADOWING MODEL WITH CONFIDENCE BAND ==========
        shadowing_label = Text("Shadowing Model", font_size=18, color=GREEN, weight=BOLD)
        shadowing_label.next_to(misfit_text, DOWN, buff=0.4, aligned_edge=LEFT)
        shadowing_line = Line(LEFT * 0.3, RIGHT * 0.3, color=GREEN, stroke_width=4)
        shadowing_line.next_to(shadowing_label, LEFT, buff=0.1)
        
        self.play(Write(shadowing_label), Create(shadowing_line))
        
        # Mean curve (same as Friis)
        mean_curve = axes.plot(
            lambda x: -60 - 30 * np.log10(x / 100),
            x_range=[50, 450],
            color=GREEN,
            stroke_width=4
        )
        
        # Confidence band (±2σ = ±16 dB for 95% confidence)
        upper_bound = axes.plot(
            lambda x: -60 - 30 * np.log10(x / 100) + 16,
            x_range=[50, 450],
            color=GREEN,
            stroke_width=2,
            stroke_opacity=0.5
        )
        
        lower_bound = axes.plot(
            lambda x: -60 - 30 * np.log10(x / 100) - 16,
            x_range=[50, 450],
            color=GREEN,
            stroke_width=2,
            stroke_opacity=0.5
        )
        
        # Create shaded region
        confidence_band = self.create_confidence_band(axes, 50, 450)
        
        self.play(FadeIn(confidence_band, run_time=1.5))
        self.play(
            Create(mean_curve, run_time=1.5),
            Create(upper_bound, run_time=1.5),
            Create(lower_bound, run_time=1.5)
        )
        self.wait(1)
        
        # Show good fit
        goodfit_text = Text("✓ Captures variation!", font_size=16, color=GREEN, weight=BOLD)
        goodfit_text.next_to(shadowing_label, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(goodfit_text))
        self.wait(1)
        
        # Highlight some points within the band
        points_in_band = VGroup(*[p for p in scatter_points])
        self.play(
            points_in_band.animate.set_color(GREEN).scale(1.3),
            run_time=1.5
        )
        self.play(points_in_band.animate.scale(1/1.3))
        
        # Final conclusion
        conclusion = VGroup(
            Text("Shadowing Model:", font_size=24, color=YELLOW, weight=BOLD),
            Text("Better for Real-World Predictions", font_size=20, color=GREEN)
        ).arrange(DOWN, buff=0.1)
        conclusion.to_edge(DOWN, buff=0.5)
        
        box = SurroundingRectangle(conclusion, color=YELLOW, buff=0.2, stroke_width=3)
        
        self.play(
            FadeIn(box),
            Write(conclusion)
        )
        self.wait(10)
    
    def create_confidence_band(self, axes, x_min, x_max):
        """Create a shaded confidence band"""
        points_upper = []
        points_lower = []
        
        for x in np.linspace(x_min, x_max, 100):
            mean_y = -60 - 30 * np.log10(x / 100)
            upper_y = mean_y + 16
            lower_y = mean_y - 16
            
            points_upper.append(axes.c2p(x, upper_y))
            points_lower.append(axes.c2p(x, lower_y))
        
        # Create polygon for shaded region
        points = points_upper + points_lower[::-1]
        band = Polygon(*points, color=GREEN, fill_opacity=0.2, stroke_width=0)
        
        return band


# To render these animations:
# manim -pql friis_vs_shadowing.py FriisVsShadowingComparison
# manim -pql friis_vs_shadowing.py DecisionTreeFlowchart
# manim -pql friis_vs_shadowing.py RealMeasurementOverlay