from manim import *
import numpy as np
import random

# Set seed for reproducibility if desired, otherwise remove
random.seed(42)
np.random.seed(42)

class MultipathComparisonFixed(Scene):
    def construct(self):
        # --- LEFT SIDE: REAL WORLD SETUP (Same as before) ---
        # Ensure tower.svg, building.svg, plane.svg, mobile.svg are in assets folder
        # model_title = Text("The Impulse Response Model of A Wireless Channel")
        model_title = Title("The Impulse Response Model of A Wireless Channel").scale(0.9)
        tower = SVGMobject("tower.svg").scale(0.6).shift(LEFT * 6 + UP * 0.5)
        building = SVGMobject("building.svg").scale(0.6).shift(LEFT * 3 + UP * 1.5)
        plane = SVGMobject("jet.svg").scale(0.3).shift(LEFT * 2.5 + DOWN * 2)
        mobile = SVGMobject("mobile.svg").scale(0.35).shift(LEFT * 0.5 + UP * 1.5)

        b_text = Text("Building (d1)", font_size=18).next_to(building, UP)
        p_text = Text("Plane (d2)", font_size=18).next_to(plane, DOWN)
        comp_text = Text("d1 << d2", font_size=20, color=YELLOW).move_to(LEFT * 2.8)

        def get_paths(target, color):
            paths = VGroup()
            for i in range(4):
                p = VMobject(color=color, stroke_width=1.5)
                # Simple path approximation
                start = tower.get_center()
                mid = target.get_center() + np.array([0, i*0.1 - 0.2, 0])
                end = mobile.get_center()
                p.set_points_as_corners([start, mid, end])
                paths.add(p)
            return paths

        blue_paths = get_paths(building, GREEN)
        orange_paths = get_paths(plane, YELLOW)

        real_world = VGroup(tower, building, plane, mobile, b_text, p_text, comp_text)
        self.add(real_world)
        
        # --- EXPANDING WAVES FROM TRANSMITTER ---
        tx = tower  # Transmitter is the tower
        wave_time = ValueTracker(0)
        
        def get_expanding_waves():
            t = wave_time.get_value()
            waves = VGroup()
            
            # Create multiple wave rings at different phases
            for phase_offset in np.linspace(0, 2*PI, 6):
                for ring_idx in range(8):
                    radius = 0.3 + (t * 0.5 + ring_idx * 0.4 + phase_offset) % 5
                    circle = Circle(
                        radius=radius,
                        color=BLUE,
                        stroke_width=2,
                        fill_opacity=0
                    ).move_to(tx.get_center())
                    
                    # Fade opacity as radius grows
                    opacity = max(0, 1 - (radius / 5))
                    circle.set_stroke(opacity=opacity)
                    waves.add(circle)
            
            return waves
        
        expanding_waves = always_redraw(get_expanding_waves)
        self.add(expanding_waves)
        
        # Animate waves for 8 seconds
        self.play(wave_time.animate.set_value(8), run_time=8, rate_func=linear)
        
        # Freeze the waves (remove the updater so they stop animating)
        self.remove(expanding_waves)
        final_waves = get_expanding_waves()
        self.add(final_waves)
        self.wait(0.5)
        
        # Now show the paths
        self.play(Create(blue_paths), Create(orange_paths), run_time=1.5)
        self.wait(4)

        # --- RIGHT SIDE: THE TWO DIAGRAMS ---

        # 1. TOP DIAGRAM: Non-Resolvable (Fluctuating Clusters)
        top_axes = Axes(x_range=[0, 10], y_range=[0, 4], x_length=5, y_length=2.5,
                        axis_config={"include_tip": False, "include_ticks": False}).shift(RIGHT * 3.5 + UP * 2)
        # top_labels = top_axes.get_axis_labels(x_label="Time", y_label="Power")
        top_x_lbl = top_axes.get_x_axis_label(MathTex("t", font_size=24), edge=RIGHT, direction=DOWN)
        top_y_lbl = top_axes.get_y_axis_label(MathTex("|h(t)|", font_size=24), edge=UP, direction=LEFT, buff=0.2)
        top_title = Text("Non-Resolvable (causes  fading)", color=WHITE, font_size=20).next_to(top_axes, UP)

        def create_fluctuating_cluster(center, color, factor):
            cluster = VGroup()
            for _ in range(30):
                x_pos = center + np.random.uniform(-0.3, 0.3)
                base_height = np.random.uniform(1, 2.5)
                # height = base_height * factor
                height = (base_height * factor) ** 1.5
                line = Line(
                    top_axes.c2p(x_pos, 0),
                    top_axes.c2p(x_pos, height),
                    color=color,
                    stroke_width=1
                )
                cluster.add(line)
            return cluster

        # Create initial static clusters
        top_c1 = create_fluctuating_cluster(2.5, GREEN, 2.5)
        top_c2 = create_fluctuating_cluster(7.5, YELLOW, 0.1)
        
        # Add sent impulse to top diagram as well
        top_sent_impulse = Arrow(top_axes.c2p(0, 0), top_axes.c2p(0, 3.2), color=RED, buff=0, stroke_width=4)
        top_sent_impulse.set_stroke(width=4)
        
        top_diag = VGroup(top_axes, top_c1, top_c2, top_sent_impulse, top_title, top_x_lbl)

        self.wait(4)
        # 2. BOTTOM DIAGRAM: Resolvable (Distinct Impulses)
        bot_axes = Axes(x_range=[0, 10], y_range=[0, 4], x_length=5, y_length=2.5,
                        axis_config={"include_tip": False, "include_ticks": False}).shift(RIGHT * 3.5 + DOWN * 1.5)
        # bot_labels = bot_axes.get_axis_labels(x_label="Time", y_label="Avg Power")
        bot_title = Text("Resolvable (causes ISI)", color=WHITE, font_size=20).next_to(bot_axes, UP)
        bot_x_lbl = bot_axes.get_x_axis_label(MathTex("t", font_size=24), edge=RIGHT, direction=DOWN)
        bot_y_lbl = bot_axes.get_y_axis_label(MathTex("|h(t)|", font_size=24), edge=UP, direction=LEFT, buff=0.2)

        # Clean, solid impulses representing the average
        impulse1 = Arrow(bot_axes.c2p(2.5, 0), bot_axes.c2p(2.5, 2.4), color=GREEN, buff=0, stroke_width=5)
        impulse2 = Arrow(bot_axes.c2p(7.5, 0), bot_axes.c2p(7.5, 1.7), color=YELLOW, buff=0, stroke_width=5)
        
        # Sent impulse (original signal - distinct dashed style)
        sent_impulse = Arrow(bot_axes.c2p(0, 0), bot_axes.c2p(0, 3.2), color=RED, buff=0, stroke_width=4)
        sent_impulse.set_stroke(width=4)
        sent_impulse_label = Text("Sent Impulse", font_size=14, color=RED).next_to(sent_impulse, UP, buff=0.1)
        
        bot_diag = VGroup(bot_axes, impulse1, impulse2, sent_impulse, bot_x_lbl)


        # --- ANIMATION SEQUENCE ---

        # 1. Show the messy reality first with fluctuation
        
        # Define the shimmering effect (Rayleigh Fading simulation)
        def shimmer(mobject):
            for line in mobject:
                # Keep x position, randomize y height randomly
                current_x = top_axes.p2c(line.get_start())[0]
                new_h = np.random.uniform(0.5, 3.0)
                line.put_start_and_end_on(
                    top_axes.c2p(current_x, 0),
                    top_axes.c2p(current_x, new_h)
                )

        # Add fluctuation updaters BEFORE drawing
        top_c1.add_updater(shimmer)
        top_c2.add_updater(shimmer)
        
        # Draw with fluctuation happening in real time
        self.play(Write(top_axes), Write(top_title))
        self.play(Create(top_c1), Create(top_c2), Create(top_sent_impulse), run_time=1.5)
        
        # Wait while they fluctuate visibly for 3 seconds
        self.wait(3)

        # Stop fluctuation (they freeze in their last random state)
        top_c1.remove_updater(shimmer)
        top_c2.remove_updater(shimmer)

        # 2. NEW ANIMATION SEQUENCE FOR BOTTOM DIAGRAM
        # Show axes only first (no signals yet)
        self.play(Write(bot_axes), Write(bot_title))
        self.wait(1)
        
        # Symbol 1 appears on TX axis
        sym1_tx = Arrow(bot_axes.c2p(2.5, 0), bot_axes.c2p(2.5, 2.4), color=GREEN, buff=0, stroke_width=5)
        self.play(Create(sym1_tx), run_time=0.5)
        self.wait(2)
        
        # Symbol 1 appears as 4 separated copies on RX axis (no ISI yet)
        sym1_rx_copies = VGroup()
        rx_positions_1 = [1.2, 2.0, 2.8, 3.6]  # Separated positions
        for pos in rx_positions_1:
            arrow = Arrow(bot_axes.c2p(pos, 0), bot_axes.c2p(pos, 2.4), color=GREEN, buff=0, stroke_width=3)
            sym1_rx_copies.add(arrow)
        self.play(Create(sym1_rx_copies), run_time=0.8)
        self.wait(2)
        
        # Symbol 2 appears on TX axis
        sym2_tx = Arrow(bot_axes.c2p(7.5, 0), bot_axes.c2p(7.5, 1.7), color=YELLOW, buff=0, stroke_width=5)
        self.play(Create(sym2_tx), run_time=0.5)
        self.wait(2)
        
        # Symbol 2 appears as 4 separated copies on RX axis (no ISI yet)
        sym2_rx_copies = VGroup()
        rx_positions_2 = [6.2, 7.0, 7.8, 8.6]  # Separated positions
        for pos in rx_positions_2:
            arrow = Arrow(bot_axes.c2p(pos, 0), bot_axes.c2p(pos, 1.7), color=YELLOW, buff=0, stroke_width=3)
            sym2_rx_copies.add(arrow)
        self.play(Create(sym2_rx_copies), run_time=0.8)
        self.wait(2)
        
        # Now move TX symbols closer to show ISI/smudging
        # Also animate RX copies to move toward TX positions and reduce from 4 to 3 copies
        self.play(
            sym1_tx.animate.shift(RIGHT * 0.8),
            sym2_tx.animate.shift(LEFT * 0.8),
            # Move RX green copies toward the green TX symbol
            sym1_rx_copies[0].animate.shift(RIGHT * 1.0),
            sym1_rx_copies[1].animate.shift(RIGHT * 0.8),
            sym1_rx_copies[2].animate.shift(RIGHT * 0.6),
            sym1_rx_copies[3].animate.shift(RIGHT * 0.4),
            # Move RX yellow copies toward the yellow TX symbol
            sym2_rx_copies[0].animate.shift(LEFT * 0.4),
            sym2_rx_copies[1].animate.shift(LEFT * 0.6),
            sym2_rx_copies[2].animate.shift(LEFT * 0.8),
            sym2_rx_copies[3].animate.shift(LEFT * 1.0),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Now fade out one copy from each to go from 4 -> 3 copies
        self.play(
            FadeOut(sym1_rx_copies[3]),
            FadeOut(sym2_rx_copies[3]),
            run_time=0.5
        )
        self.wait(1)
        
        # Fade out the remaining 3 copies
        self.play(FadeOut(sym1_rx_copies[0]), FadeOut(sym1_rx_copies[1]), FadeOut(sym1_rx_copies[2]),
                  FadeOut(sym2_rx_copies[0]), FadeOut(sym2_rx_copies[1]), FadeOut(sym2_rx_copies[2]),
                  run_time=0.5)
        
        smudged_result = VGroup()
        # Create overlapping green copies (showing smudging)
        smudged_green_positions = [2.0, 2.3, 2.6, 2.9]
        for pos in smudged_green_positions:
            arrow = Arrow(bot_axes.c2p(pos, 0), bot_axes.c2p(pos, 2.4), color=GREEN, buff=0, stroke_width=3)
            arrow.set_opacity(0.6)  # Semi-transparent to show overlap
            smudged_result.add(arrow)
        
        # Create overlapping yellow copies (showing smudging)
        smudged_yellow_positions = [6.7, 7.0, 7.3, 7.6]
        for pos in smudged_yellow_positions:
            arrow = Arrow(bot_axes.c2p(pos, 0), bot_axes.c2p(pos, 1.7), color=YELLOW, buff=0, stroke_width=3)
            arrow.set_opacity(0.6)  # Semi-transparent to show overlap
            smudged_result.add(arrow)
        
        self.play(Create(smudged_result), run_time=0.8)
        self.wait(3)
        
        # --- FINAL SECTION: SMOOTH TRANSITION ---

        # 1. Prepare the new elements that weren't in the previous scene
        tau0_label = MathTex(r"\tau_0", font_size=24).next_to(bot_axes.c2p(2.5, 0), DOWN)
        tau1_label = MathTex(r"\tau_1", font_size=24).next_to(bot_axes.c2p(7.5, 0), DOWN)
        t0_label = MathTex(r"t = 0", font_size=24).next_to(bot_axes.c2p(0, 0), DOWN)
        tx_impulse_label = Text("(tx impulse)", font_size=16, color=RED).next_to(t0_label, DOWN, buff=0.1)

        formula = MathTex(
            r"h(\tau) = \sum_{i=0}^{L-1} a_i \delta(\tau - \tau_i)",
            font_size=40,
            color=WHITE
        )

        # 2. Define the Target Positions
        # We move the title to the top
        model_title_target = model_title.copy().to_edge(UP, buff=0.5)
        
        # Position formula below title target
        formula.next_to(model_title_target, DOWN, buff=0.4)
        
        # Create box AFTER positioning the formula
        box = SurroundingRectangle(formula, color=YELLOW, buff=0.2)
        
        # Create a new bot_diag for transition (without the close symbols)
        bot_diag_transition = VGroup(bot_axes, sym1_tx, sym2_tx, sent_impulse, bot_x_lbl)
        
        # Scale and position for target
        bot_diag_target = bot_diag_transition.copy().scale(1.1).next_to(formula, DOWN, buff=0.8)
        
        # Align new labels/impulses to the MOVING target axes
        tau0_label.next_to(bot_diag_target[0].c2p(2.5, 0), DOWN)
        tau1_label.next_to(bot_diag_target[0].c2p(7.5, 0), DOWN)
        t0_label.next_to(bot_diag_target[0].c2p(0, 0), DOWN)
        tx_impulse_label.next_to(t0_label, DOWN, buff=0.1)

        # 3. THE SMOOTH TRANSITION PLAY
        self.play(
            FadeOut(real_world),
            FadeOut(final_waves),
            FadeOut(top_diag),
            FadeOut(blue_paths),
            FadeOut(orange_paths),
            FadeOut(bot_title),
            FadeOut(smudged_result),
            FadeOut(sym1_tx),
            FadeOut(sym2_tx)
        )
        
        # Create fresh impulses for the final diagram
        final_impulse1 = Arrow(bot_axes.c2p(2.5, 0), bot_axes.c2p(2.5, 2.4), color=GREEN, buff=0, stroke_width=5)
        final_impulse2 = Arrow(bot_axes.c2p(7.5, 0), bot_axes.c2p(7.5, 1.7), color=YELLOW, buff=0, stroke_width=5)
        final_sent_impulse = Arrow(bot_axes.c2p(0, 0), bot_axes.c2p(0, 3.2), color=RED, buff=0, stroke_width=4)
        final_sent_impulse.set_stroke(width=4)
        
        final_diag = VGroup(bot_axes, final_impulse1, final_impulse2, final_sent_impulse, bot_x_lbl)
        final_diag_target = final_diag.copy().scale(1.1).next_to(formula, DOWN, buff=0.8)
        
        self.play(
            # Smoothly transform the graph and title to new positions
            ReplacementTransform(final_diag, final_diag_target),
            ReplacementTransform(model_title, model_title_target),
            
            # Fade out the "messy" real world and top graph
            FadeIn(formula),
            FadeIn(box),
            FadeIn(tau0_label),
            FadeIn(tau1_label),
            FadeIn(t0_label),
            FadeIn(tx_impulse_label),
            
            run_time=0.5,
            rate_func=bezier([0, 0, 1, 1]) # Smooth start and end
        )
        self.play(Create(box), run_time=1)

        self.wait(5)