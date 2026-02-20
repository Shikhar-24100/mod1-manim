from manim import *
import numpy as np

class FriisTransmissionComplete(ThreeDScene):
    def construct(self):
        title = Text("Parameter breakdown with equation highlighting", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        
        self.wait(1)
        self.animation_7_parameters()
        self.wait(2)
        
    
    def animation_7_parameters(self):
        """Animation 7: Parameter breakdown with equation highlighting"""
        
        # Clear previous elements except title
        
        
        # Show full Friis equation
        # subtitle = Text("Understanding Each Parameter", font_size=36).next_to(self.title, DOWN)
        # self.play(Write(subtitle))
        # self.wait()
        
        friis_eq = MathTex(
            r"P_r", r"=", r"P_t", r"\cdot", r"G_t", r"\cdot", r"G_r", 
            r"\cdot", r"\left(\frac{\lambda}{4\pi d}\right)^2",
            font_size=44
        ).shift(UP*1.5)
        
        self.play(Write(friis_eq))
        self.wait()
        
        # Parameter explanations with icons
        params = [
            (0, "P_r", "Received Power", "📱", "Power at receiver", "-90 to -50 dBm"),
            (2, "P_t", "Transmitted Power", "⚡", "Power from transmitter", "20 to 50 dBm"),
            (4, "G_t", "Transmit Gain", "📡", "Transmitter antenna gain", "0 to 20 dBi"),
            (6, "G_r", "Receive Gain", "📶", "Receiver antenna gain", "0 to 15 dBi"),
            (8, r"\left(\frac{\lambda}{4\pi d}\right)^2", "Path Loss Factor", "📉", "Free space loss", "λ = c/f, d = distance"),
        ]
        
        # Animate each parameter
        for idx, param_tex, name, icon, desc, range_val in params:
            # Highlight parameter in equation
            highlight_box = SurroundingRectangle(friis_eq[idx], color=YELLOW, buff=0.1)
            self.play(Create(highlight_box))
            
            # Create info box
            info_box = VGroup()
            box_rect = RoundedRectangle(
                width=5, height=2, 
                corner_radius=0.2,
                fill_opacity=0.9,
                fill_color=GREY,
                stroke_color=WHITE,
                stroke_width=3
            ).shift(DOWN*1.5)
            
            icon_text = Text(icon, font_size=60).move_to(box_rect).shift(LEFT*1.8 + UP*0.4)
            param_name = Text(name, font_size=32, color=YELLOW).next_to(icon_text, RIGHT, buff=0.3).shift(UP*0.4)
            param_desc = Text(desc, font_size=22).move_to(box_rect).shift(DOWN*0.2)
            param_range = Text(f"Typical: {range_val}", font_size=20, color=YELLOW).next_to(param_desc, DOWN, buff=0.2)
            
            info_box.add(box_rect, icon_text, param_name, param_desc, param_range)
            
            self.play(FadeIn(info_box))
            self.wait(1.5)
            
            # Fade out
            self.play(FadeOut(info_box), FadeOut(highlight_box))
            self.wait(0.3)
        
        # Final summary
        summary = Text("All parameters together determine signal strength!", 
                      font_size=32, color=GREEN).shift(DOWN*2)
        self.play(Write(summary))
        self.wait()
        
        # Equation highlight animation
        self.play(
            friis_eq.animate.set_color(YELLOW),
            rate_func=there_and_back,
            run_time=1.5
        )
        self.wait(2)
        
        # Fade out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # Final title
        self.wait(8)


# To render this animation, use:
# manim -pql script.py FriisTransmissionComplete
# For high quality: manim -pqh script.py FriisTransmissionComplete