from manim import *

class Phase3_ISI_GhostSmear_Final(Scene):
    def construct(self):
        # -----------------------------------------
        # 0. SETUP
        # -----------------------------------------
        title = Title("Delay Spread vs. ISI").scale(0.9)
        self.add(title)

        # We need two timelines: Transmit (Tx) and Receive (Rx)
        # Shifted to match the image layout
        ax_tx = Axes(
            x_range=[0, 10, 1], y_range=[0, 1.5, 1],
            x_length=9, y_length=2,
            axis_config={"include_tip": True, "include_numbers": False}
        ).to_edge(UP, buff=1.5)
        
        ax_rx = Axes(
            x_range=[0, 10, 1], y_range=[0, 1.5, 1],
            x_length=9, y_length=2,
            axis_config={"include_tip": True, "include_numbers": False}
        ).to_edge(DOWN, buff=1.5)

        lbl_tx = Text("Tx Signal", font_size=24).next_to(ax_tx, LEFT)
        lbl_rx = Text("Rx Signal", font_size=24).next_to(ax_rx, LEFT)

        self.play(Create(ax_tx), Write(lbl_tx), Create(ax_rx), Write(lbl_rx))
        self.wait(5)

        # Helper to create blocks
        def get_block(axes, start, width, height, color, opacity=1.0, label=""):
            rect = Rectangle(
                width=axes.c2p(width,0)[0] - axes.c2p(0,0)[0],
                height=axes.c2p(0,height)[1] - axes.c2p(0,0)[1],
                fill_color=color, fill_opacity=opacity, stroke_color=WHITE, stroke_width=1
            )
            # Position: Center of rect is at (start + width/2, height/2)
            rect.move_to(axes.c2p(start + width/2, height/2))
            
            txt = Text(label, font_size=16, color=BLACK if opacity>0.5 else WHITE).move_to(rect.get_center())
            return VGroup(rect, txt)

        # -----------------------------------------
        # 1. TRANSMIT (TOP GRAPH)
        # -----------------------------------------
        # Symbol 1 (Green) at t=1
        # Gap of 1 unit
        # Symbol 2 (Blue) at t=3
        
        tx_sym1 = get_block(ax_tx, 1, 1, 1, GREEN, label="Sym 1")
        tx_sym2 = get_block(ax_tx, 4, 1, 1, BLUE, label="Sym 2")
        
        # Interval Brace
        brace_interval = Brace(Line(ax_tx.c2p(2,1), ax_tx.c2p(4,1)), direction=UP, color=GRAY)
        lbl_interval = brace_interval.get_text(r"$\frac{1}{T_r}$", buff=0.01).scale(0.6)

        self.play(Create(tx_sym1))
        
        self.wait(1)

        # -----------------------------------------
        # 2. RECEIVE SYMBOL 1 (THE GHOST TRAIN)
        # -----------------------------------------
        # Just like your image: 1, 1', 1'', 1'''
        # They overlap slightly and fade in height/opacity
        
        # Main copy
        rx_1_main = get_block(ax_rx, 1, 1, 1, GREEN, opacity=0.9, label="1")
        
        # Ghosts (Delayed & Attenuated)
        # 1': delayed by 0.4
        rx_1_g1 = get_block(ax_rx, 1.4, 1, 0.8, GREEN, opacity=0.7, label="1'")
        # 1'': delayed by 0.8
        rx_1_g2 = get_block(ax_rx, 1.8, 1, 0.6, GREEN, opacity=0.5, label="1''")
        # 1''': delayed by 1.2
        rx_1_g3 = get_block(ax_rx, 2.2, 1, 0.4, GREEN, opacity=0.3, label="1'''")
        
        # Group for animation
        green_ghosts = VGroup(rx_1_main, rx_1_g1, rx_1_g2, rx_1_g3)
        
        # Animate them appearing one by one to show the "Echo" effect
        self.play(LaggedStart(*[FadeIn(g, shift=RIGHT*0.1) for g in green_ghosts], lag_ratio=0.5))
        
        # DEFINE DELAY SPREAD
        # From start of first to end of last
        # Start = 1.0, End = 2.2 + 1.0 = 3.2
        brace_delay = Brace(Line(ax_rx.c2p(1, -0.2), ax_rx.c2p(3.2, -0.2)), direction=DOWN, color=GREEN)
        lbl_delay = brace_delay.get_text("Delay Spread", buff=0.1).scale(0.7)
        
        self.play(GrowFromCenter(brace_delay), Write(lbl_delay))
        self.wait(2)

        # -----------------------------------------
        # 3. RECEIVE SYMBOL 2 (THE COLLISION)
        # -----------------------------------------
        # Symbol 2 arrives at t=3 (based on Tx timing)
        
        # The Green Smear ends at 3.2 (Start 2.2 + Width 1.0)
        # Symbol 2 starts at 3.0
        # OVERLAP ZONE: 3.0 to 3.2
        self.play(GrowFromCenter(brace_interval), Write(lbl_interval))
        self.play(Create(tx_sym2))
        
        rx_2_main = get_block(ax_rx, 4, 1, 1, BLUE, opacity=0.9, label="2")
        # Add blue ghosts for realism, though focused on collision
        rx_2_g1 = get_block(ax_rx, 4.4, 1, 0.8, BLUE, opacity=0.7)
        rx_2_g2 = get_block(ax_rx, 4.8, 1, 0.6, BLUE, opacity=0.5)
        rx_2_g3 = get_block(ax_rx, 5.2, 1, 0.4, BLUE, opacity=0.3)
        
        self.play(Create(rx_2_main), FadeIn(rx_2_g1), FadeIn(rx_2_g2), FadeIn(rx_2_g3))
        
        # -----------------------------------------
        # 4. HIGHLIGHT THE SMUDGE
        # -----------------------------------------
        # Arrow pointing to the overlap
        # Overlap is where Green Ghost 1''' (ends at 3.2) meets Blue 2 (starts at 3.0)
        
        self.play(
            tx_sym2.animate.shift(LEFT * (ax_tx.c2p(1,0)[0] - ax_tx.c2p(0,0)[0])),
            
            # We also need to shrink the brace and its label to reflect the new interval
            brace_interval.animate.become(
                Brace(Line(ax_tx.c2p(2,1), ax_tx.c2p(3,1)), direction=UP, color=GRAY)
            ),
            lbl_interval.animate.next_to(
                Brace(Line(ax_tx.c2p(2,1), ax_tx.c2p(3,1)), direction=UP), UP, buff=0.06
            ),
            run_time=1.5
        )
        self.play(
            rx_2_main.animate.shift(LEFT * (ax_rx.c2p(1,0)[0] - ax_rx.c2p(0,0)[0])),
            rx_2_g1.animate.shift(LEFT * (ax_rx.c2p(1,0)[0] - ax_rx.c2p(0,0)[0])),
            rx_2_g2.animate.shift(LEFT * (ax_rx.c2p(1,0)[0] - ax_rx.c2p(0,0)[0])),
            rx_2_g3.animate.shift(LEFT * (ax_rx.c2p(1,0)[0] - ax_rx.c2p(0,0)[0])),
        )
        
        
        # -----------------------------------------
        # 5. THE INTUITION HIT (TRANSFORM TO TIME)
        # -----------------------------------------
        # Original concept: "Delay Spread > Interval = ISI"
        # New concept: "Interval is actually Symbol Time"
        collision_point = ax_rx.c2p(3.1, 0.5)
        arrow_smudge = Arrow(start=collision_point + UP*1.5 + LEFT*1, end=collision_point, color=RED, buff=0.1)
        lbl_smudge = Text("1''' copy smudging into 2", font_size=20, color=RED).next_to(arrow_smudge, UP)
        
        # Highlight rectangle
        intersection_rect = Rectangle(
            width=ax_rx.c2p(0.2,0)[0] - ax_rx.c2p(0,0)[0],
            height=ax_rx.c2p(0,0.4)[1] - ax_rx.c2p(0,0)[1],
            color=RED, fill_opacity=0.5, stroke_width=0
        ).move_to(ax_rx.c2p(3.1, 0.2)) # Middle of 3.0-3.2, height 0.4 (height of small ghost)

        self.play(GrowArrow(arrow_smudge), Write(lbl_smudge))
        self.play(FadeIn(intersection_rect))
        self.wait(1)


        self.play(FadeOut(brace_delay), FadeOut(lbl_delay))
        self.wait(0.5)
        # 1. Write the initial logic
        logic_text_1 = Text("Therefore the symbol rate is limited and can't grow indefinitely.", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(logic_text_1))
        self.wait(2)
        
        # 2. Transform the Top Label: "Inter-symbol Interval" -> "Symbol Time"
        self.play(Indicate(lbl_interval, color=YELLOW))
        
        # lbl_time = brace_interval.get_text(r"$\frac{1}{T_r}$", buff=0.1).scale(0.6)
        # self.play(Transform(lbl_interval, lbl_time))
        # self.wait(1)
        
        # 3. Transform the Bottom Logic to match
        # "If Symbol Time is small, symbols come fast."
        # "Therefore, Delay Spread limits Symbol Time."
        
        logic_text_2 = Text("Therefore: Delay Spread must be < Symbol Time for negligible ISI", font_size=24, color=RED).to_edge(DOWN)
        # self.play(Transform(logic_text_1))

        self.play(
            tx_sym2.animate.shift(RIGHT * (ax_tx.c2p(1,0)[0] - ax_tx.c2p(0,0)[0])),
            
            # Expand the brace back to the original interval size
            brace_interval.animate.become(
                Brace(Line(ax_tx.c2p(2,1), ax_tx.c2p(4,1)), direction=UP, color=GRAY)
            ),
            lbl_interval.animate.next_to(
                Brace(Line(ax_tx.c2p(2,1), ax_tx.c2p(4,1)), direction=UP), UP, buff=0.06
            ),
            run_time=1.5
        )
        self.play(
            rx_2_main.animate.shift(RIGHT * (ax_rx.c2p(1,0)[0] - ax_rx.c2p(0,0)[0])),
            rx_2_g1.animate.shift(RIGHT * (ax_rx.c2p(1,0)[0] - ax_rx.c2p(0,0)[0])),
            rx_2_g2.animate.shift(RIGHT * (ax_rx.c2p(1,0)[0] - ax_rx.c2p(0,0)[0])),
            rx_2_g3.animate.shift(RIGHT * (ax_rx.c2p(1,0)[0] - ax_rx.c2p(0,0)[0])),
            Transform(logic_text_1, logic_text_2),
            FadeOut(arrow_smudge),
            FadeOut(lbl_smudge),
            FadeOut(intersection_rect),
        )

        # Add final inequality for clarity - starts at bottom next to logic text
        eqn = MathTex(r"\sigma_\tau < T_{retrans}", font_size=40, color=RED).next_to(logic_text_2, UP)
        self.play(FadeIn(eqn, shift=UP))
        
        self.wait(3)
        
        # Now animate the formula to move up below the title and fade everything out
        eqn_target = eqn.copy().next_to(title, DOWN, buff=0.5)
        
        self.play(
            eqn.animate.move_to(eqn_target.get_center()),
            FadeOut(ax_tx),
            FadeOut(ax_rx),
            FadeOut(lbl_tx),
            FadeOut(lbl_rx),
            FadeOut(tx_sym1),
            FadeOut(tx_sym2),
            FadeOut(rx_1_main),
            FadeOut(rx_1_g1),
            FadeOut(rx_1_g2),
            FadeOut(rx_1_g3),
            FadeOut(rx_2_main),
            FadeOut(rx_2_g1),
            FadeOut(rx_2_g2),
            FadeOut(rx_2_g3),
            FadeOut(brace_interval),
            FadeOut(lbl_interval),
            FadeOut(logic_text_1),
            FadeOut(title),
            run_time=1.5
        )

        self.wait(3)