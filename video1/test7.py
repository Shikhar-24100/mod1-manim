from manim import *
import numpy as np

class AssumptionsVisualization(Scene):
    """Animation 10: Friis Equation Assumptions"""
    
    def construct(self):
        # Title
        title = Text("Friis Equation Assumptions", font_size=44, weight=BOLD)
        subtitle = Text("What we assume vs What we get", font_size=28, color=WHITE)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(
            title.animate.scale(0.75).to_edge(UP, buff=0.3),
            FadeOut(subtitle)
        )
        
        # ========== IDEAL SCENARIO ==========
        ideal_label = Text("Case 1: Ideal Scenario", font_size=32, color=WHITE)
        ideal_label.to_edge(UP, buff=1.2)
        
        self.play(Write(ideal_label))
        self.wait(0.5)
        
        # Create ideal scene
        # Ground/reference line
        ground = Line(LEFT * 7, RIGHT * 7, color=GRAY, stroke_width=1)
        ground.shift(DOWN * 2)
        
        # Transmitter (tower) - Use SVG
        try:
            tx_tower = SVGMobject("tower.svg").scale(0.8)
        except:
            # Fallback
            tx_signal_lines = VGroup(*[
                Line(ORIGIN, UR * 0.4).rotate(i * PI/2).shift(UP * 0.6) 
                for i in range(4)
            ])
            tx_tower = VGroup(
                Rectangle(height=1.5, width=0.3, color=BLUE, fill_opacity=0.8),
                Triangle(color=YELLOW, fill_opacity=1).scale(0.3).rotate(PI/2).shift(UP * 0.8),
                tx_signal_lines
            )
        
        tx_tower.shift(LEFT * 4 + DOWN * 0.75)
        
        # Receiver (mobile) - Use SVG
        try:
            rx_tower = SVGMobject("mobile.svg").scale(0.6)
        except:
            # Fallback
            rx_tower = VGroup(
                Rectangle(height=1.5, width=0.3, color=RED, fill_opacity=0.8),
                Triangle(color=ORANGE, fill_opacity=1).scale(0.3).rotate(-PI/2).shift(UP * 0.8)
            )
        
        rx_tower.shift(RIGHT * 4 + DOWN * 0.75)
        
        # Perfect line of sight
        los_line = DashedLine(
            tx_tower.get_top(),
            rx_tower.get_top()+UP*0.15,
            color=GREEN,
            stroke_width=3,
            dash_length=0.2
        )
        
        # Distance label
        # distance_label = VGroup(
        #     DoubleArrow(
        #         tx_tower.get_bottom() + DOWN * 0.3,
        #         rx_tower.get_bottom() + DOWN * 0.6,
        #         color=WHITE,
        #         buff=0
        #     ),
        #     Text("d (distance)", font_size=20).shift(DOWN * 2.8)
        # )
        
        self.play(
            FadeIn(ground),
            FadeIn(tx_tower, scale=1.2),
            FadeIn(rx_tower, scale=1.2)
        )
        self.play(Create(los_line))
        # self.play(Write(distance_label))
        self.wait(0.5)
        
        # Create signal propagation (clean wave)
        signal_wave = self.create_clean_signal(tx_tower.get_top(), rx_tower.get_top())
        self.play(Create(signal_wave), run_time=2)
        
        # ========== ASSUMPTIONS CHECKLIST ==========
        assumptions_title = Text("Assumptions:", font_size=26, color=YELLOW)
        assumptions_title.to_corner(UR, buff=0.6).shift(DOWN * 0.3)
        self.play(Write(assumptions_title))
        
        # Checklist items - adjusted size to prevent overlap
        checklist = VGroup(
            self.create_checklist_item("Free Space", "No obstacles"),
            self.create_checklist_item("Line of Sight", "Direct path"),
            self.create_checklist_item("No Multipath", "No reflections"),
            self.create_checklist_item("Far Field", "d >> λ")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        checklist.next_to(assumptions_title, DOWN, buff=0.25, aligned_edge=LEFT)
        
        # Animate checklist appearing with checkmarks
        for item in checklist:
            self.play(
                FadeIn(item[1:], shift=RIGHT),  # Text
                run_time=0.5
            )
            self.wait(0.2)
            self.play(
                Write(item[0]),  # Checkmark
                item[0].animate.set_color(GREEN),
                run_time=0.3
            )
            self.wait(0.3)
        
        self.wait(16)
        
        # ========== TRANSITION TO REAL WORLD ==========
        # transition_text = Text("But in the REAL WORLD...", font_size=32, color=RED, weight=BOLD)
        # transition_text.move_to(ORIGIN)
        # transition_text.shift(UP*0.5)
        
        self.play(
            FadeOut(ideal_label)
            # Write(transition_text)
        )
        self.wait(1)
        
        # Real world label
        real_label = Text("Case 2: Real World", font_size=32, color=WHITE)
        real_label.to_edge(UP, buff=1.2)
        self.play(Write(real_label))
        
        # ========== ADD REAL WORLD OBSTACLES ==========
        
        # Buildings - adjusted positions to avoid overlap
        buildings = VGroup()
        for i, (h, w) in enumerate([(2.5, 0.8), (1.8, 0.6), (2.2, 0.7)]):
            building = Rectangle(height=h, width=w, color=GRAY, fill_opacity=0.85, stroke_color=WHITE)
            buildings.add(building)
        
        buildings[0].move_to(LEFT * 1.8 + DOWN * 0.75)
        buildings[1].move_to(RIGHT * 0.2 + DOWN * 1.1)
        buildings[2].move_to(RIGHT * 2.8 + DOWN * 0.9)
        
        # Add windows to buildings
        for building in buildings:
            windows = VGroup(*[
                Rectangle(height=0.12, width=0.12, color=YELLOW, fill_opacity=0.5)
                for _ in range(6)
            ]).arrange_in_grid(rows=3, cols=2, buff=0.1)
            windows.scale(0.7).move_to(building.get_center()).shift(UP * 0.1)
            building.add(windows)
        
        # Trees - adjusted positions
        trees = VGroup()
        for pos in [LEFT * 3.2, LEFT * 0.5]:
            tree = VGroup(
                Rectangle(height=0.4, width=0.15, color="#8B4513", fill_opacity=1),
                Circle(radius=0.3, color=GREEN, fill_opacity=0.8)
            )
            tree[1].next_to(tree[0], UP, buff=-0.1)
            tree.move_to(pos + DOWN * 1.5)
            trees.add(tree)
        
        # Person
        person = VGroup(
            Circle(radius=0.15, color=BLACK, fill_opacity=1),  # Head
            Line(ORIGIN, DOWN * 0.5, color=BLACK, stroke_width=6),  # Body
            Line(ORIGIN, DL * 0.3, color=BLACK, stroke_width=4),  # Leg 1
            Line(ORIGIN, DR * 0.3, color=BLACK, stroke_width=4)   # Leg 2
        )
        person.move_to(LEFT * 2.5 + DOWN * 1.3)
        
        # Car - adjusted position
        car = VGroup(
            Rectangle(height=0.3, width=0.6, color=BLUE, fill_opacity=0.9),
            Rectangle(height=0.2, width=0.4, color="#87CEEB", fill_opacity=0.7).shift(UP * 0.15),
            Circle(radius=0.1, color=GREY, fill_opacity=1).shift(LEFT * 0.2 + DOWN * 0.2),
            Circle(radius=0.1, color=GREY, fill_opacity=1).shift(RIGHT * 0.2 + DOWN * 0.2)
        )
        car.move_to(RIGHT * 1.2 + DOWN * 1.7)
        
        # Earth curvature hint
        curvature = Arc(
            radius=15,
            start_angle=PI - 0.3,
            angle=0.6,
            color=GRAY,
            stroke_width=2
        ).shift(DOWN * 12.5)
        
        # Animate obstacles appearing
        self.play(
            FadeOut(signal_wave),
            los_line.animate.set_color(RED).set_stroke(width=2),
        )
        
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=DOWN * 0.5, scale=0.8) for b in buildings],
                lag_ratio=0.2
            ),
            run_time=1.5
        )
        
        self.play(
            FadeIn(trees, shift=UP, scale=1.2),
            FadeIn(person, shift=RIGHT),
            FadeIn(car, shift=LEFT),
            run_time=1
        )
        
        self.play(Create(curvature), run_time=1.5)
        
        # Show blocked/scattered signal paths
        scattered_paths = VGroup()
        
        # Reflection from building
        reflect_point = buildings[0].get_top() + UP * 0.2
        path1 = VMobject(color=ORANGE, stroke_width=2)
        path1.set_points_as_corners([
            tx_tower.get_top(),
            reflect_point,
            rx_tower.get_top()
        ])
        
        # Diffraction around building
        diffract_point = buildings[1].get_top() + UP * 0.3 + RIGHT * 0.2
        path2 = VMobject(color=YELLOW, stroke_width=2)
        path2.set_points_smoothly([
            tx_tower.get_top(),
            diffract_point + LEFT * 0.5,
            diffract_point,
            diffract_point + RIGHT * 0.5,
            rx_tower.get_top()
        ])
        
        # Scattered path - create the path first, then make it dashed
        scatter_point = person.get_top() + UP * 0.3
        path3_base = VMobject(color=RED, stroke_width=2)
        path3_base.set_points_as_corners([
            tx_tower.get_top(),
            scatter_point,
            rx_tower.get_top()
        ])
        path3 = DashedVMobject(path3_base, num_dashes=15)
        
        scattered_paths.add(path1, path2, path3)
        
        self.play(
            LaggedStart(
                *[Create(path) for path in scattered_paths],
                lag_ratio=0.3
            ),
            run_time=2
        )
        
        # Update checklist - cross out assumptions
        violations = VGroup()
        for i, item in enumerate(checklist):
            cross = VGroup(
                Line(UL * 0.15, DR * 0.15, color=RED, stroke_width=4),
                Line(UR * 0.15, DL * 0.15, color=RED, stroke_width=4)
            )
            cross.move_to(item[0])
            violations.add(cross)
        
        self.play(
            LaggedStart(
                *[Create(x) for x in violations],
                lag_ratio=0.2
            ),
            *[item[0].animate.set_color(RED) for item in checklist],
            run_time=1.5
        )
        
        # Final message
        warning = VGroup(
            # Text("⚠️ Friis Equation", font_size=30, color=YELLOW, weight=BOLD),
            Text("Friis Equation is only valid under ideal conditions!", font_size=28, color=WHITE)
        ).arrange(DOWN, buff=0.2)
        warning.to_edge(DOWN, buff=0.4)
        warning.shift(UP*0.5)
        
        self.play(FadeIn(warning, shift=UP))
        
        self.wait(10)
    
    def create_checklist_item(self, main_text, sub_text):
        checkmark = Text("✓", font_size=24, color=GRAY)
        main = Text(main_text, font_size=19, weight=BOLD)
        sub = Text(sub_text, font_size=14, color=GRAY, slant=ITALIC)
        
        text_group = VGroup(main, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.03)
        item = VGroup(checkmark, text_group).arrange(RIGHT, buff=0.25)
        return item
    
    def create_clean_signal(self, start, end):
        points = []
        for t in np.linspace(0, 1, 100):
            pos = start + t * (end - start)
            offset = 0.15 * np.sin(t * 8 * PI)
            direction = rotate_vector(normalize(end - start), PI/2)
            points.append(pos + offset * direction)
        
        wave = VMobject(color=GREEN, stroke_width=3)
        wave.set_points_smoothly(points)
        return wave


