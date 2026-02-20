from manim import *

class MorseCodeIntro(Scene):
    def construct(self):
        # Title
        title = Text("The Origins: Morse Code", font_size=42, weight=BOLD)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        
        # Show SOS in Morse
        sos_title = Text("SOS Signal", font_size=32, color=YELLOW)
        sos_title.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(sos_title))
        
        # Morse code representation
        morse_code = VGroup(
            Text("S = • • •", font_size=30),
            Text("O = — — —", font_size=30),
            Text("S = • • •", font_size=30)
        ).arrange(RIGHT, buff=1)
        morse_code.next_to(sos_title, DOWN, buff=0.5)
        self.play(Write(morse_code))
        
        self.wait(1)
        
        # Create axes for carrier signal
        axes = Axes(
            x_range=[0, 12, 1],
            y_range=[0, 2, 1],
            x_length=11,
            y_length=3,
            axis_config={"color": BLUE_D, "include_tip": False},
            tips=False
        ).shift(DOWN * 0.8)
        
        x_label = Text("Time", font_size=26).next_to(axes.x_axis, RIGHT)
        y_label = Text("Carrier\nAmplitude", font_size=24).next_to(axes.y_axis,UP)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Carrier ON/OFF indicator
        carrier_status = VGroup(
            Text("Carrier: ", font_size=26),
            Text("OFF", font_size=26, color=RED, weight=BOLD)
        ).arrange(RIGHT, buff=0.2)
        carrier_status.to_corner(UR).shift(LEFT * 0.5+DOWN*1.5)
        self.play(Write(carrier_status))
        
        # Define SOS timing pattern (shortened to fit in frame)
        # dot = 0.6 units, dash = 1.5 units, inter-element gap = 0.4 units, letter gap = 1 unit
        sos_pattern = [
            # S (• • •)
            (0, 0.56, "ON", GREEN),           # dot
    (0.56, 1.13, "OFF", None),        # gap
    (1.13, 1.69, "ON", GREEN),        # dot
    (1.69, 1.97, "OFF", None),        # gap
    (1.97, 2.54, "ON", GREEN),        # dot
    (2.54, 2.82, "OFF", None),        # letter gap
    
    # O (— — —)
    (2.82, 4.51, "ON", BLUE),         # dash
    (4.51, 4.79, "OFF", None),        # gap
    (4.79, 6.48, "ON", BLUE),         # dash
    (6.48, 6.76, "OFF", None),        # gap
    (6.76, 8.45, "ON", BLUE),         # dash
    (8.45, 8.73, "OFF", None),        # letter gap

    # S (• • •)
    (8.73, 9.29, "ON", GREEN),        # dot
    (9.29, 9.57, "OFF", None),        # gap
    (9.57, 10.14, "ON", GREEN),       # dot
    (10.14, 10.42, "OFF", None),      # gap
    (10.42, 10.99, "ON", GREEN)       # dot
        ]
        
        # Animate the carrier turning ON and OFF
        signal_parts = []
        
        for start, end, state, color in sos_pattern:
            if start >= 12:  # Skip if beyond our visible range
                break
                
            duration = min(end, 12) - start
            
            if state == "ON":
                # Draw signal ON
                line = axes.plot(
                    lambda x: 1.5,
                    x_range=[start, min(end, 12)],
                    color=color,
                    stroke_width=8
                )
                self.play(
                    Create(line),
                    carrier_status[1].animate.become(
                        Text("ON", font_size=26, color=GREEN, weight=BOLD)
                        .move_to(carrier_status[1])
                    ),
                    run_time=duration * 0.3
                )
                signal_parts.append(line)
            else:
                # Carrier OFF
                self.play(
                    carrier_status[1].animate.become(
                        Text("OFF", font_size=26, color=RED, weight=BOLD)
                        .move_to(carrier_status[1])
                    ),
                    run_time=duration * 0.3
                )
        
        self.wait(4)
        
        # Connection to ASK
        connection_text = Text(
            "This ON/OFF switching is conceptually similar to ASK!",
            font_size=28,
            color=YELLOW,
            weight=BOLD
        )
        connection_text.to_edge(DOWN).shift(UP * 0.3)
        
        self.play(Write(connection_text))
        self.wait(3)
        
        # Fade out everything
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )