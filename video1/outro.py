from manim import *

class OutroAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#0a0e27"
        
        # Instructor info at top
        instructor_title = Text("Instructor", font_size=36, weight=BOLD, color=TEAL)
        instructor_title.to_edge(UP, buff=0.8)
        
        instructor_name = Text("Rohit Singh", font_size=42, weight=BOLD)
        instructor_name.next_to(instructor_title, DOWN, buff=0.3)
        
        instructor_dept = Text("Department of ECE", font_size=32, color=GRAY)
        instructor_dept.next_to(instructor_name, DOWN, buff=0.2)
        
        # Team members - sliding credits style
        team_title = Text("Team Members", font_size=40, weight=BOLD, color=BLUE)
        team_title.shift(UP*0.5)
        
        # Customize team member names here
        team_members = [
            "Team Member 1 - Role/Contribution",
            "Team Member 2 - Role/Contribution", 
            "Team Member 3 - Role/Contribution",
            "Team Member 4 - Role/Contribution",
            "Team Member 5 - Role/Contribution",
        ]
        
        members_group = VGroup()
        for i, member in enumerate(team_members):
            member_text = Text(member, font_size=32)
            member_text.shift(DOWN * (i * 0.7 + 1.5))
            members_group.add(member_text)
        
        # Start positions (off-screen bottom)
        for mob in members_group:
            mob.shift(DOWN * 10)
        
        # Decorative lines
        line_top = Line(LEFT*7, RIGHT*7, color=TEAL, stroke_width=2)
        line_top.next_to(instructor_dept, DOWN, buff=0.4)
        
        # Animations
        self.play(
            Write(instructor_title, run_time=0.8),
            Create(line_top, run_time=0.6)
        )
        self.play(
            FadeIn(instructor_name, shift=DOWN*0.3),
            run_time=0.8
        )
        self.play(FadeIn(instructor_dept, run_time=0.6))
        
        self.wait(0.5)
        
        self.play(FadeIn(team_title, shift=UP*0.3, run_time=1))
        
        # Sliding credits animation - each member slides up
        for member_text in members_group:
            self.play(
                member_text.animate.shift(UP*10),
                run_time=1.5,
                rate_func=linear
            )
            self.wait(0.2)
        
        self.wait(1)
        
        # Final fade out
        self.play(*[FadeOut(mob) for mob in [
            instructor_title, instructor_name, instructor_dept, 
            line_top, team_title
        ]], run_time=1)