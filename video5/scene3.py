from manim import *
import numpy as np

config.frame_width = 16
config.frame_height = 9

class RayleighFadingScene(Scene):
    def construct(self):
        # Title
        title = Text("Scene 3: Rayleigh Fading", font_size=48, color=YELLOW)
        subtitle = Text("The 'Aimless' Wander", font_size=32, color=BLUE)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Setup IQ plane
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY, "include_tip": True},
        ).shift(LEFT * 3)
        
        x_label = MathTex("I", color=RED).next_to(axes.x_axis.get_end(), RIGHT)
        y_label = MathTex("Q", color=BLUE).next_to(axes.y_axis.get_end(), UP)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait()
        
        # Generate random walk data (Rayleigh fading)
        np.random.seed(42)
        n_points = 500
        I_values = np.cumsum(np.random.randn(n_points) * 0.1)
        Q_values = np.cumsum(np.random.randn(n_points) * 0.1)
        
        # Normalize to keep within bounds
        I_values = I_values - np.mean(I_values)
        Q_values = Q_values - np.mean(Q_values)
        scale = 2.5 / max(np.max(np.abs(I_values)), np.max(np.abs(Q_values)))
        I_values *= scale
        Q_values *= scale
        
        # Create the glowing dot
        dot = Dot(axes.c2p(0, 0), color=YELLOW, radius=0.08)
        dot.set_sheen(-0.4, DOWN)
        glow = Circle(radius=0.15, color=YELLOW, fill_opacity=0.3, stroke_width=0)
        glow.move_to(dot.get_center())
        
        dot_group = VGroup(glow, dot)
        
        self.play(FadeIn(dot_group))
        self.wait()
        
        # Text: Show only the tip
        tip_text = Text("Show only the tip of the resultant vector", font_size=28)
        tip_text.to_edge(UP)
        self.play(Write(tip_text))
        self.wait()
        
        # Create traced path
        path = VMobject(color=YELLOW, stroke_width=2)
        path.set_points_as_corners([axes.c2p(I_values[0], Q_values[0])])
        
        def update_path(mob):
            new_point = dot.get_center()
            mob.add_points_as_corners([new_point])
        
        path.add_updater(update_path)
        self.add(path)
        
        # Text: Fast forward time
        self.play(Transform(tip_text, Text("Fast Forward Time...", font_size=32, color=GREEN).to_edge(UP)))
        
        # Animate the random walk
        animations = []
        for i in range(1, n_points):
            new_pos = axes.c2p(I_values[i], Q_values[i])
            animations.append(dot_group.animate.move_to(new_pos))
        
        self.play(Succession(*animations, run_time=8, rate_func=linear))
        
        path.remove_updater(update_path)
        self.wait()
        
        # Text: Messy scribble
        self.play(Transform(tip_text, 
                          Text("A messy scribble centered at origin (0,0)", 
                               font_size=28, color=WHITE).to_edge(UP)))
        self.wait(2)
        
        # Fade out the dot, keep the path
        self.play(FadeOut(dot_group), FadeOut(tip_text))
        self.wait()
        
        # Part 2: The Distribution
        dist_title = Text("The Distribution: Where is the dot most of the time?", 
                         font_size=32, color=YELLOW)
        dist_title.to_edge(UP)
        self.play(Write(dist_title))
        self.wait()
        
        # Add histograms on the side
        # I-axis projection (bottom)
        i_hist_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 80, 20],
            x_length=6,
            y_length=1.5,
            axis_config={"color": GRAY},
        ).next_to(axes, DOWN, buff=0.3)
        
        i_hist_label = Text("I-axis distribution", font_size=20, color=RED)
        i_hist_label.next_to(i_hist_axes, DOWN)
        
        # Q-axis projection (left)
        q_hist_axes = Axes(
            x_range=[0, 80, 20],
            y_range=[-3, 3, 1],
            x_length=1.5,
            y_length=6,
            axis_config={"color": GRAY},
        ).next_to(axes, LEFT, buff=0.3)
        
        q_hist_label = Text("Q-axis\ndist.", font_size=18, color=BLUE)
        q_hist_label.next_to(q_hist_axes, LEFT)
        
        self.play(Create(i_hist_axes), Write(i_hist_label))
        self.play(Create(q_hist_axes), Write(q_hist_label))
        self.wait()
        
        # Create histogram bars
        i_hist, i_bins = np.histogram(I_values, bins=30, range=(-3, 3))
        q_hist, q_bins = np.histogram(Q_values, bins=30, range=(-3, 3))
        
        i_bars = VGroup()
        for i in range(len(i_hist)):
            bar_height = i_hist[i]
            bar = Rectangle(
                width=(i_bins[i+1] - i_bins[i]) * 2,
                height=bar_height / 10,
                fill_color=RED,
                fill_opacity=0.7,
                stroke_width=0
            )
            bar.move_to(i_hist_axes.c2p((i_bins[i] + i_bins[i+1]) / 2, bar_height / 2))
            i_bars.add(bar)
        
        q_bars = VGroup()
        for i in range(len(q_hist)):
            bar_width = q_hist[i]
            bar = Rectangle(
                width=bar_width / 10,
                height=(q_bins[i+1] - q_bins[i]) * 2,
                fill_color=BLUE,
                fill_opacity=0.7,
                stroke_width=0
            )
            bar.move_to(q_hist_axes.c2p(bar_width / 2, (q_bins[i] + q_bins[i+1]) / 2))
            q_bars.add(bar)
        
        self.play(Create(i_bars), Create(q_bars))
        self.wait()
        
        # Add Gaussian curves
        gaussian_text = Text("Both follow Gaussian (Bell Curve) distributions!", 
                            font_size=28, color=GREEN)
        gaussian_text.move_to(dist_title)
        self.play(Transform(dist_title, gaussian_text))
        
        # Gaussian curve overlay on I
        i_gaussian = i_hist_axes.plot(
            lambda x: 70 * np.exp(-x**2 / (2 * np.var(I_values))),
            x_range=[-3, 3],
            color=YELLOW,
            stroke_width=4
        )
        
        # Gaussian curve overlay on Q
        q_gaussian = q_hist_axes.plot(
            lambda y: 70 * np.exp(-y**2 / (2 * np.var(Q_values))),
            x_range=[0, 3],
            color=YELLOW,
            stroke_width=4
        )
        q_gaussian.rotate(PI/2, about_point=q_hist_axes.c2p(0, 0))
        
        self.play(Create(i_gaussian), Create(q_gaussian))
        self.wait(2)
        
        # Part 3: The Rayleigh Formula
        self.play(
            FadeOut(dist_title),
            FadeOut(i_bars), FadeOut(q_bars),
            FadeOut(i_gaussian), FadeOut(q_gaussian),
            FadeOut(i_hist_axes), FadeOut(i_hist_label),
            FadeOut(q_hist_axes), FadeOut(q_hist_label)
        )
        
        formula_title = Text("The Rayleigh Distribution", font_size=36, color=YELLOW)
        formula_title.to_edge(UP)
        self.play(Write(formula_title))
        
        # Show amplitude calculation
        amplitude_values = np.sqrt(I_values**2 + Q_values**2)
        
        # Create Rayleigh PDF on the right
        rayleigh_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1, 0.2],
            x_length=5,
            y_length=4,
            axis_config={"color": GRAY, "include_tip": True},
        ).to_edge(RIGHT).shift(UP * 0.5)
        
        rayleigh_x_label = MathTex("r", font_size=36).next_to(rayleigh_axes.x_axis.get_end(), RIGHT)
        rayleigh_y_label = MathTex("p(r)", font_size=36).next_to(rayleigh_axes.y_axis.get_end(), UP)
        
        self.play(Create(rayleigh_axes), Write(rayleigh_x_label), Write(rayleigh_y_label))
        
        # Rayleigh PDF formula
        sigma = np.std(I_values)
        rayleigh_curve = rayleigh_axes.plot(
            lambda r: (r / sigma**2) * np.exp(-r**2 / (2 * sigma**2)),
            x_range=[0, 4],
            color=YELLOW,
            stroke_width=4
        )
        
        self.play(Create(rayleigh_curve))
        
        # Add histogram of amplitudes
        amp_hist, amp_bins = np.histogram(amplitude_values, bins=40, range=(0, 4))
        amp_bars = VGroup()
        for i in range(len(amp_hist)):
            bar_height = amp_hist[i] / np.max(amp_hist) * 0.8
            bar = Rectangle(
                width=(amp_bins[i+1] - amp_bins[i]) * rayleigh_axes.x_length / 4,
                height=bar_height * rayleigh_axes.y_length,
                fill_color=BLUE,
                fill_opacity=0.5,
                stroke_width=1,
                stroke_color=WHITE
            )
            bar.move_to(rayleigh_axes.c2p((amp_bins[i] + amp_bins[i+1]) / 2, bar_height / 2))
            amp_bars.add(bar)
        
        self.play(Create(amp_bars))
        self.wait()
        
        # Formula explanation
        formula = MathTex(
            r"r = \sqrt{I^2 + Q^2}",
            font_size=40,
            color=WHITE
        ).next_to(rayleigh_axes, DOWN, buff=0.5)
        
        explanation = VGroup(
            Text("When I and Q are both Gaussian,", font_size=24),
            Text("the amplitude r follows Rayleigh distribution", font_size=24, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(formula, DOWN, buff=0.3)
        
        self.play(Write(formula))
        self.play(Write(explanation))
        self.wait(2)
        
        # Final definition
        definition = Text(
            "Rayleigh Fading: NO dominant path\nScribble centered at origin (0,0)",
            font_size=28,
            color=GREEN,
            line_spacing=1.5
        )
        definition.to_edge(DOWN)
        
        self.play(Write(definition))
        self.wait(3)
        
        # Fade all
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()