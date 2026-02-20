from manim import *
import numpy as np

class Scene2_IQ_Coordinates(Scene):
    def construct(self):
        # Title
        title = Text("Introducing the Coordinate System", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Start with a simplified version of the tip-to-tail from Scene 1
        # Show just a few phasors quickly adding up
        num_paths = 6
        angles = np.linspace(0, 2*PI, num_paths, endpoint=False)
        amplitudes = np.random.uniform(0.6, 1.2, num_paths)
        phases = np.random.uniform(0, 2*PI, num_paths)
        colors = [BLUE, GREEN, YELLOW, PURPLE, PINK, ORANGE]
        
        # Build the chain quickly
        phasors = []
        chain_arrows = []
        current_pos = ORIGIN
        
        for i in range(num_paths):
            x = amplitudes[i] * np.cos(angles[i] + phases[i])
            y = amplitudes[i] * np.sin(angles[i] + phases[i])
            phasors.append((x, y))
            
            vec = np.array([x, y, 0])
            arrow = Arrow(
                current_pos,
                current_pos + vec,
                buff=0,
                color=colors[i],
                stroke_width=3
            )
            chain_arrows.append(arrow)
            current_pos = current_pos + vec
            
        # Show all at once (recap from Scene 1)
        self.play(*[Create(arrow) for arrow in chain_arrows], run_time=1)
        
        # The resultant h
        final_pos = current_pos
        resultant = Arrow(
            ORIGIN,
            final_pos,
            buff=0,
            color=RED,
            stroke_width=8
        )
        h_label = MathTex("h", font_size=48, color=RED)
        h_label.next_to(resultant.get_center(), UP + RIGHT, buff=0.2)
        
        self.play(Create(resultant), Write(h_label), run_time=1)
        self.wait(1)
        
        # Fade out the component arrows - keep only h
        narration1 = Text("Let's focus only on the resultant h", font_size=28)
        narration1.to_edge(DOWN)
        self.play(Write(narration1))
        
        self.play(*[FadeOut(arrow) for arrow in chain_arrows], run_time=1)
        self.wait(1)
        self.play(FadeOut(narration1))
        
        # Now add the coordinate system
        narration2 = Text("We can describe h using coordinates", font_size=28)
        narration2.to_edge(DOWN)
        self.play(Write(narration2))
        
        # Create I and Q axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={
                "color": GRAY,
                "stroke_width": 2,
            },
            tips=True,
        )
        
        # Labels for axes
        i_label = MathTex("I", font_size=36, color=BLUE).next_to(axes.x_axis.get_end(), RIGHT)
        q_label = MathTex("Q", font_size=36, color=GREEN).next_to(axes.y_axis.get_end(), UP)
        
        i_full = Text("(In-Phase / Real)", font_size=20, color=BLUE)
        i_full.next_to(i_label, DOWN, buff=0.2)
        
        q_full = Text("(Quadrature / Imaginary)", font_size=20, color=GREEN)
        q_full.next_to(q_label, RIGHT, buff=0.2)
        
        self.play(Create(axes), run_time=1.5)
        self.play(Write(i_label), Write(q_label))
        self.wait(0.5)
        self.play(Write(i_full), Write(q_full))
        self.wait(2)
        
        # Fade out full labels to reduce clutter
        self.play(FadeOut(i_full), FadeOut(q_full))
        
        # Move the resultant arrow to align with the coordinate system
        # (It was already at ORIGIN, so it should fit)
        # Adjust if needed
        self.play(FadeOut(narration2))
        
        # Draw projections onto I and Q axes
        narration3 = Text("h has an I component and a Q component", font_size=28)
        narration3.to_edge(DOWN)
        self.play(Write(narration3))
        
        # Get the endpoint of h
        h_end = resultant.get_end()
        i_component = h_end[0]
        q_component = h_end[1]
        
        # Dotted lines to axes
        i_line = DashedLine(
            h_end,
            np.array([i_component, 0, 0]),
            color=BLUE,
            stroke_width=3
        )
        
        q_line = DashedLine(
            h_end,
            np.array([0, q_component, 0]),
            color=GREEN,
            stroke_width=3
        )
        
        self.play(Create(i_line), Create(q_line), run_time=1.5)
        self.wait(1)
        
        # Show I and Q values on axes
        i_dot = Dot(np.array([i_component, 0, 0]), color=BLUE, radius=0.08)
        q_dot = Dot(np.array([0, q_component, 0]), color=GREEN, radius=0.08)
        
        i_value_label = MathTex(f"I", font_size=28, color=BLUE)
        i_value_label.next_to(i_dot, DOWN, buff=0.2)
        
        q_value_label = MathTex(f"Q", font_size=28, color=GREEN)
        q_value_label.next_to(q_dot, LEFT, buff=0.2)
        
        self.play(Create(i_dot), Create(q_dot))
        self.play(Write(i_value_label), Write(q_value_label))
        self.wait(2)
        
        # Show the formula h = I + jQ
        self.play(FadeOut(narration3))
        
        formula = MathTex("h", "=", "I", "+", "j", "Q", font_size=40)
        formula[0].set_color(RED)
        formula[2].set_color(BLUE)
        formula[4].set_color(YELLOW)
        formula[5].set_color(GREEN)
        formula.to_edge(DOWN, buff=1)
        
        self.play(Write(formula), run_time=2)
        self.wait(2)
        
        # Now highlight the magnitude (gain)
        narration4 = Text("The length of h is the channel gain", font_size=28)
        narration4.next_to(formula, DOWN, buff=0.3)
        self.play(Write(narration4))
        
        # Draw a brace along the resultant
        magnitude_brace = Brace(resultant, direction=resultant.copy().rotate(PI/2).get_unit_vector())
        magnitude_label = MathTex("|h|", "=", "r", font_size=32, color=YELLOW)
        magnitude_label.next_to(magnitude_brace, UP + RIGHT, buff=0.1)
        
        self.play(Create(magnitude_brace), Write(magnitude_label), run_time=1.5)
        self.wait(2)
        
        # Show the magnitude formula
        magnitude_formula = MathTex("r", "=", "\\sqrt{", "I^2", "+", "Q^2", "}", font_size=36)
        magnitude_formula[0].set_color(YELLOW)
        magnitude_formula[3].set_color(BLUE)
        magnitude_formula[5].set_color(GREEN)
        magnitude_formula.next_to(narration4, DOWN, buff=0.3)
        
        self.play(Write(magnitude_formula), run_time=2)
        self.wait(3)
        
        # Key takeaway
        self.play(
            FadeOut(narration4),
            FadeOut(magnitude_brace),
            FadeOut(magnitude_label),
            FadeOut(magnitude_formula)
        )
        
        takeaway1 = Text("We don't track the million reflections", font_size=26)
        takeaway2 = Text("We only track this arrow with I, Q, and |h|", font_size=26, color=YELLOW)
        
        takeaways = VGroup(takeaway1, takeaway2).arrange(DOWN, buff=0.3)
        takeaways.to_edge(DOWN, buff=0.5)
        
        self.play(Write(takeaway1))
        self.wait(0.5)
        self.play(Write(takeaway2))
        self.wait(3)
        
        # Fade everything
        self.play(*[FadeOut(mob) for mob in self.mobjects])


# To render:
# manim -pql scene2_iq.py Scene2_IQ_Coordinates