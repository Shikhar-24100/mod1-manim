from manim import *
import numpy as np

class IntroAnimation(Scene):
    def construct(self):
        # Animated gradient background
        self.camera.background_color = "#0a0e27"
        
        # Create animated waveforms in background
        def create_wave(amplitude, frequency, phase, color, opacity):
            wave = FunctionGraph(
                lambda x: amplitude * np.sin(frequency * x + phase),
                x_range=[-8, 8],
                color=color,
                stroke_width=2,
                stroke_opacity=opacity
            )
            return wave
        
        waves = VGroup(
            create_wave(0.5, 2, 0, "#4a9eff", 0.3),
            create_wave(0.6, 1.8, PI/3, "#00d4ff", 0.25),
            create_wave(0.4, 2.2, PI/2, "#7b2ff7", 0.2),
        )
        waves.shift(UP * 1.5)
        
        # Add waves to scene
        self.add(waves)
        
        # Radial glow effect for opening
        glow_circle = Circle(radius=3, fill_opacity=0.1, fill_color="#4a9eff", stroke_width=0)
        glow_circle.set_fill(opacity=0)
        
        self.play(
            glow_circle.animate.set_fill(opacity=0.15).scale(1.5),
            run_time=2,
            rate_func=smooth
        )
        
        # Part 1: "Interactive Learning Initiative"
        initiative_text = Text(
            "Interactive Learning Initiative",
            font="Georgia",
            font_size=52,
            weight=BOLD,
            color=WHITE,
            slant=ITALIC
        ).set_stroke(color="#4a9eff", width=0.5, opacity=0.8)
        
        # Cinematic fade-in with scale
        initiative_text.scale(0.7)
        self.play(
            FadeIn(initiative_text, scale=1.3),
            glow_circle.animate.set_opacity(0.3),
            run_time=2.5,
            rate_func=smooth
        )
        
        # Subtle glow pulse
        self.play(
            initiative_text.animate.set_stroke(width=1.5, opacity=1),
            rate_func=there_and_back,
            run_time=1.5
        )
        
        self.wait(1)
        
        # Fade out initiative text
        self.play(
            FadeOut(initiative_text, scale=0.8),
            FadeOut(glow_circle),
            run_time=1.5
        )
        
        # Part 2: Series Title with light streaks
        series_title_1 = Text(
            "Wireless Concepts:",
            font="Georgia",
            font_size=62,
            weight=BOLD,
            color=WHITE
        )
        
        series_title_2 = Text(
            "5G and Beyond",
            font="Georgia",
            font_size=68,
            weight=BOLD,
            gradient=(BLUE, "#00d4ff", "#7b2ff7")
        ).set_stroke(color="#00d4ff", width=1.2, opacity=0.8)
        
        series_title_1.shift(UP * 0.8)
        series_title_2.next_to(series_title_1, DOWN, buff=0.4)
        
        # Light streak effects
        streaks = VGroup()
        for i in range(12):
            streak = Line(
                start=LEFT * 10 + UP * np.random.uniform(-3, 3),
                end=LEFT * 10 + UP * np.random.uniform(-3, 3) + RIGHT * np.random.uniform(2, 4),
                stroke_width=1,
                color="#00d4ff",
                stroke_opacity=0.6
            )
            streaks.add(streak)
        
        # Animate streaks passing
        self.play(
            LaggedStart(
                *[streak.animate.shift(RIGHT * 20) for streak in streaks],
                lag_ratio=0.1,
                run_time=2
            )
        )
        
        # Title appears with light trails
        self.play(
            Write(series_title_1, run_time=2, rate_func=smooth),
        )
        
        # Glowing emphasis on "5G and Beyond"
        glow_bg = Rectangle(
            height=1.2,
            width=series_title_2.width + 0.5,
            fill_color="#4a9eff",
            fill_opacity=0.1,
            stroke_width=0
        ).move_to(series_title_2)
        
        self.play(
            FadeIn(glow_bg),
            Write(series_title_2, run_time=2.5, rate_func=smooth),
        )
        
        # Shimmer effect
        self.play(
            series_title_2.animate.set_stroke(width=2, opacity=1),
            glow_bg.animate.set_fill(opacity=0.2),
            rate_func=there_and_back,
            run_time=1.5
        )
        
        self.wait(1.5)
        
        # Transition out
        self.play(
            FadeOut(series_title_1, shift=UP),
            FadeOut(series_title_2, shift=UP),
            FadeOut(glow_bg),
            run_time=1.5
        )


