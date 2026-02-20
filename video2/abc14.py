from manim import *
import numpy as np

class SummaryScene(Scene):
    def construct(self):
        # Black background is default
        
        # ================================================
        # SUBTLE BACKGROUND ANIMATION: Floating dots
        # ================================================
        
        # Create small floating dots (subtle, not distracting)
        np.random.seed(99)
        num_dots = 12
        bg_dots = VGroup()
        
        for _ in range(num_dots):
            dot = Dot(
                point=np.array([
                    np.random.uniform(-6.5, 6.5),
                    np.random.uniform(-3.5, 3.5),
                    0
                ]),
                radius=0.06,            # larger so visible
                color=WHITE,
                fill_opacity=0.6,      # more opaque
                stroke_width=0
            )
            bg_dots.add(dot)
        
        # Fade them in so the updater starts and they are clearly visible
        self.add(bg_dots)           # keep them in the scene graph
        self.play(FadeIn(bg_dots, run_time=0.8))
        
        # Gentle floating animation (runs throughout)
        def float_dots(mob, dt):
            for dot in mob:
                dot.shift(UP * 0.008 * np.sin(self.time * 0.5 + hash(id(dot)) % 10))
                dot.shift(RIGHT * 0.005 * np.cos(self.time * 0.3 + hash(id(dot)) % 10))
        
        bg_dots.add_updater(float_dots)
        
        # ================================================
        # TITLE
        # ================================================
        
        title = Text("Summary", font_size=52, weight=BOLD, color=WHITE)
        title.to_edge(UP, buff=0.6)
        
        underline = Line(LEFT * 1.5, RIGHT * 1.5, color=WHITE, stroke_width=2)
        underline.next_to(title, DOWN, buff=0.15)
        
        self.play(Write(title), Create(underline), run_time=0.8)
        
        self.wait(0.5)
        
        # ================================================
        # POINTS - ONE BY ONE
        # ================================================
        
        points = [
            "Multipath: Multiple signal copies via different paths",
            "Three mechanisms: Reflection, Diffraction, Scattering",
            "Phasor: Represents amplitude + phase as a vector",
            "Phase changes with distance (φ = 2πd/λ)",
            "Constructive & Destructive interference",
            "Rayleigh fading: Many NLOS paths → random amplitude",
        ]
        
        point_mobjects = VGroup()
        
        for i, point in enumerate(points):
            # Bullet point
            bullet = Dot(radius=0.06, color=WHITE).shift(LEFT * 5.5)
            text = Text(point, font_size=24, color=WHITE)
            text.next_to(bullet, RIGHT, buff=0.25)
            
            line = VGroup(bullet, text)
            line.shift(UP * (1.5 - i * 0.65))
            
            point_mobjects.add(line)
            self.wait(0.7)
        
        # Animate points appearing one by one
        for point in point_mobjects:
            self.play(
                FadeIn(point[0], scale=0.5),  # bullet
                Write(point[1], run_time=0.6),  # text
                run_time=0.7
            )
            self.wait(0.2)
        
        self.wait(1.0)
        
        # ================================================
        # WHAT'S NEXT - SAME FRAME, BELOW SUMMARY
        # ================================================
        
        self.wait(0.8)
        
        # "Next Video" label
        # next_label = Text("Next Video:", font_size=28, color=WHITE)
        # next_label.move_to(DOWN * 2.0 + LEFT * 4.5)
        
        # Next video title with YELLOW box
        video_title = Text(
            "Next Video: Multipath Delay & Coherence Bandwidth",
            font_size=30,
            weight=BOLD,
            color=YELLOW
        )
        video_title.to_edge(DOWN, buff=0.4)
        
        # Yellow highlighted box
        yellow_box = SurroundingRectangle(
            video_title,
            color=YELLOW,
            buff=0.2,
            stroke_width=3,
            corner_radius=0.1
        )
        
        # Animate
        # self.play(Write(next_label), run_time=0.5)
        self.play(
            Write(video_title),
            Create(yellow_box),
            run_time=0.8
        )
        
        # Subtle pulse on the yellow box
        self.play(
            yellow_box.animate.set_stroke(width=5),
            rate_func=there_and_back,
            run_time=0.6
        )
        
        self.wait(2.0)
        
        # ================================================
        # FADE OUT EVERYTHING
        # ================================================
        
        bg_dots.clear_updaters()
        
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.0
        )
        
        self.wait(0.5)