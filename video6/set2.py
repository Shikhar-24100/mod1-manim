from manim import *
import numpy as np

class CellularConceptFlow(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # ASSETS & CONFIG
        # ---------------------------------------------------------
        try:
            tower_svg = SVGMobject("assets/tower.svg").set_color(GRAY).scale(1.5)
        except:
            tower_svg = VGroup(Line(DOWN, UP), Triangle().move_to(UP)).set_color(GRAY).scale(1.5)

        # ---------------------------------------------------------
        # SCENE 1: THE 1G SETUP (Single Large Hexagon)
        # ---------------------------------------------------------
        
        # 1. Draw Large Hexagon
        # We rotate by 30 degrees (PI/6) so it stands on a point (flat sides vertical-ish) or 
        # usually flat top is standard. Let's do flat top (rotate PI/2).
        big_hex = RegularPolygon(n=6, color=BLUE, fill_opacity=0.1).scale(3)
        big_tower = tower_svg.copy().move_to(ORIGIN)
        
        # Footnote
        footnote = Text("* Why hexagonal shape? Explained later.", font_size=16, color=YELLOW).to_corner(DR)
        
        title_1g = Title("1G Uplink Scenario").to_edge(UP)

        self.play(
            Write(title_1g),
            Create(big_hex),
            FadeIn(big_tower),
            Write(footnote)
        )
        self.wait(1)

        # ---------------------------------------------------------
        # SCENE 2: THE VOICE MATH (300Hz -> 30kHz)
        # ---------------------------------------------------------

        # 1. Explain Voice Bandwidth
        # Move tower/hex slightly left to make room for math
        self.play(
            VGroup(big_hex, big_tower).animate.shift(LEFT * 3),
            FadeOut(footnote)
        )

        # Text breakdown
        voice_text_1 = Text("Human Voice: 300 Hz - 3.4 kHz", font_size=24).move_to(RIGHT * 3 + UP * 2)
        voice_text_2 = Text("With Guard Bands ~ 30 kHz", font_size=24, color=GREEN).next_to(voice_text_1, DOWN)
        
        self.play(Write(voice_text_1))
        self.wait(0.5)
        self.play(Write(voice_text_2))

        # 2. The Capacity Calculation
        # Total BW: 25MHz
        bw_text = Text("Total Uplink Spectrum: 25 MHz", font_size=24, color=BLUE).next_to(voice_text_2, DOWN, buff=0.5)
        
        math_calc = MathTex(
            r"\text{Capacity} = \frac{25 \text{ MHz}}{30 \text{ kHz}} \approx 832 \text{ Channels}",
            font_size=36
        ).next_to(bw_text, DOWN, buff=0.5)

        self.play(FadeIn(bw_text))
        self.play(Write(math_calc))
        
        # Highlight the result "832 Users"
        final_cap_label = Text("Max 832 Users", color=RED, font_size=32).next_to(big_tower, UP)
        self.play(Write(final_cap_label))
        self.wait(2)

        # ---------------------------------------------------------
        # SCENE 3: BREAKING THE CELL (The Cellular Concept)
        # ---------------------------------------------------------

        # 1. Cleanup Math
        self.play(
            FadeOut(voice_text_1),
            FadeOut(voice_text_2),
            FadeOut(bw_text),
            FadeOut(math_calc),
            FadeOut(final_cap_label),
            FadeOut(big_tower), # We replace big tower with small ones
            FadeOut(big_hex)    # We replace big hex with small hexes
        )

        # 2. Create 7 Small Hexagons (Cluster)
        # Geometry for tiling hexagons
        hex_radius = 1.0 
        # Distance between centers = sqrt(3) * radius
        hex_spacing = np.sqrt(3) * hex_radius
        
        # Angles for neighbors: 30, 90, 150, 210, 270, 330 (if flat top)
        # Let's adjust to fit nicely.
        # 0, 60, 120... is standard if point-top.
        # Let's use simple logic: Center + 6 surrounding.
        
        cluster_group = VGroup()
        centers = [ORIGIN]
        
        # Directions for flat-topped hexagons neighbors
        directions = [
            UP * np.sqrt(3), 
            UP * np.sqrt(3)/2 + RIGHT * 1.5,
            DOWN * np.sqrt(3)/2 + RIGHT * 1.5,
            DOWN * np.sqrt(3),
            DOWN * np.sqrt(3)/2 + LEFT * 1.5,
            UP * np.sqrt(3)/2 + LEFT * 1.5
        ]
        
        # Add center plus neighbors
        cell_coords = [ORIGIN]
        for d in directions:
            cell_coords.append(d * hex_radius * 0.6) # Scale spacing slightly

        # Create visuals
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK] # 7 different "frequencies"
        
        for i, pos in enumerate(cell_coords):
            # Small Hex
            h = RegularPolygon(n=6, color=WHITE, fill_color=colors[i], fill_opacity=0.3).scale(hex_radius).move_to(pos)
            # Small Tower
            t = tower_svg.copy().scale(0.3).move_to(pos) # 0.3 relative to original 1.5
            cluster_group.add(VGroup(h, t))

        # Center the cluster
        cluster_group.move_to(ORIGIN)
        
        label_split = Text("Split into 7 Cells", font_size=32).to_edge(UP)
        
        self.play(
            Transform(title_1g, label_split),
            FadeIn(cluster_group)
        )

        # 3. Channel Division Calculation
        # "Total available channels divided so neighbors don't interfere"
        
        division_math = MathTex(
            r"\text{Channels per Cell} = \frac{832}{7} \approx 118",
            font_size=32
        ).to_edge(LEFT, buff=0.5)
        
        total_check_math = MathTex(
            r"\text{Total Capacity} = 118 \times 7 = 832",
            font_size=32, color=YELLOW
        ).next_to(division_math, DOWN)
        
        note_text = Text("(No Gain Yet!)", color=YELLOW, font_size=24).next_to(total_check_math, DOWN)

        self.play(Write(division_math))
        self.wait(1)
        self.play(Write(total_check_math), Write(note_text))
        self.wait(2)

        # ---------------------------------------------------------
        # SCENE 4: FREQUENCY REUSE (Scaling)
        # ---------------------------------------------------------

        # 1. Move first cluster to left to make room
        self.play(
            FadeOut(division_math),
            FadeOut(total_check_math),
            FadeOut(note_text),
            cluster_group.animate.scale(0.6).to_edge(LEFT, buff=1)
        )

        # 2. Clone Clusters
        cluster_2 = cluster_group.copy().next_to(cluster_group, RIGHT, buff=0.2)
        cluster_3 = cluster_group.copy().next_to(cluster_2, RIGHT, buff=0.2)
        
        # Animate "Scaling"
        scale_label = Text("Frequency Reuse = Infinite Scaling", font_size=32).to_edge(UP)
        
        self.play(
            ReplacementTransform(label_split, scale_label),
            FadeIn(cluster_2),
            FadeIn(cluster_3)
        )

        # 3. Highlight The "A" Cells (Reuse)
        # In our cluster generation loop: index 0 was center (RED), index 3 was bottom (GREEN) etc.
        # Let's pick the Center Cell (Index 0 in each group) to highlight "A"
        
        # Access the hexagonal shape in the VGroups
        # Structure: cluster -> VGroup(Hex, Tower)
        
        
        # Get center hex of Cluster 1
        c1_center = cluster_group[0][0] 
        # Get center hex of Cluster 2
        c2_center = cluster_2[0][0]

        # Draw Labels
        label_A1 = Text("A", font_size=24, color=WHITE).move_to(c1_center)
        label_A2 = Text("A", font_size=24, color=WHITE).move_to(c2_center)

        # Draw "Distance" arrow
        dist_arrow = DoubleArrow(start=c1_center.get_right(), end=c2_center.get_left(), color=WHITE, buff=0.5)
        dist_text = Text("Far Apart = No Interference", font_size=18).next_to(dist_arrow, DOWN)

        self.play(
            c1_center.animate.set_fill(opacity=0.8), # Highlight
            c2_center.animate.set_fill(opacity=0.8),
            Write(label_A1),
            Write(label_A2)
        )
        
        self.play(
            GrowArrow(dist_arrow),
            Write(dist_text)
        )

        # 4. Final Capacity payoff
        final_math = MathTex(
            r"\text{New Capacity} = 832 \times N_{\text{clusters}}", 
            font_size=40, color=GREEN
        ).to_edge(DOWN, buff=1)

        self.play(Write(final_math))
        self.wait(3)