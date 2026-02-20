from manim import *

import numpy as np



class HexagonCellExplanation(Scene):

    def construct(self):

        # Title

        title = Text("Why Hexagonal Cell Shape?", font_size=40)

        title.to_edge(UP)

        self.play(Write(title))

        self.wait()

        

        # Part 1: Start with circle and radiation pattern

        explanation1 = Text("Antenna radiation pattern is circular", font_size=32)

        explanation1.next_to(title, DOWN, buff=0.5)

        self.play(Write(explanation1))

        self.wait()

        

        # Create a circle representing coverage

        circle = Circle(radius=1.5, color=BLUE)

        circle.move_to(ORIGIN)

        

        # Add antenna in center

        antenna = Dot(circle.get_center(), color=RED, radius=0.08)

        antenna_label = Text("Antenna", font_size=20).next_to(antenna, DOWN, buff=0.2)

        

        self.play(Create(circle), FadeIn(antenna), Write(antenna_label))

        self.wait()

        

        # Show radiation pattern with dashed circles

        radiation_rings = VGroup(*[

            DashedVMobject(Circle(radius=1.5 * (i/3), color=BLUE).move_to(circle.get_center()), num_dashes=20)

            for i in range(1, 4)

        ])

        self.play(Create(radiation_rings), run_time=1.5)

        self.wait(2)

        

        # Part 2: Show the problem - gaps between circles

        self.play(FadeOut(radiation_rings), FadeOut(antenna), FadeOut(antenna_label))

        self.wait(0.5)

        

        explanation2 = Text("But circles leave gaps when tiled", font_size=32)

        explanation2.next_to(title, DOWN, buff=0.5)

        self.play(FadeOut(explanation1), Write(explanation2))

        self.wait()

        

        # Create multiple circles to show gaps

        circles_group = VGroup()

        positions = [

            LEFT * 1.21,

            DOWN * 2.22,

            RIGHT * 1.21

        ]

        

        for pos in positions:

            c = Circle(radius=1.2, color=BLUE, fill_opacity=0.2)

            c.move_to(pos)

            circles_group.add(c)

        

        self.play(

            Transform(circle, circles_group[1]),

            FadeIn(circles_group[0]),

            FadeIn(circles_group[2])

        )

        self.wait()

        

        # Highlight gaps

        

        gap_label = Text("Gaps!", font_size=28, color=RED)
        gap_label.shift(DOWN*0.92)


        

        self.play(Write(gap_label))

        self.wait(2)

        

        # Clear for polygon comparison

        self.play(

            FadeOut(circles_group),

            FadeOut(circle),


            FadeOut(gap_label),

            FadeOut(explanation2)

        )

        self.wait(0.5)

        

        # Part 3: Introduce the tiling constraint BEFORE showing polygons

        explanation3 = Text("Only 3 regular polygons can tile the plane:", font_size=32)

        explanation3.next_to(title, DOWN, buff=0.5)

        self.play(Write(explanation3))

        self.wait()

        

        tiling_info = Text("Triangle • Square • Hexagon", font_size=28, color=YELLOW, weight=BOLD)

        tiling_info.next_to(explanation3, DOWN, buff=0.3)

        self.play(Write(tiling_info))

        self.wait(2)

        

        # Clear and prepare for polygon comparison

        self.play(FadeOut(explanation3), FadeOut(tiling_info))

        self.wait(0.5)

        

        explanation4 = Text("Which polygon best approximates a circle?", font_size=32)

        explanation4.next_to(title, DOWN, buff=0.5)

        self.play(Write(explanation4))

        self.wait()

        

        # Create reference circle for comparison

        ref_circle = Circle(radius=1.5, color=WHITE, stroke_width=2)

        ref_circle.move_to(ORIGIN)

        

        self.play(Create(ref_circle))

        

        # Triangle (inscribed in circle) - vertices touch the circle

        triangle = RegularPolygon(n=3, radius=1.45, color=YELLOW, fill_opacity=0.3)

        triangle.move_to(ORIGIN)
        triangle.shift(UP * 0.43) # Shift up slightly to better fit inside circle and look more like a "slice" shape

        

        triangle_label = VGroup(

            Text("Triangle", font_size=24),

            Text("~41% area", font_size=20, color=YELLOW)

        ).arrange(DOWN, buff=0.1)

        triangle_label.next_to(ref_circle, DOWN, buff=0.5)

        

        self.play(Create(triangle), Write(triangle_label))

        self.wait(2)

        

        # Fade out and prepare for square

        self.play(

            FadeOut(triangle),

            FadeOut(triangle_label)

        )

        self.wait(0.5)

        

        # Square - inscribed so vertices touch circle

        square = RegularPolygon(n=4, radius=1.5, color=GREEN, fill_opacity=0.3)

        square.move_to(ORIGIN)

        

        square_label = VGroup(

            Text("Square", font_size=24),

            Text("~64% area", font_size=20, color=GREEN)

        ).arrange(DOWN, buff=0.1)

        square_label.next_to(ref_circle, DOWN, buff=0.5)

        

        self.play(Create(square), Write(square_label))

        self.wait(2)

        

        # Fade out and prepare for hexagon

        self.play(

            FadeOut(square),

            FadeOut(square_label)

        )

        self.wait(0.5)

        

        # Hexagon - the winner! - inscribed

        hexagon = RegularPolygon(n=6, radius=1.5, color=BLUE, fill_opacity=0.3)

        hexagon.move_to(ORIGIN)

        

        hexagon_label = VGroup(

            Text("Hexagon", font_size=24, weight=BOLD),

            Text("~83% area", font_size=20, color=BLUE, weight=BOLD)

        ).arrange(DOWN, buff=0.1)

        hexagon_label.next_to(ref_circle, DOWN, buff=0.5)

        

        self.play(Create(hexagon), Write(hexagon_label))

        self.wait(2)

        

        # Highlight hexagon as the best

        highlight_box = SurroundingRectangle(

            VGroup(ref_circle, hexagon, hexagon_label),

            color=GOLD,

            buff=0.2,

            stroke_width=4

        )

        self.play(Create(highlight_box))

        self.wait(2)

        

        # Clean up before final conclusion

        self.play(

            FadeOut(highlight_box),

            FadeOut(ref_circle),

            FadeOut(hexagon),

            FadeOut(hexagon_label),

            FadeOut(explanation4)

        )

        self.wait(0.5)

        

        # Show final conclusion with hexagon

        final_hexagon = RegularPolygon(n=6, radius=2, color=BLUE, fill_opacity=0.4)

        final_hexagon.move_to(DOWN * 0.5 + RIGHT*3.2)

        

        final_conclusion = VGroup(

            Text("Hexagon: Best Approximation", font_size=36, weight=BOLD, color=BLUE),

            Text("• 83% circle coverage", font_size=24),

            Text("• Tiles perfectly (no gaps)", font_size=24),

            Text("• Minimal distance variation to edges", font_size=24),

            Text("• Optimal for cellular networks", font_size=24, color=GOLD)

        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        final_conclusion.move_to(UP * 1.1)

        

        self.play(Create(final_hexagon))

        self.wait(0.5)

        

        for line in final_conclusion:

            self.play(Write(line))

            self.wait(0.5)

        

        self.wait(3)