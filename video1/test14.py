from manim import *
import numpy as np

class UrbanVsRuralShadowing(Scene):
    """Animation 17: Urban vs Rural shadowing comparison"""
    
    def construct(self):
        # Title
        title = Text("Shadowing: Urban vs Rural Environments", font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.78).to_edge(UP, buff=0.2))
        
        # Create split screen divider
        divider = Line(UP * 3.3, DOWN * 3.5, color=WHITE, stroke_width=3)
        self.play(Create(divider))
        
        # Labels for each side
        urban_label = Text("Urban Environment", font_size=28, color=RED, weight=BOLD)
        urban_label.move_to(LEFT * 3.5 + UP * 2.8)
        
        rural_label = Text("Rural Environment", font_size=28, color=GREEN, weight=BOLD)
        rural_label.move_to(RIGHT * 3.5 + UP * 2.8)
        
        self.play(Write(urban_label), Write(rural_label))
        self.wait(0.5)
        
        # ========== URBAN SIDE (LEFT) ==========
        urban_scene = self.create_urban_scene()
        urban_scene.shift(LEFT * 3.5)
        
        self.play(FadeIn(urban_scene, lag_ratio=0.1), run_time=2)
        self.wait(1)
        
        # ========== RURAL SIDE (RIGHT) ==========
        rural_scene = self.create_rural_scene()
        rural_scene.shift(RIGHT * 3.5)
        
        self.play(FadeIn(rural_scene, lag_ratio=0.1), run_time=2)
        self.wait(1)
        
        # ========== SIGNAL PATHS ==========
        # Urban signal path (heavily fluctuating)
        urban_path = self.create_signal_path(
            LEFT * 3.5 + LEFT * 2.5 + UP * 1,
            LEFT * 3.5 + RIGHT * 2.5 + UP * 1,
            fluctuation=0.8,
            color=RED
        )
        
        # Rural signal path (smooth)
        rural_path = self.create_signal_path(
            RIGHT * 3.5 + LEFT * 2.5 + UP * 1,
            RIGHT * 3.5 + RIGHT * 2.5 + UP * 1,
            fluctuation=0.2,
            color=GREEN
        )
        
        self.play(
            Create(urban_path, run_time=2)
        )
        self.wait(1)
        
        # ========== SIGMA VALUES ==========
        # Urban sigma
        urban_sigma = VGroup(
            Text("Shadowing Spread (σ):", font_size=18, color=WHITE),
            Text("8-10 dB", font_size=24, color=RED, weight=BOLD)
        ).arrange(DOWN, buff=0.1)
        urban_sigma.move_to(LEFT * 3.5 + DOWN * 2.3)
        self.wait(10)


        self.play(
            Create(rural_path, run_time=2)
        )
        self.wait(1)
        # Rural sigma
        rural_sigma = VGroup(
            Text("Shadowing Spread (σ):", font_size=18, color=WHITE),
            Text("4-6 dB", font_size=24, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.1)
        rural_sigma.move_to(RIGHT * 3.5 + DOWN * 2.3)
        
        self.play(
            FadeIn(urban_sigma, shift=UP),
            FadeIn(rural_sigma, shift=UP)
        )
        self.wait(1)
        
        # ========== ANNOTATIONS ==========
        # urban_annotation = VGroup(
        #     Text("• Many tall buildings", font_size=16, color=YELLOW),
        #     Text("• Heavy signal blocking", font_size=16, color=YELLOW),
        #     Text("• High variability", font_size=16, color=YELLOW)
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        # urban_annotation.move_to(LEFT * 3.5 + DOWN * 0.5)
        
        # rural_annotation = VGroup(
        #     Text("• Open fields", font_size=16, color=YELLOW),
        #     Text("• Few obstacles", font_size=16, color=YELLOW),
        #     Text("• Low variability", font_size=16, color=YELLOW)
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        # rural_annotation.move_to(RIGHT * 3.5 + DOWN * 0.5)
        
        # self.play(
        #     Write(urban_annotation),
        #     Write(rural_annotation)
        # )
        self.wait(9)
    
    def create_urban_scene(self):
        """Create urban environment with buildings"""
        scene = VGroup()
        
        # Ground
        ground = Line(LEFT * 3, RIGHT * 3, color="#555555", stroke_width=2)
        ground.shift(DOWN * 1.8)
        scene.add(ground)
        
        # Load or create buildings
        buildings = VGroup()
        building_positions = [
            (LEFT * 2.2 + DOWN * 1.2, 0.8),
            (LEFT * 0.8 + DOWN * 0.8, 1.2),
            (RIGHT * 0.5 + DOWN * 1.0, 1.0),
            (RIGHT * 1.8 + DOWN * 0.6, 1.4)
        ]
        
        for pos, scale in building_positions:
            try:
                building = SVGMobject("building.svg").scale(scale * 0.6)
                building.move_to(pos)
            except:
                # Fallback building
                height = 1.5 * scale
                building = Rectangle(
                    height=height, 
                    width=0.4, 
                    color=GRAY, 
                    fill_opacity=0.8,
                    stroke_color=WHITE,
                    stroke_width=1
                )
                building.move_to(pos)
                # Add windows
                num_windows = int(height / 0.3)
                windows = VGroup(*[
                    Rectangle(height=0.08, width=0.08, color=YELLOW, fill_opacity=0.5)
                    for _ in range(num_windows * 2)
                ]).arrange_in_grid(rows=num_windows, cols=2, buff=0.08)
                windows.scale(0.6).move_to(building.get_center())
                building.add(windows)
            
            buildings.add(building)
        
        scene.add(buildings)
        
        # Add some cars
        try:
            car = SVGMobject("car.svg").scale(0.3)
            car.move_to(LEFT * 1.2 + DOWN * 1.7)
            scene.add(car)
        except:
            pass
        
        # Transmitter and receiver
        try:
            tx = SVGMobject("tower.svg").scale(0.5)
            tx.move_to(LEFT * 2.5 + UP * 1)
        except:
            tx = Triangle(color=BLUE, fill_opacity=1).scale(0.2).rotate(-PI/2)
            tx.move_to(LEFT * 2.5 + UP * 1)
        
        try:
            rx = SVGMobject("mobile.svg").scale(0.4)
            rx.move_to(RIGHT * 2.5 + UP * 1)
        except:
            rx = Rectangle(height=0.3, width=0.15, color=RED, fill_opacity=1)
            rx.move_to(RIGHT * 2.5 + UP * 1)
        
        scene.add(tx, rx)
        
        return scene
    
    def create_rural_scene(self):
        """Create rural environment with trees and open space"""
        scene = VGroup()
        
        # Ground with grass texture
        ground = Line(LEFT * 3, RIGHT * 3, color="#2E7D32", stroke_width=2)
        ground.shift(DOWN * 1.8)
        scene.add(ground)
        
        # Add grass marks
        grass = VGroup()
        for i in range(15):
            x = -2.5 + i * 0.4
            blade = Line(
                [x, -1.8, 0],
                [x, -1.65, 0],
                color="#4CAF50",
                stroke_width=1
            )
            grass.add(blade)
        scene.add(grass)
        
        # Load or create trees
        trees = VGroup()
        tree_positions = [LEFT * 2.0 + DOWN * 1.3, RIGHT * 1.5 + DOWN * 1.3]
        
        for pos in tree_positions:
            try:
                tree = SVGMobject("tree.svg").scale(0.6)
                tree.move_to(pos)
            except:
                # Fallback tree
                trunk = Rectangle(height=0.4, width=0.12, color="#8B4513", fill_opacity=1)
                foliage = Circle(radius=0.3, color=GREEN, fill_opacity=0.8)
                foliage.next_to(trunk, UP, buff=-0.1)
                tree = VGroup(trunk, foliage)
                tree.move_to(pos)
            
            trees.add(tree)
        
        scene.add(trees)
        
        # Add cattle
        try:
            cattle = SVGMobject("cattle.svg").scale(0.4)
            cattle.move_to(RIGHT * 0.2 + DOWN * 1.6)
            scene.add(cattle)
        except:
            pass
        
        # Add person
        try:
            person = SVGMobject("person.svg").scale(0.4)
            person.move_to(LEFT * 0.5 + DOWN * 1.6)
            scene.add(person)
        except:
            pass
        
        # Transmitter and receiver
        try:
            tx = SVGMobject("tower.svg").scale(0.5)
            tx.move_to(LEFT * 2.5 + UP * 1)
        except:
            tx = Triangle(color=BLUE, fill_opacity=1).scale(0.2).rotate(-PI/2)
            tx.move_to(LEFT * 2.5 + UP * 1)
        
        try:
            rx = SVGMobject("mobile.svg").scale(0.4)
            rx.move_to(RIGHT * 2.5 + UP * 1)
        except:
            rx = Rectangle(height=0.3, width=0.15, color=RED, fill_opacity=1)
            rx.move_to(RIGHT * 2.5 + UP * 1)
        
        scene.add(tx, rx)
        
        return scene
    
    def create_signal_path(self, start, end, fluctuation=0.5, color=YELLOW):
        """Create a signal path with varying fluctuation"""
        num_points = 50
        points = []
        
        for i in range(num_points):
            t = i / (num_points - 1)
            base_point = start + t * (end - start)
            
            # Add random fluctuation
            if i > 0 and i < num_points - 1:
                noise = np.random.normal(0, fluctuation * 0.3)
                fluctuated_point = base_point + UP * noise
            else:
                fluctuated_point = base_point
            
            points.append(fluctuated_point)
        
        path = VMobject(color=color, stroke_width=3)
        path.set_points_smoothly([p for p in points])
        
        return path


