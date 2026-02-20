from manim import *
import numpy as np

class PhaseDistanceSceneV2(Scene):
    def construct(self):
        # === LAYOUT: LEFT = Tower + Receivers | RIGHT = Phasors + Waves ===
        title = Text("Phase Change with Distance", font_size=38)
        title.to_edge(UP, buff=0.4)
        
        self.play(Write(title), run_time=0.8)
        self.wait(0.4)

        # Divider line (visual separation)
        divider = DashedLine(UP * 3.5, DOWN * 3.5, color=GRAY, stroke_width=2)
        self.add(divider)
        
        # =====================
        # LEFT SIDE: Tower + Two Receivers
        # =====================
        
        left_center = LEFT * 3.5
        
        # Tower
        tower = SVGMobject("tower.svg").scale(0.5)
        tower.move_to(left_center + UP * 1.5)
        tower_label = Text("Tx", font_size=20).next_to(tower, DOWN, buff=0.15)
        
        # Receiver 1 (fixed) - d1
        mobile1 = SVGMobject("mobile.svg").scale(0.3)
        mobile1.move_to(left_center + DOWN * 1.0 + LEFT * 0.8)
        d1_label = Text("d₁", font_size=22, color=GREEN).next_to(mobile1, DOWN, buff=0.15)
        
        # Receiver 2 (movable) - d2
        mobile2 = SVGMobject("mobile.svg").scale(0.3)
        mobile2.move_to(left_center + DOWN * 1.0 + RIGHT * 0.8)
        d2_label = Text("d₂", font_size=22, color=ORANGE).next_to(mobile2, DOWN, buff=0.15)
        
        # Distance lines from tower to receivers
        line1 = Line(tower.get_bottom(), mobile1.get_top(), color=GREEN, stroke_width=3)
        line2 = Line(tower.get_bottom(), mobile2.get_top(), color=ORANGE, stroke_width=3)
        
        # Show left side
        self.play(
            FadeIn(tower), Write(tower_label),
            FadeIn(mobile1), Write(d1_label),
            FadeIn(mobile2), Write(d2_label),
            Create(line1), Create(line2),
            run_time=1.2
        )
        
        # Initial state text
        equal_text = Text("d₁ = d₂", font_size=24, color=YELLOW)
        equal_text.move_to(left_center + DOWN * 2.5)
        self.play(Write(equal_text), run_time=0.6)
        
        self.wait(0.5)
        
        # =====================
        # RIGHT SIDE: Phasors + Sine Waves
        # =====================
        
        right_center = RIGHT * 2.5
        
        # --- PHASOR CIRCLES ---
        phasor_center1 = right_center + UP * 1.2 + LEFT * 1.5
        phasor_center2 = right_center + UP * 1.2 + RIGHT * 1.5
        phasor_radius = 0.7
        
        # Circle 1 (d1 - fixed)
        circle1 = Circle(radius=phasor_radius, color=GREEN, stroke_width=3)
        circle1.move_to(phasor_center1)
        phasor1_label = Text("d₁", font_size=20, color=GREEN).next_to(circle1, UP, buff=0.15)
        
        # Circle 2 (d2 - will change)
        circle2 = Circle(radius=phasor_radius, color=ORANGE, stroke_width=3)
        circle2.move_to(phasor_center2)
        phasor2_label = Text("d₂", font_size=20, color=ORANGE).next_to(circle2, UP, buff=0.15)
        
        # Phasor arrows (both start at 0°)
        phasor1 = Arrow(
            phasor_center1,
            phasor_center1 + RIGHT * phasor_radius,
            color=GREEN, buff=0, stroke_width=5,
            max_tip_length_to_length_ratio=0.2
        )
        
        phasor2 = Arrow(
            phasor_center2,
            phasor_center2 + RIGHT * phasor_radius,
            color=ORANGE, buff=0, stroke_width=5,
            max_tip_length_to_length_ratio=0.2
        )
        
        # --- SINE WAVES ---
        wave_axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=5,
            y_length=1.8,
            tips=False
        ).move_to(right_center + DOWN * 1.5)
        
        # Wave 1 (fixed - d1)
        wave1 = wave_axes.plot(
            lambda x: 1.2*np.sin(x),
            color=GREEN, stroke_width=3
        )
        
        # Wave 2 (will shift - d2)
        phase_tracker = ValueTracker(0)  # Tracks phase shift
        
        wave2 = always_redraw(lambda: wave_axes.plot(
            lambda x: np.sin(x + phase_tracker.get_value()),
            color=ORANGE, stroke_width=3
        ))
        
        wave1_label = Text("Signal 1", font_size=18, color=GREEN)
        wave1_label.next_to(wave_axes, RIGHT, buff=0.3).shift(UP * 0.3)
        wave2_label = Text("Signal 2", font_size=18, color=ORANGE)
        wave2_label.next_to(wave_axes, RIGHT, buff=0.3).shift(DOWN * 0.3)
        
        # Show right side
        self.play(
            Create(circle1), Create(circle2),
            Write(phasor1_label), Write(phasor2_label),
            GrowArrow(phasor1), GrowArrow(phasor2),
            run_time=1.0
        )
        
        self.play(
            Create(wave_axes),
            Create(wave1),
            Create(wave2),
            Write(wave1_label), Write(wave2_label),
            run_time=1.0
        )
        
        # Phase display
        phase_display = always_redraw(lambda: Text(
            f"Δφ = {phase_tracker.get_value() * 180 / PI:.0f}°",
            font_size=28, color=YELLOW
        ).move_to(right_center + DOWN * 2.6))
        
        self.play(FadeIn(phase_display), run_time=0.5)
        
        self.wait(0.8)
        
        # =====================
        # ANIMATION: Move d2, watch phase change
        # =====================
        
        # Update phasor2 based on phase
        def update_phasor2(mob):
            angle = phase_tracker.get_value()
            new_end = phasor_center2 + np.array([
                phasor_radius * np.cos(angle),
                phasor_radius * np.sin(angle),
                0
            ])
            mob.put_start_and_end_on(phasor_center2, new_end)
        
        phasor2.add_updater(update_phasor2)
        
        # Update line2 as mobile2 moves
        def update_line2(mob):
            mob.put_start_and_end_on(tower.get_bottom(), mobile2.get_top())
        
        line2.add_updater(update_line2)
        
        # Update d2 label position
        def update_d2_label(mob):
            mob.next_to(mobile2, DOWN, buff=0.15)
        
        d2_label.add_updater(update_d2_label)
        
        # --- STEP 1: Move to λ/4 (90° shift) ---
        self.play(FadeOut(equal_text), run_time=0.3)
        
        moving_text = Text("Moving d₂...", font_size=22, color=YELLOW)
        moving_text.move_to(left_center + DOWN * 2.5)
        self.play(FadeIn(moving_text), run_time=0.4)
        
        # Move mobile2 right + phase shifts 90°
        self.play(
            mobile2.animate.shift(RIGHT * 0.4),
            phase_tracker.animate.set_value(PI / 2),
            run_time=2.0,
            rate_func=smooth
        )
        
        quarter_text = Text("d₂ = d₁ + λ/4", font_size=22, color=ORANGE)
        quarter_text.move_to(left_center + DOWN * 2.5)
        self.play(
            FadeOut(moving_text),
            FadeIn(quarter_text),
            run_time=0.5
        )
        
        self.wait(1.0)
        
        # --- STEP 2: Move to λ/2 (180° shift) ---
        self.play(
            FadeOut(quarter_text),
            FadeIn(moving_text),
            run_time=0.4
        )
        
        self.play(
            mobile2.animate.shift(RIGHT * 0.4),
            phase_tracker.animate.set_value(PI),
            run_time=2.0,
            rate_func=smooth
        )
        
        # Highlight 180° - CRITICAL POINT
        half_text = Text("d₂ = d₁ + λ/2", font_size=24, color=YELLOW, weight=BOLD)
        half_text.move_to(left_center + DOWN * 2.5)
        
        critical_text = Text("180° Phase Flip!", font_size=28, color=YELLOW)
        critical_text.next_to(phase_display, DOWN, buff=0.3)
        
        self.play(
            FadeOut(moving_text),
            FadeIn(half_text),
            FadeIn(critical_text),
            run_time=0.6
        )
        
        # Flash the phasors to show opposition
        self.play(
            phasor1.animate.set_stroke(width=8),
            phasor2.animate.set_stroke(width=8),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(1.0)
        
        # --- STEP 3: Continue to full λ (360° = back to 0°) ---
        self.play(
            FadeOut(half_text),
            FadeOut(critical_text),
            FadeIn(moving_text),
            run_time=0.4
        )
        
        self.play(
            mobile2.animate.shift(RIGHT * 0.8),
            phase_tracker.animate.set_value(2 * PI),
            run_time=2.5,
            rate_func=smooth
        )
        
        full_text = Text("d₂ = d₁ + λ  →  Back in phase!", font_size=22, color=YELLOW)
        full_text.move_to(left_center + DOWN * 2.5)
        
        self.play(
            FadeOut(moving_text),
            FadeIn(full_text),
            run_time=0.6
        )
        
        self.wait(1.0)
        
        # =====================
        # KEY TAKEAWAY
        # =====================
        
        phasor2.clear_updaters()
        line2.clear_updaters()
        d2_label.clear_updaters()
        
        takeaway = Text(
            "Small distance change → Big phase change",
            font_size=28, color=WHITE
        ).to_edge(DOWN, buff=0.4)
        
        self.play(
            FadeOut(full_text),
            FadeIn(takeaway, shift=UP * 0.2),
            run_time=0.8
        )
        
        self.wait(1.5)
        
        # === FADE OUT ===
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8
        )