from manim import *

class Lecture6_Intro(Scene):
    def construct(self):
        # =====================================================
        # PART 1: Transition (0:32-0:38) — 6 seconds
        # =====================================================
        
        # Simple text on screen
        transition_text = VGroup(
            Text("So, we've seen how the", font_size=36),
            Text("wireless environment behaves.", font_size=36, color=BLUE)
        ).arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(transition_text, shift=UP), run_time=1)
        self.wait(2)
        
        question_text = Text(
            "But now, we face a critical question...",
            font_size=38,
            color=YELLOW,
            slant=ITALIC
        )
        question_text.next_to(transition_text, DOWN, buff=0.8)
        
        self.play(Write(question_text), run_time=1.5)
        self.wait(1.5)
        
        # Clear screen
        self.play(FadeOut(transition_text), FadeOut(question_text))
        
        
        
        # Question text
        question = VGroup(
            Text("What happens when hundreds — or even", font_size=32),
            Text("thousands — of users need to share", font_size=32),
            Text("the same limited spectrum simultaneously?", font_size=32, color=RED)
        ).arrange(DOWN, buff=0.2)
        question.move_to(ORIGIN)
        
        self.play(Write(question), run_time=2.5)
        self.wait(2)
        
        # Clear for next part
        self.play(
            FadeOut(question)
        )
        
        # =====================================================
        # PART 3: Problem Statement (0:50-0:58) — 8 seconds
        # =====================================================
        
        # Just text - no visuals
        problem_statement = Text(
            "This is called the Resource Allocation Problem.",
            font_size=40,
            color=YELLOW
        )
        problem_statement.move_to(ORIGIN)
        
        self.play(Write(problem_statement), run_time=1.5)
        self.wait(2.5)
        
        # Clear screen
        self.play(FadeOut(problem_statement))
        
        # =====================================================
        # PART 4: Title Card (0:58-1:02) — 4 seconds
        # =====================================================
        
        # Main title
        main_title = Text(
            "Lecture 6:",
            font_size=40,
            color=WHITE
        )
        main_title.shift(UP * 0.8)
        
        subtitle = Text(
            "Interference and Orthogonality",
            font_size=52,
            color=BLUE,
            weight=BOLD
        )
        subtitle.next_to(main_title, DOWN, buff=0.4)
        
        # Decorative line
        line = Line(LEFT * 4, RIGHT * 4, color=BLUE, stroke_width=3)
        line.next_to(subtitle, DOWN, buff=0.3)
        
        title_group = VGroup(main_title, subtitle, line)
        
        self.play(
            Write(main_title),
            Write(subtitle),
            Create(line),
            run_time=2
        )
        self.wait(2)
        
        # Fade out
        self.play(FadeOut(title_group), run_time=1)