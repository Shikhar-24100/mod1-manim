from manim import *
import numpy as np

class WirelessIntro(Scene):
    def construct(self):
        # Professional dark background
        self.camera.background_color = "#0a0e27"
        
        # Animated wireless signal waves (sine waves)
        def create_wave(amplitude, frequency, phase, color, opacity):
            wave = FunctionGraph(
                lambda x: amplitude * np.sin(frequency * x + phase),
                x_range=[-7, 7, 0.01],
                color=color,
                stroke_width=2,
                stroke_opacity=opacity
            )
            return wave
        
        # Multiple waves at different frequencies
        waves = VGroup()
        colors = ["#1e90ff", "#4169e1", "#6495ed", "#00bfff"]
        for i in range(4):
            wave = create_wave(
                amplitude=0.4 + i*0.15,
                frequency=0.8 + i*0.2,
                phase=i*PI/4,
                color=colors[i],
                opacity=0.3 + i*0.1
            )
            wave.shift(UP * (1.5 - i*0.5))
            waves.add(wave)
        
        self.play(
            LaggedStart(*[Create(wave) for wave in waves], lag_ratio=0.2),
            run_time=2
        )
        
        # Add subtle grid
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": "#1e3a8a",
                "stroke_width": 0.5,
                "stroke_opacity": 0.15
            },
            axis_config={"stroke_opacity": 0}
        )
        self.add(grid)
        self.bring_to_back(grid)
        
        # Corner accents (well-spaced)
        corner_tl = VGroup(
            Line(ORIGIN, RIGHT * 1.2, stroke_width=3, color="#1e90ff"),
            Line(ORIGIN, DOWN * 1.2, stroke_width=3, color="#1e90ff")
        ).move_to(LEFT * 6 + UP * 3.2)
        
        corner_tr = VGroup(
            Line(ORIGIN, LEFT * 1.2, stroke_width=3, color="#1e90ff"),
            Line(ORIGIN, DOWN * 1.2, stroke_width=3, color="#1e90ff")
        ).move_to(RIGHT * 6 + UP * 3.2)
        
        self.play(
            LaggedStart(Create(corner_tl), Create(corner_tr), lag_ratio=0.3),
            run_time=0.8
        )
        
        # Key equations (well-spaced, top area only)
        equations = VGroup(
            MathTex(r"f = \frac{c}{\lambda}", font_size=32, color="#60a5fa"),
            MathTex(r"P = \frac{V^2}{R}", font_size=32, color="#60a5fa"),
            MathTex(r"\omega = 2\pi f", font_size=32, color="#60a5fa"),
            MathTex(r"SNR_{dB} = 10\log_{10}\left(\frac{P_s}{P_n}\right)", font_size=28, color="#60a5fa")
        )
        
        # Position in top corners (away from center)
        equations[0].to_corner(UL, buff=0.8)
        equations[1].to_corner(UR, buff=0.8)
        equations[2].move_to(LEFT * 5 + UP * 2)
        equations[3].move_to(RIGHT * 4.5 + UP * 2)
        
        self.play(
            LaggedStart(*[FadeIn(eq, scale=0.8) for eq in equations], lag_ratio=0.15),
            run_time=1.5
        )
        
        # Module badge (top center)
        module_badge = RoundedRectangle(
            width=7, height=0.7,
            corner_radius=0.1,
            fill_color="#1e293b",
            fill_opacity=0.9,
            stroke_color="#334155",
            stroke_width=1.5
        ).shift(UP * 3)
        
        module_text = Text(
            "Module 1: Fundamentals of Wireless Communication",
            font_size=22,
            color="#94a3b8",
            weight=MEDIUM
        ).move_to(module_badge)
        
        self.play(
            FadeIn(module_badge, shift=DOWN*0.3),
            Write(module_text),
            run_time=1
        )
        
        # Main title with glow
        title = Text(
            "WIRELESS CONCEPTS",
            font_size=64,
            weight=BOLD,
            color="#ffffff",
            gradient=(WHITE, "#60a5fa")
        )
        
        subtitle = Text(
            "5G & BEYOND",
            font_size=40,
            weight=BOLD,
            color="#60a5fa"
        ).next_to(title, DOWN, buff=0.4)
        
        title_group = VGroup(title, subtitle).move_to(UP * 0.3)
        
        # Animated title appearance
        self.play(
            Write(title, run_time=1.5),
            FadeIn(subtitle, shift=UP*0.3),
            *[wave.animate.set_stroke(opacity=0.5) for wave in waves],
        )
        
        # Topic section (below title)
        topic_box = RoundedRectangle(
            width=9, height=1.1,
            corner_radius=0.15,
            fill_color="#1e293b",
            fill_opacity=0.95,
            stroke_color="#1e90ff",
            stroke_width=2.5
        ).shift(DOWN * 1.5)
        
        topic_text = Text(
            "Degradation In Wireless Channels",
            font_size=38,
            color=WHITE,
            weight=BOLD
        ).move_to(topic_box)
        
        self.play(
            FadeIn(topic_box, scale=0.95),
            Write(topic_text),
            run_time=1.2
        )
        
        # Pulse effect
        self.play(
            topic_box.animate.set_stroke(width=4),
            topic_text.animate.scale(1.05),
            run_time=0.4,
            rate_func=there_and_back
        )
        
        # Professor section (bottom right, compact)
        prof_container = RoundedRectangle(
            width=4.5, height=1.5,
            corner_radius=0.12,
            fill_color="#1e293b",
            fill_opacity=0.95,
            stroke_color="#334155",
            stroke_width=2
        ).to_corner(DR, buff=0.6)
        
        # Try to load image, fallback to icon
        try:
            prof_image = ImageMobject("rohit.jpeg")
            prof_image.height = 1.2
            prof_image.next_to(prof_container.get_left(), RIGHT, buff=0.3)
            has_image = True
        except:
            prof_icon = Circle(radius=0.5, color="#60a5fa", fill_opacity=0.3, stroke_width=2)
            prof_icon.next_to(prof_container.get_left(), RIGHT, buff=0.3)
            prof_image = prof_icon
            has_image = False
        
        prof_text = VGroup(
            Text("Dr. Rohit Singh", font_size=20, color=WHITE, weight=BOLD),
            Text("N.I.T Jalandhar", font_size=16, color="#94a3b8", slant=ITALIC)
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        prof_text.next_to(prof_image, RIGHT, buff=0.4)
        
        prof_group = Group(prof_container, prof_image, prof_text)
        
        self.play(
            FadeIn(prof_group, shift=LEFT*0.4),
            run_time=1
        )
        
        # Final wave animation
        self.play(
            *[wave.animate.shift(RIGHT * 0.2).set_stroke(opacity=0.6) for wave in waves],
            run_time=1,
            rate_func=there_and_back
        )
        
        self.wait(1.5)
        
        # Clean fade out
        self.play(
            *[FadeOut(mob, shift=DOWN*0.4) for mob in [module_badge, module_text, title_group, topic_box, topic_text]],
            *[FadeOut(eq, shift=UP*0.3, scale=0.8) for eq in equations],
            FadeOut(corner_tl, scale=0.7),
            FadeOut(corner_tr, scale=0.7),
            FadeOut(prof_group, shift=RIGHT*0.3),
            *[FadeOut(wave, shift=UP*0.2) for wave in waves],
            run_time=1.2
        )


class WirelessOutro(Scene):
    def construct(self):
        # Professional dark background
        self.camera.background_color = "#0a0e27"
        
        # Subtle grid
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": "#1e3a8a",
                "stroke_width": 0.5,
                "stroke_opacity": 0.12
            },
            axis_config={"stroke_opacity": 0}
        )
        self.add(grid)
        
        # Animated signal waves
        def create_wave(amplitude, frequency, phase, color, opacity):
            wave = FunctionGraph(
                lambda x: amplitude * np.sin(frequency * x + phase),
                x_range=[-7, 7, 0.01],
                color=color,
                stroke_width=2,
                stroke_opacity=opacity
            )
            return wave
        
        waves = VGroup()
        colors = ["#1e90ff", "#4169e1", "#6495ed"]
        for i in range(3):
            wave = create_wave(
                amplitude=0.35 + i*0.15,
                frequency=0.9 + i*0.25,
                phase=i*PI/3,
                color=colors[i],
                opacity=0.25 + i*0.1
            )
            wave.shift(DOWN * (0.5 + i*0.4))
            waves.add(wave)
        
        self.play(
            LaggedStart(*[Create(wave) for wave in waves], lag_ratio=0.2),
            run_time=1.5
        )
        
        # Corner decorations
        corners = VGroup()
        for direction in [UL, UR]:
            corner = VGroup(
                Line(ORIGIN, RIGHT * 1 if direction == UL else LEFT * 1, stroke_width=2.5, color="#1e90ff"),
                Line(ORIGIN, DOWN * 1, stroke_width=2.5, color="#1e90ff")
            ).move_to(direction * 6 + UP * 3)
            corners.add(corner)
        
        self.play(
            LaggedStart(*[Create(c) for c in corners], lag_ratio=0.15),
            run_time=0.8
        )
        
        # Key equations (top area only)
        equations = VGroup(
            MathTex(r"c = \lambda f", font_size=32, color="#60a5fa"),
            MathTex(r"\beta = \frac{2\pi}{\lambda}", font_size=32, color="#60a5fa"),
            MathTex(r"Z_0 = \sqrt{\frac{\mu}{\epsilon}}", font_size=30, color="#60a5fa")
        )
        
        equations[0].to_corner(UL, buff=0.8)
        equations[1].to_corner(UR, buff=0.8)
        equations[2].move_to(UP * 2.5)
        
        self.play(
            LaggedStart(*[FadeIn(eq, scale=0.8) for eq in equations], lag_ratio=0.15),
            run_time=1.2
        )
        
        # Main thank you section (centered)
        thanks_box = RoundedRectangle(
            width=9, height=1.8,
            corner_radius=0.2,
            fill_color="#1e293b",
            fill_opacity=0.95,
            stroke_color="#1e90ff",
            stroke_width=3
        ).shift(UP * 1.2)
        
        thanks_text = Text(
            "Thank You for Watching",
            font_size=56,
            color=WHITE,
            weight=BOLD,
            gradient=(WHITE, "#60a5fa")
        ).move_to(thanks_box)
        
        self.play(
            FadeIn(thanks_box, scale=0.95),
            Write(thanks_text, run_time=1.5),
            *[wave.animate.set_stroke(opacity=0.4) for wave in waves],
        )
        
        # Pulse effect
        self.play(
            thanks_box.animate.set_stroke(width=4),
            thanks_text.animate.scale(1.06),
            run_time=0.5,
            rate_func=there_and_back
        )
        
        # Call to action (below thank you)
        cta_box = RoundedRectangle(
            width=7, height=1.2,
            corner_radius=0.15,
            fill_color="#1e293b",
            fill_opacity=0.9,
            stroke_color="#334155",
            stroke_width=2
        ).shift(DOWN * 0.8)
        
        cta_text = VGroup(
            Text("Subscribe for more", font_size=24, color="#94a3b8"),
            Text("Wireless Concepts", font_size=34, color="#60a5fa", weight=BOLD)
        ).arrange(DOWN, buff=0.2).move_to(cta_box)
        
        self.play(
            FadeIn(cta_box, scale=0.95),
            Write(cta_text),
            run_time=1.2
        )
        
        # Footer info (bottom, well-spaced)
        editor_box = RoundedRectangle(
            width=4, height=0.7,
            corner_radius=0.1,
            fill_color="#1e293b",
            fill_opacity=0.9,
            stroke_color="#334155",
            stroke_width=1.5
        ).to_corner(DL, buff=0.5)
        
        editor_text = Text(
            "Editor: Shikhar Shrivastav",
            font_size=16,
            color="#94a3b8"
        ).move_to(editor_box)
        
        brand_box = RoundedRectangle(
            width=4, height=0.7,
            corner_radius=0.1,
            fill_color="#1e293b",
            fill_opacity=0.9,
            stroke_color="#334155",
            stroke_width=1.5
        ).to_corner(DR, buff=0.5)
        
        brand_text = Text(
            "WIRELESS CONCEPTS",
            font_size=16,
            color="#60a5fa",
            weight=BOLD
        ).move_to(brand_box)
        
        self.play(
            FadeIn(VGroup(editor_box, editor_text), shift=RIGHT*0.3),
            FadeIn(VGroup(brand_box, brand_text), shift=LEFT*0.3),
            run_time=1
        )
        
        # Final wave animation
        self.play(
            *[wave.animate.shift(RIGHT * 0.3).set_stroke(opacity=0.5) for wave in waves],
            run_time=1.2,
            rate_func=there_and_back
        )
        
        self.wait(2)
        
        # Smooth fade out
        self.play(
            *[FadeOut(mob) for mob in [
                thanks_box, thanks_text, cta_box, cta_text,
                editor_box, editor_text, brand_box, brand_text
            ]],
            *[FadeOut(eq, scale=0.8) for eq in equations],
            *[FadeOut(c, scale=0.7) for c in corners],
            *[FadeOut(wave) for wave in waves],
            FadeOut(grid),
            run_time=1.5
        )