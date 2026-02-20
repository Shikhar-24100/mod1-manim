from manim import *
import numpy as np

class Phase3_RealWorldPDP_Dark(Scene):
    def construct(self):
        # -----------------------------------------
        # 0. SETUP: DARK THEME AXES
        # -----------------------------------------
        # No background color set -> defaults to BLACK.
        
        title = Title("Real-World Power Delay Profile", color=WHITE).scale(0.9)
        self.add(title)

        # Axes config matching Figure 4.10
        # Using WHITE for visibility against dark background
        axes = Axes(
            x_range=[-70, 450, 70],
            y_range=[-30, 10, 10],
            x_length=9,
            y_length=5,
            axis_config={
                "include_tip": False, 
                "font_size": 20,
                "color": WHITE,         # <--- Lines are white
                # "label_color": WHITE,   # <--- Numbers are white
                "tick_size": 0.05
            },
            y_axis_config={"numbers_to_include": range(-30, 20, 10)}
        ).to_edge(DOWN).shift(UP*0.5 + LEFT*0.5)

        # Labels in WHITE
        x_label = axes.get_x_axis_label(Tex("Excess Delay (ns)", font_size=24, color=WHITE), edge=DOWN, buff=0.3)
        y_label = axes.get_y_axis_label(Tex("Normalized Received Power (dB Scale)", font_size=24, color=WHITE).rotate(90*DEGREES), edge=LEFT, direction=LEFT, buff=0.8)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(1)

        # -----------------------------------------
        # 1. GENERATE THE CURVE
        # -----------------------------------------
        # (Same procedural generation as before)
        np.random.seed(42) 

        def get_component(t, center, peak_power, width):
            envelope = peak_power * np.exp(-0.5 * ((t - center) / width)**2)
            jitter = np.random.uniform(0.5, 1.5)
            return envelope * jitter

        def get_textbook_pdp(t):
            noise = -22 + np.random.uniform(-1.5, 1.5)
            # Define components to match visual peaks
            components = [
                (0, 1.0, 5), (20, 0.5, 8), (45, 0.25, 10), (75, 0.1, 12),
                (100, 0.05, 15), (150, 0.02, 20), (250, 0.01, 25)
            ]
            total_power_linear = 0
            for center, peak, width in components:
                total_power_linear += get_component(t, center, peak, width)
            
            signal_db = 10 * np.log10(total_power_linear + 1e-9)
            final_signal_db = max(signal_db, noise)
            if final_signal_db > 0: final_signal_db = 0
            
            return final_signal_db

        t_values = np.linspace(0, 450, 1000)
        pdp_points = [axes.c2p(t, get_textbook_pdp(t)) for t in t_values]
        
        # Curve is WHITE for high contrast
        pdp_curve = VMobject().set_points_as_corners(pdp_points).set_color(WHITE).set_stroke(width=1.5)

        self.play(Create(pdp_curve), run_time=4, rate_func=linear)
        self.wait(1)

        # -----------------------------------------
        # 2. ANNOTATE PARAMETERS (Smart Placement)
        # -----------------------------------------
        # Using relative positioning to avoid overlaps.

        # A. Threshold Level (-20 dB)
        thresh_y = -20
        thresh_line = Line(axes.c2p(0, thresh_y), axes.c2p(450, thresh_y), color=GRAY, stroke_width=2)
        
        # Place label to the RIGHT of the graph area
        thresh_label = Text("Threshold Level = -20 dB", font_size=18, color=GRAY).next_to(axes, RIGHT, aligned_edge=UP).shift(DOWN*3.5)
        # Arrow points from label to line
        thresh_arrow = Arrow(start=thresh_label.get_left(), end=axes.c2p(400, thresh_y), buff=0.1, color=GRAY, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        
        self.play(Create(thresh_line))
        self.play(Write(thresh_label), GrowArrow(thresh_arrow))
        self.wait(1)
        
        # B. Mean Excess Delay (~45ns)
        mean_x = 45.05
        mean_line = Line(axes.c2p(mean_x, -30), axes.c2p(mean_x, -2), color=BLUE, stroke_width=2)
        
        # Place label BELOW the curve, to the right of the line
        mean_text = Text("Mean Excess Delay = 45.05 ns", font_size=18, color=BLUE).move_to(axes.c2p(200, -30))
        mean_arrow = Arrow(start=mean_text.get_left(), end=mean_line.get_center() + DOWN*1.8, buff=0.1, color=BLUE, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        
        self.play(Create(mean_line))
        self.play(Write(mean_text), GrowArrow(mean_arrow))
        self.wait(1)

        # C. RMS Delay Spread (~46ns width)
        rms_left = 45 - 23
        rms_right = 45 + 23
        rms_y = 3
        
        rms_line_l = Line(axes.c2p(rms_left, rms_y-1), axes.c2p(rms_left, rms_y+1), color=GREEN)
        rms_line_r = Line(axes.c2p(rms_right, rms_y-1), axes.c2p(rms_right, rms_y+1), color=GREEN)
        rms_conn = DoubleArrow(axes.c2p(rms_left, rms_y), axes.c2p(rms_right, rms_y), buff=0, color=GREEN, tip_length=0.15, stroke_width=2)
        
        # Place label ABOVE the connector
        rms_text = Text("RMS Delay Spread = 46.40 ns", font_size=18, color=GREEN).next_to(rms_conn, UP)
        
        self.play(Create(rms_line_l), Create(rms_line_r), GrowFromCenter(rms_conn))
        self.play(Write(rms_text))
        self.wait(1)

        # D. Max Excess Delay (< 10 dB)
        # max_x = 84
        # max_y_thresh = -10
        # level_line = DashedLine(axes.c2p(0, max_y_thresh), axes.c2p(100, max_y_thresh), color=YELLOW, stroke_width=2)
        
        # Place label to the RIGHT, above the threshold label
        # max_text = Text("Max Excess Delay < 10 dB = 84 ns", font_size=18, color=YELLOW).next_to(thresh_label, UP, aligned_edge=LEFT, buff=0.5)
        # max_arrow = Arrow(start=max_text.get_left(), end=axes.c2p(mSax_x, max_y_thresh), color=YELLOW, buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.15)

        # self.play(Create(level_line))
        # self.play(Write(max_text), GrowArrow(max_arrow))

        self.wait(5)