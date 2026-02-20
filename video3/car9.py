from manim import *
import numpy as np

class Phase4_CoherenceBandwidth(Scene):
    """
    Phase 4: Frequency-Domain Effects of Delay Spread
    Pedagogical sequence: intuition → justification → definition → math → correlation → comparison → transition
    """
    
    def construct(self):
        self.scene_4_1_time_spread_frequency_ripples()
        self.scene_4_2_why_frequency_response_matters()
        self.scene_4_3_definition_coherence_bandwidth()
        self.scene_4_4_mathematical_relationship()
        self.scene_4_5_correlation_based_definitions()
        self.scene_4_6_high_vs_low_bc()
        self.scene_4_7_transition_forward()
    
    # ================================================================
    # SCENE 4.1: Time Spread ↔ Frequency Ripples (INTUITION FIRST)
    # ================================================================
    def scene_4_1_time_spread_frequency_ripples(self):
        """
        Goal: Visually establish inverse relationship.
        NO formulas, NO Bc term yet.
        """
        title = Title("Time Spread Causes Frequency Ripples", color=BLUE_B).scale(0.85)
        self.add(title)
        self.wait(1)
        
        # LEFT SIDE: Small delay spread → Smooth H(f)
        left_label = Text("Small σ_τ", font_size=18, color=YELLOW_B, weight=BOLD)
        left_label.to_edge(LEFT, buff=1).shift(UP * 3.5)
        
        ax_left = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.5, 0.5],
            x_length=4, y_length=3,
            axis_config={"color": GREY_B, "font_size": 12},
            tips=False
        ).to_edge(LEFT, buff=1).shift(DOWN * 0.5)
        
        # Smooth frequency response (small delay spread)
        h_smooth = ax_left.plot(
            lambda f: 1.0 + 0.15 * np.cos(0.5 * f),
            color=GREEN_C,
            x_range=[0, 10]
            
        )
        
        # RIGHT SIDE: Large delay spread → Ripples
        right_label = Text("Large σ_τ", font_size=18, color=RED_C, weight=BOLD)
        right_label.to_edge(RIGHT, buff=1).shift(UP * 3.5)
        
        ax_right = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.5, 0.5],
            x_length=4, y_length=3,
            axis_config={"color": GREY_B, "font_size": 12},
            tips=False
        ).to_edge(RIGHT, buff=1).shift(DOWN * 0.5)
        
        # Rippled frequency response (large delay spread)
        h_ripples = ax_right.plot(
            lambda f: 1.0 + 0.8 * np.cos(3.5 * f) + 0.4 * np.sin(5 * f),
            color=RED_C,
            x_range=[0, 10]
            
        )
        
        # Axes labels
        left_ylabel = Text("|H(f)|", font_size=12, color=GREY_B).next_to(ax_left.y_axis, LEFT, buff=0.2)
        right_ylabel = Text("|H(f)|", font_size=12, color=GREY_B).next_to(ax_right.y_axis, LEFT, buff=0.2)
        
        self.add(left_label, ax_left, left_ylabel)
        self.play(Write(h_smooth))
        self.wait(1.5)
        
        self.add(right_label, ax_right, right_ylabel)
        self.play(Write(h_ripples))
        self.wait(1.5)
        
        insight = Text(
            "More spread in time → More ripples in frequency",
            font_size=16, color=WHITE, weight=BOLD
        ).shift(DOWN * 3.8)
        self.play(FadeIn(insight))
        self.wait(2.5)
        
        self.play(FadeOut(title), FadeOut(left_label), FadeOut(ax_left), FadeOut(left_ylabel),
                 FadeOut(h_smooth), FadeOut(right_label), FadeOut(ax_right), FadeOut(right_ylabel),
                 FadeOut(h_ripples), FadeOut(insight))
        self.wait(0.5)
    
    # ================================================================
    # SCENE 4.2: Why Frequency Response Matters
    # ================================================================
    def scene_4_2_why_frequency_response_matters(self):
        """
        Goal: Show Y(f) = X(f) * H(f) and justify frequency flatness.
        """
        title = Title("Why Frequency Response Matters", color=BLUE_B).scale(0.85)
        self.add(title)
        self.wait(1)
        
        # Setup: Three frequency plots stacked vertically
        ax_x = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.5, 0.5],
            x_length=10, y_length=2.5,
            axis_config={"color": GREY_B, "font_size": 12},
            tips=False
        ).shift(UP * 2)
        
        ax_h = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.5, 0.5],
            x_length=10, y_length=2.5,
            axis_config={"color": GREY_B, "font_size": 12},
            tips=False
        ).shift(DOWN * 0.5)
        
        ax_y = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.5, 0.5],
            x_length=10, y_length=2.5,
            axis_config={"color": GREY_B, "font_size": 12},
            tips=False
        ).shift(DOWN * 3)
        
        # Labels
        label_x = Text("X(f): Signal Spectrum", font_size=13, color=BLUE, weight=BOLD)
        label_x.next_to(ax_x, LEFT, buff=0.3)
        
        label_h = Text("H(f): Channel Response", font_size=13, color=YELLOW, weight=BOLD)
        label_h.next_to(ax_h, LEFT, buff=0.3)
        
        label_y = Text("Y(f): Output Spectrum", font_size=13, color=GREEN_C, weight=BOLD)
        label_y.next_to(ax_y, LEFT, buff=0.3)
        
        # Plot signal spectrum (narrow)
        plot_x = ax_x.plot(
            lambda f: 1.2 * np.exp(-6 * (f - 5)**2),
            color=BLUE,
            x_range=[3, 7],
            
        )
        
        # Plot channel response (flat in this example)
        plot_h = ax_h.plot(
            lambda f: 1.0 + 0.1 * np.cos(f),
            color=YELLOW,
            x_range=[0, 10],
            
        )
        
        # Plot output (product)
        plot_y = ax_y.plot(
            lambda f: 1.2 * np.exp(-6 * (f - 5)**2) * (1.0 + 0.1 * np.cos(f)),
            color=GREEN_C,
            x_range=[3, 7],
            
        )
        
        self.add(ax_x, label_x)
        self.play(Write(plot_x))
        self.wait(1.5)
        
        self.add(ax_h, label_h)
        self.play(Write(plot_h))
        self.wait(1.5)
        
        # Show multiplication equation
        eq_multiply = MathTex(r"Y(f) = X(f) \cdot H(f)", color=WHITE, font_size=40)
        eq_multiply.next_to(ax_h, RIGHT, buff=0.5)
        self.play(Write(eq_multiply))
        self.wait(1)
        
        # Draw output
        self.add(ax_y, label_y)
        self.play(Write(plot_y))
        self.wait(1.5)
        
        # Narrative
        narrative = Text(
            "Channel multiplies the signal in frequency domain.\n" +
            "Output distortion depends on how much H(f) changes\n" +
            "across the signal's frequency range.",
            font_size=14, color=WHITE
        ).shift(DOWN * 4.2)
        self.play(FadeIn(narrative))
        self.wait(2.5)
        
        self.play(FadeOut(title), FadeOut(ax_x), FadeOut(label_x), FadeOut(plot_x),
                 FadeOut(ax_h), FadeOut(label_h), FadeOut(plot_h), FadeOut(eq_multiply),
                 FadeOut(ax_y), FadeOut(label_y), FadeOut(plot_y), FadeOut(narrative))
        self.wait(0.5)
    
    # ================================================================
    # SCENE 4.3: Definition of Coherence Bandwidth
    # ================================================================
    def scene_4_3_definition_coherence_bandwidth(self):
        """
        Goal: Define Bc as a channel property (frequency range where H(f) is constant).
        """
        title = Title("Coherence Bandwidth: A Channel Property", color=BLUE_B).scale(0.85)
        self.add(title)
        self.wait(1)
        
        # Draw a typical frequency response with a flat region highlighted
        ax = Axes(
            x_range=[0, 10, 1], y_range=[0, 1.5, 0.5],
            x_length=11, y_length=4,
            axis_config={"color": GREY_B, "font_size": 13},
            tips=False
        ).shift(DOWN * 0.5)
        
        x_label = Text("Frequency", font_size=12, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.3)
        y_label = Text("|H(f)|", font_size=12, color=GREY_B).next_to(ax.y_axis, LEFT, buff=0.3)
        
        # Channel response with varying smoothness
        h_response = ax.plot(
            lambda f: 1.0 + 0.6 * np.cos(2 * PI * f / 10) + 0.3 * np.sin(3 * PI * f / 10),
            color=YELLOW,
            x_range=[0, 10],
            
        )
        
        self.add(ax, x_label, y_label)
        self.play(Write(h_response))
        self.wait(1)
        
        # Highlight a flat region (around f=2 to f=4)
        flat_region = Rectangle(
            width=ax.x_length * (2 / 10),
            height=1.5,
            color=GREEN_C,
            fill_opacity=0.2,
            stroke_color=GREEN_C,
            
        )
        flat_region.next_to(ax.c2p(3, 0.75), ORIGIN, coor_mask=np.array([0, 0, 0]))
        flat_region.align_to(ax.c2p(2, 0), UL)
        
        self.play(FadeIn(flat_region))
        self.wait(1)
        
        # Label the flat region
        bc_arrow = Arrow(
            flat_region.get_top() + UP * 0.5,
            flat_region.get_center(),
            color=GREEN_C,
            
            buff=0.1
        )
        bc_label_text = Text("Coherence Bandwidth B_c", font_size=14, color=GREEN_C, weight=BOLD)
        bc_label_text.next_to(bc_arrow, UP, buff=0.3)
        
        self.play(Write(bc_arrow), Write(bc_label_text))
        self.wait(1.5)
        
        # Definition box
        definition = VGroup(
            Text("DEFINITION", font_size=15, color=GREEN_B, weight=BOLD),
            Text("Coherence Bandwidth B_c:", font_size=13, color=GREEN_C),
            Text(
                "The range of frequencies over which\n" +
                "the channel response is approximately constant.",
                font_size=12, color=WHITE
            )
        ).arrange(DOWN, buff=0.3)
        definition.next_to(ax, RIGHT, buff=0.8).shift(UP * 0.5)
        
        definition_box = Rectangle(
            width=definition.width + 0.4,
            height=definition.height + 0.4,
            color=GREEN_C,
            fill_opacity=0.1,
            
        ).surround(definition)
        
        self.play(FadeIn(definition_box), Write(definition))
        self.wait(2)
        
        # Clarification: Signal vs Channel
        clarification = VGroup(
            Text("Important Distinction:", font_size=13, color=YELLOW_A, weight=BOLD),
            Text("Signal Bandwidth B_s  →  Property of SIGNAL", font_size=11, color=BLUE),
            Text("Coherence Bandwidth B_c  →  Property of CHANNEL", font_size=11, color=YELLOW)
        ).arrange(DOWN, buff=0.3).shift(DOWN * 3.5)
        
        self.play(FadeIn(clarification))
        self.wait(2.5)
        
        self.play(FadeOut(title), FadeOut(ax), FadeOut(x_label), FadeOut(y_label),
                 FadeOut(h_response), FadeOut(flat_region), FadeOut(bc_arrow),
                 FadeOut(bc_label_text), FadeOut(definition_box), FadeOut(definition),
                 FadeOut(clarification))
        self.wait(0.5)
    
    # ================================================================
    # SCENE 4.4: Mathematical Relationship (Now It's Earned)
    # ================================================================
    def scene_4_4_mathematical_relationship(self):
        """
        Goal: Tie Bc back to delay spread. Introduce formula.
        """
        title = Title("Coherence Bandwidth Delay Spread", color=BLUE_B).scale(0.85)
        self.add(title)
        self.wait(1)
        
        # Recall the visual from Scene 4.1
        left_label = Text("Small σ_τ", font_size=17, color=YELLOW_B, weight=BOLD)
        left_label.to_edge(LEFT, buff=1).shift(UP * 3)
        
        ax_left = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.5, 0.5],
            x_length=4, y_length=2.5,
            axis_config={"color": GREY_B, "font_size": 11},
            tips=False
        ).to_edge(LEFT, buff=1).shift(DOWN * 0.2)
        
        h_smooth = ax_left.plot(
            lambda f: 1.0 + 0.15 * np.cos(0.5 * f),
            color=GREEN_C,
            x_range=[0, 10]
            
        )
        
        right_label = Text("Large σ_τ", font_size=17, color=RED_C, weight=BOLD)
        right_label.to_edge(RIGHT, buff=1).shift(UP * 3)
        
        ax_right = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.5, 0.5],
            x_length=4, y_length=2.5,
            axis_config={"color": GREY_B, "font_size": 11},
            tips=False
        ).to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        h_ripples = ax_right.plot(
            lambda f: 1.0 + 0.8 * np.cos(3.5 * f) + 0.4 * np.sin(5 * f),
            color=RED_C,
            x_range=[0, 10]
            
        )
        
        self.add(left_label, ax_left, h_smooth)
        self.add(right_label, ax_right, h_ripples)
        self.wait(1)
        
        # Now introduce the formula
        formula = MathTex(
            r"B_c \approx \frac{1}{5\sigma_\tau}",
            color=BLUE,
            font_size=56
        ).shift(DOWN * 2)
        
        self.play(Write(formula))
        self.wait(1.5)
        
        # One-line intuition
        intuition = Text(
            "More spread in time (στ) → Less stability in frequency (narrower B_c)",
            font_size=13, color=WHITE, weight=BOLD
        ).next_to(formula, DOWN, buff=0.8)
        
        self.play(FadeIn(intuition))
        self.wait(2.5)
        
        self.play(FadeOut(title), FadeOut(left_label), FadeOut(ax_left), FadeOut(h_smooth),
                 FadeOut(right_label), FadeOut(ax_right), FadeOut(h_ripples),
                 FadeOut(formula), FadeOut(intuition))
        self.wait(0.5)
    
    # ================================================================
    # SCENE 4.5: Correlation-Based Definitions (Refinement)
    # ================================================================
    def scene_4_5_correlation_based_definitions(self):
        """
        Goal: Show frequency correlation function and two practical thresholds.
        """
        title = Title("Coherence Bandwidth: Correlation Perspective", color=BLUE_B).scale(0.85)
        self.add(title)
        self.wait(1)
        
        # Frequency correlation function
        ax = Axes(
            x_range=[0, 3, 0.5], y_range=[0, 1.2, 0.2],
            x_length=10, y_length=4,
            axis_config={"color": GREY_B, "font_size": 12},
            tips=False
        ).shift(DOWN * 0.3)
        
        x_label = Text("Δf (Frequency Separation)", font_size=12, color=GREY_B)
        x_label.next_to(ax.x_axis, DOWN, buff=0.3)
        
        y_label = Text("|R_H(Δf)| (Correlation)", font_size=12, color=GREY_B)
        y_label.next_to(ax.y_axis, LEFT, buff=0.3)
        
        # Correlation function (decreasing exponential-like)
        corr_func = ax.plot(
            lambda df: np.exp(-3 * df),
            color=BLUE,
            x_range=[0, 3],
            
        )
        
        self.add(ax, x_label, y_label)
        self.play(Write(corr_func))
        self.wait(1.5)
        
        # Threshold 1: 0.9 correlation (stricter)
        threshold_09 = ax.get_horizontal_line_to_graph(0.9, corr_func)
        point_09 = ax.c2p(1/3, 0.9)
        dot_09 = Dot(point_09, color=GREEN_C, radius=0.08)
        
        bc_09_x = ax.x_axis.point_from_proportion(0.11)  # Approximate
        bc_09_line = DashedLine(point_09, ax.c2p(1/3, 0), color=GREEN_C)
        
        self.play(Write(threshold_09), FadeIn(dot_09))
        self.wait(0.8)
        self.play(Write(bc_09_line))
        
        label_09 = Text("B_c,0.9", font_size=12, color=GREEN_C, weight=BOLD)
        label_09.next_to(ax.c2p(1/3, -0.15), DOWN, buff=0.2)
        self.play(Write(label_09))
        self.wait(1)
        
        # Threshold 2: 0.5 correlation (looser)
        threshold_05 = ax.get_horizontal_line_to_graph(0.5, corr_func)
        point_05 = ax.c2p(np.log(2)/3, 0.5)
        dot_05 = Dot(point_05, color=ORANGE, radius=0.08)
        
        bc_05_line = DashedLine(point_05, ax.c2p(np.log(2)/3, 0), color=ORANGE)
        
        self.play(Write(threshold_05), FadeIn(dot_05))
        self.wait(0.8)
        self.play(Write(bc_05_line))
        
        label_05 = Text("B_c,0.5", font_size=12, color=ORANGE, weight=BOLD)
        label_05.next_to(ax.c2p(np.log(2)/3, -0.15), DOWN, buff=0.2)
        self.play(Write(label_05))
        self.wait(1.5)
        
        # Explanation
        explanation = VGroup(
            Text("Different Definitions of Coherence Bandwidth:", font_size=13, color=YELLOW_A, weight=BOLD),
            Text("B_c,0.9  (Stricter):  Smaller bandwidth, higher correlation required", font_size=11, color=GREEN_C),
            Text("B_c,0.5  (Looser):   Larger bandwidth, lower correlation required", font_size=11, color=ORANGE)
        ).arrange(DOWN, buff=0.35).shift(DOWN * 3.5)
        
        self.play(FadeIn(explanation))
        self.wait(2.5)
        
        self.play(FadeOut(title), FadeOut(ax), FadeOut(x_label), FadeOut(y_label),
                 FadeOut(corr_func), FadeOut(threshold_09), FadeOut(dot_09), FadeOut(bc_09_line),
                 FadeOut(label_09), FadeOut(threshold_05), FadeOut(dot_05), FadeOut(bc_05_line),
                 FadeOut(label_05), FadeOut(explanation))
        self.wait(0.5)
    
    # ================================================================
    # SCENE 4.6: High Bc vs Low Bc (COMPARISON)
    # ================================================================
    def scene_4_6_high_vs_low_bc(self):
        """
        Goal: Show that same signal, different Bc → different distortion.
        Emphasize: signal is unchanged, only channel changes.
        """
        title = Title("Impact of Coherence Bandwidth on Signals", color=BLUE_B).scale(0.85)
        self.add(title)
        self.wait(1)
        
        # Setup axes
        ax_high = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.5, 0.5],
            x_length=4.5, y_length=3,
            axis_config={"color": GREY_B, "font_size": 11},
            tips=False
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        
        ax_low = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.5, 0.5],
            x_length=4.5, y_length=3,
            axis_config={"color": GREY_B, "font_size": 11},
            tips=False
        ).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.3)
        
        # Signal spectrum (SAME in both cases)
        signal = lambda f: 1.2 * np.exp(-4 * (f - 5)**2)
        
        signal_high = ax_high.plot(signal, color=BLUE, x_range=[3, 7])
        signal_low = ax_low.plot(signal, color=BLUE, x_range=[3, 7])
        
        # HIGH Bc: smooth channel response
        h_high = ax_high.plot(
            lambda f: 1.0 + 0.1 * np.cos(0.4 * f),
            color=YELLOW,
            x_range=[0, 10],
            
        )
        
        # LOW Bc: rippled channel response
        h_low = ax_low.plot(
            lambda f: 1.0 + 0.7 * np.cos(2.5 * f) + 0.3 * np.sin(3.5 * f),
            color=YELLOW,
            x_range=[0, 10],
            
        )
        
        # Labels
        label_high = Text("High Coherence Bandwidth", font_size=13, color=GREEN_C, weight=BOLD)
        label_high.next_to(ax_high, UP, buff=0.3)
        
        label_low = Text("Low Coherence Bandwidth", font_size=13, color=RED_C, weight=BOLD)
        label_low.next_to(ax_low, UP, buff=0.3)
        
        self.add(label_high, ax_high)
        self.play(Write(signal_high), Write(h_high))
        self.wait(1.5)
        
        self.add(label_low, ax_low)
        self.play(Write(signal_low), Write(h_low))
        self.wait(1.5)
        
        # Critical insight
        insight = Text(
            "Same signal. Different channels.\n" +
            "Notice how the channel affects the output differently.",
            font_size=14, color=WHITE, weight=BOLD
        ).shift(DOWN * 3.8)
        self.play(FadeIn(insight))
        self.wait(2.5)
        
        self.play(FadeOut(title), FadeOut(ax_high), FadeOut(label_high),
                 FadeOut(signal_high), FadeOut(h_high),
                 FadeOut(ax_low), FadeOut(label_low),
                 FadeOut(signal_low), FadeOut(h_low),
                 FadeOut(insight))
        self.wait(0.5)
    
    # ================================================================
    # SCENE 4.7: Transition Forward (NO CLASSIFICATION YET)
    # ================================================================
    def scene_4_7_transition_forward(self):
        """
        Goal: Set up next phase without defining flat/frequency-selective fading.
        """
        title = Title("The Key Question", color=BLUE_B).scale(0.9)
        self.add(title)
        self.wait(1)
        
        # Big question
        question = MathTex(
            r"\text{Does my signal fit inside B_c?}",
            color=BLUE,
            font_size=52
        ).shift(UP * 1)
        
        self.play(Write(question))
        self.wait(2)
        
        # Outline what happens next
        outline = VGroup(
            Text("What we'll explore next:", font_size=14, color=YELLOW_A, weight=BOLD),
            Text("", font_size=1),
            Text("• When signal bandwidth ≪ coherence bandwidth", font_size=12, color=WHITE),
            Text("• When signal bandwidth > coherence bandwidth", font_size=12, color=WHITE),
            Text("• How to design systems to handle either case", font_size=12, color=WHITE)
        ).arrange(DOWN, buff=0.4).shift(DOWN * 1.5)
        
        self.play(FadeIn(outline))
        self.wait(3)
        
        self.play(FadeOut(title), FadeOut(question), FadeOut(outline))
        self.wait(1)
