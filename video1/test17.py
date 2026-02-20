from manim import *
import numpy as np

class DecisionTreeFlowchart(Scene):
    """Animation 20: Decision tree flowchart"""
    
    def construct(self):
        # Title
        title = Text("Which Model Should You Use?", font_size=42, weight=BOLD)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.6).to_edge(UP, buff=0.2))
        
        # ========== CREATE FLOWCHART ==========
        # Start node
        start_box = self.create_box("Need to predict\nsignal strength?", YELLOW, 2.5, 0.8)
        start_box.shift(UP * 2.5)
        
        self.play(FadeIn(start_box, scale=1.2))
        self.wait(0.5)
        
        # First branch arrow
        arrow_down = Arrow(start_box.get_bottom(), start_box.get_bottom() + DOWN * 0.8, buff=0)
        self.play(GrowArrow(arrow_down))
        
        # First decision
        decision1 = self.create_diamond("Quick estimate?\nLOS?\nFree space?", BLUE, 2.2, 1.2)
        decision1.next_to(arrow_down, DOWN, buff=0)
        
        self.play(FadeIn(decision1, shift=DOWN))
        self.wait(0.5)
        
        # YES branch to Friis
        yes_label1 = Text("YES", font_size=18, color=GREEN, weight=BOLD)
        arrow_yes1 = Arrow(decision1.get_left(), decision1.get_left() + LEFT * 2, buff=0.2, color=GREEN)
        yes_label1.next_to(arrow_yes1, UP, buff=0.05)
        
        friis_box = self.create_box("Use Friis\nEquation", GREEN, 2.0, 0.8)
        friis_box.next_to(arrow_yes1, LEFT, buff=0)
        
        # Add icon
        try:
            friis_icon = SVGMobject("tower.svg").scale(0.3)
        except:
            friis_icon = Triangle(color=BLUE, fill_opacity=1).scale(0.2)
        friis_icon.next_to(friis_box, DOWN, buff=0.2)
        
        self.play(
            GrowArrow(arrow_yes1),
            Write(yes_label1)
        )
        self.play(FadeIn(friis_box, shift=LEFT))
        self.play(FadeIn(friis_icon, scale=1.2))
        self.wait(1)
        
        # NO branch - continue down
        no_label1 = Text("NO", font_size=18, color=RED, weight=BOLD)
        arrow_no1 = Arrow(decision1.get_bottom(), decision1.get_bottom() + DOWN * 0.8, buff=0, color=RED)
        no_label1.next_to(arrow_no1, RIGHT, buff=0.05)
        
        self.play(
            GrowArrow(arrow_no1),
            Write(no_label1)
        )
        
        # Second decision
        decision2 = self.create_diamond("Realistic?\nObstacles?\nStatistical?", RED, 2.2, 1.2)
        decision2.next_to(arrow_no1, DOWN, buff=0)
        
        self.play(FadeIn(decision2, shift=DOWN))
        self.wait(0.5)
        
        # YES branch to Shadowing
        yes_label2 = Text("YES", font_size=18, color=GREEN, weight=BOLD)
        arrow_yes2 = Arrow(decision2.get_right(), decision2.get_right() + RIGHT * 2, buff=0.2, color=GREEN)
        yes_label2.next_to(arrow_yes2, UP, buff=0.05)
        
        shadowing_box = self.create_box("Use Shadowing\nModel", GREEN, 2.0, 0.8)
        shadowing_box.next_to(arrow_yes2, RIGHT, buff=0)
        
        # Add icons
        obstacles_group = VGroup()
        try:
            building = SVGMobject("building.svg").scale(0.15)
            tree = SVGMobject("tree.svg").scale(0.15)
            person = SVGMobject("person.svg").scale(0.12)
            obstacles_group = VGroup(building, tree, person).arrange(RIGHT, buff=0.1)
        except:
            obstacles_group = VGroup(
                Rectangle(height=0.2, width=0.08, color=GRAY, fill_opacity=0.7),
                Circle(radius=0.08, color=GREEN, fill_opacity=0.7),
                Rectangle(height=0.15, width=0.05, color=BLUE, fill_opacity=0.7)
            ).arrange(RIGHT, buff=0.1)
        
        obstacles_group.next_to(shadowing_box, DOWN, buff=0.2)
        
        self.play(
            GrowArrow(arrow_yes2),
            Write(yes_label2)
        )
        self.play(FadeIn(shadowing_box, shift=RIGHT))
        self.play(FadeIn(obstacles_group, lag_ratio=0.2))
        self.wait(1)
        
        # Highlight the complete paths
        # Highlight Friis path
        friis_path = VGroup(start_box, arrow_down, decision1, arrow_yes1, friis_box)
        self.play(
            friis_path.animate.set_color(BLUE),
            friis_icon.animate.scale(1.2),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            friis_path.animate.set_color(WHITE),
            friis_icon.animate.scale(1/1.2)
        )
        
        # Highlight Shadowing path
        shadowing_path = VGroup(start_box, arrow_down, decision1, arrow_no1, decision2, arrow_yes2, shadowing_box)
        self.play(
            shadowing_path.animate.set_color(RED),
            obstacles_group.animate.scale(1.2),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            shadowing_path.animate.set_color(WHITE),
            obstacles_group.animate.scale(1/1.2)
        )
        
        self.wait(2)
    
    def create_box(self, text, color, width, height):
        """Create a rectangular box with text"""
        box = Rectangle(width=width, height=height, color=color, stroke_width=3, fill_opacity=0.1)
        label = Text(text, font_size=16, color=WHITE).move_to(box.get_center())
        return VGroup(box, label)
    
    def create_diamond(self, text, color, width, height):
        """Create a diamond-shaped decision node"""
        diamond = Polygon(
            UP * height/2,
            RIGHT * width/2,
            DOWN * height/2,
            LEFT * width/2,
            color=color,
            stroke_width=3,
            fill_opacity=0.1
        )
        label = Text(text, font_size=14, color=WHITE).move_to(diamond.get_center())
        return VGroup(diamond, label)