class ModuleIntroAnimation(Scene):
    def construct(self):
        # Customize these variables
        module_number = "1"
        module_topic = "Introduction to 5G Architecture"
        prof_name = "Prof. Rohit Singh"
        dept = "Department of ECE"
        institute = "NIT Jalandhar"
        
        self.camera.background_color = "#0a0e27"
        
        # Add subtle animated background pulses
        pulse_circles = VGroup()
        for i in range(3):
            circle = Circle(
                radius=2 + i,
                stroke_color="#4a9eff",
                stroke_width=1,
                stroke_opacity=0.15 - i * 0.04
            )
            pulse_circles.add(circle)
        
        self.add(pulse_circles)
        
        # Module title section
        module_label = Text(
            f"Module {module_number}",
            font="Open Sans",
            font_size=44,
            weight=BOLD,
            color="#00d4ff"
        ).set_stroke(color="#4a9eff", width=0.8)
        
        topic_text = Text(
            module_topic,
            font="Georgia",
            font_size=38,
            weight=NORMAL,
            color=WHITE,
            slant=ITALIC
        )
        
        module_group = VGroup(module_label, topic_text)
        module_group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        module_group.to_edge(UP, buff=1.5).shift(RIGHT * 0.5)
        
        # Glowing line separator
        separator_line = Line(
            LEFT * 6, RIGHT * 6,
            stroke_width=2,
            color="#4a9eff",
            stroke_opacity=0.6
        ).next_to(module_group, DOWN, buff=0.6)
        
        # Professor info section
        prof_circle = Circle(
            radius=1.2,
            fill_color="#1a1a3e",
            fill_opacity=0.8,
            stroke_color="#00d4ff",
            stroke_width=3
        )
        
        photo_label = Text(
            "PHOTO",
            font="Open Sans",
            font_size=18,
            color="#8a8a8a"
        ).move_to(prof_circle)
        
        photo_group = VGroup(prof_circle, photo_label)
        photo_group.shift(DOWN * 1.2 + LEFT * 3.5)
        
        # Replace with: ImageMobject("prof_photo.jpg").scale_to_fit_height(2.4).move_to(prof_circle)
        
        by_text = Text("By:", font="Open Sans", font_size=22, color="#8a8a8a")
        prof_name_text = Text(prof_name, font="Georgia", font_size=36, weight=BOLD, color=WHITE)
        dept_text = Text(dept, font="Open Sans", font_size=26, color="#00d4ff")
        institute_text = Text(institute, font="Open Sans", font_size=26, color="#8a8a8a")
        
        info_group = VGroup(by_text, prof_name_text, dept_text, institute_text)
        info_group.arrange(DOWN, center=False, aligned_edge=LEFT, buff=0.25)
        info_group.next_to(photo_group, RIGHT, buff=1.2)
        
        # Animations with opposite sliding directions
        # Module info slides from right
        self.play(
            module_group.animate.shift(LEFT * 10),
            run_time=1
        )
        self.play(
            module_group.animate.shift(RIGHT * 10),
            run_time=1.5,
            rate_func=smooth
        )
        
        # Glowing separator appears
        self.play(
            Create(separator_line, run_time=1),
            separator_line.animate.set_stroke(opacity=1),
            rate_func=smooth
        )
        
        self.wait(0.3)
        
        # Professor info slides from left
        instructor_section = VGroup(photo_group, info_group)
        self.play(
            instructor_section.animate.shift(RIGHT * 10),
            run_time=1
        )
        self.play(
            instructor_section.animate.shift(LEFT * 10),
            run_time=1.5,
            rate_func=smooth
        )
        
        # Glow pulse on photo circle
        self.play(
            prof_circle.animate.set_stroke(width=5, opacity=1),
            rate_func=there_and_back,
            run_time=1
        )
        
        self.wait(2.5)
        
        # Elegant fade out
        self.play(
            *[FadeOut(mob, scale=0.95) for mob in self.mobjects],
            run_time=1.5
        )


class OutroAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#0a0e27"
        
        # Subtle grid/wave background
        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": "#1a1a3e",
                "stroke_width": 0.8,
                "stroke_opacity": 0.2,
            }
        )
        self.add(grid)
        
        # Drifting particles for depth
        particles = VGroup()
        for _ in range(25):
            dot = Dot(
                point=[np.random.uniform(-7, 7), np.random.uniform(-4, 4), 0],
                radius=0.03,
                color="#4a9eff",
                fill_opacity=np.random.uniform(0.2, 0.5)
            )
            particles.add(dot)
        
        self.add(particles)
        
        # Instructor section (stays fixed)
        instructor_label = Text(
            "Instructor",
            font="Open Sans",
            font_size=28,
            weight=BOLD,
            color="#8a8a8a"
        )
        
        instructor_name = Text(
            "Prof. Rohit Singh",
            font="Georgia",
            font_size=44,
            weight=BOLD,
            color=WHITE
        ).set_stroke(color="#4a9eff", width=0.5)
        
        instructor_dept = Text(
            "Department of ECE, NIT Jalandhar",
            font="Open Sans",
            font_size=28,
            color="#00d4ff"
        )
        
        instructor_section = VGroup(instructor_label, instructor_name, instructor_dept)
        instructor_section.arrange(DOWN, buff=0.35)
        instructor_section.to_edge(UP, buff=1.2)
        
        # Divider with glow
        divider = Line(
            LEFT * 6.5, RIGHT * 6.5,
            stroke_width=2,
            color="#4a9eff",
            stroke_opacity=0.5
        ).next_to(instructor_section, DOWN, buff=0.7)
        
        # Fade in instructor section
        self.play(
            FadeIn(instructor_label, shift=DOWN * 0.3),
            run_time=1
        )
        self.play(
            Write(instructor_name, run_time=1.2),
        )
        self.play(
            FadeIn(instructor_dept, shift=DOWN * 0.3),
            run_time=1
        )
        self.play(
            Create(divider),
            divider.animate.set_stroke(opacity=0.8),
            run_time=1
        )
        
        self.wait(0.5)
        
        # Team section - scrolling credits
        team_label = Text(
            "Team Members",
            font="Open Sans",
            font_size=32,
            weight=BOLD,
            color="#8a8a8a"
        )
        
        # Customize team members here
        team_members = [
            "Animation Lead - Member Name 1",
            "Content Developer - Member Name 2",
            "Technical Reviewer - Member Name 3",
            "Video Producer - Member Name 4",
            "Research Analyst - Member Name 5",
        ]
        
        members_group = VGroup()
        for member in team_members:
            member_text = Text(
                member,
                font="Open Sans",
                font_size=28,
                color=WHITE
            )
            members_group.add(member_text)
        
        members_group.arrange(DOWN, center=True, buff=0.55)
        
        credits_group = VGroup(team_label, members_group)
        credits_group.arrange(DOWN, buff=0.8)
        
        # Start off-screen
        credits_group.shift(DOWN * 12)
        
        # Smooth scroll upward
        self.play(
            credits_group.animate.shift(UP * 20),
            run_time=len(team_members) * 2 + 3,
            rate_func=linear
        )
        
        self.wait(0.5)
        
        # Final closing frame
        final_text = Text(
            "Interactive Learning Initiative",
            font="Georgia",
            font_size=48,
            weight=BOLD,
            color=WHITE,
            slant=ITALIC
        ).set_stroke(color="#4a9eff", width=0.8)
        
        radial_glow = Circle(
            radius=4,
            fill_color="#4a9eff",
            fill_opacity=0.15,
            stroke_width=0
        ).move_to(final_text)
        
        self.play(
            FadeOut(instructor_section),
            FadeOut(divider),
            run_time=1
        )
        
        self.play(
            FadeIn(radial_glow, scale=0.5),
            FadeIn(final_text, scale=1.2),
            run_time=2,
            rate_func=smooth
        )
        
        # Radial pulse
        self.play(
            radial_glow.animate.scale(1.3).set_opacity(0.25),
            rate_func=there_and_back,
            run_time=2
        )
        
        self.wait(1)
        
        # Fade to black
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2.5,
            rate_func=smooth
        )


# RENDERING COMMANDS:
# manim -pqh filename.py IntroAnimation
# manim -pqh filename.py ModuleIntroAnimation
# manim -pqh filename.py OutroAnimation
#
# For 4K quality: use -pqk instead of -pqh
# For 60fps: add --frame_rate 60