from manim import *

class IconBasedCategorization(Scene):
    """Animation 4: Icon-based categorization - One Tower, One Receiver"""
    
    def construct(self):

        title2 = Text("Wireless Impairment Categories", font_size=48, weight=BOLD)
        subtitle = Text("Path Loss, Shadowing & MultiPath", font_size=32)
        subtitle.next_to(title2, DOWN)
        
        self.play(Write(title2))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title2), FadeOut(subtitle))


        title = Text("Types Of Wireless Impairments", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        
        self.wait(1)

        # Title
        # title = Tex("Wireless Impairment Categories", font_size=42)
        # self.play(Write(title))
        # self.wait(1)
        # self.play(title.animate.to_edge(UP, buff=0.3))
        
        # ===== SETUP: ONE TOWER AND ONE RECEIVER =====
        # Central Tower
        tower = SVGMobject("tower.svg").scale(0.6)
        # tower.set_color(BLUE)
        tower.move_to(LEFT * 5 + DOWN * 0.5)
        
        # Single Receiver
        receiver = SVGMobject("mobile.svg").scale(0.5)
        # receiver.set_color(BLUE)
        receiver.move_to(RIGHT * 5 + DOWN * 0.5)
        
        # Show tower and receiver
        self.play(FadeIn(tower, scale=1.5))
        self.wait(0.5)
        self.play(FadeIn(receiver, scale=1.5))
        self.wait(1)
        
        # ===== EFFECT 1: PATH LOSS =====
        path_loss_title = Tex("1. Path Loss", font_size=36, color=WHITE)
        path_loss_title.to_edge(LEFT, buff=0.5).shift(UP * 2.5)
        
        self.play(Write(path_loss_title))
        
        # Highlight receiver
        # rx_highlight = Circle(radius=0.6, color=YELLOW, stroke_width=4)
        # rx_highlight.move_to(receiver)
        # self.play(Create(rx_highlight))
        
        # Change receiver color to yellow
        # self.play(receiver.animate.set_color(YELLOW))
        
        # Create thinning arrow for path loss
        num_segments = 8
        arrow_segments = VGroup()
        start_point = tower.get_right()+0.25
        end_point = receiver.get_left()
        
        for i in range(num_segments):
            t1 = i / num_segments
            t2 = (i + 1) / num_segments
            
            p1 = start_point + t1 * (end_point - start_point)
            p2 = start_point + t2 * (end_point - start_point)
            
            # Width and opacity decrease with distance
            width1 = 0.4 * (1 - t1 * 0.75)
            width2 = 0.4 * (1 - t2 * 0.75)
            opacity = 0.9 * (1 - t1 * 0.5)
            
            # Calculate perpendicular direction
            direction = np.array([-(p2[1] - p1[1]), p2[0] - p1[0], 0])
            direction = direction / np.linalg.norm(direction) if np.linalg.norm(direction) > 0 else np.array([0, 1, 0])
            
            segment = Polygon(
                p1 + direction * width1,
                p2 + direction * width2,
                p2 - direction * width2,
                p1 - direction * width1,
                fill_color=YELLOW,
                fill_opacity=opacity,
                stroke_color=YELLOW,
                stroke_width=1
            )
            arrow_segments.add(segment)
        
        # Arrowhead
        # arrowhead = Triangle(fill_color=YELLOW, fill_opacity=0.8, stroke_color=YELLOW)
        # arrow_direction = end_point - start_point
        # angle = np.arctan2(arrow_direction[1], arrow_direction[0])
        # arrowhead.scale(0.25).rotate(angle).move_to(end_point - arrow_direction * 0.15 / np.linalg.norm(arrow_direction))
        
        # Animate path loss arrow
        self.play(
            LaggedStart(*[FadeIn(seg, shift=RIGHT * 0.2) for seg in arrow_segments], lag_ratio=0.08),
            run_time=2
        )
        # self.play(FadeIn(arrowhead))
        
        # Add distance markers
        distance_labels = VGroup()
        for i, t in enumerate([0.3, 0.6, 0.9]):
            pos = start_point + t * (end_point - start_point)
            power_loss = int(t * 100)
            label = Tex(f"-{power_loss}dB", font_size=18, color=RED)
            label.next_to(pos, DOWN, buff=0.2)
            label.shift(0.2)
            distance_labels.add(label)
        
        self.play(FadeIn(distance_labels, lag_ratio=0.2))
        
        # Description
        path_loss_desc = Tex("Signal weakens\\\\with distance", font_size=22, color=YELLOW)
        path_loss_desc.next_to(path_loss_title, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(path_loss_desc))
        self.wait(10)
        
        # Fade out path loss elements
        self.play(
            FadeOut(arrow_segments),
            FadeOut(distance_labels),
            FadeOut(path_loss_title),
            FadeOut(path_loss_desc)
        )
        
        # ===== EFFECT 2: SHADOWING =====
        shadowing_title = Tex("2. Shadowing", font_size=36, color=WHITE)
        # path_loss_title.to_edge(LEFT, buff=0.5).shift()
        shadowing_title.to_edge(LEFT, buff=0.5).shift(UP * 2.5)
        
        self.play(Write(shadowing_title))
        
        # Highlight receiver
        # rx_highlight = Circle(radius=0.6, color=GRAY, stroke_width=4)
        # rx_highlight.move_to(receiver)
        # self.play(Create(rx_highlight))
        
        # Change receiver color to gray
        # self.play(receiver.animate.set_color(GRAY))
        
        # Building obstacle
        building = SVGMobject("building.svg").scale(0.7)
        # building.set_color(GRAY)
        building.move_to((tower.get_center() + receiver.get_center()) / 2)
        
        # Signal paths (before and after obstacle)
        signal_before = Line(
            tower.get_right(),
            building.get_left(),
            color=BLUE,
            stroke_width=5
        )
        
        signal_after = Line(
            building.get_right(),
            receiver.get_left(),
            color=RED,
            stroke_width=5,
            stroke_opacity=0.8
        )
        
        # Animate signal hitting building
        self.play(Create(signal_before), run_time=1)
        self.play(FadeIn(building, shift=DOWN * 0.3))
        
        # X mark on building
        x_mark = VGroup(
            Line(UP * 0.4 + LEFT * 0.4, DOWN * 0.4 + RIGHT * 0.4, color=RED, stroke_width=6),
            Line(UP * 0.4 + RIGHT * 0.4, DOWN * 0.4 + LEFT * 0.4, color=RED, stroke_width=6)
        ).move_to(building.get_center())
        
        self.play(Create(x_mark), run_time=0.5)
        self.play(Create(signal_after), run_time=1)
        
        # Blocking label
        blocked_label = Tex("BLOCKED", font_size=24, color=RED)
        blocked_label.next_to(building, UP, buff=0.3)
        self.play(Write(blocked_label))
        
        # Description
        shadowing_desc = Tex("Obstacles block\\\\signal path", font_size=22, color=YELLOW)
        shadowing_desc.next_to(shadowing_title, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(shadowing_desc))
        self.wait(10)
        
        # Fade out shadowing elements
        self.play(
            # FadeOut(rx_highlight),
            FadeOut(signal_before),
            FadeOut(signal_after),
            FadeOut(building),
            FadeOut(x_mark),
            FadeOut(blocked_label),
            FadeOut(shadowing_title),
            FadeOut(shadowing_desc)
        )
        
        # ===== EFFECT 3: MULTIPATH =====
        multipath_title = Tex("3. Multipath", font_size=36, color=WHITE)
        # shadowing_title.to_edge(LEFT, buff=0.5).shift(UP * 2.5)
        multipath_title.to_edge(LEFT, buff=0.5).shift(UP * 2.5)
        
        self.play(Write(multipath_title))
        
        # Highlight receiver
        # rx_highlight = Circle(radius=0.6, color=RED, stroke_width=4)
        # rx_highlight.move_to(receiver)
        # self.play(Create(rx_highlight))
        
        # Change receiver color to red
        # self.play(receiver.animate.set_color(RED))
        
        # Add obstacles for multipath reflections
        person = SVGMobject("person.svg").scale(0.5)
        # person.set_color(GRAY)
        person.move_to(RIGHT * 0 + DOWN * 1.7)
        
        tree = SVGMobject("tree.svg").scale(0.4)
        # tree.set_color(GRAY)
        tree.move_to(RIGHT * 2.5 + UP * 1)
        
        obstacles = VGroup(person, tree)
        
        # Direct path
        direct_path = Arrow(
            tower.get_right(),
            receiver.get_left(),
            color=WHITE,
            stroke_width=4,
            buff=0.1,
            max_tip_length_to_length_ratio=0.1
        )
        
        # Reflected path via person
        reflect_person = Arrow(
            tower.get_right(),
            person.get_top(),
            color=WHITE,
            stroke_width=3,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        reflect_person_to_rx = Arrow(
            person.get_top(),
            receiver.get_left(),
            color=WHITE,
            stroke_width=3,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        
        # Reflected path via tree
        reflect_tree = Arrow(
            tower.get_right(),
            tree.get_top(),
            color=WHITE,
            stroke_width=3,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        reflect_tree_to_rx = Arrow(
            tree.get_top(),
            receiver.get_left(),
            color=WHITE,
            stroke_width=3,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        
        # Reflection markers
        reflection_dots = VGroup(
            Dot(person.get_top(), color=WHITE, radius=0.1),
            Dot(tree.get_top(), color=WHITE, radius=0.1)
        )
        
        # Animate multipath
        self.play(GrowArrow(direct_path), run_time=1)
        
        self.play(FadeIn(person, shift=UP * 0.3))
        self.play(
            GrowArrow(reflect_person),
            FadeIn(reflection_dots[0])
        )
        self.play(GrowArrow(reflect_person_to_rx))
        
        self.play(FadeIn(tree, shift=UP * 0.3))
        self.play(
            GrowArrow(reflect_tree),
            FadeIn(reflection_dots[1])
        )
        self.play(GrowArrow(reflect_tree_to_rx))
        
        # Path labels
        # path_legend = VGroup(
        #     VGroup(
        #         Line(LEFT * 0.2, RIGHT * 0.2, color=GREEN, stroke_width=4),
        #         Tex("Direct", font_size=18, color=GREEN)
        #     ).arrange(RIGHT, buff=0.1),
        #     VGroup(
        #         Line(LEFT * 0.2, RIGHT * 0.2, color=ORANGE, stroke_width=3),
        #         Tex("Reflected", font_size=18, color=ORANGE)
        #     ).arrange(RIGHT, buff=0.1),
        #     VGroup(
        #         Line(LEFT * 0.2, RIGHT * 0.2, color=PURPLE, stroke_width=3),
        #         Tex("Scattered", font_size=18, color=PURPLE)
        #     ).arrange(RIGHT, buff=0.1)
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        
        # path_legend.to_corner(DR, buff=0.5)
        # legend_box = SurroundingRectangle(path_legend, color=WHITE, buff=0.2, corner_radius=0.1)
        
        # self.play(
        #     Create(legend_box),
        #     FadeIn(path_legend, shift=UP * 0.2)
        # )
        
        # Description
        multipath_desc = Tex("Multiple signal\\\\paths interfere", font_size=22, color=YELLOW)
        multipath_desc.next_to(multipath_title, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(multipath_desc))
        self.wait(2)
        
        # Fade out multipath labels
        self.play(
            # FadeOut(rx_highlight),
            FadeOut(multipath_title),
            FadeOut(multipath_desc)
        )
        
        # ===== FINAL SUMMARY =====
        # Change title
        # final_title = Tex("All Three Impairments Combined", font_size=38, color=WHITE)
        # final_title.to_edge(UP, buff=1)
        
        # self.play(
        #     FadeOut(title),
        #     Write(final_title)
        # )
        
        # # Reset receiver color to blue
        # self.play(receiver.animate.set_color(BLUE))
        
        # # Summary text
        summary = Tex(
            "Three Main Types of Wireless Impairments",
            font_size=28,
            color=WHITE
        ).to_edge(DOWN, buff=0.3)
        
        self.play(Write(summary))
        self.wait(8)