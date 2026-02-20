from manim import *

class FrequencyReuseSummary(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # INTRO: Frequency Reuse Concept
        # ---------------------------------------------------------
        
        # Title
        title = Text("Frequency Reuse: Foundation of Wireless Communication", 
                     font_size=32, weight=BOLD).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        
        # Simple hexagonal cluster showing frequency reuse
        hex_group = VGroup()
        colors = [RED, BLUE, GREEN, ORANGE, PURPLE, PINK, TEAL]
        letters = ["A", "B", "C", "D", "E", "F", "G"]
        
        # Create a small cluster
        R = 0.4
        positions = [
            [0, 0],           # A - center
            [0.7, 0],         # B - right
            [0.35, 0.6],      # C - top-right
            [-0.35, 0.6],     # D - top-left
            [-0.7, 0],        # E - left
            [-0.35, -0.6],    # F - bottom-left
            [0.35, -0.6],     # G - bottom-right
        ]
        
        for i, (letter, color, pos) in enumerate(zip(letters, colors, positions)):
            hex_cell = RegularPolygon(n=6, color=color, fill_opacity=0.4, stroke_width=3)
            hex_cell.scale(R).rotate(30*DEGREES).move_to([pos[0], pos[1], 0])
            label = Text(letter, font_size=24, color=WHITE, weight=BOLD).move_to(hex_cell)
            hex_group.add(VGroup(hex_cell, label))
        
        hex_group.move_to(LEFT * 3.5 + DOWN * 0.5)
        
        self.play(LaggedStart(*[FadeIn(cell) for cell in hex_group], lag_ratio=0.1), run_time=1.5)
        
        # Label it
        reuse_label = Text("Frequency\nReuse", font_size=20, color=YELLOW).next_to(hex_group, DOWN)
        self.play(Write(reuse_label), run_time=0.8)
        self.wait(5)
        
        # ---------------------------------------------------------
        # EVOLUTION TIMELINE
        # ---------------------------------------------------------
        
        # Create timeline on the right side
        timeline_title = Text("Evolution Across Generations", font_size=28, weight=BOLD, color=BLUE)
        timeline_title.move_to(RIGHT * 2.5 + UP * 2)
        
        self.play(Write(timeline_title), run_time=1)
        
        # Timeline entries
        generations = VGroup()
        
        # 1G - Frequency
        gen_1g = VGroup(
            Text("1G: ", font_size=24, weight=BOLD, color=RED),
            Text("Frequency Division", font_size=20, color=WHITE)
        ).arrange(RIGHT, buff=0.2)
        gen_1g.move_to(RIGHT * 2.5 + UP * 1)
        
        # 2G - Time Slots
        gen_2g = VGroup(
            Text("2G: ", font_size=24, weight=BOLD, color=ORANGE),
            Text("Time Slots (TDMA)", font_size=20, color=WHITE)
        ).arrange(RIGHT, buff=0.2)
        gen_2g.move_to(RIGHT * 2.5 + UP * 0.2)
        
        # 3G - Codes
        gen_3g = VGroup(
            Text("3G: ", font_size=24, weight=BOLD, color=GREEN),
            Text("CDMA Codes", font_size=20, color=WHITE)
        ).arrange(RIGHT, buff=0.2)
        gen_3g.move_to(RIGHT * 2.5 + DOWN * 0.6)
        
        # 4G/5G - Resource Blocks
        gen_4g = VGroup(
            Text("4G/5G: ", font_size=24, weight=BOLD, color=PURPLE),
            Text("Resource Blocks", font_size=20, color=WHITE)
        ).arrange(RIGHT, buff=0.2)
        gen_4g.move_to(RIGHT * 2.5 + DOWN * 1.4)
        
        generations.add(gen_1g, gen_2g, gen_3g, gen_4g)
        
        # Animate timeline entries with arrows
        # arrow_start = hex_group.get_right() + RIGHT * 0.3
        # for gen in generations:
        #     arrow = Arrow(arrow_start, gen.get_left() + LEFT * 0.2, 
        #                  color=YELLOW, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        #     self.play(
        #         GrowArrow(arrow),
        #         FadeIn(gen, shift=RIGHT * 0.3),
        #         run_time=0.8
        #     )
        #     self.wait(0.3)
        
        # self.wait(1)
        
        # ---------------------------------------------------------
        # CONCLUSION
        # ---------------------------------------------------------
        
        # Fade out timeline, keep title
        self.play(
            *[FadeOut(mob) for mob in [hex_group, reuse_label, timeline_title, generations]],
            run_time=6
        )
        
        # Final message
        self.wait(5)
        conclusion = VGroup(
            Text("The same principle:", font_size=28, color=YELLOW),
            Text("Divide resources efficiently", font_size=32, weight=BOLD, color=GREEN),
            Text("to enable seamless communication", font_size=28, color=BLUE)
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        
        self.play(Write(conclusion), run_time=2.5)
        self.wait(5)
        
        self.play(FadeOut(conclusion), FadeOut(title), run_time=1)