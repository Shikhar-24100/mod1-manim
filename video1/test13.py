from manim import *
class PathLossExponentComparison(Scene):
    """Animation 16: Path Loss Exponent 'n' Comparison"""
    
    def construct(self):
        # Title
        title = Text("Path Loss Exponent (n)", font_size=44, weight=BOLD)
        subtitle = Text("How environment affects signal decay", font_size=28, color=BLUE)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(
            title.animate.scale(0.75).to_edge(UP, buff=0.3),
            FadeOut(subtitle)
        )
        
        # ========== SETUP AXES ==========
        # Reference values (moved before axes so we can estimate y-range)
        P0 = -30  # Reference power at 1m in dBm
        d0 = 1    # Reference distance
        max_d = 500
        x_start = 1
        x_step = 100

        # Estimate y-range from representative curves (n = 2..5)
        sample_ds = np.logspace(np.log10(x_start), np.log10(max_d), 300)
        env_ns = [2, 3, 4, 5]
        def path_val(n, d):
            return P0 if d < d0 else P0 - 10 * n * np.log10(d / d0)
        sampled_vals = []
        for n in env_ns:
            sampled_vals.extend([path_val(n, d) for d in sample_ds])

        y_min = min(sampled_vals) - 10  # padding
        y_max = max(sampled_vals) + 5
        # round to nice ticks
        y_min = np.floor(y_min / 10) * 10
        y_max = np.ceil(y_max / 10) * 10
        y_step = 20

        axes = Axes(
            x_range=[x_start, max_d, x_step],
            y_range=[y_min, y_max, y_step],
            x_length=10,   # wider so 1..500 is readable
            y_length=6,    # taller so large negative values fit
            axis_config={
                "color": WHITE,
                "include_numbers": True,
                "font_size": 18,
            }
        ).shift(DOWN * 0.3)
        
        x_label = Text("Distance (m)", font_size=24).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("Received Power (dBm)", font_size=24).rotate(PI/2).next_to(axes.y_axis, LEFT, buff=0.4)
        
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label)
        )
        self.wait(0.5)
        
        # ========== PATH LOSS FUNCTION ==========
        P0 = -30  # Reference power at 1m in dBm
        d0 = 1    # Reference distance
        
        def path_loss_curve(n):
            def func(d):
                if d < d0:
                    return P0
                return P0 - 10 * n * np.log10(d / d0)
            return func
        
        # ========== CREATE CURVES FOR DIFFERENT n VALUES ==========
        
        # Starting point marker
        start_point = Dot(axes.c2p(d0, P0), color=WHITE, radius=0.1)
        start_label = Text("Reference\npoint", font_size=16, color=WHITE).next_to(start_point, UP, buff=0.2)
        
        self.play(
            FadeIn(start_point, scale=1.5),
            Write(start_label)
        )
        self.wait(0.5)
        
        # Define environments
        environments = [
            {"n": 2, "color": GREEN, "label": "Free Space (n=2)", "env": "Open area, LOS"},
            {"n": 3, "color": YELLOW, "label": "Urban (n=3)", "env": "Suburban, some buildings"},
            {"n": 4, "color": ORANGE, "label": "Dense Urban (n=4)", "env": "City center, tall buildings"},
            {"n": 5, "color": RED, "label": "Indoor/Obstructed (n≥5)", "env": "Inside buildings, heavy obstruction"}
        ]
        
        curves = VGroup()
        curve_labels = VGroup()
        
        # Animate curves one by one
        for i, env in enumerate(environments):
            n = env["n"]
            color = env["color"]
            label_text = env["label"]
            env_desc = env["env"]
            
            # Create curve
            curve = axes.plot(
                path_loss_curve(n),
                x_range=[d0, 500],
                color=color,
                stroke_width=4
            )
            curves.add(curve)
            
            # Animate curve drawing
            self.play(Create(curve), run_time=1.5)
            
            # Add label on the curve
            end_point = axes.c2p(500, path_loss_curve(n)(500))
            curve_label = VGroup(
                Text(label_text, font_size=20, color=color, weight=BOLD),
                Text(env_desc, font_size=14, color=color, slant=ITALIC)
            ).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
            
            # Position labels on right side
            curve_label.next_to(end_point, RIGHT, buff=0.2)
            curve_label.shift(UP * 0.3 + LEFT*1)  # stagger vertically
            
            # Draw arrow from label to curve
            # arrow = Arrow(
            #     curve_label.get_left(),
            #     end_point,
            #     color=color,
            #     buff=0.1,
            #     stroke_width=2
            # )
            
            self.play(
                FadeIn(curve_label, shift=LEFT)
            )
            curve_labels.add(VGroup(curve_label))
            
            self.wait(0.5)
        
        self.wait(1)
        
        # ========== LEGEND BOX ==========
        # legend_title = Text("Environment Types", font_size=26, color=BLUE, weight=BOLD)
        # legend_title.to_corner(UL, buff=0.5).shift(DOWN * 1)
        
        # legend_items = VGroup()
        # for env in environments:
        #     item = VGroup(
        #         Line(ORIGIN, RIGHT * 0.4, color=env["color"], stroke_width=6),
        #         Text(env["label"], font_size=18, color=env["color"])
        #     ).arrange(RIGHT, buff=0.2)
        #     legend_items.add(item)
        
        # legend_items.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        # legend_items.next_to(legend_title, DOWN, buff=0.2, aligned_edge=LEFT)
        
        # legend_box = SurroundingRectangle(
        #     VGroup(legend_title, legend_items),
        #     color=BLUE,
        #     buff=0.2,
        #     stroke_width=2,
        #     fill_opacity=0.1,
        #     fill_color=BLACK
        # )
        
        # self.play(
        #     Create(legend_box),
        #     Write(legend_title),
        #     FadeIn(legend_items, shift=RIGHT, lag_ratio=0.1)
        # )
        self.wait(1)
        
        # ========== COMPARISON ANNOTATIONS ==========
        
        # Show decay rate comparison at specific distance
        compare_distance = 200
        compare_line = DashedLine(
            axes.c2p(compare_distance, -120),
            axes.c2p(compare_distance, -20),
            color=WHITE,
            dash_length=0.1,
            stroke_width=2
        )
        
        compare_label = Text(f"At {compare_distance}m", font_size=18, color=WHITE)
        compare_label.next_to(compare_line, DOWN, buff=0.2)
        
        self.play(
            Create(compare_line),
            Write(compare_label)
        )
        
        # Add dots at intersection points
        dots = VGroup()
        power_labels = VGroup()
        
        for i, env in enumerate(environments):
            n = env["n"]
            color = env["color"]
            power_at_d = path_loss_curve(n)(compare_distance)
            
            dot = Dot(axes.c2p(compare_distance, power_at_d), color=color, radius=0.08)
            dots.add(dot)
            
            power_label = MathTex(
                f"{power_at_d:.1f}",
                font_size=16,
                color=color
            ).next_to(dot, LEFT, buff=0.15)
            power_labels.add(power_label)
        
        self.play(
            LaggedStart(*[FadeIn(dot, scale=1.5) for dot in dots], lag_ratio=0.2),
            LaggedStart(*[Write(label) for label in power_labels], lag_ratio=0.2)
        )
        self.wait(1)
        
        # Show power difference
        power_diff = path_loss_curve(2)(compare_distance) - path_loss_curve(5)(compare_distance)
        
        diff_brace = BraceBetweenPoints(
            axes.c2p(compare_distance, path_loss_curve(2)(compare_distance)),
            axes.c2p(compare_distance, path_loss_curve(5)(compare_distance)),
            direction=RIGHT,
            color=YELLOW
        )
        
        diff_label = MathTex(
            f"\\Delta = {power_diff:.1f} \\text{{ dB}}",
            font_size=22,
            color=YELLOW
        ).next_to(diff_brace, RIGHT, buff=0.1)
        
        self.play(
            GrowFromCenter(diff_brace),
            Write(diff_label)
        )
        self.wait(1)
        
        # ========== KEY INSIGHTS ==========
        # insights_title = Text("Key Insights:", font_size=24, color=BLUE, weight=BOLD)
        # insights_title.to_edge(DOWN, buff=1.2)
        
        # insights = VGroup(
        #     Text("• Larger n → Faster signal decay", font_size=18),
        #     Text("• All curves start at same point (d₀, P₀)", font_size=18),
        #     Text("• Environment dramatically affects coverage!", font_size=18, color=RED, weight=BOLD)
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        # insights.next_to(insights_title, DOWN, buff=0.15, aligned_edge=LEFT)
        
        # insights_box = SurroundingRectangle(
        #     # VGroup(insights_title, insights),
        #     color=BLUE,
        #     buff=0.2,
        #     stroke_width=2
        # )
        
        # self.play(
        #     Create(insights_box),
        #     Write(insights_title),
        #     FadeIn(insights, shift=UP, lag_ratio=0.15)
        # )
        
        self.wait(4)
        
        # ========== PRACTICAL EXAMPLE ==========
        # Fade out comparison elements
        self.play(
            FadeOut(VGroup(compare_line, compare_label, dots, power_labels, diff_brace, diff_label))
        )
        
        # example_text = Text("Practical Example:", font_size=28, color=GREEN, weight=BOLD)
        # example_text.move_to(ORIGIN).shift(UP * 2)
        
        # example_content = VGroup(
        #     Text("For 500m range:", font_size=22, color=WHITE),
        #     Text("Free Space (n=2): -57 dBm", font_size=20, color=GREEN),
        #     Text("Dense Urban (n=4): -90 dBm", font_size=20, color=ORANGE),
        #     Text("→ 33 dB difference!", font_size=22, color=RED, weight=BOLD)
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        # example_content.next_to(example_text, DOWN, buff=0.3)
        
        example_box = SurroundingRectangle(
            color=GREEN,
            buff=0.3,
            fill_opacity=0.1,
            fill_color=BLACK
        )
        
        # self.play(
        #     FadeIn(example_box),
        #     Write(example_text),
        #     FadeIn(example_content, shift=UP, lag_ratio=0.15),
        #     run_time=2
        # )
        
        self.wait(10)