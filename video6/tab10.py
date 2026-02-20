from manim import *

class TDMA_Animation(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        # 1. Colors for the 6 signals
        # We use a mix of distinct colors to show different users
        # colors = [TEAL_C, MAROON_D, GREEN, YELLOW, PURPLE, RED]
        colors = [TEAL_C, MAROON_D, GREEN, YELLOW, GRAY, RED]
        title = Title("Time Division Multiple Access (TDMA)", font_size=36)
        self.play(Write(title))
        # 2. Setup the Axes
        # X-axis: Time, Y-axis: Frequency
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1.5, 1],
            x_length=4.5,
            y_length=2,
            axis_config={"include_tip": True, "color": WHITE},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": []}
        )
        axes.to_edge(LEFT)

        # Labels
        # labels = VGroup(
        #     Text("Time", color=RED, font_size=20).move_to(axes_3d.c2p(7, 0, 0) + RIGHT * 0.5),
        #     Text("Frequency", color=BLUE, font_size=20).move_to(axes_3d.c2p(0, -4, 0) + UP * 0.1),
        #     Text("Power", color=BLACK, font_size=20).rotate(90*DEGREES, axis=RIGHT).move_to(axes_3d.c2p(0, 0, 2) + UP * 0.5)
        # )
        x_label = Text("Time", color = BLUE,font_size=20).move_to(axes.c2p(4, 0) + RIGHT * 0.5)
        y_label = Text("Frequency",color=BLUE, font_size=20).move_to(axes.c2p(0, 1.5) + UP * 0.5)
        # x_label = axes.get_x_axis_label("Time")
        # y_label = axes.get_y_axis_label("Frequency")
        
        # Specific Label "Freq 1" as seen in image
        freq_label = Text("F1", font_size=24).next_to(axes.c2p(0, 1), LEFT)

        # --- ANIMATION PART 1: SETUP ---
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Write(freq_label))
        self.wait(0.5)

        # --- CREATE BLOCKS ---
        blocks = VGroup()
        labels = VGroup()
        
        # We will create 6 slots
        # Each slot is 1 unit wide in time, and sits at Frequency level 1
        for i in range(2):
            c = colors[i]
            
            # Dimensions
            start_time = 1 + i  # Start at t=1, then t=2, etc.
            width = 1
            height = 0.8 # Visual height of the block
            
            # Create the block (Rectangle)
            # We anchor it to the axis coordinates
            # Bottom-left corner at (start_time, 1 - height/2) roughly?
            # Let's center it at y=1
            
            # Position: 
            # X center = start_time + width/2
            # Y center = 1 (Since it's Freq 1)
            
            center_pos = axes.c2p(start_time + width/2, 1)
            
            # Calculate width/height in scene units
            # X-unit size * width
            scene_width = axes.x_axis.unit_size * width
            scene_height = axes.y_axis.unit_size * 0.6 # slightly smaller than full unit
            
            rect = Rectangle(
                width=scene_width,
                height=scene_height,
                fill_color=c,
                fill_opacity=0.6,
                stroke_color=WHITE,
                stroke_width=2
            )
            rect.move_to(center_pos)
            
            # Pattern/Hatching (Optional styling to match the "sketch" look)
            # Manim doesn't have built-in easy hatch patterns for rectangles in basic objects,
            # so we stick to solid fill which is cleaner for video.
            
            blocks.add(rect)
            
            # Add User Label inside
            # "User 1", "User 2", ... "User 6"
            # Or if it repeats like the image: User 1, 2, 3, 1...
            # The prompt asked for "6 signals with different colors", implying 6 distinct users.
            label = Text(f"User {i+1}", font_size=20, color=WHITE)
            label.move_to(rect.get_center())
            labels.add(label)

        # --- ANIMATION PART 2: SEQUENTIAL APPEARANCE ---
        # Animate them appearing one by one to show "Time Division"
        
        for i in range(3):
            # 1. Highlight the time slot on axis (optional, adds detail)
            tick = Line(
                axes.c2p(i+1, -0.1), 
                axes.c2p(i+1, 0.1), 
                color=YELLOW
            )
            self.play(Create(tick, run_time=0.2))
            if(i<2):
            
                # 2. Show the block appearing (Grow from left to right looks like transmission)
                self.play(
                    
                    FadeIn(blocks[i], shift=RIGHT * 0.5), # Slides in slightly
                    Write(labels[i]),
                    run_time=0.8
                )
                # Small pause to emphasize the "Wait your turn" concept
                self.wait(0.2)

        # --- FINAL HOLD ---
        
        # Add a brace to show they share the bandwidth
        brace = Brace(blocks, direction=UP, buff=0.2)
        brace_text = brace.get_text("Shared Channel").scale(0.6)
        
        self.play(GrowFromCenter(brace), FadeIn(brace_text))
        
        self.wait(3)

        t0_label = Text("0", font_size=18)
        t_half_label = Text("T/2", font_size=18)
        t_label = Text("T", font_size=18)

        # Position them on the x-axis
        t0_label.next_to(axes.c2p(1, 0), DOWN)
        t_half_label.next_to(axes.c2p(2, 0), DOWN)   # mid of 0 to 4 → T/2
        t_label.next_to(axes.c2p(3, 0), DOWN)

        # Animate after axes are drawn
        self.play(
            FadeIn(t0_label),
            FadeIn(t_half_label),
            FadeIn(t_label)
        )

        self.wait(0.3)
        
        # --- ORTHOGONALITY CALCULATION ---
        self.wait(1)
        
        # Change title
        # ortho_title = Title("Time Division Multiple Access (TDMA) - Orthogonality", font_size=32)
        # self.play(Transform(title, ortho_title))
        # self.wait(1)
        
        # Create a vertical line to separate graph and calculations
        separator = Line(
            start=UP * 2.3,
            end=DOWN * 3.5,
            color=GRAY
        ).move_to(ORIGIN)
        self.play(Create(separator))
        
        # Step 1: Show the correlation integral formula
        correlation_formula = MathTex(
            r"\int_{0}^{T} x_1(t) \cdot x_2(t) \, dt",
            font_size=32
        )
        correlation_formula.move_to(RIGHT * 3.5 + UP * 1.5)
        
        self.play(Write(correlation_formula))
        self.wait(1.5)
        
        # Step 2: Break into two integrals for different time ranges
        split_formula = MathTex(
            r"= \int_{0}^{T/2} x_1(t) \cdot x_2(t) \, dt",
            r"+ \int_{T/2}^{T} x_1(t) \cdot x_2(t) \, dt",
            font_size=28
        )
        split_formula.next_to(correlation_formula, DOWN, buff=0.5)
        
        self.play(Write(split_formula))
        self.wait(1.5)
        
        # Step 3: Show that signals are zero in non-overlapping regions
        # explanation_1 = MathTex(
        #     r"\text{In } [0, T/2]: \, x_2(t) = 0",
        #     font_size=24,
        #     color=YELLOW
        # ).move_to(RIGHT * 3.5 + UP * 0.2)
        
        # explanation_2 = MathTex(
        #     r"\text{In } [T/2, T]: \, x_1(t) = 0",
        #     font_size=24,
        #     color=YELLOW
        # ).move_to(RIGHT * 3.5 + DOWN * 0.3)
        
        # self.play(Write(explanation_1))
        # self.wait(1)
        # self.play(Write(explanation_2))
        # self.wait(1.5)
        self.wait(3)
        
        # Step 4: Substitute zeros
        zero_integrals = MathTex(
            r"= \int_{0}^{T/2} x_1(t) \cdot 0 \, dt",
            r"+ \int_{T/2}^{T} 0 \cdot x_2(t) \, dt",
            font_size=28
        )
        zero_integrals.move_to(RIGHT * 3.5 + DOWN * 1.3)
        
        self.play(Write(zero_integrals))
        self.wait(1.5)
        
        # Step 5: Simplify to zero
        final_result = MathTex(
            r"= 0 + 0 = 0",
            font_size=32,
            color=GREEN
        )
        final_result.move_to(RIGHT * 3.5 + DOWN * 2.2)
        
        self.play(Write(final_result))
        self.wait(1.5)
        
        # Step 6: Conclusion
        conclusion = Text(
            "∴ Orthogonality Persists",
            font_size=26,
            color=GREEN
        ).move_to(RIGHT * 3.5 + DOWN * 3)
        
        box = SurroundingRectangle(conclusion, color=GREEN, buff=0.15)
        
        self.play(
            Write(conclusion),
            Create(box)
        )
        self.wait(3)