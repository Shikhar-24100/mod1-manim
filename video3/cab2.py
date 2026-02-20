from manim import *

class Phase2_Textbook_Final(Scene):
    def construct(self):
        # -----------------------------------------
        # 0. SETUP: THE GRAPH ANCHOR (Bottom Half)
        # -----------------------------------------
        title = Title("Time Dispersion Parameters").scale(0.9)
        self.add(title)

        # Graph stays fixed at the bottom
        axes = Axes(
            x_range=[0, 100, 10], y_range=[0, 1.2, 0.5],
            x_length=9, y_length=3.5,
            axis_config={"include_tip": True, "font_size": 20, "include_numbers": False}
        ).to_edge(DOWN, buff=0.8)

        x_lbl = axes.get_x_axis_label(Tex("Delay $\\tau$", font_size=24), edge=DOWN, direction=DOWN, buff=0.3)
        y_lbl = axes.get_y_axis_label(Tex("Power $P(\\tau)$", font_size=24).rotate(90*DEGREES), edge=LEFT, direction=LEFT, buff=0.2)
        
        # self.play(Create(axes), Write(x_lbl), Write(y_lbl))

        # Create Taps corresponding to a typical profile
        tap_data = [
            (10, 1.0, "0"),     # Strongest
            (25, 0.6, "1"),     # Echo 1
            (40, 0.3, "2"),     # Echo 2
            (76, 0.135, "N-3"),
            (80, 0.115, "N-2"),
            (85, 0.1, "N-1")    # Weak Tail
        ]
        
        taps_group = VGroup()
        for t, p, idx in tap_data:
            line = Line(axes.c2p(t, 0), axes.c2p(t, p), color=BLUE, stroke_width=4)
            tip = Triangle(fill_color=BLUE, fill_opacity=1, stroke_width=0).scale(0.08).move_to(axes.c2p(t, p))
            
            lbl_tau = MathTex(f"\\tau_{{{idx}}}", font_size=16).next_to(axes.c2p(t, 0), DOWN, buff=0.15)
            
            taps_group.add(VGroup(line, tip, lbl_tau))

        # Add ellipsis dots to indicate more taps between tap 2 and tap N-3
        ellipsis_dots = VGroup()
        dot_x_positions = [42,47,52,57,62,67,72]  # Positions between 40 and 76
        for dot_x in dot_x_positions:
            dot = Dot(point=axes.c2p(dot_x, 0.1), radius=0.025, color=WHITE, fill_opacity=0.6)
            ellipsis_dots.add(dot)

        # self.play(Create(axes), Write(x_lbl), Write(y_lbl))
        # self.play(LaggedStart(*[GrowFromEdge(t, DOWN) for t in taps_group], lag_ratio=0.2))
        # self.play(FadeIn(ellipsis_dots), run_time=0.5)
        # self.wait(1) 

        # -----------------------------------------
        # INTRO: WHY DO WE NEED THESE?
        # -----------------------------------------
        # Sourced from the provided image text
        intro_text = Paragraph(
            "parameters which grossly quantify how the multipath channel are used.",
            font_size=24, color=YELLOW, alignment="center"
        ).to_edge(UP, buff=2.0)

        self.play(Write(intro_text), run_time=3)
        self.wait(4) # Let them read the "Why"
        self.play(FadeOut(intro_text)) # Redact it as requested


        self.play(Create(axes), Write(x_lbl), Write(y_lbl))
        self.play(LaggedStart(*[GrowFromEdge(t, DOWN) for t in taps_group], lag_ratio=0.2))
        self.play(FadeIn(ellipsis_dots), run_time=0.5)
        self.wait(1) 

        # -----------------------------------------
        # 1. METRIC A: MAXIMUM EXCESS DELAY
        # -----------------------------------------
        header_A = Text("1. Maximum Excess Delay", font_size=28, color=YELLOW).to_edge(UP, buff=1.5).to_edge(LEFT, buff=1)
        
        def_A = Text("The time duration between the first and last received multipath components.", font_size=20).next_to(header_A, DOWN, aligned_edge=LEFT)
        
        form_A = MathTex(
            r"\tau_{max} = \tau_{N-1} - \tau_0", font_size=32
        ).next_to(def_A, DOWN, aligned_edge=LEFT, buff=0.3)
        
        self.play(Write(header_A))
        self.play(FadeIn(def_A))
        self.play(Write(form_A))
        self.wait(3) 

        critique = Text("does not account for whether most of the signal's power", font_size=20).next_to(form_A, DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(Write(critique))
        
        # Highlight the last three taps (N-3, N-2, N-1) - change color to RED
        last_three_taps = VGroup(taps_group[3], taps_group[4], taps_group[5])
        
        # Store original state of each tap
        original_taps = VGroup(*[tap.copy() for tap in last_three_taps])
        
        # Change color to RED with stroke width up animation
        self.play(
            last_three_taps.animate.set_color(RED),
            run_time=0.5
        )
        self.wait(3)  # Keep highlighted for 3 seconds
        
        # Restore to original appearance
        self.play(
            AnimationGroup(
                *[Transform(last_three_taps[i], original_taps[i]) for i in range(3)],
                lag_ratio=0.1
            ),
            run_time=0.5
        )
        self.wait(0.5) 
        
        self.play(
            FadeOut(header_A), FadeOut(def_A), FadeOut(form_A), FadeOut(critique)
        )

        # -----------------------------------------
        # 2. METRIC B: MEAN EXCESS DELAY
        # -----------------------------------------
        header_B = Text("2. Mean Excess Delay", font_size=28, color=YELLOW).to_edge(UP, buff=1.5).to_edge(LEFT, buff=1)
        
        # Definition: "The first moment of the power delay profile"
        def_B = Text("The first moment of the power delay profile.", font_size=20).next_to(header_B, DOWN, aligned_edge=LEFT)
        
        # Formula 4.35 from the book image
        form_B = MathTex(
            r"\bar{\tau} = \frac{\sum P(\tau_k) \tau_k}{\sum P(\tau_k)}", 
            font_size=30
        ).next_to(def_B, DOWN, aligned_edge=LEFT, buff=0.2)

        self.play(Write(header_B)) 
        self.play(FadeIn(def_B))
        self.play(Write(form_B))
        self.wait(4)

        self.play(
            FadeOut(header_B), FadeOut(def_B), FadeOut(form_B)
        )

        # -----------------------------------------
        # 3. METRIC C: RMS DELAY SPREAD
        # -----------------------------------------
        header_C = Text("3. RMS Delay Spread", font_size=28, color=YELLOW).to_edge(UP, buff=1.5).to_edge(LEFT, buff=1)
        
        # Definition: "Square root of the second central moment"
        def_C = Paragraph(
            "The square root of the second central moment of the power delay profile.",
            font_size=20, alignment="left"
        ).next_to(header_C, DOWN, aligned_edge=LEFT)
        
        # Formula 4.36 from the book image
        form_C = MathTex(
            r"\sigma_\tau = \sqrt{\overline{\tau^2} - (\bar{\tau})^2}", 
            font_size=32
        ).next_to(def_C, DOWN, aligned_edge=LEFT, buff=0.4)
        
        # Formula 4.37 (Second Moment) from the book image
        sub_form_C = MathTex(
            r"\text{where } \overline{\tau^2} = \frac{\sum P(\tau_k) \tau_k^2}{\sum P(\tau_k)}",
            font_size=26, color=LIGHT_GRAY
        ).next_to(form_C, RIGHT, buff=0.3)

        self.play(Write(header_C))
        self.play(FadeIn(def_C))
        self.play(Write(form_C))
        self.wait(2)
        self.play(Write(sub_form_C))
        
        self.play(Indicate(form_C, scale_factor=1.2, color=GREEN))
        self.wait(4)