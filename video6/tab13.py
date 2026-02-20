from manim import *

class CDMA_Stacked_Codes(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        # 1. Six distinct colors
        title = Title("Frequency Division Multiple Access (FDMA)", font_size=36)
        self.play(Write(title))
        subtitle = Text("All users use the same frequency and transmit simultaneously", font_size=24, color = YELLOW)
        subtitle.next_to(title, DOWN)
        self.play(Write(subtitle))
        
        # 
        colors = [TEAL_C, MAROON_D, GREEN, GRAY]
        
        # 2. Text labels for the codes
        # Following the pattern: 001(c1), 002(c2)...
        code_labels = [
            "C_1 = [+1, +1, +1, +1]", 
            "C_2 = [+1, -1, +1, -1]", 
            "C_3 = [+1, +1, -1, -1]", 
            "C_4 = [+1, -1, -1, +1]"
        ]

        # --- CREATE OBJECTS ---
        stack_group = VGroup()
        
        for i in range(4):
            # Create the rectangle
            rect = Rectangle(
                width=5, 
                height=0.5, 
                fill_color=colors[i], 
                fill_opacity=0.85, 
                stroke_color=WHITE, 
                stroke_width=2
            )
            
            # Create the text (using MathTex for the subscript look)
            label = MathTex(
                code_labels[i], 
                font_size=36, 
                color=WHITE
            )
            
            # Combine rect and label
            item = VGroup(rect, label)
            stack_group.add(item)

        # --- ARRANGEMENT ---
        # Stack them vertically (UP) with zero buffer (touching)
        # To make them look like layers of a single signal
        stack_group.arrange(UP, buff=0)
        
        # Center the whole stack
        stack_group.shift(LEFT*3.5)
        # --- ANIMATION ---
        self.play(
            LaggedStart(
                *[GrowFromCenter(item) for item in stack_group],
                lag_ratio=0.2
            )
        )
        subtitle2 = Text("Codes must be mathematically Orthogonal (Perpendicular) to function", font_size=24, color = YELLOW)
        subtitle2.next_to(title, DOWN)
        self.play(Transform(subtitle, subtitle2))
        # Add a brace to emphasize they are all together
        self.wait(3)
        # self.play(FadeOut(stack_group))
        orth_check = VGroup(
            MathTex("C_1 \\cdot C_2 = (+1)(+1) + (+1)(-1) + (+1)(+1) + (+1)(-1)", font_size=24),
            MathTex("= 1 - 1 + 1 - 1 = 0 \\; \\checkmark", font_size=24, color=GREEN),
            MathTex("C_1 \\cdot C_3 = 0 \\; \\checkmark, \\quad C_1 \\cdot C_4 = 0 \\; \\checkmark", 
                    font_size=24, color=GREEN),
            Text("All pairs orthogonal!", font_size=24, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        orth_check.shift(RIGHT*3.5)
        
        self.play(Write(orth_check))
        self.wait(3)
        self.play(FadeOut(orth_check))
        subtitle3 = Text("The receiver must possess the unique Code of the target Tx beforehand.", font_size=24, color = YELLOW)
        subtitle3.next_to(subtitle2, DOWN)
        self.play(Write(subtitle3))
        self.wait(3)

        tower = SVGMobject("assets/tower.svg").scale(0.5).to_edge(RIGHT)
        self.play(FadeIn(tower))
        rx_label = Text("rx", font_size=24, color=YELLOW).next_to(tower, DOWN)
        self.play(Write(rx_label))
        code_label1 = MathTex("(C_2)", font_size=28, color=YELLOW).next_to(tower, UP)
        self.play(Write(code_label1))
        self.wait(5)

        stack_group.shift(LEFT*1)

        final_check = VGroup(
            MathTex(
                r"C_4 \cdot C_2 = (+1)(+1) + (-1)(-1) + (-1)(+1) + (+1)(-1) = 0 \;\; \times",
                font_size=24, color=RED 
            ),
            MathTex(
                r"C_3 \cdot C_2 = (+1)(+1) + (+1)(-1) + (-1)(+1) + (-1)(-1) = 0 \;\; \times",
                font_size=24, color=RED
            ),
            MathTex(
                r"C_2 \cdot C_2 = (+1)(+1) + (-1)(-1) + (+1)(+1) + (-1)(-1) = 4 \;\; \checkmark",
                font_size=24, color=GREEN
            ),
            MathTex(
                r"C_1 \cdot C_2 = (+1)(+1) + (-1)(-1) + (-1)(+1) + (+1)(-1) = 0 \;\; \times",
                font_size=24, color=RED
            ),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        final_check.next_to(stack_group, RIGHT, buff=0.5)

        correct_box = SurroundingRectangle(final_check[2], color=GREEN, buff=0.15)
        
        self.play(Write(final_check), run_time=10)

        self.play(Create(correct_box))
        self.play(FadeOut(final_check[0], final_check[1], final_check[3]))
        # self.play(Fa)
        self.wait(5)