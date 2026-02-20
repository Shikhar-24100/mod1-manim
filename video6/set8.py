from manim import *
import numpy as np

class CoChannelInterference(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # CONFIGURATION
        # ---------------------------------------------------------
        R = 0.6  # Hexagon radius
        N = 7    # Cluster size
        D_val = np.sqrt(3 * N) * R  # Distance to interferers
        
        # ---------------------------------------------------------
        # SCENE 1: THE GEOMETRY
        # ---------------------------------------------------------
        
        title = Text("Co-channel Interference & Capacity", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Serving Cell (Center)
        serving_hex = RegularPolygon(n=6, color=GREEN, fill_opacity=0.3, stroke_width=3).scale(R)
        serving_bs = Dot(color=GREEN, radius=0.08)
        # serving_label = Text("S", font_size=20, color=WHITE, weight=BOLD).move_to(ORIGIN)
        
        # Mobile at cell edge (worst case)
        user_pos = np.array([R * 0.85, 0, 0])
        user = Dot(point=user_pos, color=YELLOW, radius=0.1)
        user_label = Text("M", font_size=18, color=BLACK, weight=BOLD).move_to(user_pos)
        
        # Interfering Cells (6 surrounding at distance D)
        interferers = VGroup()
        interferer_signals = VGroup()
        
        for i in range(6):
            angle = i * 60 * DEGREES
            pos = np.array([D_val * np.cos(angle), D_val * np.sin(angle), 0])
            
            # Hexagon and base station
            h = RegularPolygon(n=6, color=RED, fill_opacity=0.15, stroke_width=2).scale(R).move_to(pos)
            bs = Dot(color=RED, radius=0.06).move_to(pos)
            label = Text("I", font_size=16, color=WHITE, weight=BOLD).move_to(pos)
            
            # Interference signal line
            signal = DashedLine(start=pos, end=user_pos, color=RED, stroke_width=2, stroke_opacity=0.5, dash_length=0.08)
            
            interferers.add(VGroup(h, bs, label))
            interferer_signals.add(signal)
        
        # Group and scale to fit
        entire_map = VGroup(serving_hex, serving_bs, user, user_label, interferers, interferer_signals)
        entire_map.scale(0.65).shift(LEFT * 3)
        
        # ---------------------------------------------------------
        # ANIMATION: BUILD THE SCENE
        # ---------------------------------------------------------
        
        # Show serving cell
        self.play(
            Create(serving_hex),
            FadeIn(serving_bs)
        )
        self.wait(0.3)
        
        # Show mobile
        self.play(FadeIn(user), Write(user_label))
        self.wait(0.3)
        
        # Desired signal
        desired_signal = Arrow(
            start=serving_bs.get_center(),
            end=user.get_center(),
            color=GREEN,
            buff=0.1,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        )
        s_label = MathTex("S", color=GREEN, font_size=28).next_to(desired_signal, UP, buff=0.05)
        
        self.play(GrowArrow(desired_signal), Write(s_label))
        self.wait(0.5)
        
        # Show interferers
        self.play(FadeIn(interferers), run_time=1)
        self.wait(0.3)
        
        # Show interference signals
        self.play(Create(interferer_signals), run_time=1.5)
        i_label = MathTex("I_i", color=RED, font_size=24).next_to(interferer_signals[0].get_center(), UP, buff=0.1)
        self.play(Write(i_label))
        self.wait(1)
        
        # ---------------------------------------------------------
        # SHOW KEY DISTANCES
        # ---------------------------------------------------------
        
        # Show R (radius)
        r_line = Line(serving_bs.get_center(), serving_hex.get_vertices()[0], color=BLUE, stroke_width=3)
        r_label = MathTex("R", font_size=24, color=BLUE).next_to(r_line, LEFT, buff=0.1)
        
        self.play(Create(r_line), Write(r_label))
        self.wait(1)
        self.play(FadeOut(r_line), FadeOut(r_label))
        
        # Show D (distance to interferer)
        d_line = Line(serving_bs.get_center(), interferers[0][1].get_center(), color=YELLOW, stroke_width=3)
        d_label = MathTex("D", font_size=24, color=YELLOW).next_to(d_line.get_center(), DOWN, buff=0.1)
        
        self.play(Create(d_line), Write(d_label))
        self.wait(1)
        self.play(FadeOut(d_line), FadeOut(d_label))
        
        # ---------------------------------------------------------
        # SCENE 2: THE MATHEMATICS
        # ---------------------------------------------------------
        
        # Q Definition
        eq_q = MathTex(
            r"Q = \frac{D}{R} = \sqrt{3N}",
            font_size=40,
            color=BLUE
        ).to_edge(RIGHT, buff=0.8).shift(UP * 2.2 + LEFT*1.5)
        
        q_box = SurroundingRectangle(eq_q, color=BLUE, buff=0.15, stroke_width=2)
        
        self.play(Create(q_box), Write(eq_q))
        self.wait(1)
        
        # S/I Ratio
        eq_sir = MathTex(
            r"\frac{S}{I} = \frac{S}{\sum_{k=1}^{i_0} I_k}",
            font_size=32
        ).next_to(q_box, DOWN, buff=0.5, aligned_edge=LEFT)
        
        self.play(Write(eq_sir))
        self.wait(0.8)
        
        # Path loss
        eq_pathloss = MathTex(
            r"P_r \propto d^{-n}",
            font_size=28
        ).next_to(eq_sir, DOWN, buff=0.4, aligned_edge=LEFT)
        
        n_note = Text("n = path loss exponent", font_size=16, color=GRAY).next_to(eq_pathloss, RIGHT, buff=0.3)
        
        self.play(Write(eq_pathloss), FadeIn(n_note))
        self.wait(1)
        
        # Approximation (6 interferers, equal distance)
        # eq_sir = MathTex(
        #    ,
        #     font_size=32
        # )
        eq_approx = MathTex(
             r"\frac{S}{I} = \frac{R^{-n}}{\sum_{k=1}^{i_0} D_k^{-n}}",
            font_size=32
        ).next_to(eq_pathloss, DOWN, buff=0.5, aligned_edge=LEFT)
        
        self.play(Write(eq_approx))
        self.wait(1)
        
        # Final simplified form
        eq_final = MathTex(
            r"\frac{S}{I} = \frac{Q^n}{i_0} = \frac{(\sqrt{3N})^n}{i_0}",
            font_size=36,
            color=YELLOW
        ).next_to(eq_approx, DOWN, buff=0.6)
        
        final_box = SurroundingRectangle(eq_final, color=YELLOW, buff=0.15, stroke_width=3)
        
        self.play(Create(final_box), Write(eq_final))
        self.wait(2)
        
        # ---------------------------------------------------------
        # SCENE 3: THE TRADEOFF TABLE
        # ---------------------------------------------------------
        
        # Clear scene
        self.play(
            FadeOut(entire_map),
            FadeOut(desired_signal),
            FadeOut(s_label),
            FadeOut(i_label),
            # FadeOut(eq_q),
            # FadeOut(q_box),
            eq_q.animate.shift(LEFT * 6.5 + UP*0.45).set_color(YELLOW).scale(0.8),
            q_box.animate.shift(LEFT * 6.5 + UP*0.45).set_color(YELLOW).scale(0.8),
            FadeOut(eq_sir),
            FadeOut(eq_pathloss),
            FadeOut(n_note),
            FadeOut(eq_approx),
            eq_final.animate.to_edge(UP, buff=0.8).scale(0.9),
            final_box.animate.to_edge(UP, buff=0.8).scale(0.9),
            title.animate.scale(0.8).to_edge(UP, buff=0.3)
        )
        self.wait(0.5)
        
        # Table title
        table_title = Text(
            "Tradeoff: Capacity vs Quality",
            font_size=30,
            color=BLUE
        ).next_to(final_box, DOWN, buff=0.8)
        table_title.shift(LEFT * 2.5)
        
        self.play(Write(table_title))
        self.wait(0.5)
        
        # Table data (assuming n=4)
        # S/I = (sqrt(3N))^4 / 6 = 9N^2 / 6 = 1.5 N^2
        # S/I_dB = 10 log(1.5 N^2)
        
        table_data = [
            ["N", "Q", "S/I (dB)", "Quality"],
            ["3", "3.0", "11.3", "Poor"],
            ["7", "4.6", "18.7", "Good"],
            ["12", "6.0", "23.3", "Excellent"]
        ]
        
        table = Table(
            table_data,
            include_outer_lines=True,
            line_config={"stroke_width": 2}
        ).scale(0.45).next_to(table_title, DOWN, buff=0.5)
        speed_test = 1234/567
        
        # Color header
        table.get_horizontal_lines()[0].set_color(YELLOW)
        table.get_horizontal_lines()[1].set_color(YELLOW)
        
        self.play(Create(table))
        self.wait(1)
        
        # Highlight N=7 (common choice)
        highlight_row = SurroundingRectangle(
            VGroup(*[table.get_entries((3, i)) for i in range(1, 5)]),
            color=GREEN,
            buff=0.05,
            stroke_width=3
        )
        
        self.play(Create(highlight_row))
        
        # standard_note = Text(
        #     "N=7 is commonly used (balances capacity & quality)",
        #     font_size=20,
        #     color=GREEN
        # ).next_to(table, DOWN, buff=0.4)
        
        # self.play(Write(standard_note))
        self.wait(1.5)
        
        # Key insight
        insight_box = Rectangle(
            height=1.2,
            width=9,
            color=ORANGE,
            stroke_width=3
        ).to_edge(DOWN, buff=0.5)
        
        insight = VGroup(
            Text("↑ N → Better S/I → Higher Quality → Lower Capacity", font_size=22),
            Text("↓ N → Worse S/I → Lower Quality → Higher Capacity", font_size=22)
        ).arrange(DOWN, buff=0.15)
        insight.move_to(insight_box.get_center())
        
        self.play(Create(insight_box))
        for line in insight:
            self.play(Write(line), run_time=0.8)
            self.wait(0.3)
        
        self.wait(3)
        
        # Fadeout
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()