from manim import *

class SimpleTradeoff(Scene):
    def construct(self):
        # Simple text at top
        users_text = Text("Users: 100", font_size=36, color=WHITE)
        users_text.to_edge(UP, buff=1)
        
        quality_text = Text("Quality: 100%", font_size=36, color=WHITE)
        quality_text.next_to(users_text, DOWN, buff=0.5)
        
        # Network signal indicator in center
        bars = VGroup()
        for i in range(5):
            bar = Rectangle(
                height=0.3 + i * 0.3,
                width=0.3,
                fill_opacity=1,
                fill_color=WHITE,
                stroke_width=0
            )
            bar.move_to(ORIGIN + RIGHT * i * 0.5 + LEFT*1)
            bar.align_to(ORIGIN + DOWN * 1, DOWN)
            bars.add(bar)
        
        # Show initial state
        self.play(Write(users_text), Write(quality_text))
        self.play(FadeIn(bars))
        self.wait(1)
        
        # Simulate user increase and quality decrease
        stages = [
            (500, 80, 4),
            (1000, 60, 3),
            (2000, 40, 2),
            (5000, 20, 1),
        ]
        
        for users, quality, active_bars in stages:
            # Fade out bars that should disappear
            fade_anims = []
            for i in range(5):
                if i >= active_bars:
                    fade_anims.append(bars[i].animate.set_opacity(0.2))
            
            # Update text and bars
            new_users = Text(f"Users: {users}", font_size=36, color=WHITE)
            new_users.move_to(users_text)
            
            new_quality = Text(f"Quality: {quality}%", font_size=36, color=WHITE)
            new_quality.move_to(quality_text)
            
            self.play(
                Transform(users_text, new_users),
                Transform(quality_text, new_quality),
                *fade_anims,
                run_time=1.5
            )
            self.wait(0.5)
        
        # Final message
        self.wait(0.5)
        message = Text("We need a smarter approach!", font_size=42, color=WHITE)
        message.to_edge(DOWN, buff=1)
        
        self.play(Write(message))
        self.wait(2)