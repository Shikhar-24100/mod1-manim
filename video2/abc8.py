from manim import *
import numpy as np

class InterferenceScene(Scene):
    def construct(self):
        # Title
        title = Text("Constructive vs Destructive Interference", font_size=40, weight=BOLD)
        title.to_edge(UP)
        subtitle = Text('"This is where magic — and disaster — happens"', 
                       font_size=28, color=YELLOW, slant=ITALIC)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(subtitle, shift=DOWN))
        self.wait(1)
        self.play(FadeOut(subtitle))
        
        # ===== CASE 1: CONSTRUCTIVE INTERFERENCE =====
        case1_title = Text("Case 1: Constructive Interference", 
                          font_size=32, color=WHITE).to_edge(UP, buff=0.8)
        self.play(Transform(title, case1_title))
        self.wait(0.5)
        
        # Create phasor diagram on the left
        phasor_origin = LEFT * 4 + UP * 0.5
        axes = Axes(
            x_range=[-0.5, 3, 1],
            y_range=[-0.5, 3, 1],
            x_length=3,
            y_length=3,
            tips=False
        ).shift(phasor_origin)
        
        axes_labels = VGroup(
            Text("Real", font_size=20).next_to(axes.x_axis, RIGHT, buff=0.1),
            Text("Imag", font_size=20).next_to(axes.y_axis, UP, buff=0.1)
        )
        
        self.play(Create(axes), FadeIn(axes_labels))
        
        # Two phasors pointing in same direction (0° phase difference)
        phasor1 = Arrow(axes.c2p(0, 0), axes.c2p(1.2, 0), 
                       buff=0, color=BLUE, stroke_width=6)
        phasor1_label = Text("Signal 1", font_size=18, color=BLUE).next_to(phasor1, DOWN, buff=0.2)
        
        phasor2 = Arrow(axes.c2p(1.2, 0), axes.c2p(2.4, 0), 
                       buff=0, color=RED, stroke_width=6)
        phasor2_label = Text("Signal 2", font_size=18, color=RED).next_to(phasor2, DOWN, buff=0.2)
        
        phase_text = Text("Phase difference: 0°", font_size=20, color=YELLOW)
        phase_text.next_to(axes, DOWN, buff=0.5)
        
        self.play(GrowArrow(phasor1), Write(phasor1_label))
        self.wait(0.3)
        self.play(GrowArrow(phasor2), Write(phasor2_label))
        self.play(FadeIn(phase_text))
        self.wait(0.5)
        
        # Show resultant (addition)
        resultant = Arrow(axes.c2p(0, 0), axes.c2p(2.4, 0), 
                         buff=0, color=YELLOW, stroke_width=8)
        resultant_label = Text("Resultant", font_size=20, color=YELLOW, weight=BOLD)
        resultant_label.next_to(resultant, UP, buff=0.2)
        
        plus_sign = MathTex("+", font_size=48, color=WHITE).move_to(axes.c2p(1.8, 1.2))
        equals_sign = MathTex("=", font_size=48, color=WHITE).move_to(axes.c2p(1.2, 1.8))
        
        self.play(Write(plus_sign))
        self.wait(0.3)
        self.play(
            phasor1.animate.set_opacity(0.3),
            phasor2.animate.set_opacity(0.3),
            phasor1_label.animate.set_opacity(0.3),
            phasor2_label.animate.set_opacity(0.3),
            Write(equals_sign)
        )
        self.play(GrowArrow(resultant), Write(resultant_label))
        self.wait(0.5)
        
        # Show corresponding sine waves on the right
        wave_axes = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=3,
            tips=False
        ).shift(RIGHT * 2.5 + UP * 0.5)
        
        wave_axes_label = Text("Time →", font_size=18).next_to(wave_axes.x_axis, RIGHT, buff=0.1)
        
        self.play(Create(wave_axes), FadeIn(wave_axes_label))
        
        # Individual waves - OFFSET so both are visible
        wave1 = wave_axes.plot(lambda x: np.sin(x) + 0.2, color=BLUE, stroke_width=4)
        wave2 = wave_axes.plot(lambda x: np.sin(x) - 0.2, color=RED, stroke_width=4)
        
        wave1_label = Text("Wave 1", font_size=16, color=BLUE).next_to(wave_axes, LEFT, buff=0.3).shift(UP * 0.5)
        wave2_label = Text("Wave 2", font_size=16, color=RED).next_to(wave_axes, LEFT, buff=0.3).shift(DOWN * 0.5)
        
        self.play(
            Create(wave1),
            FadeIn(wave1_label, shift=RIGHT*0.2)
        )
        self.play(
            Create(wave2),
            FadeIn(wave2_label, shift=RIGHT*0.2)
        )
        self.wait(0.3)
        
        # Combined wave (constructive)
        combined_wave = wave_axes.plot(lambda x: 2*np.sin(x), color=YELLOW, stroke_width=6)
        
        self.play(
            wave1.animate.set_opacity(0.3),
            wave2.animate.set_opacity(0.3),
            wave1_label.animate.set_opacity(0.3),
            wave2_label.animate.set_opacity(0.3),
            Create(combined_wave)
        )
        self.wait(0.5)
        
        # Text explanation
        explanation1 = VGroup(
            Text("In phase → Signals ADD→ Strong signal", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT)
        explanation1.to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(explanation1, shift=UP))
        self.wait(1.5)
        
        # Clear for Case 2
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title]
        )
        
        # ===== CASE 2: DESTRUCTIVE INTERFERENCE =====
        case2_title = Text("Case 2: Destructive Interference", 
                          font_size=32, color=WHITE).to_edge(UP, buff=0.8)
        self.play(Transform(title, case2_title))
        self.wait(0.5)
        
        # Recreate axes
        axes2 = Axes(
            x_range=[-0.5, 2, 1],
            y_range=[-2, 2, 1],
            x_length=3,
            y_length=3,
            tips=False
        ).shift(phasor_origin)
        
        axes_labels2 = VGroup(
            Text("Real", font_size=20).next_to(axes2.x_axis, RIGHT, buff=0.1),
            Text("Imag", font_size=20).next_to(axes2.y_axis, UP, buff=0.1)
        )
        
        self.play(Create(axes2), FadeIn(axes_labels2))
        
        # Two phasors pointing opposite directions (180° phase difference)
        phasor3 = Arrow(axes2.c2p(0, 0), axes2.c2p(1.2, 0), 
                       buff=0, color=BLUE, stroke_width=6)
        phasor3_label = Text("Signal 1", font_size=18, color=BLUE).next_to(phasor3, DOWN, buff=0.2)
        
        phasor4 = Arrow(axes2.c2p(0, 0), axes2.c2p(-1.2, 0), 
                       buff=0, color=RED, stroke_width=6)
        phasor4_label = Text("Signal 2", font_size=18, color=RED).next_to(phasor4, DOWN, buff=0.2)
        
        phase_text2 = Text("Phase difference: 180°", font_size=20, color=YELLOW)
        phase_text2.next_to(axes2, DOWN, buff=0.5)
        
        self.play(GrowArrow(phasor3), Write(phasor3_label))
        self.wait(0.3)
        self.play(GrowArrow(phasor4), Write(phasor4_label))
        self.play(FadeIn(phase_text2))
        self.wait(0.5)
        
        # Show near-zero resultant
        resultant2 = Dot(axes2.c2p(0, 0), color=YELLOW, radius=0.1)
        resultant2_label = Text("≈ 0", font_size=24, color=YELLOW, weight=BOLD)
        resultant2_label.next_to(resultant2, UP, buff=0.3)
        
        plus_sign2 = MathTex("+", font_size=48, color=WHITE).move_to(axes2.c2p(0.6, 1.2))
        equals_sign2 = MathTex("=", font_size=48, color=WHITE).move_to(axes2.c2p(0, 1.8))
        
        self.play(Write(plus_sign2))
        self.wait(0.3)
        self.play(
            phasor3.animate.set_opacity(0.3),
            phasor4.animate.set_opacity(0.3),
            phasor3_label.animate.set_opacity(0.3),
            phasor4_label.animate.set_opacity(0.3),
            Write(equals_sign2)
        )
        self.play(FadeIn(resultant2), Write(resultant2_label))
        self.wait(0.5)
        
        # Show corresponding sine waves
        wave_axes2 = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=3,
            tips=False
        ).shift(RIGHT * 2.5 + UP * 0.5)
        
        wave_axes_label2 = Text("Time →", font_size=18).next_to(wave_axes2.x_axis, RIGHT, buff=0.1)
        
        self.play(Create(wave_axes2), FadeIn(wave_axes_label2))
        
        # Individual waves (180° out of phase)
        wave3 = wave_axes2.plot(lambda x: np.sin(x), color=BLUE, stroke_width=3)
        wave4 = wave_axes2.plot(lambda x: -np.sin(x), color=RED, stroke_width=3)
        
        self.play(Create(wave3), Create(wave4))
        self.wait(0.3)
        
        # Combined wave (destructive - flat line)
        combined_wave2 = wave_axes2.plot(lambda x: 0, color=YELLOW, stroke_width=6)
        
        self.play(
            wave3.animate.set_opacity(0.3),
            wave4.animate.set_opacity(0.3),
            Create(combined_wave2)
        )
        self.wait(0.5)
        
        # Text explanation
        explanation2 = VGroup(
            Text("Out of phase → Signals CANCEL→ Weak/no signal", font_size=28, color=WHITE),
            # Text("", font_size=28, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT)
        explanation2.to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(explanation2, shift=UP))
        self.wait(1.5)
        
        # Clear for real-world example
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # ===== REAL-WORLD HOOK =====
        real_title = Text("Real-World hook", font_size=36)
        real_title.to_edge(UP)
        self.play(Write(real_title))
        self.wait(0.5)
        
        # Load SVG icons
        tower = SVGMobject("tower.svg").scale(0.8).shift(LEFT * 5.5 + DOWN * 0.5)
        phone = SVGMobject("mobile.svg").scale(0.6).shift(LEFT * 1 + DOWN * 0.5)
        building = SVGMobject("building.svg").scale(0.7).shift(LEFT * 3.5 + UP * 1.2)
        
        tx_label = Text("TX", font_size=20, color=RED).next_to(tower, DOWN, buff=0.2)
        rx_label = Text("RX", font_size=20, color=BLUE).next_to(phone, DOWN, buff=0.2)
        
        self.play(FadeIn(tower), FadeIn(tx_label))
        self.play(FadeIn(building))
        self.play(FadeIn(phone), FadeIn(rx_label))
        self.wait(0.5)
        
        # Create phasor diagram on the right
        phasor_origin = RIGHT * 3.5 + UP * 1.5
        phasor_axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=2.5,
            y_length=2.5,
            tips=False
        ).shift(phasor_origin)
        
        phasor_title = Text("Phasors at RX", font_size=22, weight=BOLD).next_to(phasor_axes, DOWN, buff=0.3)
        
        self.play(Create(phasor_axes), Write(phasor_title))
        
        # Initial phasors (two signals with slight phase difference)
        phasor1 = Arrow(phasor_axes.c2p(0, 0), phasor_axes.c2p(1, 0), 
                       buff=0, color=BLUE, stroke_width=5)
        phasor2 = Arrow(phasor_axes.c2p(0, 0), phasor_axes.c2p(0.8, 0.5), 
                       buff=0, color=RED, stroke_width=5)
        
        # Calculate initial resultant
        result_x = 1 + 0.8
        result_y = 0 + 0.5
        resultant = Arrow(phasor_axes.c2p(0, 0), phasor_axes.c2p(result_x, result_y), 
                         buff=0, color=YELLOW, stroke_width=6)
        
        self.play(GrowArrow(phasor1), GrowArrow(phasor2))
        self.wait(0.3)
        self.play(GrowArrow(resultant))
        self.wait(0.5)
        
        # Create sine wave display below
        wave_origin = RIGHT * 3.5 + DOWN * 1.5
        wave_axes = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=2,
            tips=False
        ).shift(wave_origin)
        
        wave_title = Text("Signal at RX", font_size=22, weight=BOLD).next_to(wave_axes, DOWN)
        
        self.play(Create(wave_axes), Write(wave_title))
        
        # Initial sine wave (strong signal)
        amplitude = np.sqrt(result_x**2 + result_y**2)
        sine_wave = wave_axes.plot(lambda x: amplitude * 0.4 * np.sin(x), 
                                   color=YELLOW, stroke_width=4)
        
        self.play(Create(sine_wave))
        self.wait(0.5)
        
        # Show signal paths from tower to phone
        # FIXED: Direct path and reflected path from building edge
        building_top = building.get_top()
        
        signal_path1 = DashedLine(tower.get_right(), phone.get_left(), 
                                  color=BLUE, stroke_width=2)
        signal_path2_part1 = DashedLine(tower.get_right(), building_top, 
                                       color=RED, stroke_width=2)
        signal_path2_part2 = DashedLine(building_top, phone.get_left(), 
                                       color=RED, stroke_width=2)
        
        path_label1 = Text("Direct", font_size=16, color=BLUE).next_to(signal_path1, DOWN, buff=0.1)
        path_label2 = Text("Reflected", font_size=16, color=RED).next_to(signal_path2_part1, UP, buff=0.1)
        
        self.play(
            Create(signal_path1),
            Create(signal_path2_part1),
            Create(signal_path2_part2)
        )
        self.play(FadeIn(path_label1), FadeIn(path_label2))
        self.wait(0.8)
        
        # Message about phone movement
        move_msg = Text("Phone moves slightly...", font_size=24, color=ORANGE, slant=ITALIC)
        move_msg.move_to(LEFT * 3 + UP * 2)
        self.play(FadeIn(move_msg))
        self.wait(0.5)
        
        # Animate phone moving and everything updating
        for i in range(4):
            # Calculate new position and phase
            move_dist = 0.4
            new_phone_pos = phone.get_center() + DOWN * move_dist
            
            # New phase difference (changing due to path length change)
            phase_change = (i + 1) * 40 * DEGREES
            new_phasor2_angle = 30 * DEGREES + phase_change
            
            # Calculate new phasor2 endpoint
            phasor2_length = 0.9
            new_p2_x = phasor2_length * np.cos(new_phasor2_angle)
            new_p2_y = phasor2_length * np.sin(new_phasor2_angle)
            
            # New resultant
            new_result_x = 1 + new_p2_x
            new_result_y = 0 + new_p2_y
            new_amplitude = np.sqrt(new_result_x**2 + new_result_y**2)
            
            new_phasor2 = Arrow(phasor_axes.c2p(0, 0), 
                               phasor_axes.c2p(new_p2_x, new_p2_y), 
                               buff=0, color=RED, stroke_width=5)
            new_resultant = Arrow(phasor_axes.c2p(0, 0), 
                                 phasor_axes.c2p(new_result_x, new_result_y), 
                                 buff=0, color=YELLOW, stroke_width=6)
            
            # New sine wave with updated amplitude
            new_sine_wave = wave_axes.plot(lambda x: new_amplitude * 0.4 * np.sin(x), 
                                          color=YELLOW, stroke_width=4)
            
            # Update signal paths - FIXED to go through building
            new_signal_path1 = DashedLine(tower.get_right(), new_phone_pos + LEFT * 0.3, 
                                         color=BLUE, stroke_width=2)
            new_signal_path2_part1 = DashedLine(tower.get_right(), building_top, 
                                               color=RED, stroke_width=2)
            new_signal_path2_part2 = DashedLine(building_top, new_phone_pos + LEFT * 0.3, 
                                               color=RED, stroke_width=2)
            
            # Animate all changes simultaneously
            self.play(
                phone.animate.move_to(new_phone_pos),
                rx_label.animate.next_to(phone.get_center() + DOWN * 0.8, DOWN, buff=0),
                Transform(phasor2, new_phasor2),
                Transform(resultant, new_resultant),
                Transform(sine_wave, new_sine_wave),
                Transform(signal_path1, new_signal_path1),
                Transform(signal_path2_part1, new_signal_path2_part1),
                Transform(signal_path2_part2, new_signal_path2_part2),
                path_label1.animate.next_to(new_signal_path1, DOWN, buff=0.1),
                run_time=0.8
            )
            self.wait(0.3)
        
        # Final message
        self.play(FadeOut(move_msg))
        final_message = VGroup(
            Text("This is why signal drops when you move inches!", font_size=28, color=WHITE, weight=BOLD),
            # Text("", font_size=30, color=RED, weight=BOLD)
        ).arrange(DOWN)
        final_message.to_edge(DOWN, buff=0.5)
        
        box = SurroundingRectangle(final_message, color=YELLOW, corner_radius=0.1)
        
        self.play(FadeIn(box), Write(final_message))
        self.wait(2.5)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)