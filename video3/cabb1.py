from manim import *

class CoherenceBandwidthProfessional(Scene):
    def construct(self):
        # PALETTE DEFINITIONS (Professional & Minimal)
        C_TEXT = WHITE
        C_MATH = BLUE_C
        C_HIGHLIGHT = YELLOW_C
        
        # 1. INVERSE RELATIONSHIP
        # -----------------------
        title = Title("Bandwidth and Delay Spread", color=C_TEXT).scale(0.8)
        self.add(title)

        # Formula: B_ch proportional to 1/tau
        relation = MathTex(
            r"B_{ch} \propto \frac{1}{\tau_{spread}}",
            color=C_MATH, font_size=60
        ).shift(UP*0.5)
        
        text_inv = Text(
            "Inverse Relationship", 
            font_size=28, color=C_TEXT
        ).next_to(relation, UP, buff=0.5)

        self.play(Write(text_inv), Write(relation))
        self.wait(2)

        # 2. DEFINING THE "CONSTANT" RANGE
        # --------------------------------
        # Move formula aside
        self.play(
            relation.animate.scale(0.7).to_edge(LEFT).shift(DOWN*0.5),
            FadeOut(text_inv)
        )

        # Draw Frequency Response Curve
        ax = Axes(
            x_range=[0, 6], y_range=[0, 1.5], 
            x_length=6, y_length=2.5, 
            axis_config={"include_tip": False, "color": GREY}
        ).shift(UP*0.5)
        
        # Axis labels
        x_label = MathTex("f", color=C_TEXT, font_size=24).next_to(ax.x_axis, DOWN, buff=0.12)
        y_label = MathTex(r"|H(f)|", color=C_TEXT, font_size=24).next_to(ax.y_axis, LEFT, buff=0.12)
        labels = VGroup(x_label, y_label)

        # Curve with a flat top (Constant region)
        curve = ax.plot(
            lambda x: 1.0 if 2 < x < 4 else (1.0 - 0.5*(x-4)**2 if x>4 else 1.0 - 0.5*(2-x)**2), 
            color=C_MATH, x_range=[1, 5], stroke_width=4
        )
        
        # --- NEW VISUALIZATION: Vertical Lines & Arrow ---
        # Vertical dashed lines marking the constant region (x=2 to x=4)
        line_left = DashedLine(
            start=ax.c2p(2, 0), end=ax.c2p(2, 1.2), 
            color=C_HIGHLIGHT, stroke_opacity=0.7
        )
        line_right = DashedLine(
            start=ax.c2p(4, 0), end=ax.c2p(4, 1.2), 
            color=C_HIGHLIGHT, stroke_opacity=0.7
        )
        
        # Dimension arrow spanning the lines
        bw_arrow = DoubleArrow(
            start=ax.c2p(2, 1.1), end=ax.c2p(4, 1.1), 
            buff=0, color=C_HIGHLIGHT
        )
        
        bw_text = Text("Constant Gain Region", font_size=20, color=C_HIGHLIGHT).next_to(bw_arrow, UP, buff=0.1)

        self.play(Create(ax), Write(labels), Create(curve))
        self.play(Create(line_left), Create(line_right))
        self.play(GrowFromCenter(bw_arrow), Write(bw_text))
        self.wait(2)

        # 3. TRANSITION TO COHERENCE BANDWIDTH (Bc)
        # -----------------------------------------
        rename_text = Text(
            "This range is the Coherence Bandwidth", 
            color=C_TEXT, font_size=28
        ).to_edge(UP, buff=1.2).shift(DOWN*0.4)
        
        self.play(Write(rename_text))
        self.wait(1)

        # Transform B_ch -> B_c in the formula
        new_relation = MathTex(
            r"B_c \propto \frac{1}{\tau_{spread}}", 
            font_size=42, color=C_MATH
        ).move_to(relation)

        # Transform label on graph: "Constant Gain Region" -> "Bc"
        new_bw_text = MathTex("B_c", color=C_HIGHLIGHT, font_size=36).next_to(bw_arrow, UP, buff=0.1)

        self.play(
            Transform(relation, new_relation),
            Transform(bw_text, new_bw_text)
        )
        self.wait(2)

        # Clear graph for formulas
        self.play(
            FadeOut(ax), FadeOut(labels), FadeOut(curve), 
            FadeOut(line_left), FadeOut(line_right), 
            FadeOut(bw_arrow), FadeOut(bw_text), FadeOut(rename_text)
        )

        # 4. CORRELATION FORMULAS
        # -----------------------
        # Move main relation to top center
        self.play(relation.animate.move_to(UP * 2).scale(1.2))

        # Case 1: 0.9 Correlation
        case_09 = MathTex(
            r"B_c \approx \frac{1}{50\sigma_\tau}", 
            r"\quad (\text{if } \text{corr} \ge 0.9)",
            font_size=36, color=C_TEXT
        ).shift(UP * 0.5)
        case_09[0].set_color(C_MATH) # Highlight formula part

        # Case 2: 0.5 Correlation
        case_05 = MathTex(
            r"B_c \approx \frac{1}{5\sigma_\tau}", 
            r"\quad (\text{if } \text{corr} \ge 0.5)",
            font_size=36, color=C_TEXT
        ).shift(DOWN * 0.7)
        case_05[0].set_color(C_MATH)

        self.play(Write(case_09))
        self.wait(1)
        self.play(Write(case_05))
        self.wait(3)