class LimitationScenarios(Scene):
    """Animation 11: Friis Equation Limitations"""
    
    def construct(self):
        # Title
        title = Text("Friis Equation Limitations", font_size=44, weight=BOLD)
        subtitle = Text("Prediction vs Reality", font_size=28, color=ORANGE)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(
            title.animate.scale(0.65).to_edge(UP, buff=0.2),
            FadeOut(subtitle)
        )
        
        # ========== FRIIS EQUATION DISPLAY ==========
        friis_eq = MathTex(
            r"P_r = P_t G_t G_r \left(\frac{\lambda}{4\pi d}\right)^2",
            font_size=32
        )
        friis_eq.to_corner(UL, buff=0.6).shift(DOWN * 0.3)
        friis_label = Text("Friis Equation:", font_size=22, color=YELLOW)
        friis_label.next_to(friis_eq, UP, aligned_edge=LEFT, buff=0.15)
        
        self.play(
            Write(friis_label),
            Write(friis_eq)
        )
        self.wait(1)
        
        # ========== IDEAL SCENARIO SETUP ==========
        scenario_label = Text("Scenario: Urban Communication", font_size=26, color=BLUE)
        scenario_label.to_edge(UP, buff=1.3)
        self.play(Write(scenario_label))
        
        # Ground
        ground = Line(LEFT * 7, RIGHT * 7, color="#8B7355", stroke_width=2)
        ground.shift(DOWN * 2.5)
        self.play(Create(ground))
        
        # Transmitter - Use SVG
        try:
            tx = SVGMobject("tower.svg").scale(1.0)
        except:
            # Fallback
            tx_signal_lines = VGroup(*[
                Line(ORIGIN, UR * 0.5).rotate(i * PI/2).shift(UP * 0.9) 
                for i in range(4)
            ])
            tx = VGroup(
                Rectangle(height=2, width=0.4, color=BLUE, fill_opacity=0.9, stroke_color=WHITE),
                Triangle(color=YELLOW, fill_opacity=1).scale(0.4).rotate(PI/2).shift(UP * 1.1),
                tx_signal_lines
            )
        
        tx.shift(LEFT * 5 + DOWN * 1.5)
        
        # Receiver - Use SVG
        try:
            rx = SVGMobject("mobile.svg").scale(0.7)
        except:
            # Fallback
            rx = VGroup(
                Rectangle(height=1.5, width=0.35, color=RED, fill_opacity=0.9, stroke_color=WHITE),
                Triangle(color=ORANGE, fill_opacity=1).scale(0.35).rotate(-PI/2).shift(UP * 0.85)
            )
        
        rx.shift(RIGHT * 5 + DOWN * 1.75)
        
        tx_label = Text("Base Station", font_size=16).next_to(tx, DOWN, buff=0.15)
        rx_label = Text("Mobile", font_size=16).next_to(rx, DOWN, buff=0.15)
        
        self.play(
            FadeIn(tx, scale=1.3),
            FadeIn(rx, scale=1.3),
            Write(tx_label),
            Write(rx_label)
        )
        
        # Clean LOS with animated signal wave
        los_clean = DashedLine(
            tx.get_right() + RIGHT * 0.2,
            rx.get_left() + LEFT * 0.2,
            color=GREEN,
            stroke_width=4
        )
        
        # Add animated signal waves traveling along LOS
        signal_waves = VGroup()
        for i in range(3):
            wave = self.create_traveling_wave(
                tx.get_right() + RIGHT * 0.2,
                rx.get_left() + LEFT * 0.2,
                GREEN
            )
            signal_waves.add(wave)
        
        self.play(Create(los_clean), run_time=1.5)
        self.play(
            LaggedStart(
                *[Create(wave) for wave in signal_waves],
                lag_ratio=0.3
            ),
            run_time=2
        )
        
        # Power prediction box (Friis prediction) - adjusted to prevent overlap
        prediction_box = VGroup(
            Rectangle(height=1.0, width=2.8, color=GREEN, stroke_width=3, fill_opacity=0.1),
            Text("Friis Predicts:", font_size=18, color=GREEN),
            MathTex(r"P_r = -65 \text{ dBm}", font_size=24, color=GREEN)
        ).arrange(DOWN, buff=0.15)
        prediction_box.to_corner(UR, buff=0.4).shift(DOWN * 0.5)
        
        self.play(FadeIn(prediction_box, shift=LEFT))
        self.wait(1)
        
        # ========== FADE IN OBSTACLES ==========
        fade_text = Text("Reality Check...", font_size=30, color=RED, slant=ITALIC)
        fade_text.move_to(ORIGIN)
        
        self.play(Write(fade_text))
        self.wait(0.8)
        self.play(FadeOut(fade_text))
        
        # Create buildings with fade-in - adjusted positions to prevent overlap
        buildings = VGroup()
        building_positions = [
            (LEFT * 2.8, 2.5, 0.8),
            (LEFT * 0.8, 2.0, 0.65),
            (RIGHT * 1.2, 2.6, 0.9),
            (RIGHT * 3.2, 2.2, 0.75)
        ]
        
        for pos, height, width in building_positions:
            building = Rectangle(
                height=height,
                width=width,
                color=GRAY,
                fill_opacity=0.0,  # Start transparent
                stroke_color=WHITE,
                stroke_width=2
            )
            building.move_to(pos + DOWN * 1.25 + UP * height/2)
            
            # Add windows
            num_floors = int(height / 0.4)
            windows = VGroup(*[
                Rectangle(height=0.1, width=0.1, color=YELLOW, fill_opacity=0.5)
                for _ in range(num_floors * 2)
            ]).arrange_in_grid(rows=num_floors, cols=2, buff=0.12)
            windows.scale(0.6).move_to(building.get_center())
            
            building.add(windows)
            buildings.add(building)
        
        # Fade in buildings with smoother animation
        self.play(
            LaggedStart(
                *[building.animate.set_fill(opacity=0.9) for building in buildings],
                lag_ratio=0.15
            ),
            los_clean.animate.set_color(RED).set_stroke(width=2, opacity=0.3),
            FadeOut(signal_waves),  # Remove clean waves
            run_time=2.5
        )
        
        # Add shadow/blocked signal indicators
        blocked_regions = VGroup()
        for building in buildings:
            shadow = Polygon(
                building.get_corner(DR),
                building.get_corner(DR) + RIGHT * 0.7 + DOWN * 0.4,
                building.get_corner(UR) + RIGHT * 0.7 + UP * 0.25,
                building.get_corner(UR),
                color=BLACK,
                fill_opacity=0.25,
                stroke_width=0
            )
            blocked_regions.add(shadow)
        
        self.play(FadeIn(blocked_regions, lag_ratio=0.1), run_time=1.5)
        
        # Add more obstacles - adjusted positions
        vehicle = VGroup(
            Rectangle(height=0.35, width=0.7, color="#4169E1", fill_opacity=0.9),
            Circle(radius=0.11, color=BLACK, fill_opacity=1).shift(LEFT * 0.28 + DOWN * 0.22),
            Circle(radius=0.11, color=BLACK, fill_opacity=1).shift(RIGHT * 0.28 + DOWN * 0.22)
        )
        vehicle.move_to(LEFT * 4 + DOWN * 2.15)
        
        person = self.create_person()
        person.move_to(RIGHT * 0.1 + DOWN * 2)
        
        trees = VGroup()
        for x_pos in [LEFT * 4.8, RIGHT * 2.5]:
            tree = self.create_tree()
            tree.move_to(x_pos + DOWN * 2.2)
            trees.add(tree)
        
        self.play(
            FadeIn(vehicle, shift=RIGHT, scale=0.8),
            FadeIn(person, shift=LEFT, scale=0.8),
            FadeIn(trees, scale=0.9),
            run_time=1.5
        )
        
        # ========== SHOW MULTIPATH ==========
        multipath_label = Text("Multipath Propagation:", font_size=22, color=ORANGE)
        multipath_label.next_to(scenario_label, DOWN, buff=0.25)
        self.play(Write(multipath_label))
        
        # Complex signal paths with labels
        paths = VGroup()
        path_labels = VGroup()
        
        # Reflected path 1
        reflect1 = buildings[0].get_top() + UP * 0.15
        path1 = VMobject(color=ORANGE, stroke_width=2.5)
        path1.set_points_as_corners([
            tx.get_right() + RIGHT * 0.2,
            reflect1,
            rx.get_left() + LEFT * 0.2
        ])
        label1 = Text("Reflection", font_size=13, color=ORANGE).next_to(reflect1, UP, buff=0.08)
        
        # Reflected path 2
        reflect2 = buildings[2].get_top() + UP * 0.15
        path2 = VMobject(color=YELLOW, stroke_width=2.5)
        path2.set_points_as_corners([
            tx.get_right() + RIGHT * 0.2,
            reflect2,
            rx.get_left() + LEFT * 0.2
        ])
        label2 = Text("Reflection", font_size=13, color=YELLOW).next_to(reflect2, UP, buff=0.08)
        
        # Diffracted path
        diffract = buildings[1].get_top() + UP * 0.35
        path3 = VMobject(color=RED, stroke_width=2)
        path3.set_points_smoothly([
            tx.get_right() + RIGHT * 0.2,
            diffract + LEFT * 0.7,
            diffract,
            diffract + RIGHT * 0.7,
            rx.get_left() + LEFT * 0.2
        ])
        label3 = Text("Diffraction", font_size=13, color=RED).next_to(diffract, UP, buff=0.08)
        
        # Scattered paths - create the path first, then make it dashed
        scatter_pt = vehicle.get_top() + UP * 0.25
        path4_base = VMobject(color=PURPLE, stroke_width=1.5)
        path4_base.set_points_as_corners([
            tx.get_right() + RIGHT * 0.2,
            scatter_pt,
            rx.get_left() + LEFT * 0.2
        ])
        path4 = DashedVMobject(path4_base, num_dashes=20)
        label4 = Text("Scattering", font_size=13, color=PURPLE).next_to(scatter_pt, RIGHT, buff=0.15)
        
        paths.add(path1, path2, path3, path4)
        path_labels.add(label1, label2, label3, label4)
        
        # Animate paths appearing one by one with their labels
        for path, label in zip(paths, path_labels):
            self.play(
                Create(path),
                FadeIn(label, scale=0.8),
                run_time=0.8
            )
            self.wait(0.3)
        
        # ========== ACTUAL MEASUREMENT ==========
        actual_box = VGroup(
            Rectangle(height=1.0, width=2.8, color=RED, stroke_width=3, fill_opacity=0.1),
            Text("Actual Measured:", font_size=18, color=RED),
            MathTex(r"P_r = -89 \text{ dBm}", font_size=24, color=RED)
        ).arrange(DOWN, buff=0.15)
        actual_box.next_to(prediction_box, DOWN, buff=0.3, aligned_edge=RIGHT)
        
        self.play(FadeIn(actual_box, shift=UP))
        
        # Show mismatch
        mismatch = VGroup(
            Text("Mismatch:", font_size=20, color=YELLOW, weight=BOLD),
            MathTex(r"\Delta = 24 \text{ dB}", font_size=23, color=YELLOW)
        ).arrange(DOWN, buff=0.12)
        mismatch.next_to(actual_box, DOWN, buff=0.25, aligned_edge=RIGHT)
        
        error_arrow = Arrow(
            prediction_box.get_bottom(),
            actual_box.get_top(),
            color=YELLOW,
            stroke_width=4,
            buff=0.08
        )
        
        self.play(
            GrowArrow(error_arrow),
            Write(mismatch)
        )
        
        self.wait(1)
        
        # ========== CONCLUSION ==========
        conclusion = VGroup(
            Text("Why Friis Fails:", font_size=25, color=RED, weight=BOLD),
            Text("✗ Multipath interference", font_size=18),
            Text("✗ Shadowing losses", font_size=18),
            Text("✗ Reflection & diffraction", font_size=18),
            Text("✗ Scattering from objects", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        conclusion.to_edge(DOWN, buff=0.25).shift(LEFT * 2.2)
        
        solution = VGroup(
            Text("Better Models:", font_size=25, color=GREEN, weight=BOLD),
            Text("• Okumura-Hata", font_size=18),
            Text("• COST-231", font_size=18),
            Text("• Ray tracing", font_size=18),
            Text("• Empirical measurements", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        solution.next_to(conclusion, RIGHT, buff=0.9, aligned_edge=UP)
        
        self.play(
            FadeIn(conclusion, shift=UP, lag_ratio=0.1),
            FadeIn(solution, shift=UP, lag_ratio=0.1),
            run_time=2
        )
        
        self.wait(4)
    
    def create_person(self):
        person = VGroup(
            Circle(radius=0.14, color="#FFD700", fill_opacity=1),
            Line(ORIGIN, DOWN * 0.45, color="#FFD700", stroke_width=6),
            Line(ORIGIN, DL * 0.32, color="#FFD700", stroke_width=4),
            Line(ORIGIN, DR * 0.32, color="#FFD700", stroke_width=4)
        )
        person[2].shift(DOWN * 0.23)
        person[3].shift(DOWN * 0.23)
        return person
    
    def create_tree(self):
        tree = VGroup(
            Rectangle(height=0.45, width=0.16, color="#8B4513", fill_opacity=1),
            Circle(radius=0.32, color=GREEN, fill_opacity=0.85),
            Circle(radius=0.26, color="#228B22", fill_opacity=0.7).shift(UL * 0.13),
            Circle(radius=0.23, color="#32CD32", fill_opacity=0.8).shift(UR * 0.11)
        )
        tree[1].next_to(tree[0], UP, buff=-0.13)
        tree[2].move_to(tree[1].get_center())
        tree[3].move_to(tree[1].get_center())
        return tree
    
    def create_traveling_wave(self, start, end, color):
        """Create a traveling sine wave between two points"""
        points = []
        for t in np.linspace(0, 1, 80):
            pos = start + t * (end - start)
            offset = 0.2 * np.sin(t * 6 * PI)
            direction = rotate_vector(normalize(end - start), PI/2)
            points.append(pos + offset * direction)
        
        wave = VMobject(color=color, stroke_width=2.5)
        wave.set_points_smoothly(points)
        return wave