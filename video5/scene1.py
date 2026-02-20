from manim import *
import numpy as np

class Scene1_RandomWalk(Scene):
    def construct(self):
        # Title
        title = Text("What happens when many waves arrive?", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Receiver in center
        rx = Dot(ORIGIN, radius=0.2, color=YELLOW)
        rx_label = Text("RX", font_size=24).next_to(rx, DOWN, buff=0.3)
        self.play(Create(rx), Write(rx_label))
        self.wait(0.5)
        
        # Create multiple phasor paths arriving from different angles
        num_paths = 8
        angles = np.linspace(0, 2*PI, num_paths, endpoint=False)
        colors = [BLUE, GREEN, YELLOW, PURPLE, PINK, ORANGE, TEAL, MAROON]
        
        # Generate random amplitudes and phases
        amplitudes = np.random.uniform(0.8, 1.5, num_paths)
        phases = np.random.uniform(0, 2*PI, num_paths)
        
        # Store phasors
        phasors = []
        phasor_arrows = []
        
        # Show individual paths arriving
        for i in range(num_paths):
            # Calculate phasor endpoint
            x = amplitudes[i] * np.cos(angles[i] + phases[i])
            y = amplitudes[i] * np.sin(angles[i] + phases[i])
            
            # Create arrow from receiver outward (just for visualization)
            temp_arrow = Arrow(
                ORIGIN, 
                np.array([x, y, 0]) * 1.5, 
                buff=0,
                color=colors[i],
                stroke_width=3
            )
            self.play(Create(temp_arrow), run_time=0.3)
            phasors.append((x, y))
            phasor_arrows.append(temp_arrow)
        
        # Label a few paths
        path_labels = []
        for i in [0, 2, 4]:
            label = Text(f"Path {i+1}", font_size=18, color=colors[i])
            label.next_to(phasor_arrows[i].get_end(), 
                         phasor_arrows[i].get_end() - ORIGIN, buff=0.1)
            path_labels.append(label)
            self.play(Write(label), run_time=0.3)
        
        self.wait(1)
        
        # Remove initial arrows and show tip-to-tail addition
        narration1 = Text("Vector addition: Tip-to-Tail", font_size=28)
        narration1.to_edge(DOWN)
        self.play(Write(narration1))
        
        self.play(*[FadeOut(arrow) for arrow in phasor_arrows],
                 *[FadeOut(label) for label in path_labels])
        self.wait(0.5)
        
        # Tip-to-tail addition animation
        chain_arrows = []
        current_pos = ORIGIN
        
        for i, (x, y) in enumerate(phasors):
            vec = np.array([x, y, 0])
            arrow = Arrow(
                current_pos,
                current_pos + vec,
                buff=0,
                color=colors[i],
                stroke_width=4
            )
            chain_arrows.append(arrow)
            self.play(Create(arrow), run_time=0.4)
            current_pos = current_pos + vec
        
        self.wait(1)
        
        # Draw the resultant vector (h)
        resultant = Arrow(
            ORIGIN,
            current_pos,
            buff=0,
            color=RED,
            stroke_width=8
        )
        
        h_label = MathTex("h", font_size=48, color=RED)
        h_label.next_to(resultant.get_center(), UP, buff=0.2)
        
        self.play(FadeOut(narration1))
        narration2 = Text("This resultant is our channel coefficient h", font_size=28)
        narration2.to_edge(DOWN)
        self.play(Write(narration2))
        
        self.play(Create(resultant), Write(h_label), run_time=1.5)
        self.wait(2)
        
        # Now animate the motion - phasors change randomly
        self.play(FadeOut(narration2))
        narration3 = Text("What if time passes... or the user moves?", font_size=28)
        narration3.to_edge(DOWN)
        self.play(Write(narration3))
        self.wait(1)
        
        # Animate random changes
        def update_chain(mob, dt):
            # Update phasor phases randomly
            for i in range(len(phasors)):
                phases[i] += np.random.uniform(-0.1, 0.1)
                amplitudes[i] += np.random.uniform(-0.05, 0.05)
                amplitudes[i] = np.clip(amplitudes[i], 0.5, 2.0)
                
                x = amplitudes[i] * np.cos(angles[i] + phases[i])
                y = amplitudes[i] * np.sin(angles[i] + phases[i])
                phasors[i] = (x, y)
            
            # Rebuild the chain
            current_pos = ORIGIN
            for i, (x, y) in enumerate(phasors):
                vec = np.array([x, y, 0])
                chain_arrows[i].put_start_and_end_on(current_pos, current_pos + vec)
                current_pos = current_pos + vec
            
            # Update resultant
            resultant.put_start_and_end_on(ORIGIN, current_pos)
            h_label.next_to(resultant.get_center(), UP, buff=0.2)
        
        # Animate for several seconds
        self.play(
            UpdateFromFunc(resultant, lambda m: update_chain(m, 0.1)),
            run_time=5,
            rate_func=linear
        )
        
        self.wait(1)
        
        # Final message
        self.play(FadeOut(narration3))
        conclusion1 = Text("We can't track millions of paths...", font_size=28)
        conclusion2 = Text("but we CAN track this single h", font_size=28, color=RED)
        conclusion3 = Text("Question: How does h behave statistically?", font_size=28, color=YELLOW)
        
        conclusions = VGroup(conclusion1, conclusion2, conclusion3).arrange(DOWN, buff=0.3)
        conclusions.to_edge(DOWN, buff=0.5)
        
        self.play(Write(conclusion1))
        self.wait(0.5)
        self.play(Write(conclusion2))
        self.wait(0.5)
        self.play(Write(conclusion3))
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


# To render this scene, run:
# manim -pql scene1_multipath.py Scene1_RandomWalk
# Use -pqh for high quality