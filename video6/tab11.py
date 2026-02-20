from manim import *

class FDMA_Staggered_Proof(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        colors = [TEAL_C, MAROON_D, GREEN]
        
        title = Title("Frequency Division Multiple Access (FDMA)", font_size=36)
        self.play(Write(title))
        
        # 2. Setup the Axes
        # Increased x_range to fit the staggered blocks that go further in time
        axes = Axes(
            x_range=[0, 7, 1], 
            y_range=[0, 4, 1],
            x_length=6,        
            y_length=3.5,
            axis_config={"include_tip": True, "color": WHITE},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": []}
        )
        axes.to_edge(LEFT).shift(DOWN * 0.5)

        x_label = Text("Time", color=BLUE, font_size=20).move_to(axes.c2p(7, 0) + RIGHT * 0.5)
        y_label = Text("Frequency", color=BLUE, font_size=20).move_to(axes.c2p(0, 4) + UP * 0.3)
        
        # Labels for F1, F2, F3
        freq_label1 = Text("F1", font_size=24).next_to(axes.c2p(0, 1), LEFT)
        freq_label2 = Text("F2", font_size=24).next_to(axes.c2p(0, 2), LEFT)
        freq_label3 = Text("F3", font_size=24).next_to(axes.c2p(0, 3), LEFT)

        # --- ANIMATION PART 1: SETUP ---
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Write(freq_label1), Write(freq_label2), Write(freq_label3))
        self.wait(0.5)

        # --- CREATE BLOCKS ---
        blocks = VGroup()
        labels = VGroup()

        # Create 3 Staggered Blocks
        for i in range(3):
            c = colors[i]
            
            # Dimensions & Stagger Logic
            start_time = 0.5 + (i * 1.0) 
            width = 2.5         
            height = 0.6        
            
            center_pos = axes.c2p(start_time + width/2, 1 + i)
            
            scene_width = axes.x_axis.unit_size * width
            scene_height = axes.y_axis.unit_size * height
            
            rect = Rectangle(
                width=scene_width,
                height=scene_height,
                fill_color=c,
                fill_opacity=0.6,
                stroke_color=WHITE,
                stroke_width=2
            )
            rect.move_to(center_pos)
            blocks.add(rect)
            
            label = Text(f"User {i+1}", font_size=20, color=WHITE)
            label.move_to(rect.get_center())
            labels.add(label)

        # --- ANIMATION PART 2: APPEARANCE ---
        for i in range(3):
            self.play(
                FadeIn(blocks[i], shift=RIGHT * 0.5),
                Write(labels[i]),
                run_time=0.8
            )
        
        self.wait(1)

        # Brace
        brace = Brace(blocks, direction=RIGHT, buff=0.1)
        brace_text = Text("Distinct Frequency", font_size=20).next_to(brace, RIGHT, buff=0.1)
        self.play(GrowFromCenter(brace), FadeIn(brace_text))
        self.wait(1)

        # --- NEW FDMA PROOF (RHS) ---
        
        # 1. Separator Line
        separator = Line(
            start=UP * 2.3,
            end=DOWN * 3.5,
            color=GRAY
        ).move_to(ORIGIN).shift(RIGHT * 1) 
        self.play(Create(separator))
        
        # 2. General Formula
        header = Text("Orthogonality Proof:", font_size=20, color=YELLOW, weight=BOLD)
        header.move_to(RIGHT * 4.5 + UP * 2.5)
        # self.play(Write(header))
        
        formula = MathTex(
            r"\int_{0}^{T} x_1(t) \cdot x_2(t) \, dt",
            font_size=28
        ).next_to(header, DOWN, buff=0.5)
        self.play(Write(formula))
        self.wait(1)
        
        # 3. Substitution (Cosines)
        # We shift existing formula up slightly or just place this below
        substitution = MathTex(
            r"\text{Let } x_1 = \cos(2\pi f_1 t), \, x_2 = \cos(2\pi f_2 t)",
            font_size=22, color=BLUE
        ).next_to(formula, DOWN, buff=0.3)
        self.play(Write(substitution))
        self.wait(1)

        # 4. Trig Identity Step
        identity_step = MathTex(
            r"= \int_{0}^{T} \frac{1}{2} [\cos(2\pi(f_1 - f_2)t) + \cos(2\pi(f_1 + f_2)t)] \, dt",
            font_size=22
        ).next_to(substitution, DOWN, buff=0.4)
        self.play(Write(identity_step))
        self.wait(2)
        
        # 5. The Result (Zero)
        result = MathTex(
            r"= 0",
            font_size=36,
            color=GREEN
        ).next_to(identity_step, DOWN, buff=0.3)
        
        condition = MathTex(
            r"(\text{if } f_1 \neq f_2)",
            font_size=20,
            color=GRAY
        ).next_to(result, RIGHT, buff=0.2)
        
        self.play(Write(result), FadeIn(condition))
        self.wait(1)
        
        # 6. Conclusion Box
        final_text = MathTex(
            r"\text{Frequency separation ensures orthogonality } \checkmark", 
            font_size=22, color=GREEN
        ).next_to(result, DOWN, buff=0.5)
        
        proof_box = SurroundingRectangle(final_text, color=GREEN, buff=0.15)
        
        self.play(
            Write(final_text),
            Create(proof_box)
        )
        
        self.wait(3)