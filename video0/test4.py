from manim import *

class ModulationProblem(Scene):
    def construct(self):
        # Title
        title = Text("Why Do We Need Modulation?", font_size=40, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # ===== Part 1: Digital Data (Left Side) =====
        
        # Binary bits text
        bits_text = Text("1 0 1 1 0 1 0", font_size=36, color=YELLOW)
        bits_text.shift(LEFT * 4 + UP * 1.5)
        
        # Create square wave representation
        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 1.5, 0.5],
            x_length=5,
            y_length=2,
            axis_config={"include_tip": False, "include_numbers": False},
        ).shift(LEFT * 4)
        
        # Define the square wave based on bits "1011010"
        bits = [1, 0, 1, 1, 0, 1, 0]
        square_wave = VGroup()
        
        for i, bit in enumerate(bits):
            height = 1 if bit == 1 else 0
            # Vertical line
            if i > 0:
                prev_height = 1 if bits[i-1] == 1 else 0
                vertical = Line(
                    axes.c2p(i, prev_height),
                    axes.c2p(i, height),
                    color=YELLOW,
                    stroke_width=3
                )
                square_wave.add(vertical)
            
            # Horizontal line
            horizontal = Line(
                axes.c2p(i, height),
                axes.c2p(i + 1, height),
                color=YELLOW,
                stroke_width=3
            )
            square_wave.add(horizontal)
        
        # Label for digital signal
        digital_label = Text("Digital Signal", font_size=24, color=YELLOW)
        digital_label.next_to(axes, DOWN, buff=0.3)
        
        # Animate digital data appearance
        self.play(Write(bits_text))
        self.wait(0.3)
        self.play(Create(axes), Create(square_wave))
        self.play(FadeIn(digital_label))
        self.wait(0.5)
        
        # ===== Part 2: Antenna (Right Side) =====
        
        # Load the tower SVG
        try:
            antenna = SVGMobject("tower.svg")
            antenna.scale(1.2)
            antenna.shift(RIGHT * 4)
        except:
            # Fallback: Create a simple antenna if SVG doesn't load
            antenna = VGroup()
            base = Rectangle(width=0.3, height=0.5, color=GRAY, fill_opacity=1)
            tower = Triangle(color=RED, fill_opacity=1).scale(0.8)
            tower.next_to(base, UP, buff=0)
            antenna.add(base, tower)
            antenna.shift(RIGHT * 4)
        
        antenna_label = Text("Antenna", font_size=24, color=WHITE)
        antenna_label.next_to(antenna, DOWN, buff=0.5)
        
        # Animate antenna appearance
        self.play(FadeIn(antenna), Write(antenna_label))
        self.wait(0.5)
        
        # ===== Part 3: Problem Visualization =====
        
        # Create digital bits trying to travel
        traveling_bits = VGroup()
        for i, bit in enumerate([1, 0, 1, 1, 0, 1, 0]):
            bit_square = Square(side_length=0.3, color=YELLOW, fill_opacity=0.8)
            bit_text = Text(str(bit), font_size=20, color=BLACK)
            bit_text.move_to(bit_square.get_center())
            bit_mob = VGroup(bit_square, bit_text)
            bit_mob.move_to(axes.get_right() + RIGHT * 0.5 + UP * (i * 0.1 - 1))
            traveling_bits.add(bit_mob)
        
        # Animate bits trying to reach antenna
        animations = []
        for bit_mob in traveling_bits:
            target_pos = antenna.get_left() + LEFT * 0.5 + UP * np.random.uniform(-0.5, 0.5)
            animations.append(bit_mob.animate.move_to(target_pos).set_opacity(0.3))
        
        self.play(*animations, run_time=2)
        self.wait(0.3)
        
        # Show failure - Red X marks
        failure_marks = VGroup()
        for bit_mob in traveling_bits:
            x_mark = Text("✗", font_size=40, color=RED)
            x_mark.move_to(bit_mob.get_center())
            failure_marks.add(x_mark)
        
        self.play(
            *[FadeIn(mark, scale=1.5) for mark in failure_marks],
            *[bit_mob.animate.set_opacity(0.1) for bit_mob in traveling_bits],
            run_time=0.8
        )
        self.wait(2.5)
        
        # ===== Part 4: Text Overlays =====
        
        # First message
        problem_text = Text(
            "Digital signals cannot travel through air efficiently",
            font_size=28,
            color=RED,
            line_spacing=1.2
        )
        problem_text.to_edge(DOWN, buff=1.5)
        
        self.play(Write(problem_text))
        self.wait(2)
        
        # Second message - Solution hint
        solution_text = Text(
            "We need a carrier wave!",
            font_size=32,
            color=GREEN,
            weight=BOLD
        )
        solution_text.next_to(problem_text, DOWN, buff=0.5)
        
        self.play(
            Write(solution_text),
            solution_text.animate.scale(1.1),
            rate_func=there_and_back
        )
        self.wait(4)
        
        # Fade out everything for next scene
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1
        )
        self.wait(4)