from manim import *

class Phase3_ISI_SingleCase_Delays(Scene):
    def construct(self):
        # -----------------------------------------
        # 0. SETUP
        # -----------------------------------------
        title = Title("Intersymbol Interference (ISI)").scale(0.9)
        self.add(title)

        common_config = {
            "x_range": [0, 8, 1], "y_range": [0, 1.8, 1],
            "x_length": 9, "y_length": 1.2,
            "axis_config": {"include_tip": False, "font_size": 16, "include_numbers": False},
        }

        ax1 = Axes(**common_config).to_edge(UP, buff=1.3)
        ax2 = Axes(**common_config).next_to(ax1, DOWN, buff=0.6)
        ax3 = Axes(**common_config).next_to(ax2, DOWN, buff=0.8)

        # Conceptual Labels
        l1 = Text("Path 1 (Direct)", font_size=20, color=WHITE).next_to(ax1, LEFT)
        l2 = Text("Path 2 (Echo)", font_size=20, color=WHITE).next_to(ax2, LEFT)
        l3 = Text("Receiver Sum", font_size=20, color=YELLOW).next_to(ax3, LEFT)

        self.play(Create(ax1), Write(l1), Create(ax2), Write(l2), Create(ax3), Write(l3))

        # Helper for Square Pulses
        def get_pulse(axes, start, width, height, color):
            return VGroup(
                Line(axes.c2p(start, 0), axes.c2p(start, height), color=color),
                Line(axes.c2p(start, height), axes.c2p(start+width, height), color=color),
                Line(axes.c2p(start+width, height), axes.c2p(start+width, 0), color=color)
            )

        # -----------------------------------------
        # 1. DEFINING THE DELAYS (New Addition)
        # -----------------------------------------
        t0 = 1.0        # Direct arrival
        t1 = 2.5        # Echo arrival
        width = 1.0     
        
        # Tau 0 Line (Horizontal from Y-axis to start of t0)
        # We put it slightly above the axis (at y=0.5) for visibility
        line_tau0 = Arrow(ax1.c2p(0, 0.5), ax1.c2p(t0, 0.5), buff=0, color=YELLOW, tip_length=0.15)
        lbl_tau0 = MathTex(r"\tau_0", color=YELLOW, font_size=24).next_to(line_tau0, UP, buff=0.05)
        
        # Tau 1 Line (Horizontal from Y-axis to start of t1)
        line_tau1 = Arrow(ax2.c2p(0, 0.5), ax2.c2p(t1, 0.5), buff=0, color=YELLOW, tip_length=0.15)
        lbl_tau1 = MathTex(r"\tau_1", color=YELLOW, font_size=24).next_to(line_tau1, UP, buff=0.05)

        # Animate the Delays first to establish the timing difference
        self.play(GrowArrow(line_tau0), Write(lbl_tau0))
        self.play(GrowArrow(line_tau1), Write(lbl_tau1))
        self.wait(1)

        # -----------------------------------------
        # 2. SENDING THE SIGNALS
        # -----------------------------------------
        
        # PATH 1 (Direct): "1", "0", "1"
        p1 = VGroup(
            get_pulse(ax1, t0, width, 1.0, WHITE), # Bit 1
            get_pulse(ax1, t0 + 2*width, width, 1.0, WHITE) # Bit 3
        )
        
        # Show "Logic 0" Gap explicitly
        # gap_brace = Brace(Line(ax1.c2p(2.0, 0), ax1.c2p(3.0, 0)), direction=UP, color=GREEN, buff=0.1)
        # gap_lbl = gap_brace.get_text("'0'", buff=0.1).scale(0.8)

        # PATH 2 (Echo): Echo of "1", "0", "1"
        p2 = VGroup(
            get_pulse(ax2, t1, width, 0.6, WHITE),
            get_pulse(ax2, t1 + 2*width, width, 0.6, WHITE)
        )

        self.play(Create(p1))
        self.play(Create(p2))
        self.wait(1)

        # -----------------------------------------
        # 3. HIGHLIGHTING THE COLLISION
        # -----------------------------------------
        # Collision Zone: 2.5 to 3.0
        collision_box = SurroundingRectangle(
            Line(ax2.c2p(2.5, 0), ax2.c2p(3.0, 0.6)), color=ORANGE, buff=0.1
        )
        collision_txt = Text("Echo invades the '0' slot", font_size=18, color=ORANGE).next_to(collision_box, UP)
        
        self.play(Create(collision_box), Write(collision_txt))
        self.wait(2)

        # -----------------------------------------
        # 4. THE SUMMATION (Visualizing the Error)
        # -----------------------------------------
        sum_isi = VGroup(
            # 1.0-2.0: Green(1) + Red(0) = 1
            Line(ax3.c2p(1.0, 0), ax3.c2p(1.0, 1), color=YELLOW),
            Line(ax3.c2p(1.0, 1), ax3.c2p(2.0, 1), color=YELLOW),
            Line(ax3.c2p(2.0, 1), ax3.c2p(2.0, 0), color=YELLOW),
            
            # 2.0-2.5: Green(0) + Red(0) = 0 (Clean start of '0')
            Line(ax3.c2p(2.0, 0), ax3.c2p(2.5, 0), color=YELLOW),
            
            # 2.5-3.0: Green(0) + Red(0.6) = 0.6 (THE BUMP)
            Line(ax3.c2p(2.5, 0), ax3.c2p(2.5, 0.6), color=ORANGE), # Jump
            Line(ax3.c2p(2.5, 0.6), ax3.c2p(3.0, 0.6), color=ORANGE), # Plateau
            
            # 3.0-3.5: Green(1) + Red(0.6) = 1.6
            Line(ax3.c2p(3.0, 0.6), ax3.c2p(3.0, 1.6), color=YELLOW),
            Line(ax3.c2p(3.0, 1.6), ax3.c2p(3.5, 1.6), color=YELLOW),
            
            # 3.5-4.0: Green(1) + Red(0) = 1.0 (Clean tail of '1')
            Line(ax3.c2p(3.5, 1.6), ax3.c2p(3.5, 1.0), color=YELLOW),
            Line(ax3.c2p(3.5, 1.0), ax3.c2p(4.0, 1.0), color=YELLOW),
            Line(ax3.c2p(4.0, 1.0), ax3.c2p(4.0, 0), color=YELLOW),

            # Tail (echo of bit 3)
            Line(ax3.c2p(4.0, 0), ax3.c2p(4.5, 0), color=YELLOW),
            Line(ax3.c2p(4.5, 0), ax3.c2p(4.5, 0.6), color=YELLOW),
            Line(ax3.c2p(4.5, 0.6), ax3.c2p(5.5, 0.6), color=YELLOW),
            Line(ax3.c2p(5.5, 0.6), ax3.c2p(5.5, 0), color=YELLOW)
        )
        
        self.play(Create(sum_isi))
        self.wait(1)

        # -----------------------------------------
        # 5. THE SAMPLING MOMENT
        # -----------------------------------------
        # Sample deep inside the error zone (t=2.75)
        sample_time = 2.75
        
        sample_line = DashedLine(ax3.c2p(sample_time, 0), ax3.c2p(sample_time, 1.8), color=WHITE)
        sample_lbl = Text("Sample", font_size=16).next_to(sample_line, UP)
        
        self.play(Create(sample_line), Write(sample_lbl))
        
        # Show Math Calculation
        d1 = Dot(ax1.c2p(sample_time, 0), color=WHITE) # Green is 0
        d2 = Dot(ax2.c2p(sample_time, 0.6), color=WHITE) # Red is 0.6
        d3 = Dot(ax3.c2p(sample_time, 0.6), color=YELLOW) # Sum is 0.6
        
        self.play(FadeIn(d1), FadeIn(d2), FadeIn(d3))
        
        equation = MathTex("0 \\text{ (Signal)} + 0.6 \\text{ (Echo)} = 0.6 \\text{ (Error!)}", font_size=24)
        equation.next_to(ax3, DOWN, buff=0.5)
        
        self.play(Write(equation))
        
        self.wait(5)