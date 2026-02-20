from manim import *

class ConstellationDiagrams(Scene):
    def construct(self):
        # Title
        title = Text("Constellation Diagrams", font_size=48, weight=BOLD)
        subtitle = Text("Visualizing Symbols on the I-Q Plane", font_size=32)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Introduction to I-Q Plane
        self.introduce_iq_plane()
        self.wait(1)
        
        # Show each modulation constellation
        self.show_ask_constellation()
        self.wait(1)
        
        self.show_fsk_constellation()
        self.wait(1)
        
        self.show_psk_constellation()
        self.wait(1)
        
        # Compare all three
        self.compare_all_constellations()
        self.wait(2)

    def introduce_iq_plane(self):
        """Introduce the I-Q plane concept"""
        intro_text = Text("The I-Q Plane (Constellation Diagram)", font_size=36)
        self.play(Write(intro_text))
        self.wait(1)
        self.play(intro_text.animate.to_edge(UP))
        
        # Create axes
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={"color": BLUE, "include_tip": True},
        )
        
        # Labels
        x_label = MathTex("I", color=BLUE, font_size=40).next_to(axes.x_axis, RIGHT)
        y_label = MathTex("Q", color=BLUE, font_size=40).next_to(axes.y_axis, UP)
        
        i_text = Text("In-phase", font_size=24, color=BLUE).next_to(x_label, DOWN)
        q_text = Text("Quadrature", font_size=24, color=BLUE).next_to(y_label, RIGHT)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(FadeIn(i_text), FadeIn(q_text))
        self.wait(2)
        
        # Explanation
        explanation = VGroup(
            Text("Each point represents a symbol", font_size=28),
            Text("I: Amplitude of cos component", font_size=24),
            Text("Q: Amplitude of sin component", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.to_corner(UL).shift(DOWN * 1.5)
        
        self.play(Write(explanation))
        self.wait(3)
        
        # Clear for next section
        self.play(
            FadeOut(intro_text),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(i_text),
            FadeOut(q_text),
            FadeOut(explanation)
        )

    def create_iq_axes(self, scale=1.0):
        """Helper function to create I-Q axes"""
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4 * scale,
            y_length=4 * scale,
            axis_config={"color": GRAY, "include_tip": True, "tip_width": 0.15, "tip_height": 0.15},
        )
        x_label = MathTex("I", font_size=30).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = MathTex("Q", font_size=30).next_to(axes.y_axis, UP, buff=0.1)
        return VGroup(axes, x_label, y_label)

    def show_ask_constellation(self):
        """Show ASK constellation diagram"""
        title = Text("ASK - Amplitude Shift Keying", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create axes
        iq_plane = self.create_iq_axes()
        iq_plane.shift(LEFT * 3)
        self.play(Create(iq_plane))
        
        # ASK symbols (only I-axis, no Q component)
        axes = iq_plane[0]
        symbol_0 = Dot(axes.c2p(0.5, 0), color=YELLOW, radius=0.12)
        symbol_1 = Dot(axes.c2p(1.5, 0), color=YELLOW, radius=0.12)
        
        label_0 = MathTex("0", font_size=28).next_to(symbol_0, DOWN)
        label_1 = MathTex("1", font_size=28).next_to(symbol_1, DOWN)
        
        self.play(
            Create(symbol_0),
            Create(symbol_1),
            Write(label_0),
            Write(label_1)
        )
        
        # Explanation
        explanation = VGroup(
            Text("ASK Characteristics:", font_size=28, weight=BOLD),
            Text("• Symbols on I-axis only", font_size=24),
            Text("• Different amplitudes", font_size=24),
            Text("• Same phase (Q = 0)", font_size=24),
            Text("• Distance = amplitude difference", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.to_corner(UR).shift(DOWN*2)
        
        self.play(Write(explanation))
        
        # Highlight the distance
        distance_line = Line(
            symbol_0.get_center(),
            symbol_1.get_center(),
            color=YELLOW,
            stroke_width=3
        )
        distance_label = MathTex(r"d", font_size=28, color=YELLOW).next_to(distance_line, UP)
        
        self.play(Create(distance_line), Write(distance_label))
        self.wait(10)
        
        # Clear
        self.play(
            FadeOut(title),
            FadeOut(iq_plane),
            FadeOut(symbol_0),
            FadeOut(symbol_1),
            FadeOut(label_0),
            FadeOut(label_1),
            FadeOut(explanation),
            FadeOut(distance_line),
            FadeOut(distance_label)
        )

    def show_fsk_constellation(self):
        """Show FSK constellation diagram"""
        title = Text("FSK - Frequency Shift Keying", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create axes
        iq_plane = self.create_iq_axes()
        iq_plane.shift(LEFT * 3)
        self.play(Create(iq_plane))
        
        # FSK symbols (orthogonal, perpendicular positions)
        axes = iq_plane[0]
        symbol_0 = Dot(axes.c2p(1.2, 0), color=YELLOW, radius=0.12)
        symbol_1 = Dot(axes.c2p(0, 1.2), color=YELLOW, radius=0.12)
        
        label_0 = MathTex("f_1", font_size=28).next_to(symbol_0, DOWN)
        label_1 = MathTex("f_2", font_size=28).next_to(symbol_1, LEFT)
        
        self.play(
            Create(symbol_0),
            Create(symbol_1),
            Write(label_0),
            Write(label_1)
        )
        
        # Explanation
        explanation = VGroup(
            Text("FSK Characteristics:", font_size=28, weight=BOLD),
            Text("• Orthogonal frequencies", font_size=24),
            Text("• Symbols at 90° apart", font_size=24),
            Text("• Same amplitude, different freq", font_size=24),
            Text("• Maximum separation in 2D", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.to_corner(UR).shift(DOWN*2)
        
        self.play(Write(explanation))
        
        # Show orthogonality
        line_0 = Line(axes.c2p(0, 0), symbol_0.get_center(), color=RED, stroke_width=2)
        line_1 = Line(axes.c2p(0, 0), symbol_1.get_center(), color=GREEN, stroke_width=2)
        
        angle_arc = Arc(
            radius=0.4,
            start_angle=0,
            angle=PI/2,
            color=YELLOW,
            arc_center=axes.c2p(0, 0)
        )
        angle_label = MathTex("90°", font_size=24, color=YELLOW).move_to(axes.c2p(0.5, 0.5))
        
        self.play(Create(line_0), Create(line_1))
        self.play(Create(angle_arc), Write(angle_label))
        self.wait(10)
        
        # Clear
        self.play(
            FadeOut(title),
            FadeOut(iq_plane),
            FadeOut(symbol_0),
            FadeOut(symbol_1),
            FadeOut(label_0),
            FadeOut(label_1),
            FadeOut(explanation),
            FadeOut(line_0),
            FadeOut(line_1),
            FadeOut(angle_arc),
            FadeOut(angle_label)
        )

    def show_psk_constellation(self):
        """Show PSK constellation diagrams (BPSK and QPSK)"""
        title = Text("PSK - Phase Shift Keying", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Show BPSK first
        subtitle_bpsk = Text("BPSK (2 symbols)", font_size=28)
        subtitle_bpsk.next_to(title, DOWN)
        self.play(Write(subtitle_bpsk))
        
        # Create axes for BPSK
        iq_plane_bpsk = self.create_iq_axes()
        iq_plane_bpsk.shift(LEFT * 3 + UP * 0.5)
        self.play(Create(iq_plane_bpsk))
        
        # BPSK symbols (180° apart)
        axes_bpsk = iq_plane_bpsk[0]
        symbol_0_bpsk = Dot(axes_bpsk.c2p(-1.2, 0), color=YELLOW, radius=0.12)
        symbol_1_bpsk = Dot(axes_bpsk.c2p(1.2, 0), color=YELLOW, radius=0.12)
        
        label_0_bpsk = MathTex("0", font_size=28).next_to(symbol_0_bpsk, DOWN)
        label_1_bpsk = MathTex("1", font_size=28).next_to(symbol_1_bpsk, DOWN)
        
        self.play(
            Create(symbol_0_bpsk),
            Create(symbol_1_bpsk),
            Write(label_0_bpsk),
            Write(label_1_bpsk)
        )
        
        # Show phase difference
        line_0 = Line(axes_bpsk.c2p(0, 0), symbol_0_bpsk.get_center(), color=RED, stroke_width=2)
        line_1 = Line(axes_bpsk.c2p(0, 0), symbol_1_bpsk.get_center(), color=GREEN, stroke_width=2)
        phase_label = MathTex("180°", font_size=24, color=YELLOW).move_to(axes_bpsk.c2p(0, -0.5))
        
        self.play(Create(line_0), Create(line_1), Write(phase_label))
        self.wait(5)
        
        # Transition to QPSK
        self.play(
            FadeOut(subtitle_bpsk),
            FadeOut(iq_plane_bpsk),
            FadeOut(symbol_0_bpsk),
            FadeOut(symbol_1_bpsk),
            FadeOut(label_0_bpsk),
            FadeOut(label_1_bpsk),
            FadeOut(line_0),
            FadeOut(line_1),
            FadeOut(phase_label)
        )
        
        # Show QPSK
        subtitle_qpsk = Text("QPSK (4 symbols)", font_size=28)
        subtitle_qpsk.next_to(title, DOWN)
        self.play(Write(subtitle_qpsk))
        
        # Create axes for QPSK
        iq_plane = self.create_iq_axes()
        iq_plane.shift(LEFT * 3)
        self.play(Create(iq_plane))
        
        # QPSK symbols (90° apart)
        axes = iq_plane[0]
        r = 1.2
        symbol_00 = Dot(axes.c2p(r*np.cos(3*PI/4), r*np.sin(3*PI/4)), color=YELLOW, radius=0.12)
        symbol_01 = Dot(axes.c2p(r*np.cos(PI/4), r*np.sin(PI/4)), color=YELLOW, radius=0.12)
        symbol_11 = Dot(axes.c2p(r*np.cos(-PI/4), r*np.sin(-PI/4)), color=YELLOW, radius=0.12)
        symbol_10 = Dot(axes.c2p(r*np.cos(-3*PI/4), r*np.sin(-3*PI/4)), color=YELLOW, radius=0.12)
        
        label_00 = MathTex("00", font_size=24).next_to(symbol_00, UL, buff=0.1)
        label_01 = MathTex("01", font_size=24).next_to(symbol_01, UR, buff=0.1)
        label_11 = MathTex("11", font_size=24).next_to(symbol_11, DR, buff=0.1)
        label_10 = MathTex("10", font_size=24).next_to(symbol_10, DL, buff=0.1)
        
        self.play(
            Create(symbol_00),
            Create(symbol_01),
            Create(symbol_11),
            Create(symbol_10),
            Write(label_00),
            Write(label_01),
            Write(label_11),
            Write(label_10)
        )
        
        # Explanation
        explanation = VGroup(
            Text("PSK Characteristics:", font_size=28, weight=BOLD),
            Text("• Constant amplitude", font_size=24),
            Text("• Equally spaced phases", font_size=24),
            Text("• Symbols on a circle", font_size=24),
            Text("• QPSK: 90° phase separation", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.to_corner(UR).shift(DOWN*2)
        
        self.play(Write(explanation))
        
        # Draw circle to show equal amplitude
        circle = Circle(radius=r*axes.x_axis.unit_size, color=YELLOW, stroke_width=2)
        circle.move_to(axes.c2p(0, 0))
        self.play(Create(circle))
        
        self.wait(10)
        
        # Clear
        self.play(
            FadeOut(title),
            FadeOut(subtitle_qpsk),
            FadeOut(iq_plane),
            FadeOut(symbol_00),
            FadeOut(symbol_01),
            FadeOut(symbol_11),
            FadeOut(symbol_10),
            FadeOut(label_00),
            FadeOut(label_01),
            FadeOut(label_11),
            FadeOut(label_10),
            FadeOut(explanation),
            FadeOut(circle)
        )

    def compare_all_constellations(self):
        """Compare all three constellations side by side"""
        title = Text("Constellation Comparison", font_size=40, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create three sets of axes
        scale = 0.8
        
        # ASK
        ask_title = Text("ASK", font_size=28, color=YELLOW)
        ask_plane = self.create_iq_axes(scale)
        ask_group = VGroup(ask_title, ask_plane).arrange(DOWN, buff=0.3)
        ask_group.shift(LEFT * 4)
        
        axes_ask = ask_plane[0]
        ask_sym0 = Dot(axes_ask.c2p(0.5, 0), color=YELLOW, radius=0.1)
        ask_sym1 = Dot(axes_ask.c2p(1.3, 0), color=YELLOW, radius=0.1)
        
        # FSK
        fsk_title = Text("FSK", font_size=28, color=YELLOW)
        fsk_plane = self.create_iq_axes(scale)
        fsk_group = VGroup(fsk_title, fsk_plane).arrange(DOWN, buff=0.3)
        
        axes_fsk = fsk_plane[0]
        fsk_sym0 = Dot(axes_fsk.c2p(1.0, 0), color=YELLOW, radius=0.1)
        fsk_sym1 = Dot(axes_fsk.c2p(0, 1.0), color=YELLOW, radius=0.1)
        
        # QPSK
        qpsk_title = Text("QPSK", font_size=28, color=YELLOW)
        qpsk_plane = self.create_iq_axes(scale)
        qpsk_group = VGroup(qpsk_title, qpsk_plane).arrange(DOWN, buff=0.3)
        qpsk_group.shift(RIGHT * 4)
        
        axes_qpsk = qpsk_plane[0]
        r = 1.0
        qpsk_sym0 = Dot(axes_qpsk.c2p(r*np.cos(3*PI/4), r*np.sin(3*PI/4)), color=YELLOW, radius=0.1)
        qpsk_sym1 = Dot(axes_qpsk.c2p(r*np.cos(PI/4), r*np.sin(PI/4)), color=YELLOW, radius=0.1)
        qpsk_sym2 = Dot(axes_qpsk.c2p(r*np.cos(-PI/4), r*np.sin(-PI/4)), color=YELLOW, radius=0.1)
        qpsk_sym3 = Dot(axes_qpsk.c2p(r*np.cos(-3*PI/4), r*np.sin(-3*PI/4)), color=YELLOW, radius=0.1)
        
        # Animate all together
        self.play(
            Create(ask_group),
            Create(fsk_group),
            Create(qpsk_group)
        )
        
        self.play(
            Create(ask_sym0), Create(ask_sym1),
            Create(fsk_sym0), Create(fsk_sym1),
            Create(qpsk_sym0), Create(qpsk_sym1),
            Create(qpsk_sym2), Create(qpsk_sym3)
        )
        
        # Key differences
        # key_points = VGroup(
        #     Text("Key Observations:", font_size=28, weight=BOLD),
        #     Text("• ASK: 1D (amplitude only)", font_size=22),
        #     Text("• FSK: 2D orthogonal", font_size=22),
        #     Text("• PSK: 2D circular (best)", font_size=22),
        # ).arrange(RIGHT, aligned_edge=LEFT, buff=0.2)
        # key_points.to_edge(LEFT).shift(DOWN * 0.5)
        
        # self.play(Write(key_points))
        self.wait(10)