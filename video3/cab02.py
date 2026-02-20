from manim import *
import numpy as np

class RealisticPDP(Scene):
    def construct(self):
        # -----------------------------------------
        # 1. SETUP AXES based on the image scales
        # -----------------------------------------
        # Y-axis: -115 to -85 dBm
        # X-axis: 0 to 100 microseconds
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[-115, -85, 5],
            x_length=9,
            y_length=5.5,
            axis_config={
                "include_tip": False,
                "font_size": 20,
            },
            y_axis_config={"numbers_to_exclude": [-85]} # Adjust top label if needed
        ).to_edge(DOWN + LEFT, buff=1)

        # Add Labels representing the real units
        x_label = axes.get_x_axis_label(
            Tex("Excess Delay Time, [$\\mu$s]", font_size=24), 
            edge=DOWN, direction=DOWN, buff=0.3
        )
        y_label = axes.get_y_axis_label(
            Tex("Received Signal Level, [dBm]", font_size=24).rotate(90*DEGREES), 
            edge=LEFT, direction=LEFT, buff=0.4
        )
        axes.add_coordinates(font_size=18)

        # -----------------------------------------
        # 2. GENERATE SYNTHETIC "REAL-WORLD" DATA
        # -----------------------------------------
        # We need many points to make it look "spiky" and continuous
        num_points = 500
        x_values = np.linspace(0, 100, num_points)
        y_values = []

        np.random.seed(42) # Fixed seed for reproducible "randomness"

        # Define major multipath clusters seen in the image
        # Format: (center_time, approx_peak_dbm, width_spread)
        clusters = [
            (2, -90, 1.5),  (6, -93, 2),    (9, -94, 1.5),  # Early strong paths
            (18, -104, 2),  (22, -106, 3),  (28, -103, 2),  # Second cluster
            (48, -104, 2),  (52, -102, 1.5),(62, -106, 3),  # Third cluster areas
            (85, -106, 4),  (95, -108, 2)                   # Late tail
        ]
        
        base_noise_floor = -113

        for x in x_values:
            # 1. Start with random noise floor
            current_signal = base_noise_floor + np.random.uniform(-1.5, 2.5)
            
            # 2. Add energy from multipath clusters
            for center, peak, spread in clusters:
                # Calculate distance from cluster center
                dist = abs(x - center)
                # If within range of a cluster, add energy with random variation
                if dist < spread * 3:
                    # Simple bell-curve shape for cluster influence
                    influence = np.exp(-0.5 * (dist / spread)**2)
                    # Calculate boost amount from noise floor to peak
                    boost = (peak - base_noise_floor) * influence
                    # Add boosted signal with highly random jitter (the "spikiness")
                    current_signal += boost * np.random.uniform(0.5, 1.5)
            
            # 3. Clip values to stay within realistic bounds of the graph
            final_y = np.clip(current_signal, -114.8, -88)
            y_values.append(final_y)

        # -----------------------------------------
        # 3. CREATE THE PLOT CURVE
        # -----------------------------------------
        # Convert (x,y) data points to Manim coordinates
        points = [axes.c2p(x, y) for x, y in zip(x_values, y_values)]
        # Use a VMobject connecting points with corners for the spiky look
        pdp_curve = VMobject().set_points_as_corners(points).set_color(WHITE).set_stroke(width=1.5)

        # -----------------------------------------
        # 4. ADD THRESHOLD LINE & ANNOTATIONS
        # -----------------------------------------
        threshold_dbm = -111.5
        threshold_line = Line(
            start=axes.c2p(0, threshold_dbm),
            end=axes.c2p(100, threshold_dbm),
            color=RED, stroke_width=2
        )

        # Text annotations from the image top-right
        annotations = VGroup(
            Text("Display Threshold = -111.5 dBm", font_size=16),
            Text("RMS Delay Spread ≈ 22.85 μs", font_size=16),
            Text("Worst Case San Francisco measurement", font_size=16),
            Text("Mansell St.", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        # Position relative to the axes coordinates
        annotations.move_to(axes.c2p(70, -90))


        # -----------------------------------------
        # 5. ANIMATION SEQUENCE
        # -----------------------------------------
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=2)
        
        # Animate the curve drawing from left to right
        self.play(Create(pdp_curve), run_time=4, rate_func=linear)
        
        self.play(Create(threshold_line))
        self.play(Write(annotations))
        
        self.wait(3)