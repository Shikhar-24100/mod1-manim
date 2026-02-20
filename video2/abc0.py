from manim import *

class BridgeScene(Scene):
    def construct(self):
        # Load SVGs (adjust paths as needed)
        tower = SVGMobject("tower.svg").scale(0.8).to_edge(LEFT, buff=1.5)
        mobile = SVGMobject("mobile.svg").scale(0.5).to_edge(RIGHT, buff=1.5)
        building = SVGMobject("building.svg").scale(1.2)
        
        # Position building in center (starts off-screen below)
        building.move_to(ORIGIN).shift(DOWN * 5)
        
        # Labels
        tower_label = Text("Transmitter", font_size=24).next_to(tower, DOWN)
        mobile_label = Text("Receiver", font_size=24).next_to(mobile, DOWN)
        
        # Direct path line (green)
        direct_path = Line(
            tower.get_right(), 
            mobile.get_left(),
            color=GREEN,
            stroke_width=4
        )
        
        # Signal dots traveling along path
        signal_dot = Dot(color=GREEN, radius=0.1)
        signal_dot.move_to(tower.get_right())
        
        # --- SCENE 1: Show transmitter, receiver, direct path ---
        self.play(
            FadeIn(tower), 
            FadeIn(mobile),
            Write(tower_label),
            Write(mobile_label),
            run_time=1
        )
        
        self.play(Create(direct_path), run_time=0.8)
        
        # Animate signal traveling (repeat once)
        self.play(
            MoveAlongPath(signal_dot, direct_path),
            run_time=0.8,
            rate_func=linear
        )
        for _ in range(2):
            signal_dot.move_to(tower.get_right())
            self.play(MoveAlongPath(signal_dot, direct_path), run_time=0.5)
        self.remove(signal_dot)
        
        self.wait(6)
        
        # --- SCENE 2: Building slides in and blocks path ---
        self.play(
            building.animate.move_to(ORIGIN),
            run_time=1
        )
        
        # Path turns red and dashed
        blocked_path = DashedLine(
            tower.get_right(),
            mobile.get_left(),
            color=RED,
            stroke_width=4,
            dash_length=0.15
        )
        
        # X mark on the blocked path
        x_mark = Cross(scale_factor=0.3, color=RED).move_to(ORIGIN)
        
        self.play(
            ReplacementTransform(direct_path, blocked_path),
            FadeIn(x_mark),
            run_time=0.8
        )
        
        self.wait(0.3)
        
        # --- SCENE 3: Question mark above receiver ---
        question = Text("?", font_size=72, color=YELLOW)
        question.next_to(mobile, UP, buff=0.3)
        
        self.play(
            FadeIn(question, shift=UP * 0.3),
            question.animate.scale(1.2),
            run_time=0.5
        )
        self.play(question.animate.scale(1/1.2), run_time=0.3)
        
        self.wait(0.5)
        
        # --- SCENE 4: Hook text ---
        hook_text = Text(
            "How does the signal still reach?",
            font_size=32,
            color=WHITE
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(hook_text), run_time=1)
        
        self.wait(1)
        
        # Fade out everything for transition
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8
        )