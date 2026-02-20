from manim import *

class ThreeModulationComparison(Scene):
    def construct(self):
        # Title
        title = Text("Digital Modulation", font_size=48, weight=BOLD)
        subtitle = Text("Visualizing ASK, PSK, FSK", font_size=32)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))


        intro_text = Text("Digital Modulation Techniques", font_size=36)
        self.play(Write(intro_text))
        self.wait(1)
        self.play(intro_text.animate.to_edge(UP))
        self.wait(0.5)
        
        # ===== Create Three Columns =====
        
        # Column headers
        ask_header = Text("ASK", font_size=32, color=RED, weight=BOLD)
        fsk_header = Text("FSK", font_size=32, color=BLUE, weight=BOLD)
        psk_header = Text("PSK", font_size=32, color=GREEN, weight=BOLD)
        
        ask_subtitle = Text("(Amplitude Shift Keying)", font_size=18, color=RED)
        fsk_subtitle = Text("(Frequency Shift Keying)", font_size=18, color=BLUE)
        psk_subtitle = Text("(Phase Shift Keying)", font_size=18, color=GREEN)
        
        # Position headers - three columns
        ask_header.shift(LEFT * 4 + UP * 2.5)
        fsk_header.shift(UP * 2.5)
        psk_header.shift(RIGHT * 4 + UP * 2.5)
        
        ask_subtitle.next_to(ask_header, DOWN, buff=0.1)
        fsk_subtitle.next_to(fsk_header, DOWN, buff=0.1)
        psk_subtitle.next_to(psk_header, DOWN, buff=0.1)
        
        self.play(
            Write(ask_header), Write(fsk_header), Write(psk_header)
        )
        self.play(
            Write(ask_subtitle), Write(fsk_subtitle), Write(psk_subtitle)
        )
        self.wait(0.5)
        
        # ===== Binary Data Pattern =====
        bits = [1, 0, 1, 1, 0]
        bit_duration = 1.0  # Duration for each bit in x-axis units
        
        # ===== Create Digital Signal (Square Wave) for All Three Columns =====
        
        def create_digital_signal(position, color=YELLOW):
            """Create a digital square wave based on bit pattern"""
            axes = Axes(
                x_range=[0, len(bits), 1],
                y_range=[0, 1.5, 0.5],
                x_length=2.5,
                y_length=1,
                axis_config={"include_tip": False, "include_numbers": False},
            ).shift(position)
            
            square_wave = VGroup()
            for i, bit in enumerate(bits):
                height = 1 if bit == 1 else 0.2
                if i > 0:
                    prev_height = 1 if bits[i-1] == 1 else 0.2
                    vertical = Line(
                        axes.c2p(i, prev_height),
                        axes.c2p(i, height),
                        color=color,
                        stroke_width=2
                    )
                    square_wave.add(vertical)
                
                horizontal = Line(
                    axes.c2p(i, height),
                    axes.c2p(i + 1, height),
                    color=color,
                    stroke_width=2
                )
                square_wave.add(horizontal)
            
            label = Text("Data", font_size=16, color=color)
            label.next_to(axes, LEFT, buff=0.2)
            
            return VGroup(axes, square_wave, label)
        
        # ===== Create Carrier Wave for All Three Columns =====
        
        def create_carrier_wave(position, color=YELLOW):
            """Create a carrier wave (sine wave)"""
            axes = Axes(
                x_range=[0, len(bits), 1],
                y_range=[-1.5, 1.5, 0.5],
                x_length=2.5,
                y_length=1.5,
                axis_config={"include_tip": False, "include_numbers": False},
            ).shift(position)
            
            carrier = axes.plot(
                lambda t: np.cos(8 * PI * t),
                color=color,
                stroke_width=2
            )
            
            label = Text("Carrier", font_size=16, color=color)
            label.next_to(axes, LEFT, buff=0.2)
            
            return axes, carrier, label
        
        # ===== Position Elements in Three Columns =====
        
        # ASK Column (Left)
        ask_digital = create_digital_signal(LEFT * 4 + UP * 0.8, YELLOW)
        ask_axes, ask_carrier, ask_label = create_carrier_wave(LEFT * 4 + DOWN * 2, YELLOW)
        
        # FSK Column (Center)
        fsk_digital = create_digital_signal(UP * 0.8, YELLOW)
        fsk_axes, fsk_carrier, fsk_label = create_carrier_wave(DOWN * 2, YELLOW)
        
        # PSK Column (Right)
        psk_digital = create_digital_signal(RIGHT * 4 + UP * 0.8, YELLOW)
        psk_axes, psk_carrier, psk_label = create_carrier_wave(RIGHT * 4 + DOWN * 2, YELLOW)
        
        # Show all digital signals and carriers
        self.play(
            Create(ask_digital), Create(fsk_digital), Create(psk_digital)
        )
        self.wait(0.3)
        self.play(
            Create(ask_axes), Create(ask_carrier), Create(ask_label),
            Create(fsk_axes), Create(fsk_carrier), Create(fsk_label),
            Create(psk_axes), Create(psk_carrier), Create(psk_label)
        )
        self.wait(1)
        
        # ===== Modulation Label =====
        modulation_text = Text("↓ Modulation ↓", font_size=20, color=GOLD)
        
        # ===== ASK MODULATION (Left Column) =====
        
        self.play(Indicate(ask_header, color=RED, scale_factor=1.3))
        
        # Create ASK modulated signal - VERY VISIBLE amplitude changes
        def ask_signal(t):
            """ASK: Amplitude changes dramatically based on bit"""
            bit_index = int(t / bit_duration)
            if bit_index >= len(bits):
                bit_index = len(bits) - 1
            amplitude = 1.0 if bits[bit_index] == 1 else 0.2  # Much more visible difference
            return amplitude * np.cos(8 * PI * t)
        
        ask_modulated = ask_axes.plot(
            ask_signal,
            color=RED,
            stroke_width=3
        )
        
        ask_mod_label = Text("ASK Signal", font_size=16, color=RED)
        ask_mod_label.next_to(ask_axes, LEFT, buff=0.2)
        
        # Show ASK modulation with arrow
        arrow_ask = modulation_text.copy().shift(LEFT * 4)
        self.play(FadeIn(arrow_ask))
        self.wait(0.3)
        
        self.play(
            ReplacementTransform(ask_carrier, ask_modulated),
            Transform(ask_label, ask_mod_label),
            run_time=2.5
        )
        self.play(FadeOut(arrow_ask))
        self.wait(1.5)
        
        # ===== FSK MODULATION (Center Column) =====
        
        self.play(Indicate(fsk_header, color=BLUE, scale_factor=1.3))
        
        # Create FSK modulated signal - VERY VISIBLE frequency changes
        def fsk_signal(t):
            """FSK: Frequency changes dramatically based on bit"""
            bit_index = int(t / bit_duration)
            if bit_index >= len(bits):
                bit_index = len(bits) - 1
            frequency = 14 if bits[bit_index] == 1 else 4  # Much more visible difference
            return np.cos(frequency * PI * t)
        
        fsk_modulated = fsk_axes.plot(
            fsk_signal,
            color=BLUE,
            stroke_width=3
        )
        
        fsk_mod_label = Text("FSK Signal", font_size=16, color=BLUE)
        fsk_mod_label.next_to(fsk_axes, LEFT, buff=0.2)
        
        # Show FSK modulation with arrow
        arrow_fsk = modulation_text.copy()
        self.play(FadeIn(arrow_fsk))
        self.wait(0.3)
        
        self.play(
            ReplacementTransform(fsk_carrier, fsk_modulated),
            Transform(fsk_label, fsk_mod_label),
            run_time=2.5
        )
        self.play(FadeOut(arrow_fsk))
        self.wait(1.5)
        
        # ===== PSK MODULATION (Right Column) =====
        
        self.play(Indicate(psk_header, color=GREEN, scale_factor=1.3))
        
        # Create PSK modulated signal - VERY VISIBLE phase changes
        def psk_signal(t):
            """PSK: Phase flips 180° based on bit - very visible"""
            bit_index = int(t / bit_duration)
            if bit_index >= len(bits):
                bit_index = len(bits) - 1
            phase = 0 if bits[bit_index] == 1 else PI  # 180° phase shift
            return np.cos(8 * PI * t + phase)
        
        psk_modulated = psk_axes.plot(
            psk_signal,
            color=GREEN,
            stroke_width=3
        )
        
        psk_mod_label = Text("PSK Signal", font_size=16, color=GREEN)
        psk_mod_label.next_to(psk_axes, LEFT, buff=0.2)
        
        # Show PSK modulation with arrow
        arrow_psk = modulation_text.copy().shift(RIGHT * 4)
        self.play(FadeIn(arrow_psk))
        self.wait(0.3)
        
        self.play(
            ReplacementTransform(psk_carrier, psk_modulated),
            Transform(psk_label, psk_mod_label),
            run_time=2.5
        )
        self.play(FadeOut(arrow_psk))
        self.wait(1.5)
        
        # ===== Add bit markers to show which is which =====
        
        # Add bit labels above digital signals
        bit_labels_ask = VGroup()
        bit_labels_fsk = VGroup()
        bit_labels_psk = VGroup()
        
        for i, bit in enumerate(bits):
            # ASK bit markers
            marker = Text(str(bit), font_size=14, color=RED if bit == 1 else GRAY)
            marker.move_to(ask_digital[0].c2p(i + 0.5, 1.6))
            bit_labels_ask.add(marker)
            
            # FSK bit markers
            marker = Text(str(bit), font_size=14, color=BLUE if bit == 1 else GRAY)
            marker.move_to(fsk_digital[0].c2p(i + 0.5, 1.6))
            bit_labels_fsk.add(marker)
            
            # PSK bit markers
            marker = Text(str(bit), font_size=14, color=GREEN if bit == 1 else GRAY)
            marker.move_to(psk_digital[0].c2p(i + 0.5, 1.6))
            bit_labels_psk.add(marker)
        
        self.play(
            FadeIn(bit_labels_ask),
            FadeIn(bit_labels_fsk),
            FadeIn(bit_labels_psk)
        )
        self.wait(1)
        
        # ===== Final Summary =====
        
        summary = Text(
            "Same data (1 0 1 1 0), three different modulation methods!",
            font_size=26,
            color=GOLD,
            weight=BOLD
        )
        summary.to_edge(DOWN, buff=0.3)
        
        self.play(Write(summary))
        self.wait(2)
        
        # Highlight differences
        ask_box = SurroundingRectangle(ask_modulated, color=RED, buff=0.1)
        fsk_box = SurroundingRectangle(fsk_modulated, color=BLUE, buff=0.1)
        psk_box = SurroundingRectangle(psk_modulated, color=GREEN, buff=0.1)
        
        self.play(
            Create(ask_box),
            Create(fsk_box),
            Create(psk_box)
        )
        self.wait(2)
        
        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
        self.wait(0.5)