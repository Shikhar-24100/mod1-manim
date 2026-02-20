from manim import *
import numpy as np

class TimeVaryingChannel(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        COLOR_STATIC = BLUE_C
        COLOR_DYNAMIC = YELLOW
        
        # --- PART 1: THE STATIC SCENARIO (Lecture 4) ---
        
        # Title
        title_static = Text("Lecture 4: Static Channel (Frozen)", font_size=36).to_edge(UP)
        self.play(Write(title_static))

        # The Old Equation
        eq_static = MathTex(
            r"h(\tau)", r"=", r"\sum_{i=1}^{N}", r"a_i", r"e^{-j \phi_i}", r"\delta(\tau - \tau_i)"
        ).scale(1.2).shift(UP*2)
        
        self.play(Write(eq_static))
        self.wait(1)

        # The Axes
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1.5, 0.5],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": True, "color": WHITE},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": []}
        ).shift(DOWN*1)
        
        labels = ax.get_axis_labels(x_label=r"\tau \text{ (Delay)}", y_label=r"|h|")
        self.play(Create(ax), Write(labels))

        # Static Pulses
        delays_static = [2, 5, 8]
        amps_static = [1.2, 0.8, 0.4]
        
        static_group = VGroup()
        for d, a in zip(delays_static, amps_static):
            line = Line(ax.c2p(d, 0), ax.c2p(d, a), color=COLOR_STATIC, stroke_width=4)
            dot = Dot(ax.c2p(d, a), color=COLOR_STATIC)
            static_group.add(VGroup(line, dot))
            
        self.play(Create(static_group))
        self.wait(1)
        

        # --- PART 2: THE TRANSITION (Lecture 5) ---
        
        # Animate the Title Change
        title_dynamic = Text("Lecture 5: Time-Varying Channel (Mobile)", font_size=36, color=COLOR_DYNAMIC).to_edge(UP)
        self.play(Transform(title_static, title_dynamic))

        # Transform the Equation
        eq_dynamic = MathTex(
            r"h(t, \tau)", r"=", r"\sum_{i=1}^{N}", 
            r"a_i(t, \tau)", 
            r"e^{-j 2\pi f_c \tau_i(t)}", 
            r"\delta(\tau - \tau_i(t))" 
        ).scale(1.0).move_to(eq_static)

        eq_dynamic.set_color_by_tex("t", COLOR_DYNAMIC)

        self.play(TransformMatchingTex(eq_static, eq_dynamic))
        self.wait(1)

        note = Tex(r"Parameters now depend on wall-clock time $t$", font_size=24, color=GRAY)
        note.next_to(eq_dynamic, DOWN)
        self.play(FadeIn(note))

        # --- PART 3: THE DYNAMIC ANIMATION ---
        
        time_tracker = ValueTracker(0)

        def get_dynamic_pulses():
            t = time_tracker.get_value()
            new_group = VGroup()
            
            # Pulse logic
            d1 = 2 + 0.3 * np.sin(t)
            a1 = 1.2 + 0.2 * np.cos(2*t)
            c1 = interpolate_color(BLUE, RED, (np.sin(t*3) + 1)/2)
            
            d2 = 5 - 0.5 * np.sin(0.8*t)
            a2 = 0.8 + 0.3 * np.sin(3*t)
            c2 = interpolate_color(GREEN, PURPLE, (np.cos(t*4) + 1)/2)
            
            d3 = 8 + 0.2 * np.cos(t)
            a3 = 0.4 + 0.1 * np.sin(5*t)
            c3 = interpolate_color(YELLOW, PINK, (np.sin(t*2) + 1)/2)

            for d, a, c in [(d1, a1, c1), (d2, a2, c2), (d3, a3, c3)]:
                a = max(0, a) 
                line = Line(ax.c2p(d, 0), ax.c2p(d, a), color=c, stroke_width=4)
                dot = Dot(ax.c2p(d, a), color=c)
                new_group.add(VGroup(line, dot))
            
            return new_group

        dynamic_pulses = always_redraw(get_dynamic_pulses)
        
        self.remove(static_group)
        self.add(dynamic_pulses)
        
        # --- FIX APPLIED HERE: Added Z-axis (0) to coordinates ---
        play_icon = Polygon([0,0,0], [0,1,0], [0.8, 0.5, 0], color=WHITE, fill_opacity=1).scale(0.5).to_corner(DR)
        play_text = Text("t > 0", font_size=24).next_to(play_icon, DOWN)
        self.play(FadeIn(play_icon), Write(play_text))

        self.play(time_tracker.animate.set_value(10), run_time=8, rate_func=linear)
        
        self.wait()