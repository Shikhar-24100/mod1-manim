from manim import *

# ── SVG ASSETS (place these files in your utils/ folder) ──────────────────
# utils/mobile.svg       — mobile phone icon
# utils/bs_tower.svg     — cell tower / base station icon
# utils/hlr_box.svg      — database cylinder or server icon (for HLR)
# utils/vlr_box.svg      — database cylinder or server icon (for VLR)
# utils/msc_switch.svg   — network switch / MSC icon
# utils/shield.svg       — shield icon (authentication)
# utils/phone_ring.svg   — ringing phone icon
# ──────────────────────────────────────────────────────────────────────────

UTILS = "utils/"

# ── Palette (matching Video 1) ─────────────────────────────────────────────
CREAM       = "#FFFBE6"
DARK_BG     = "#1C1C2E"
ACCENT_BLUE = "#58C4DD"
ACCENT_RED  = "#FF6B6B"
ACCENT_GRN  = "#6BCB77"
DIM_GREY    = "#888899"
SOFT_WHITE  = "#E8E8F0"
ALT_YELLOW  = "#F2D388"
ACCENT_PURP = "#C084FC"


# ══════════════════════════════════════════════════════════════════════════
# ── SHARED HELPERS ────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════

def load_icon(svg_name, fallback_shape, scale=0.55):
    try:
        icon = SVGMobject(UTILS + svg_name).scale(scale)
    except Exception:
        icon = fallback_shape
    return icon


def make_card(icon_svg, fallback, col, name, desc, icon_scale=0.45):
    icon = load_icon(icon_svg, fallback, scale=icon_scale)
    name_lbl = Text(name, font_size=16, color=col, weight=BOLD)
    desc_lbl = Text(desc, font_size=13, color=SOFT_WHITE)
    content = VGroup(icon, name_lbl, desc_lbl).arrange(DOWN, buff=0.15)
    box = SurroundingRectangle(
        content, corner_radius=0.14,
        color=DIM_GREY, fill_color="#151522",
        fill_opacity=0.75, buff=0.20, stroke_width=1.5
    )
    return VGroup(box, content)


def make_hex(center, col, scale=1.55):
    return RegularPolygon(
        n=6, start_angle=PI / 6,
        color=col, fill_opacity=0.10, stroke_width=2
    ).scale(scale).move_to(center)


def make_bs(center, col, label="BS"):
    try:
        icon = SVGMobject(UTILS + "bs_tower.svg").scale(0.35)
    except Exception:
        icon = Triangle(color=col, fill_opacity=0.5).scale(0.30)
    icon.move_to(center)
    lbl = Text(label, font_size=11, color=col, weight=BOLD).next_to(icon, DOWN, buff=0.08)
    return VGroup(icon, lbl)


def make_mobile(center, col=ALT_YELLOW, label=""):
    try:
        ico = SVGMobject(UTILS + "mobile.svg").scale(0.30)
    except Exception:
        ico = RoundedRectangle(corner_radius=0.08, width=0.26, height=0.42,
                               color=ALT_YELLOW, fill_opacity=0.5)
    ico.move_to(center)
    if label:
        lbl = Text(label, font_size=11, color=SOFT_WHITE, weight=BOLD).next_to(ico, DOWN, buff=0.06)
        return VGroup(ico, lbl)
    return VGroup(ico)


def make_db(center, svg_name, label, col, scale=0.28):
    try:
        ico = SVGMobject(UTILS + svg_name).scale(scale)
    except Exception:
        ico = RoundedRectangle(corner_radius=0.08, width=0.40, height=0.34,
                               color=col, fill_opacity=0.4)
    ico.move_to(center)
    lbl = Text(label, font_size=11, color=col, weight=BOLD).next_to(ico, DOWN, buff=0.06)
    return VGroup(ico, lbl)


def make_msc(center, label="MSC", col=ACCENT_PURP):
    try:
        ico = SVGMobject(UTILS + "msc_switch.svg").scale(0.38)
    except Exception:
        ico = RoundedRectangle(corner_radius=0.12, width=0.70, height=0.55,
                               color=col, fill_opacity=0.35)
    ico.move_to(center)
    lbl = Text(label, font_size=12, color=col, weight=BOLD).next_to(ico, DOWN, buff=0.06)
    return VGroup(ico, lbl)


def arrow_between(mob_a, mob_b, col=SOFT_WHITE, label="", tip_scale=0.35):
    arr = Arrow(
        mob_a.get_center(), mob_b.get_center(),
        buff=0.22, color=col,
        stroke_width=2.5,
        max_tip_length_to_length_ratio=tip_scale
    )
    if label:
        mid = arr.get_center()
        lbl = Text(label, font_size=11, color=col).move_to(mid + UP * 0.22)
        return VGroup(arr, lbl)
    return arr


def step_label(text, col=ACCENT_BLUE, size=15):
    return Text(text, font_size=size, color=col)


def callout_box(text, col=CREAM):
    t = Text(text, font_size=16, color=col, line_spacing=1.2)
    box = SurroundingRectangle(t, corner_radius=0.12, color=col,
                               fill_color="#151522", fill_opacity=0.8,
                               buff=0.18, stroke_width=1.2)
    return VGroup(box, t)


# ══════════════════════════════════════════════════════════════════════════
# SCENE 1 — RECAP
# ══════════════════════════════════════════════════════════════════════════

class Scene1Recap(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # Title
        title = Text("Quick Recap", font_size=40, weight=BOLD, color=SOFT_WHITE)
        sub   = Text("What happens when a phone powers ON", font_size=22, color=ACCENT_BLUE)
        hdr   = VGroup(title, sub).arrange(DOWN, buff=0.22).to_edge(UP, buff=0.45)
        self.play(FadeIn(hdr, shift=DOWN * 0.2))
        self.wait(0.3)

        # Three recap cards
        cards_data = [
            (
                "mobile.svg",
                RoundedRectangle(corner_radius=0.1, width=0.45, height=0.78,
                                 color=ALT_YELLOW, fill_opacity=0.3),
                ALT_YELLOW,
                "Mobile Powers ON",
                "Scans FOCC signals from\nall nearby Base Stations."
            ),
            (
                "bs_tower.svg",
                Triangle(color=ACCENT_GRN, fill_opacity=0.3).scale(0.48),
                ACCENT_GRN,
                "Connects to Best BS",
                "Selects BS with the\nstrongest signal strength."
            ),
            (
                "hlr_box.svg",
                RoundedRectangle(corner_radius=0.1, width=0.65, height=0.52,
                                 color=ACCENT_BLUE, fill_opacity=0.3),
                ACCENT_BLUE,
                "HLR / VLR Updated",
                "Network always knows\nwhere the user is located."
            ),
        ]

        card_group = VGroup()
        for svg, fallback, col, name, desc in cards_data:
            card_group.add(make_card(svg, fallback, col, name, desc))
        card_group.arrange(RIGHT, buff=0.40).next_to(hdr, DOWN, buff=0.55)
        card_group.scale_to_fit_width(12.5)

        for card in card_group:
            self.play(FadeIn(card, scale=0.85), run_time=0.55)
            self.wait(0.2)
        self.wait(0.8)

        # Transition arrow
        q = Text("Now — what happens when a CALL is made?",
                 font_size=22, color=ALT_YELLOW, weight=BOLD)
        q.to_edge(DOWN, buff=0.65)
        underline = Line(q.get_left() + DOWN*0.08, q.get_right() + DOWN*0.08,
                         color=ALT_YELLOW, stroke_width=1.5)
        self.play(FadeIn(q, shift=UP*0.2), run_time=0.7)
        self.play(Create(underline), run_time=0.5)
        self.wait(1.5)

        self.play(FadeOut(VGroup(hdr, card_group, q, underline), shift=UP*0.3), run_time=0.7)
        self.wait(0.2)


# ══════════════════════════════════════════════════════════════════════════
# SCENE 2 — NEW ENTITIES (MS, BS, MSC)
# ══════════════════════════════════════════════════════════════════════════

class Scene2NewEntities(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        title = Text("Key Players in Call Establishment", font_size=36, weight=BOLD, color=SOFT_WHITE)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN*0.2))
        self.wait(0.3)

        # Three entity cards
        cards_data = [
            (
                "mobile.svg",
                RoundedRectangle(corner_radius=0.1, width=0.45, height=0.78,
                                 color=ALT_YELLOW, fill_opacity=0.3),
                ALT_YELLOW,
                "MS",
                "Mobile Station\nCaller / Receiver"
            ),
            (
                "bs_tower.svg",
                Triangle(color=ACCENT_GRN, fill_opacity=0.3).scale(0.48),
                ACCENT_GRN,
                "BTS / BS",
                "Base Station\nRadio Interface"
            ),
            (
                "msc_switch.svg",
                RoundedRectangle(corner_radius=0.12, width=0.70, height=0.55,
                                 color=ACCENT_PURP, fill_opacity=0.35),
                ACCENT_PURP,
                "MSC",
                "Mobile Switching Center\nCall Control Brain"
            ),
        ]

        card_group = VGroup()
        for svg, fallback, col, name, desc in cards_data:
            card_group.add(make_card(svg, fallback, col, name, desc, icon_scale=0.42))
        card_group.arrange(RIGHT, buff=0.55).next_to(title, DOWN, buff=0.55)
        card_group.scale_to_fit_width(12.8)

        for card in card_group:
            self.play(FadeIn(card, scale=0.85), run_time=0.55)
            self.wait(0.2)
        self.wait(0.5)

        # Network topology diagram
        diag_title = Text("Network Topology", font_size=18, color=DIM_GREY, slant=ITALIC)
        diag_title.next_to(card_group, DOWN, buff=0.45)
        self.play(FadeIn(diag_title))

        # Nodes
        ms_node  = Circle(radius=0.22, color=ALT_YELLOW, fill_opacity=0.35).shift(LEFT*4.5 + DOWN*1.5)
        bs_node  = Circle(radius=0.22, color=ACCENT_GRN, fill_opacity=0.35).shift(LEFT*2.0 + DOWN*1.5)
        msc_node = RoundedRectangle(corner_radius=0.1, width=0.9, height=0.5,
                                    color=ACCENT_PURP, fill_opacity=0.35).shift(DOWN*1.5)
        hlr_node = Circle(radius=0.22, color=ACCENT_BLUE, fill_opacity=0.35).shift(RIGHT*2.2 + DOWN*1.0)
        vlr_node = Circle(radius=0.22, color=ACCENT_RED,  fill_opacity=0.35).shift(RIGHT*2.2 + DOWN*2.0)
        pstn_node= RoundedRectangle(corner_radius=0.1, width=0.9, height=0.4,
                                    color=DIM_GREY, fill_opacity=0.25).shift(RIGHT*4.2 + DOWN*1.5)

        node_labels = [
            Text("MS",   font_size=11, color=ALT_YELLOW).move_to(ms_node),
            Text("BS",   font_size=11, color=ACCENT_GRN).move_to(bs_node),
            Text("MSC",  font_size=11, color=ACCENT_PURP).move_to(msc_node),
            Text("HLR",  font_size=11, color=ACCENT_BLUE).move_to(hlr_node),
            Text("VLR",  font_size=11, color=ACCENT_RED ).move_to(vlr_node),
            Text("PSTN", font_size=11, color=DIM_GREY   ).move_to(pstn_node),
        ]

        nodes = VGroup(ms_node, bs_node, msc_node, hlr_node, vlr_node, pstn_node)
        lbls  = VGroup(*node_labels)

        edges_data = [
            (ms_node, bs_node,  SOFT_WHITE),
            (bs_node, msc_node, SOFT_WHITE),
            (msc_node, hlr_node, ACCENT_BLUE),
            (msc_node, vlr_node, ACCENT_RED),
            (msc_node, pstn_node, DIM_GREY),
        ]
        edges = VGroup(*[
            Line(a.get_right() if a.get_right()[0] < b.get_left()[0] else a.get_center(),
                 b.get_left()  if a.get_right()[0] < b.get_left()[0] else b.get_center(),
                 color=c, stroke_width=2)
            for a, b, c in edges_data
        ])

        self.play(
            LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.15),
            LaggedStart(*[FadeIn(l) for l in lbls],  lag_ratio=0.15),
        )
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.18), run_time=1.0)
        self.wait(1.5)

        self.play(FadeOut(VGroup(title, card_group, diag_title, nodes, lbls, edges),
                          shift=UP*0.3), run_time=0.7)
        self.wait(0.2)


# ══════════════════════════════════════════════════════════════════════════
# SCENE 3 — GENERIC CALL STEPS
# ══════════════════════════════════════════════════════════════════════════

class Scene3GenericSteps(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        title = Text("Generic Steps in Any Call", font_size=38, weight=BOLD, color=SOFT_WHITE)
        sub   = Text("These steps apply to every cellular call scenario",
                     font_size=19, color=ACCENT_BLUE)
        hdr   = VGroup(title, sub).arrange(DOWN, buff=0.22).to_edge(UP, buff=0.45)
        self.play(FadeIn(hdr, shift=DOWN*0.2))
        self.wait(0.3)

        steps = [
            ("1", "Call Request Initiation",   ALT_YELLOW,  "Mobile dials → sends request via RECC to BS"),
            ("2", "Authentication & Validation", ACCENT_GRN,  "MSC verifies subscriber identity via HLR"),
            ("3", "Location Identification",    ACCENT_BLUE, "HLR/VLR pinpoints which cell the receiver is in"),
            ("4", "Channel Allocation",         ACCENT_PURP, "MSC assigns a Traffic Channel (TCH)"),
            ("5", "Call Routing",               ACCENT_RED,  "Signal routed through BS(s) and MSC(s)"),
            ("6", "Call Setup — Connected!",    ACCENT_GRN,  "Receiver rings → answers → call established"),
        ]

        step_items = VGroup()
        for num, title_s, col, desc in steps:
            num_circle = Circle(radius=0.24, color=col, fill_opacity=0.25, stroke_width=2)
            num_text   = Text(num, font_size=18, color=col, weight=BOLD).move_to(num_circle)
            num_mob    = VGroup(num_circle, num_text)

            step_title = Text(title_s, font_size=17, color=col, weight=BOLD)
            step_desc  = Text(desc,   font_size=13, color=DIM_GREY)
            text_col   = VGroup(step_title, step_desc).arrange(DOWN, buff=0.06, aligned_edge=LEFT)

            row = VGroup(num_mob, text_col).arrange(RIGHT, buff=0.28)
            step_items.add(row)

        step_items.arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        step_items.next_to(hdr, DOWN, buff=0.5)
        step_items.to_edge(LEFT, buff=1.0)

        # Vertical connector line
        line_x = step_items.get_left()[0] + 0.24
        top_y  = step_items[0].get_center()[1]
        bot_y  = step_items[-1].get_center()[1]
        v_line = DashedLine(
            [line_x, top_y, 0], [line_x, bot_y, 0],
            color=DIM_GREY, stroke_width=1.2, dash_length=0.1
        )

        self.play(Create(v_line), run_time=0.6)

        for item in step_items:
            self.play(FadeIn(item, shift=RIGHT*0.3), run_time=0.45)
            self.wait(0.15)
        self.wait(1.5)

        # Highlight final step
        self.play(
            step_items[-1][1][0].animate.set_color(ACCENT_GRN),
            run_time=0.4
        )
        self.wait(1.0)

        self.play(FadeOut(VGroup(hdr, step_items, v_line), shift=UP*0.3), run_time=0.7)
        self.wait(0.2)


# ══════════════════════════════════════════════════════════════════════════
# SCENE 4 — CASE 1: SAME CELL
# ══════════════════════════════════════════════════════════════════════════

class Scene4Case1SameCell(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # Header
        case_tag = Text("CASE 1", font_size=14, color=ACCENT_BLUE, weight=BOLD)
        title    = Text("Caller & Receiver — Same Cell", font_size=34, weight=BOLD, color=SOFT_WHITE)
        sub      = Text("Same BS  ·  Same MSC  ·  No inter-cell routing",
                        font_size=17, color=DIM_GREY)
        hdr = VGroup(case_tag, title, sub).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr, shift=DOWN*0.15))
        self.wait(0.3)

        # Single hex cell
        cell_center = UP * 0.2
        hex1 = make_hex(cell_center, ACCENT_BLUE, scale=2.0)
        cell_lbl = Text("Cell 1", font_size=16, color=ACCENT_BLUE,
                        weight=BOLD).move_to(cell_center + DOWN*1.7)
        self.play(DrawBorderThenFill(hex1), FadeIn(cell_lbl))

        # BS in center
        bs  = make_bs(cell_center + UP*0.1, ACCENT_BLUE)
        self.play(FadeIn(bs, scale=0.7))

        # MSC top right
        msc = make_msc(cell_center + RIGHT*2.8 + UP*1.1)
        self.play(FadeIn(msc, scale=0.8))

        # HLR + VLR top left
        hlr = make_db(cell_center + LEFT*2.8 + UP*1.1, "hlr_box.svg", "HLR", ACCENT_BLUE)
        vlr = make_db(cell_center + LEFT*2.8 + UP*0.35, "vlr_box.svg", "VLR", ACCENT_RED)
        self.play(FadeIn(hlr, scale=0.8), FadeIn(vlr, scale=0.8))

        # Caller (left) and Receiver (right)
        caller   = make_mobile(cell_center + LEFT*1.4 + DOWN*0.5, ALT_YELLOW, "Caller")
        receiver = make_mobile(cell_center + RIGHT*1.4 + DOWN*0.5, ACCENT_GRN, "Receiver")
        self.play(FadeIn(caller, scale=0.8), FadeIn(receiver, scale=0.8))
        self.wait(0.4)

        # Step-by-step arrows
        steps_grp = VGroup()

        def flash_arrow(start_mob, end_mob, col, lbl, direction=UP):
            arr = Arrow(start_mob.get_center(), end_mob.get_center(),
                        buff=0.22, color=col, stroke_width=2.5,
                        max_tip_length_to_length_ratio=0.3)
            mid = arr.get_center()
            t   = Text(lbl, font_size=11, color=col).move_to(mid + direction*0.22)
            grp = VGroup(arr, t)
            steps_grp.add(grp)
            return grp

        # Step annotations on right side
        step_texts = VGroup()
        step_data = [
            "① Caller → BS  (Call Request via RECC)",
            "② BS → MSC  (Forward request)",
            "③ MSC ↔ HLR/VLR  (Verify subscriber)",
            "④ MSC → BS → Receiver  (Paging)",
            "⑤ TCH allocated  (Traffic Channel)",
            "⑥ Call Connected! ✓",
        ]
        for i, s in enumerate(step_data):
            col = [ALT_YELLOW, ACCENT_GRN, ACCENT_BLUE, ACCENT_PURP, DIM_GREY, ACCENT_GRN][i]
            t = Text(s, font_size=13, color=col)
            step_texts.add(t)
        step_texts.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        step_texts.to_edge(RIGHT, buff=0.3).shift(DOWN*0.3)

        # Animate each step
        a1 = flash_arrow(caller, bs, ALT_YELLOW, "Call Req")
        self.play(Create(a1[0]), FadeIn(a1[1]), FadeIn(step_texts[0]), run_time=0.6)
        self.wait(0.3)

        a2 = flash_arrow(bs, msc, ACCENT_GRN, "Forward")
        self.play(Create(a2[0]), FadeIn(a2[1]), FadeIn(step_texts[1]), run_time=0.6)
        self.wait(0.3)

        a3 = Arrow(msc.get_center(), hlr.get_center(), buff=0.22, color=ACCENT_BLUE,
                   stroke_width=2.5, max_tip_length_to_length_ratio=0.3)
        a3b= Arrow(hlr.get_center(), msc.get_center(), buff=0.22, color=ACCENT_BLUE,
                   stroke_width=2.0, max_tip_length_to_length_ratio=0.3)
        verify_lbl = Text("Verify", font_size=11, color=ACCENT_BLUE).move_to(
            a3.get_center() + LEFT*0.3 + UP*0.2)
        steps_grp.add(VGroup(a3, a3b, verify_lbl))
        self.play(Create(a3), Create(a3b), FadeIn(verify_lbl),
                  FadeIn(step_texts[2]), run_time=0.7)
        self.wait(0.3)

        a4 = flash_arrow(msc, receiver, ACCENT_PURP, "Page", direction=DOWN)
        self.play(Create(a4[0]), FadeIn(a4[1]), FadeIn(step_texts[3]), run_time=0.6)
        self.wait(0.3)

        # TCH double arrow
        tch = DashedLine(caller.get_right(), receiver.get_left(),
                         color=DIM_GREY, stroke_width=2, dash_length=0.12)
        tch_lbl = Text("TCH", font_size=11, color=DIM_GREY).move_to(tch.get_center() + UP*0.22)
        steps_grp.add(VGroup(tch, tch_lbl))
        self.play(Create(tch), FadeIn(tch_lbl), FadeIn(step_texts[4]), run_time=0.6)
        self.wait(0.3)

        # Connected glow
        glow = SurroundingRectangle(VGroup(caller, receiver), color=ACCENT_GRN,
                                    corner_radius=0.2, stroke_width=2.5, buff=0.15)
        self.play(Create(glow), FadeIn(step_texts[5]), run_time=0.6)
        self.wait(0.5)

        # Callout
        note = callout_box("No inter-cell routing → low latency, efficient", ACCENT_GRN)
        note.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(note, shift=UP*0.2))
        self.wait(2.0)

        all_obj = VGroup(hdr, hex1, cell_lbl, bs, msc, hlr, vlr, caller, receiver,
                         steps_grp, step_texts, glow, note)
        self.play(FadeOut(all_obj, shift=UP*0.3), run_time=0.7)
        self.wait(0.2)


# ══════════════════════════════════════════════════════════════════════════
# SCENE 5 — CASE 2: DIFFERENT CELL, SAME MSC
# ══════════════════════════════════════════════════════════════════════════

class Scene5Case2DiffCellSameMSC(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        case_tag = Text("CASE 2", font_size=14, color=ACCENT_GRN, weight=BOLD)
        title    = Text("Different Cell — Same MSC", font_size=34, weight=BOLD, color=SOFT_WHITE)
        sub      = Text("Caller in Cell 1  ·  Receiver in Cell 2  ·  Shared MSC",
                        font_size=17, color=DIM_GREY)
        hdr = VGroup(case_tag, title, sub).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr, shift=DOWN*0.15))
        self.wait(0.3)

        # Two cells
        c1_center = LEFT*3.0 + DOWN*0.2
        c2_center = RIGHT*3.0 + DOWN*0.2

        hex1 = make_hex(c1_center, ACCENT_BLUE, scale=1.65)
        hex2 = make_hex(c2_center, ACCENT_GRN,  scale=1.65)
        lbl1 = Text("Cell 1", font_size=14, color=ACCENT_BLUE, weight=BOLD).move_to(c1_center + DOWN*1.5)
        lbl2 = Text("Cell 2", font_size=14, color=ACCENT_GRN,  weight=BOLD).move_to(c2_center + DOWN*1.5)

        self.play(
            LaggedStart(DrawBorderThenFill(hex1), DrawBorderThenFill(hex2), lag_ratio=0.3),
            LaggedStart(FadeIn(lbl1), FadeIn(lbl2), lag_ratio=0.3),
        )

        bs1 = make_bs(c1_center + UP*0.1, ACCENT_BLUE, "BS₁")
        bs2 = make_bs(c2_center + UP*0.1, ACCENT_GRN,  "BS₂")
        self.play(FadeIn(bs1, scale=0.7), FadeIn(bs2, scale=0.7))

        # Shared MSC at top center
        msc = make_msc(UP*2.1)
        self.play(FadeIn(msc, scale=0.8))

        # VLR next to MSC
        vlr = make_db(UP*2.1 + RIGHT*1.4, "vlr_box.svg", "VLR", ACCENT_RED, scale=0.24)
        hlr = make_db(UP*2.1 + LEFT*1.4,  "hlr_box.svg", "HLR", ACCENT_BLUE, scale=0.24)
        self.play(FadeIn(vlr, scale=0.8), FadeIn(hlr, scale=0.8))

        caller   = make_mobile(c1_center + LEFT*1.0 + DOWN*0.6, ALT_YELLOW, "Caller")
        receiver = make_mobile(c2_center + RIGHT*1.0 + DOWN*0.6, ACCENT_GRN, "Receiver")
        self.play(FadeIn(caller, scale=0.8), FadeIn(receiver, scale=0.8))
        self.wait(0.4)

        # Step annotations (left side)
        step_data = [
            ("① Caller → BS₁ → MSC", ALT_YELLOW),
            ("② MSC queries VLR → receiver in Cell 2", ACCENT_RED),
            ("③ Paging → BS₂ → Receiver", ACCENT_GRN),
            ("④ Channel allocated in both cells", ACCENT_PURP),
            ("⑤ Call connected via MSC ✓", ACCENT_GRN),
        ]
        step_texts = VGroup(*[Text(s, font_size=12, color=c) for s, c in step_data])
        step_texts.arrange(DOWN, buff=0.20, aligned_edge=LEFT).to_edge(LEFT, buff=0.25).shift(DOWN*0.5)

        arrows_grp = VGroup()

        # Step 1
        a1 = Arrow(caller.get_top(), bs1.get_bottom(), buff=0.1, color=ALT_YELLOW,
                   stroke_width=2.5, max_tip_length_to_length_ratio=0.3)
        a1b= Arrow(bs1.get_top(), msc.get_bottom(), buff=0.1, color=ALT_YELLOW,
                   stroke_width=2.5, max_tip_length_to_length_ratio=0.3)
        arrows_grp.add(a1, a1b)
        self.play(Create(a1), Create(a1b), FadeIn(step_texts[0]), run_time=0.7)
        self.wait(0.3)

        # Step 2 — VLR highlight
        vlr_highlight = SurroundingRectangle(vlr, color=ACCENT_RED, stroke_width=2.5, buff=0.08)
        self.play(Create(vlr_highlight), FadeIn(step_texts[1]), run_time=0.6)
        self.wait(0.3)

        # Step 3
        a3 = Arrow(msc.get_bottom(), bs2.get_top(), buff=0.1, color=ACCENT_GRN,
                   stroke_width=2.5, max_tip_length_to_length_ratio=0.3)
        a3b= Arrow(bs2.get_bottom(), receiver.get_top(), buff=0.1, color=ACCENT_GRN,
                   stroke_width=2.5, max_tip_length_to_length_ratio=0.3)
        arrows_grp.add(a3, a3b)
        self.play(Create(a3), Create(a3b), FadeIn(step_texts[2]), run_time=0.7)
        self.wait(0.3)

        # Step 4 — dashed TCH lines
        tch1 = DashedLine(caller.get_top(), msc.get_left(),
                          color=ACCENT_PURP, stroke_width=1.8, dash_length=0.1)
        tch2 = DashedLine(msc.get_right(), receiver.get_top(),
                          color=ACCENT_PURP, stroke_width=1.8, dash_length=0.1)
        arrows_grp.add(tch1, tch2)
        self.play(Create(tch1), Create(tch2), FadeIn(step_texts[3]), run_time=0.7)
        self.wait(0.3)

        # Step 5 — glow
        glow = VGroup(
            SurroundingRectangle(caller,   color=ACCENT_GRN, corner_radius=0.15,
                                 stroke_width=2, buff=0.1),
            SurroundingRectangle(receiver, color=ACCENT_GRN, corner_radius=0.15,
                                 stroke_width=2, buff=0.1),
        )
        self.play(Create(glow), FadeIn(step_texts[4]), run_time=0.6)
        self.wait(0.5)

        note = callout_box("Uses paging + location tracking via VLR", ACCENT_GRN)
        note.to_edge(DOWN, buff=0.30)
        self.play(FadeIn(note, shift=UP*0.2))
        self.wait(2.0)

        all_obj = VGroup(hdr, hex1, hex2, lbl1, lbl2, bs1, bs2, msc, vlr, hlr,
                         caller, receiver, arrows_grp, vlr_highlight, glow,
                         step_texts, note)
        self.play(FadeOut(all_obj, shift=UP*0.3), run_time=0.7)
        self.wait(0.2)


# ══════════════════════════════════════════════════════════════════════════
# SCENE 6 — CASE 3: INTER-MSC CALL
# ══════════════════════════════════════════════════════════════════════════

class Scene6Case3InterMSC(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        case_tag = Text("CASE 3", font_size=14, color=ACCENT_PURP, weight=BOLD)
        title    = Text("Inter-MSC Call", font_size=34, weight=BOLD, color=SOFT_WHITE)
        sub      = Text("Caller in Cell 1 (MSC-A)  ·  Receiver in Cell 3 (MSC-B)",
                        font_size=17, color=DIM_GREY)
        hdr = VGroup(case_tag, title, sub).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr, shift=DOWN*0.15))
        self.wait(0.3)

        # Left cluster: MSC-A + Cell 1
        ca_center = LEFT*3.2 + DOWN*0.3
        cb_center = RIGHT*3.2 + DOWN*0.3

        hex_a = make_hex(ca_center, ACCENT_BLUE, scale=1.55)
        hex_b = make_hex(cb_center, ACCENT_RED,  scale=1.55)
        lbl_a = Text("Cell 1", font_size=13, color=ACCENT_BLUE, weight=BOLD).move_to(ca_center + DOWN*1.4)
        lbl_b = Text("Cell 3", font_size=13, color=ACCENT_RED,  weight=BOLD).move_to(cb_center + DOWN*1.4)

        self.play(
            LaggedStart(DrawBorderThenFill(hex_a), DrawBorderThenFill(hex_b), lag_ratio=0.3),
            LaggedStart(FadeIn(lbl_a), FadeIn(lbl_b), lag_ratio=0.3),
        )

        bs_a = make_bs(ca_center + UP*0.05, ACCENT_BLUE, "BS-A")
        bs_b = make_bs(cb_center + UP*0.05, ACCENT_RED,  "BS-B")
        self.play(FadeIn(bs_a, scale=0.7), FadeIn(bs_b, scale=0.7))

        # MSC-A (above left cell) and MSC-B (above right cell)
        msca = make_msc(ca_center + UP*2.2 + RIGHT*0.3, "MSC-A", ACCENT_PURP)
        mscb = make_msc(cb_center + UP*2.2 + LEFT*0.3,  "MSC-B", ALT_YELLOW)
        self.play(FadeIn(msca, scale=0.8), FadeIn(mscb, scale=0.8))

        # HLR-A under MSC-A, VLR-B under MSC-B
        hlr_a = make_db(ca_center + UP*2.2 + LEFT*1.1, "hlr_box.svg", "HLR-A", ACCENT_BLUE, 0.22)
        vlr_b = make_db(cb_center + UP*2.2 + RIGHT*1.1, "vlr_box.svg", "VLR-B", ACCENT_RED, 0.22)
        self.play(FadeIn(hlr_a, scale=0.8), FadeIn(vlr_b, scale=0.8))

        caller   = make_mobile(ca_center + LEFT*1.0 + DOWN*0.7, ALT_YELLOW, "Caller")
        receiver = make_mobile(cb_center + RIGHT*1.0 + DOWN*0.7, ACCENT_GRN,  "Receiver")
        self.play(FadeIn(caller, scale=0.8), FadeIn(receiver, scale=0.8))
        self.wait(0.4)

        # Step annotations — bottom strip
        step_data = [
            ("① Caller → BS-A → MSC-A", ALT_YELLOW),
            ("② MSC-A queries HLR-A for receiver's location", ACCENT_BLUE),
            ("③ HLR-A returns MSC-B address", ACCENT_BLUE),
            ("④ Call routed: MSC-A → MSC-B", ACCENT_PURP),
            ("⑤ MSC-B pages receiver via BS-B", ACCENT_RED),
            ("⑥ Channel allocated → Call connected ✓", ACCENT_GRN),
        ]
        step_texts = VGroup(*[Text(s, font_size=12, color=c) for s, c in step_data])
        step_texts.arrange(DOWN, buff=0.17, aligned_edge=LEFT).to_edge(DOWN, buff=0.25)

        arrows_grp = VGroup()

        # Step 1
        a1 = Arrow(caller.get_top(), bs_a.get_bottom(), buff=0.08, color=ALT_YELLOW,
                   stroke_width=2, max_tip_length_to_length_ratio=0.3)
        a1b= Arrow(bs_a.get_top(), msca.get_bottom(), buff=0.08, color=ALT_YELLOW,
                   stroke_width=2, max_tip_length_to_length_ratio=0.3)
        arrows_grp.add(a1, a1b)
        self.play(Create(a1), Create(a1b), FadeIn(step_texts[0]), run_time=0.6)
        self.wait(0.25)

        # Step 2
        a2 = Arrow(msca.get_left(), hlr_a.get_right(), buff=0.08, color=ACCENT_BLUE,
                   stroke_width=2, max_tip_length_to_length_ratio=0.3)
        hlr_glow = SurroundingRectangle(hlr_a, color=ACCENT_BLUE, stroke_width=2.5, buff=0.08)
        arrows_grp.add(a2)
        self.play(Create(a2), Create(hlr_glow), FadeIn(step_texts[1]), run_time=0.6)
        self.wait(0.25)

        # Step 3 — HLR returns MSC-B address
        a3 = Arrow(hlr_a.get_right(), msca.get_left(), buff=0.08, color=ACCENT_BLUE,
                   stroke_width=2.0, max_tip_length_to_length_ratio=0.3)
        arrows_grp.add(a3)
        self.play(Create(a3), FadeIn(step_texts[2]), run_time=0.6)
        self.wait(0.25)

        # Step 4 — Inter-MSC arrow (the big highlight)
        inter_arr = Arrow(msca.get_right(), mscb.get_left(), buff=0.1, color=ACCENT_PURP,
                          stroke_width=3.5, max_tip_length_to_length_ratio=0.25)
        inter_lbl = Text("Inter-MSC Routing", font_size=12, color=ACCENT_PURP,
                         weight=BOLD).move_to(inter_arr.get_center() + UP*0.25)
        arrows_grp.add(inter_arr)
        self.play(Create(inter_arr), FadeIn(inter_lbl), FadeIn(step_texts[3]), run_time=0.8)
        self.wait(0.3)

        # Step 5
        a5 = Arrow(mscb.get_bottom(), bs_b.get_top(), buff=0.08, color=ACCENT_RED,
                   stroke_width=2, max_tip_length_to_length_ratio=0.3)
        a5b= Arrow(bs_b.get_bottom(), receiver.get_top(), buff=0.08, color=ACCENT_RED,
                   stroke_width=2, max_tip_length_to_length_ratio=0.3)
        arrows_grp.add(a5, a5b)
        self.play(Create(a5), Create(a5b), FadeIn(step_texts[4]), run_time=0.6)
        self.wait(0.25)

        # Step 6 — glow
        glow = VGroup(
            SurroundingRectangle(caller,   color=ACCENT_GRN, corner_radius=0.15,
                                 stroke_width=2, buff=0.1),
            SurroundingRectangle(receiver, color=ACCENT_GRN, corner_radius=0.15,
                                 stroke_width=2, buff=0.1),
        )
        self.play(Create(glow), FadeIn(step_texts[5]), run_time=0.6)
        self.wait(1.0)

        note = callout_box("HLR lookup + inter-MSC signaling", ACCENT_PURP)
        note.next_to(step_texts, DOWN, buff=0.18)
        self.play(FadeIn(note, shift=UP*0.2))
        self.wait(2.0)

        all_obj = VGroup(hdr, hex_a, hex_b, lbl_a, lbl_b, bs_a, bs_b,
                         msca, mscb, hlr_a, vlr_b, caller, receiver,
                         arrows_grp, hlr_glow, inter_lbl, glow,
                         step_texts, note)
        self.play(FadeOut(all_obj, shift=UP*0.3), run_time=0.7)
        self.wait(0.2)


# ══════════════════════════════════════════════════════════════════════════
# SCENE 7 — CASE 4: ROAMING CALLER
# ══════════════════════════════════════════════════════════════════════════

class Scene7Case4Roaming(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        case_tag = Text("CASE 4", font_size=14, color=ACCENT_RED, weight=BOLD)
        title    = Text("Roaming Caller — Visiting Cell", font_size=34, weight=BOLD, color=SOFT_WHITE)
        sub      = Text("Caller's home is Cell A  ·  Currently visiting Cell B",
                        font_size=17, color=DIM_GREY)
        hdr = VGroup(case_tag, title, sub).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr, shift=DOWN*0.15))
        self.wait(0.3)

        # Cell A (home) — left
        # Cell B (visited) — right
        ca_center = LEFT*3.2 + DOWN*0.3
        cb_center = RIGHT*3.2 + DOWN*0.3

        hex_home = make_hex(ca_center, ACCENT_BLUE, scale=1.55)
        hex_visit= make_hex(cb_center, ACCENT_RED,  scale=1.55)

        home_lbl  = Text("Cell A\n(Home)", font_size=13, color=ACCENT_BLUE,
                         weight=BOLD).move_to(ca_center + DOWN*1.45)
        visit_lbl = Text("Cell B\n(Visited)", font_size=13, color=ACCENT_RED,
                         weight=BOLD).move_to(cb_center + DOWN*1.45)

        self.play(
            LaggedStart(DrawBorderThenFill(hex_home), DrawBorderThenFill(hex_visit), lag_ratio=0.3),
            LaggedStart(FadeIn(home_lbl), FadeIn(visit_lbl), lag_ratio=0.3),
        )

        bs_a = make_bs(ca_center + UP*0.05, ACCENT_BLUE, "BS-A")
        bs_b = make_bs(cb_center + UP*0.05, ACCENT_RED,  "BS-B")
        self.play(FadeIn(bs_a, scale=0.7), FadeIn(bs_b, scale=0.7))

        # HLR-A in home cell, VLR-B in visited cell
        hlr_a = make_db(ca_center + UP*1.8 + LEFT*0.6, "hlr_box.svg", "HLR-A", ACCENT_BLUE, 0.24)
        msc_a = make_msc(ca_center + UP*1.8 + RIGHT*0.6, "MSC-A", ACCENT_BLUE)
        vlr_b = make_db(cb_center + UP*1.8 + LEFT*0.6, "vlr_box.svg", "VLR-B", ACCENT_RED, 0.24)
        msc_b = make_msc(cb_center + UP*1.8 + RIGHT*0.6, "MSC-B", ACCENT_RED)
        self.play(FadeIn(hlr_a, scale=0.8), FadeIn(msc_a, scale=0.8),
                  FadeIn(vlr_b, scale=0.8), FadeIn(msc_b, scale=0.8))

        # Caller is in Cell B (visitor!) with visitor badge
        caller = make_mobile(cb_center + LEFT*1.0 + DOWN*0.7, ACCENT_RED, "Caller\n(Visitor)")
        visitor_badge = Text("VISITOR", font_size=9, color=ACCENT_RED,
                             weight=BOLD, slant=ITALIC)
        badge_box = SurroundingRectangle(visitor_badge, color=ACCENT_RED, fill_color="#2a0a0a",
                                         fill_opacity=0.8, buff=0.06, stroke_width=1.2,
                                         corner_radius=0.06)
        visitor_tag = VGroup(badge_box, visitor_badge).next_to(caller, UP, buff=0.04)

        self.play(FadeIn(caller, scale=0.8), FadeIn(visitor_tag, scale=0.8))
        self.wait(0.4)

        # Step annotations
        step_data = [
            ("① Caller sends request via visited BS-B", ALT_YELLOW),
            ("② Visited MSC-B checks VLR-B", ACCENT_RED),
            ("③ VLR-B queries HLR-A (home network)", ACCENT_BLUE),
            ("④ Authentication performed by HLR-A", ACCENT_GRN),
            ("⑤ Call proceeds — routed via MSC-B", ACCENT_PURP),
            ("⑥ VLR plays the major role ✓", ACCENT_RED),
        ]
        step_texts = VGroup(*[Text(s, font_size=12, color=c) for s, c in step_data])
        step_texts.arrange(DOWN, buff=0.17, aligned_edge=LEFT).to_edge(DOWN, buff=0.25)

        arrows_grp = VGroup()

        # Step 1
        a1 = Arrow(caller.get_top(), bs_b.get_bottom(), buff=0.08, color=ALT_YELLOW,
                   stroke_width=2, max_tip_length_to_length_ratio=0.3)
        a1b= Arrow(bs_b.get_top(), msc_b.get_bottom(), buff=0.08, color=ALT_YELLOW,
                   stroke_width=2, max_tip_length_to_length_ratio=0.3)
        arrows_grp.add(a1, a1b)
        self.play(Create(a1), Create(a1b), FadeIn(step_texts[0]), run_time=0.6)
        self.wait(0.25)

        # Step 2 — VLR-B highlight
        vlr_glow = SurroundingRectangle(vlr_b, color=ACCENT_RED, stroke_width=2.5, buff=0.08)
        a2 = Arrow(msc_b.get_left(), vlr_b.get_right(), buff=0.08, color=ACCENT_RED,
                   stroke_width=2, max_tip_length_to_length_ratio=0.3)
        arrows_grp.add(a2)
        self.play(Create(a2), Create(vlr_glow), FadeIn(step_texts[1]), run_time=0.6)
        self.wait(0.25)

        # Step 3 — VLR-B queries HLR-A (cross-cell)
        cross_arr = Arrow(vlr_b.get_left(), hlr_a.get_right(), buff=0.1, color=ACCENT_BLUE,
                          stroke_width=2.5, max_tip_length_to_length_ratio=0.28)
        cross_lbl = Text("Query HLR-A", font_size=11, color=ACCENT_BLUE, weight=BOLD).move_to(
            cross_arr.get_center() + UP*0.25)
        arrows_grp.add(cross_arr)
        self.play(Create(cross_arr), FadeIn(cross_lbl), FadeIn(step_texts[2]), run_time=0.7)
        self.wait(0.25)

        # Step 4 — Authentication (shield pulse)
        try:
            shield = SVGMobject(UTILS + "shield.svg").scale(0.40)
        except Exception:
            shield = RegularPolygon(n=5, color=ACCENT_GRN, fill_opacity=0.4).scale(0.30)
        shield.move_to(hlr_a.get_center() + LEFT*0.6)
        auth_lbl = Text("Auth ✓", font_size=12, color=ACCENT_GRN,
                         weight=BOLD).next_to(shield, DOWN, buff=0.08)
        hlr_glow = SurroundingRectangle(hlr_a, color=ACCENT_GRN, stroke_width=2.5, buff=0.08)
        self.play(FadeIn(shield, scale=0.5), FadeIn(auth_lbl),
                  Create(hlr_glow), FadeIn(step_texts[3]), run_time=0.7)
        self.wait(0.25)

        # Step 5 — call proceeds via MSC-B
        a5 = Arrow(msc_b.get_bottom(), bs_b.get_top(), buff=0.08, color=ACCENT_PURP,
                   stroke_width=2, max_tip_length_to_length_ratio=0.3)
        arrows_grp.add(a5)
        self.play(Create(a5), FadeIn(step_texts[4]), run_time=0.5)
        self.wait(0.25)

        # Step 6 — VLR highlight final
        self.play(
            vlr_b.animate.set_color(ACCENT_RED),
            FadeIn(step_texts[5]), run_time=0.5
        )
        self.wait(0.5)

        note = callout_box("VLR plays the major role\nHLR-A is queried for authentication & routing", ACCENT_RED)
        note.next_to(step_texts, DOWN, buff=0.15)
        self.play(FadeIn(note, shift=UP*0.2))
        self.wait(2.0)

        all_obj = VGroup(hdr, hex_home, hex_visit, home_lbl, visit_lbl,
                         bs_a, bs_b, hlr_a, msc_a, vlr_b, msc_b,
                         caller, visitor_tag, arrows_grp,
                         vlr_glow, cross_lbl, shield, auth_lbl, hlr_glow,
                         step_texts, note)
        self.play(FadeOut(all_obj, shift=UP*0.3), run_time=0.7)
        self.wait(0.2)


# ══════════════════════════════════════════════════════════════════════════
# SCENE 8 — SUMMARY COMPARISON TABLE
# ══════════════════════════════════════════════════════════════════════════

class Scene8Summary(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        title = Text("Summary — All 4 Cases", font_size=38, weight=BOLD, color=SOFT_WHITE)
        sub   = Text("Call Establishment in 1G AMPS Cellular Network",
                     font_size=20, color=ACCENT_BLUE)
        hdr   = VGroup(title, sub).arrange(DOWN, buff=0.20).to_edge(UP, buff=0.42)
        self.play(FadeIn(hdr, shift=DOWN*0.15))
        self.wait(0.3)

        # Table headers
        col_headers = ["Case", "Caller", "Receiver", "Key Mechanism", "Key Entity"]
        col_colors  = [SOFT_WHITE] * 5
        col_widths  = [1.0, 2.0, 2.5, 3.0, 2.2]
        col_x_pos   = [-5.2, -3.6, -1.8, 0.5, 3.2]

        header_row = VGroup()
        for txt, col, x in zip(col_headers, col_colors, col_x_pos):
            t = Text(txt, font_size=15, color=ACCENT_BLUE, weight=BOLD).move_to([x, 1.9, 0])
            header_row.add(t)

        header_line = Line(LEFT*6.5 + UP*1.65, RIGHT*6.5 + UP*1.65,
                           color=ACCENT_BLUE, stroke_width=1.5)
        self.play(
            LaggedStart(*[FadeIn(h) for h in header_row], lag_ratio=0.1),
            Create(header_line),
            run_time=0.8
        )

        # Table data
        rows_data = [
            ("1", "Home Cell", "Same Cell", "Direct — no routing", ACCENT_BLUE,   ACCENT_GRN),
            ("2", "Home Cell", "Diff Cell\n(Same MSC)", "Paging + VLR lookup", ACCENT_GRN, ACCENT_RED),
            ("3", "Home Cell", "Diff MSC\n(Cell 3)", "HLR lookup +\nInter-MSC route", ACCENT_PURP, ACCENT_PURP),
            ("4", "Visiting\n(Roaming)", "Any cell", "VLR → HLR auth\n+ routing", ACCENT_RED, ACCENT_RED),
        ]

        row_y = [1.0, 0.1, -0.95, -2.1]
        row_colors = [ACCENT_BLUE, ACCENT_GRN, ACCENT_PURP, ACCENT_RED]

        for i, ((case, caller, recv, mech, row_col, key_col), y) in enumerate(
                zip(rows_data, row_y)):

            row_bg = RoundedRectangle(
                corner_radius=0.1, width=13.0, height=0.78 if "\n" not in caller else 0.95,
                color=row_col, fill_opacity=0.07, stroke_width=0.8
            ).move_to([0, y, 0])

            cells = [
                Text(case,   font_size=14, color=row_col, weight=BOLD),
                Text(caller, font_size=13, color=SOFT_WHITE),
                Text(recv,   font_size=13, color=SOFT_WHITE),
                Text(mech,   font_size=12, color=SOFT_WHITE),
                Text("HLR" if i == 0 else "VLR+Paging" if i == 1 else
                     "HLR+MSC" if i == 2 else "VLR→HLR",
                     font_size=13, color=key_col, weight=BOLD),
            ]
            for cell, x in zip(cells, col_x_pos):
                cell.move_to([x, y, 0])

            row_grp = VGroup(row_bg, *cells)
            self.play(
                FadeIn(row_bg, shift=RIGHT*0.4),
                LaggedStart(*[FadeIn(c, shift=RIGHT*0.2) for c in cells], lag_ratio=0.08),
                run_time=0.65
            )
            self.wait(0.2)

        # Separator line
        sep_line = Line(LEFT*6.5 + UP*1.65, LEFT*6.5 + DOWN*2.7,
                        color=DIM_GREY, stroke_width=0.8)

        self.wait(0.5)

        # Final key insight
        final_msg = Text(
            "The network ALWAYS knows where you are.",
            font_size=24, color=ALT_YELLOW, weight=BOLD
        ).to_edge(DOWN, buff=0.55)
        final_sub = Text(
            "HLR (permanent) + VLR (temporary) = seamless mobility",
            font_size=16, color=DIM_GREY
        ).next_to(final_msg, DOWN, buff=0.18)

        self.play(
            FadeIn(final_msg, scale=0.9),
            run_time=0.7
        )
        self.play(FadeIn(final_sub, shift=UP*0.15), run_time=0.5)
        self.wait(2.5)

        # Fade out everything
        self.play(FadeOut(Group(*self.mobjects), shift=UP*0.3), run_time=0.9)
        self.wait(0.3)


# ══════════════════════════════════════════════════════════════════════════
# FULL VIDEO — renders all scenes sequentially in ONE render pass
# Run with: manim -pqh video2_call_establishment.py FullVideo2
# ══════════════════════════════════════════════════════════════════════════

class FullVideo2(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # ── Scene 1: Recap ───────────────────────────────────────────
        title = Text("Quick Recap", font_size=40, weight=BOLD, color=SOFT_WHITE)
        sub   = Text("What happens when a phone powers ON", font_size=22, color=ACCENT_BLUE)
        hdr   = VGroup(title, sub).arrange(DOWN, buff=0.22).to_edge(UP, buff=0.45)
        self.play(FadeIn(hdr, shift=DOWN * 0.2))
        self.wait(0.3)

        cards_data = [
            ("mobile.svg",
             RoundedRectangle(corner_radius=0.1, width=0.45, height=0.78,
                              color=ALT_YELLOW, fill_opacity=0.3),
             ALT_YELLOW, "Mobile Powers ON",
             "Scans FOCC signals from\nall nearby Base Stations."),
            ("bs_tower.svg",
             Triangle(color=ACCENT_GRN, fill_opacity=0.3).scale(0.48),
             ACCENT_GRN, "Connects to Best BS",
             "Selects BS with the\nstrongest signal strength."),
            ("hlr_box.svg",
             RoundedRectangle(corner_radius=0.1, width=0.65, height=0.52,
                              color=ACCENT_BLUE, fill_opacity=0.3),
             ACCENT_BLUE, "HLR / VLR Updated",
             "Network always knows\nwhere the user is located."),
        ]
        card_group = VGroup(*[make_card(s, f, c, n, d) for s, f, c, n, d in cards_data])
        card_group.arrange(RIGHT, buff=0.40).next_to(hdr, DOWN, buff=0.55)
        card_group.scale_to_fit_width(12.5)
        for card in card_group:
            self.play(FadeIn(card, scale=0.85), run_time=0.55)
            self.wait(0.2)
        self.wait(0.6)

        q = Text("Now — what happens when a CALL is made?",
                 font_size=22, color=ALT_YELLOW, weight=BOLD).to_edge(DOWN, buff=0.65)
        uline = Line(q.get_left()+DOWN*0.08, q.get_right()+DOWN*0.08,
                     color=ALT_YELLOW, stroke_width=1.5)
        self.play(FadeIn(q, shift=UP*0.2), run_time=0.6)
        self.play(Create(uline), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(VGroup(hdr, card_group, q, uline), shift=UP*0.3), run_time=0.6)

        # ── Scene 2: New Entities ────────────────────────────────────
        title2 = Text("Key Players in Call Establishment",
                      font_size=36, weight=BOLD, color=SOFT_WHITE).to_edge(UP, buff=0.45)
        self.play(FadeIn(title2, shift=DOWN*0.2))
        self.wait(0.2)

        cards2_data = [
            ("mobile.svg",
             RoundedRectangle(corner_radius=0.1, width=0.45, height=0.78,
                              color=ALT_YELLOW, fill_opacity=0.3),
             ALT_YELLOW, "MS", "Mobile Station\nCaller / Receiver"),
            ("bs_tower.svg",
             Triangle(color=ACCENT_GRN, fill_opacity=0.3).scale(0.48),
             ACCENT_GRN, "BTS / BS", "Base Station\nRadio Interface"),
            ("msc_switch.svg",
             RoundedRectangle(corner_radius=0.12, width=0.70, height=0.55,
                              color=ACCENT_PURP, fill_opacity=0.35),
             ACCENT_PURP, "MSC", "Mobile Switching Center\nCall Control Brain"),
        ]
        cg2 = VGroup(*[make_card(s, f, c, n, d, 0.42) for s, f, c, n, d in cards2_data])
        cg2.arrange(RIGHT, buff=0.55).next_to(title2, DOWN, buff=0.55)
        cg2.scale_to_fit_width(12.8)
        for card in cg2:
            self.play(FadeIn(card, scale=0.85), run_time=0.5)
            self.wait(0.18)
        self.wait(0.5)

        diag_title = Text("Network Topology", font_size=18, color=DIM_GREY,
                          slant=ITALIC).next_to(cg2, DOWN, buff=0.35)
        self.play(FadeIn(diag_title))

        ms_n  = Circle(radius=0.22, color=ALT_YELLOW, fill_opacity=0.35).shift(LEFT*4.5+DOWN*1.7)
        bs_n  = Circle(radius=0.22, color=ACCENT_GRN, fill_opacity=0.35).shift(LEFT*2.0+DOWN*1.7)
        msc_n = RoundedRectangle(corner_radius=0.1, width=0.9, height=0.5,
                                 color=ACCENT_PURP, fill_opacity=0.35).shift(DOWN*1.7)
        hlr_n = Circle(radius=0.22, color=ACCENT_BLUE, fill_opacity=0.35).shift(RIGHT*2.2+DOWN*1.2)
        vlr_n = Circle(radius=0.22, color=ACCENT_RED,  fill_opacity=0.35).shift(RIGHT*2.2+DOWN*2.2)
        pstn_n= RoundedRectangle(corner_radius=0.1, width=0.9, height=0.4,
                                 color=DIM_GREY, fill_opacity=0.25).shift(RIGHT*4.2+DOWN*1.7)
        nlbls = VGroup(
            Text("MS",   font_size=11, color=ALT_YELLOW).move_to(ms_n),
            Text("BS",   font_size=11, color=ACCENT_GRN).move_to(bs_n),
            Text("MSC",  font_size=11, color=ACCENT_PURP).move_to(msc_n),
            Text("HLR",  font_size=11, color=ACCENT_BLUE).move_to(hlr_n),
            Text("VLR",  font_size=11, color=ACCENT_RED ).move_to(vlr_n),
            Text("PSTN", font_size=11, color=DIM_GREY   ).move_to(pstn_n),
        )
        nodes2 = VGroup(ms_n, bs_n, msc_n, hlr_n, vlr_n, pstn_n)
        edges2 = VGroup(
            Line(ms_n.get_right(),  bs_n.get_left(),  color=SOFT_WHITE, stroke_width=2),
            Line(bs_n.get_right(),  msc_n.get_left(), color=SOFT_WHITE, stroke_width=2),
            Line(msc_n.get_right(), hlr_n.get_left(), color=ACCENT_BLUE, stroke_width=2),
            Line(msc_n.get_right(), vlr_n.get_left(), color=ACCENT_RED,  stroke_width=2),
            Line(msc_n.get_right(), pstn_n.get_left(),color=DIM_GREY,   stroke_width=2),
        )
        self.play(LaggedStart(*[FadeIn(n) for n in nodes2], lag_ratio=0.12),
                  LaggedStart(*[FadeIn(l) for l in nlbls], lag_ratio=0.12))
        self.play(LaggedStart(*[Create(e) for e in edges2], lag_ratio=0.15), run_time=0.9)
        self.wait(1.2)
        self.play(FadeOut(VGroup(title2, cg2, diag_title, nodes2, nlbls, edges2),
                          shift=UP*0.3), run_time=0.6)

        # ── Scene 3: Generic Steps ───────────────────────────────────
        t3  = Text("Generic Steps in Any Call", font_size=38, weight=BOLD, color=SOFT_WHITE)
        s3  = Text("These steps apply to every cellular call scenario",
                   font_size=19, color=ACCENT_BLUE)
        hdr3= VGroup(t3, s3).arrange(DOWN, buff=0.22).to_edge(UP, buff=0.45)
        self.play(FadeIn(hdr3, shift=DOWN*0.2))
        self.wait(0.2)

        steps3 = [
            ("1", "Call Request Initiation",    ALT_YELLOW,  "Mobile dials → sends request via RECC to BS"),
            ("2", "Authentication & Validation", ACCENT_GRN,  "MSC verifies subscriber identity via HLR"),
            ("3", "Location Identification",    ACCENT_BLUE, "HLR/VLR pinpoints which cell the receiver is in"),
            ("4", "Channel Allocation",         ACCENT_PURP, "MSC assigns a Traffic Channel (TCH)"),
            ("5", "Call Routing",               ACCENT_RED,  "Signal routed through BS(s) and MSC(s)"),
            ("6", "Call Setup — Connected!",    ACCENT_GRN,  "Receiver rings → answers → call established"),
        ]
        sitems = VGroup()
        for num, ts, col, desc in steps3:
            nc = Circle(radius=0.24, color=col, fill_opacity=0.25, stroke_width=2)
            nt = Text(num, font_size=18, color=col, weight=BOLD).move_to(nc)
            nm = VGroup(nc, nt)
            stitle = Text(ts,   font_size=17, color=col, weight=BOLD)
            sdesc  = Text(desc, font_size=13, color=DIM_GREY)
            tc     = VGroup(stitle, sdesc).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            sitems.add(VGroup(nm, tc).arrange(RIGHT, buff=0.28))
        sitems.arrange(DOWN, buff=0.30, aligned_edge=LEFT)
        sitems.next_to(hdr3, DOWN, buff=0.45).to_edge(LEFT, buff=1.0)

        lx = sitems.get_left()[0] + 0.24
        vl = DashedLine([lx, sitems[0].get_center()[1], 0],
                        [lx, sitems[-1].get_center()[1], 0],
                        color=DIM_GREY, stroke_width=1.2, dash_length=0.1)
        self.play(Create(vl), run_time=0.5)
        for item in sitems:
            self.play(FadeIn(item, shift=RIGHT*0.3), run_time=0.42)
            self.wait(0.12)
        self.wait(1.2)
        self.play(FadeOut(VGroup(hdr3, sitems, vl), shift=UP*0.3), run_time=0.6)

        # ── Scene 4: Case 1 ─────────────────────────────────────────
        ct1 = Text("CASE 1", font_size=14, color=ACCENT_BLUE, weight=BOLD)
        tt1 = Text("Caller & Receiver — Same Cell", font_size=34, weight=BOLD, color=SOFT_WHITE)
        st1 = Text("Same BS  ·  Same MSC  ·  No inter-cell routing", font_size=17, color=DIM_GREY)
        hdr4= VGroup(ct1, tt1, st1).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr4, shift=DOWN*0.15))
        self.wait(0.2)

        cc1 = UP * 0.2
        hx1 = make_hex(cc1, ACCENT_BLUE, scale=2.0)
        cl1 = Text("Cell 1", font_size=16, color=ACCENT_BLUE, weight=BOLD).move_to(cc1+DOWN*1.7)
        self.play(DrawBorderThenFill(hx1), FadeIn(cl1))

        bs4 = make_bs(cc1+UP*0.1, ACCENT_BLUE)
        self.play(FadeIn(bs4, scale=0.7))

        msc4= make_msc(cc1+RIGHT*2.8+UP*1.1)
        self.play(FadeIn(msc4, scale=0.8))

        hlr4= make_db(cc1+LEFT*2.8+UP*1.1, "hlr_box.svg", "HLR", ACCENT_BLUE)
        vlr4= make_db(cc1+LEFT*2.8+UP*0.35, "vlr_box.svg", "VLR", ACCENT_RED)
        self.play(FadeIn(hlr4, scale=0.8), FadeIn(vlr4, scale=0.8))

        cal4 = make_mobile(cc1+LEFT*1.4+DOWN*0.5, ALT_YELLOW, "Caller")
        rec4 = make_mobile(cc1+RIGHT*1.4+DOWN*0.5, ACCENT_GRN, "Receiver")
        self.play(FadeIn(cal4, scale=0.8), FadeIn(rec4, scale=0.8))
        self.wait(0.3)

        stexts4 = VGroup(*[
            Text(s, font_size=13, color=c) for s, c in [
                ("① Caller → BS  (Call Request via RECC)", ALT_YELLOW),
                ("② BS → MSC  (Forward request)", ACCENT_GRN),
                ("③ MSC ↔ HLR/VLR  (Verify subscriber)", ACCENT_BLUE),
                ("④ MSC → BS → Receiver  (Paging)", ACCENT_PURP),
                ("⑤ TCH allocated  (Traffic Channel)", DIM_GREY),
                ("⑥ Call Connected! ✓", ACCENT_GRN),
            ]
        ])
        stexts4.arrange(DOWN, buff=0.20, aligned_edge=LEFT).to_edge(RIGHT, buff=0.25).shift(DOWN*0.3)

        ag4 = VGroup()
        a4_1 = Arrow(cal4.get_center(), bs4.get_center(), buff=0.22, color=ALT_YELLOW,
                     stroke_width=2.5, max_tip_length_to_length_ratio=0.3)
        ag4.add(a4_1)
        self.play(Create(a4_1), FadeIn(stexts4[0]), run_time=0.55)
        self.wait(0.2)

        a4_2 = Arrow(bs4.get_center(), msc4.get_center(), buff=0.22, color=ACCENT_GRN,
                     stroke_width=2.5, max_tip_length_to_length_ratio=0.3)
        ag4.add(a4_2)
        self.play(Create(a4_2), FadeIn(stexts4[1]), run_time=0.55)
        self.wait(0.2)

        a4_3 = Arrow(msc4.get_center(), hlr4.get_center(), buff=0.22, color=ACCENT_BLUE,
                     stroke_width=2.5, max_tip_length_to_length_ratio=0.3)
        a4_3b= Arrow(hlr4.get_center(), msc4.get_center(), buff=0.22, color=ACCENT_BLUE,
                     stroke_width=2.0, max_tip_length_to_length_ratio=0.3)
        ag4.add(a4_3, a4_3b)
        self.play(Create(a4_3), Create(a4_3b), FadeIn(stexts4[2]), run_time=0.6)
        self.wait(0.2)

        a4_4 = Arrow(msc4.get_center(), rec4.get_center(), buff=0.22, color=ACCENT_PURP,
                     stroke_width=2.5, max_tip_length_to_length_ratio=0.3)
        ag4.add(a4_4)
        self.play(Create(a4_4), FadeIn(stexts4[3]), run_time=0.55)
        self.wait(0.2)

        tch4 = DashedLine(cal4.get_right(), rec4.get_left(),
                          color=DIM_GREY, stroke_width=2, dash_length=0.12)
        tch4l= Text("TCH", font_size=11, color=DIM_GREY).move_to(tch4.get_center()+UP*0.22)
        ag4.add(tch4, tch4l)
        self.play(Create(tch4), FadeIn(tch4l), FadeIn(stexts4[4]), run_time=0.55)
        self.wait(0.2)

        glow4= SurroundingRectangle(VGroup(cal4, rec4), color=ACCENT_GRN,
                                    corner_radius=0.2, stroke_width=2.5, buff=0.15)
        self.play(Create(glow4), FadeIn(stexts4[5]), run_time=0.55)
        self.wait(0.4)

        note4= callout_box("No inter-cell routing → low latency, efficient", ACCENT_GRN)
        note4.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(note4, shift=UP*0.2))
        self.wait(1.8)
        self.play(FadeOut(VGroup(hdr4, hx1, cl1, bs4, msc4, hlr4, vlr4,
                                 cal4, rec4, ag4, stexts4, glow4, note4),
                          shift=UP*0.3), run_time=0.6)

        # ── Scene 5: Case 2 ─────────────────────────────────────────
        ct2 = Text("CASE 2", font_size=14, color=ACCENT_GRN, weight=BOLD)
        tt2 = Text("Different Cell — Same MSC", font_size=34, weight=BOLD, color=SOFT_WHITE)
        st2 = Text("Caller in Cell 1  ·  Receiver in Cell 2  ·  Shared MSC",
                   font_size=17, color=DIM_GREY)
        hdr5= VGroup(ct2, tt2, st2).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr5, shift=DOWN*0.15))
        self.wait(0.2)

        c5a = LEFT*3.0+DOWN*0.2
        c5b = RIGHT*3.0+DOWN*0.2
        hx5a= make_hex(c5a, ACCENT_BLUE, scale=1.65)
        hx5b= make_hex(c5b, ACCENT_GRN,  scale=1.65)
        l5a = Text("Cell 1", font_size=14, color=ACCENT_BLUE, weight=BOLD).move_to(c5a+DOWN*1.5)
        l5b = Text("Cell 2", font_size=14, color=ACCENT_GRN,  weight=BOLD).move_to(c5b+DOWN*1.5)
        self.play(LaggedStart(DrawBorderThenFill(hx5a), DrawBorderThenFill(hx5b), lag_ratio=0.3),
                  LaggedStart(FadeIn(l5a), FadeIn(l5b), lag_ratio=0.3))

        bs5a= make_bs(c5a+UP*0.1, ACCENT_BLUE, "BS₁")
        bs5b= make_bs(c5b+UP*0.1, ACCENT_GRN,  "BS₂")
        msc5= make_msc(UP*2.1)
        vlr5= make_db(UP*2.1+RIGHT*1.4, "vlr_box.svg", "VLR", ACCENT_RED, 0.24)
        hlr5= make_db(UP*2.1+LEFT*1.4,  "hlr_box.svg", "HLR", ACCENT_BLUE, 0.24)
        self.play(FadeIn(bs5a, scale=0.7), FadeIn(bs5b, scale=0.7))
        self.play(FadeIn(msc5, scale=0.8), FadeIn(vlr5, scale=0.8), FadeIn(hlr5, scale=0.8))

        cal5 = make_mobile(c5a+LEFT*1.0+DOWN*0.6, ALT_YELLOW, "Caller")
        rec5 = make_mobile(c5b+RIGHT*1.0+DOWN*0.6, ACCENT_GRN, "Receiver")
        self.play(FadeIn(cal5, scale=0.8), FadeIn(rec5, scale=0.8))
        self.wait(0.3)

        stexts5 = VGroup(*[Text(s, font_size=12, color=c) for s, c in [
            ("① Caller → BS₁ → MSC", ALT_YELLOW),
            ("② MSC queries VLR → receiver in Cell 2", ACCENT_RED),
            ("③ Paging → BS₂ → Receiver", ACCENT_GRN),
            ("④ Channel allocated in both cells", ACCENT_PURP),
            ("⑤ Call connected via MSC ✓", ACCENT_GRN),
        ]])
        stexts5.arrange(DOWN, buff=0.20, aligned_edge=LEFT).to_edge(LEFT, buff=0.20).shift(DOWN*0.5)

        ag5 = VGroup()
        a5_1 = Arrow(cal5.get_top(), bs5a.get_bottom(), buff=0.08, color=ALT_YELLOW,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        a5_1b= Arrow(bs5a.get_top(), msc5.get_bottom(), buff=0.08, color=ALT_YELLOW,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        ag5.add(a5_1, a5_1b)
        self.play(Create(a5_1), Create(a5_1b), FadeIn(stexts5[0]), run_time=0.6)
        self.wait(0.2)

        vlr5g= SurroundingRectangle(vlr5, color=ACCENT_RED, stroke_width=2.5, buff=0.08)
        self.play(Create(vlr5g), FadeIn(stexts5[1]), run_time=0.55)
        self.wait(0.2)

        a5_3 = Arrow(msc5.get_bottom(), bs5b.get_top(), buff=0.08, color=ACCENT_GRN,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        a5_3b= Arrow(bs5b.get_bottom(), rec5.get_top(), buff=0.08, color=ACCENT_GRN,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        ag5.add(a5_3, a5_3b)
        self.play(Create(a5_3), Create(a5_3b), FadeIn(stexts5[2]), run_time=0.6)
        self.wait(0.2)

        tch5a= DashedLine(cal5.get_top(), msc5.get_left(),
                          color=ACCENT_PURP, stroke_width=1.8, dash_length=0.1)
        tch5b= DashedLine(msc5.get_right(), rec5.get_top(),
                          color=ACCENT_PURP, stroke_width=1.8, dash_length=0.1)
        ag5.add(tch5a, tch5b)
        self.play(Create(tch5a), Create(tch5b), FadeIn(stexts5[3]), run_time=0.6)
        self.wait(0.2)

        glow5= VGroup(
            SurroundingRectangle(cal5, color=ACCENT_GRN, corner_radius=0.15,
                                 stroke_width=2, buff=0.1),
            SurroundingRectangle(rec5, color=ACCENT_GRN, corner_radius=0.15,
                                 stroke_width=2, buff=0.1),
        )
        self.play(Create(glow5), FadeIn(stexts5[4]), run_time=0.55)
        self.wait(0.4)

        note5= callout_box("Uses paging + location tracking via VLR", ACCENT_GRN)
        note5.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note5, shift=UP*0.2))
        self.wait(1.8)
        self.play(FadeOut(VGroup(hdr5, hx5a, hx5b, l5a, l5b, bs5a, bs5b,
                                 msc5, vlr5, hlr5, cal5, rec5, ag5,
                                 vlr5g, glow5, stexts5, note5),
                          shift=UP*0.3), run_time=0.6)

        # ── Scene 6: Case 3 ─────────────────────────────────────────
        ct3 = Text("CASE 3", font_size=14, color=ACCENT_PURP, weight=BOLD)
        tt3 = Text("Inter-MSC Call", font_size=34, weight=BOLD, color=SOFT_WHITE)
        st3 = Text("Caller in Cell 1 (MSC-A)  ·  Receiver in Cell 3 (MSC-B)",
                   font_size=17, color=DIM_GREY)
        hdr6= VGroup(ct3, tt3, st3).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr6, shift=DOWN*0.15))
        self.wait(0.2)

        c6a = LEFT*3.2+DOWN*0.3
        c6b = RIGHT*3.2+DOWN*0.3
        hx6a= make_hex(c6a, ACCENT_BLUE, scale=1.55)
        hx6b= make_hex(c6b, ACCENT_RED,  scale=1.55)
        l6a = Text("Cell 1", font_size=13, color=ACCENT_BLUE, weight=BOLD).move_to(c6a+DOWN*1.4)
        l6b = Text("Cell 3", font_size=13, color=ACCENT_RED,  weight=BOLD).move_to(c6b+DOWN*1.4)
        self.play(LaggedStart(DrawBorderThenFill(hx6a), DrawBorderThenFill(hx6b), lag_ratio=0.3),
                  LaggedStart(FadeIn(l6a), FadeIn(l6b), lag_ratio=0.3))

        bs6a= make_bs(c6a+UP*0.05, ACCENT_BLUE, "BS-A")
        bs6b= make_bs(c6b+UP*0.05, ACCENT_RED,  "BS-B")
        msca6= make_msc(c6a+UP*2.2+RIGHT*0.3, "MSC-A", ACCENT_PURP)
        mscb6= make_msc(c6b+UP*2.2+LEFT*0.3,  "MSC-B", ALT_YELLOW)
        hlra6= make_db(c6a+UP*2.2+LEFT*1.1, "hlr_box.svg", "HLR-A", ACCENT_BLUE, 0.22)
        vlrb6= make_db(c6b+UP*2.2+RIGHT*1.1, "vlr_box.svg", "VLR-B", ACCENT_RED, 0.22)
        self.play(FadeIn(bs6a, scale=0.7), FadeIn(bs6b, scale=0.7))
        self.play(FadeIn(msca6, scale=0.8), FadeIn(mscb6, scale=0.8))
        self.play(FadeIn(hlra6, scale=0.8), FadeIn(vlrb6, scale=0.8))

        cal6 = make_mobile(c6a+LEFT*1.0+DOWN*0.7, ALT_YELLOW, "Caller")
        rec6 = make_mobile(c6b+RIGHT*1.0+DOWN*0.7, ACCENT_GRN,  "Receiver")
        self.play(FadeIn(cal6, scale=0.8), FadeIn(rec6, scale=0.8))
        self.wait(0.3)

        stexts6= VGroup(*[Text(s, font_size=12, color=c) for s, c in [
            ("① Caller → BS-A → MSC-A", ALT_YELLOW),
            ("② MSC-A queries HLR-A for receiver's location", ACCENT_BLUE),
            ("③ HLR-A returns MSC-B address", ACCENT_BLUE),
            ("④ Call routed: MSC-A → MSC-B", ACCENT_PURP),
            ("⑤ MSC-B pages receiver via BS-B", ACCENT_RED),
            ("⑥ Channel allocated → Call connected ✓", ACCENT_GRN),
        ]])
        stexts6.arrange(DOWN, buff=0.17, aligned_edge=LEFT).to_edge(DOWN, buff=0.22)

        ag6 = VGroup()
        a6_1 = Arrow(cal6.get_top(), bs6a.get_bottom(), buff=0.08, color=ALT_YELLOW,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        a6_1b= Arrow(bs6a.get_top(), msca6.get_bottom(), buff=0.08, color=ALT_YELLOW,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        ag6.add(a6_1, a6_1b)
        self.play(Create(a6_1), Create(a6_1b), FadeIn(stexts6[0]), run_time=0.6)
        self.wait(0.2)

        a6_2 = Arrow(msca6.get_left(), hlra6.get_right(), buff=0.08, color=ACCENT_BLUE,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        hlr6g= SurroundingRectangle(hlra6, color=ACCENT_BLUE, stroke_width=2.5, buff=0.08)
        ag6.add(a6_2)
        self.play(Create(a6_2), Create(hlr6g), FadeIn(stexts6[1]), run_time=0.6)
        self.wait(0.2)

        a6_3 = Arrow(hlra6.get_right(), msca6.get_left(), buff=0.08, color=ACCENT_BLUE,
                     stroke_width=2.0, max_tip_length_to_length_ratio=0.3)
        ag6.add(a6_3)
        self.play(Create(a6_3), FadeIn(stexts6[2]), run_time=0.55)
        self.wait(0.2)

        inter6= Arrow(msca6.get_right(), mscb6.get_left(), buff=0.1, color=ACCENT_PURP,
                      stroke_width=3.5, max_tip_length_to_length_ratio=0.25)
        intl6 = Text("Inter-MSC Routing", font_size=11, color=ACCENT_PURP,
                     weight=BOLD).move_to(inter6.get_center()+UP*0.25)
        ag6.add(inter6)
        self.play(Create(inter6), FadeIn(intl6), FadeIn(stexts6[3]), run_time=0.7)
        self.wait(0.2)

        a6_5 = Arrow(mscb6.get_bottom(), bs6b.get_top(), buff=0.08, color=ACCENT_RED,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        a6_5b= Arrow(bs6b.get_bottom(), rec6.get_top(), buff=0.08, color=ACCENT_RED,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        ag6.add(a6_5, a6_5b)
        self.play(Create(a6_5), Create(a6_5b), FadeIn(stexts6[4]), run_time=0.6)
        self.wait(0.2)

        glow6= VGroup(
            SurroundingRectangle(cal6, color=ACCENT_GRN, corner_radius=0.15,
                                 stroke_width=2, buff=0.1),
            SurroundingRectangle(rec6, color=ACCENT_GRN, corner_radius=0.15,
                                 stroke_width=2, buff=0.1),
        )
        self.play(Create(glow6), FadeIn(stexts6[5]), run_time=0.55)
        self.wait(1.5)
        self.play(FadeOut(VGroup(hdr6, hx6a, hx6b, l6a, l6b, bs6a, bs6b,
                                 msca6, mscb6, hlra6, vlrb6, cal6, rec6,
                                 ag6, hlr6g, intl6, glow6, stexts6),
                          shift=UP*0.3), run_time=0.6)

        # ── Scene 7: Case 4 ─────────────────────────────────────────
        ct4 = Text("CASE 4", font_size=14, color=ACCENT_RED, weight=BOLD)
        tt4 = Text("Roaming Caller — Visiting Cell", font_size=34, weight=BOLD, color=SOFT_WHITE)
        st4 = Text("Caller's home is Cell A  ·  Currently visiting Cell B",
                   font_size=17, color=DIM_GREY)
        hdr7= VGroup(ct4, tt4, st4).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.38)
        self.play(FadeIn(hdr7, shift=DOWN*0.15))
        self.wait(0.2)

        c7a = LEFT*3.2+DOWN*0.3
        c7b = RIGHT*3.2+DOWN*0.3
        hx7a= make_hex(c7a, ACCENT_BLUE, scale=1.55)
        hx7b= make_hex(c7b, ACCENT_RED,  scale=1.55)
        hl7a= Text("Cell A\n(Home)",    font_size=13, color=ACCENT_BLUE, weight=BOLD).move_to(c7a+DOWN*1.45)
        hl7b= Text("Cell B\n(Visited)", font_size=13, color=ACCENT_RED,  weight=BOLD).move_to(c7b+DOWN*1.45)
        self.play(LaggedStart(DrawBorderThenFill(hx7a), DrawBorderThenFill(hx7b), lag_ratio=0.3),
                  LaggedStart(FadeIn(hl7a), FadeIn(hl7b), lag_ratio=0.3))

        bs7a = make_bs(c7a+UP*0.05, ACCENT_BLUE, "BS-A")
        bs7b = make_bs(c7b+UP*0.05, ACCENT_RED,  "BS-B")
        hlr7a= make_db(c7a+UP*1.8+LEFT*0.6,  "hlr_box.svg", "HLR-A", ACCENT_BLUE, 0.24)
        msc7a= make_msc(c7a+UP*1.8+RIGHT*0.6, "MSC-A", ACCENT_BLUE)
        vlr7b= make_db(c7b+UP*1.8+LEFT*0.6,  "vlr_box.svg", "VLR-B", ACCENT_RED, 0.24)
        msc7b= make_msc(c7b+UP*1.8+RIGHT*0.6, "MSC-B", ACCENT_RED)
        self.play(FadeIn(bs7a, scale=0.7), FadeIn(bs7b, scale=0.7))
        self.play(FadeIn(hlr7a, scale=0.8), FadeIn(msc7a, scale=0.8),
                  FadeIn(vlr7b, scale=0.8), FadeIn(msc7b, scale=0.8))

        cal7 = make_mobile(c7b+LEFT*1.0+DOWN*0.7, ACCENT_RED, "Caller\n(Visitor)")
        vb_t  = Text("VISITOR", font_size=9, color=ACCENT_RED, weight=BOLD, slant=ITALIC)
        vb_box= SurroundingRectangle(vb_t, color=ACCENT_RED, fill_color="#2a0a0a",
                                     fill_opacity=0.8, buff=0.06, stroke_width=1.2,
                                     corner_radius=0.06)
        vtag  = VGroup(vb_box, vb_t).next_to(cal7, UP, buff=0.04)
        self.play(FadeIn(cal7, scale=0.8), FadeIn(vtag, scale=0.8))
        self.wait(0.3)

        stexts7= VGroup(*[Text(s, font_size=12, color=c) for s, c in [
            ("① Caller sends request via visited BS-B", ALT_YELLOW),
            ("② Visited MSC-B checks VLR-B", ACCENT_RED),
            ("③ VLR-B queries HLR-A (home network)", ACCENT_BLUE),
            ("④ Authentication performed by HLR-A", ACCENT_GRN),
            ("⑤ Call proceeds — routed via MSC-B", ACCENT_PURP),
            ("⑥ VLR plays the major role ✓", ACCENT_RED),
        ]])
        stexts7.arrange(DOWN, buff=0.17, aligned_edge=LEFT).to_edge(DOWN, buff=0.22)

        ag7 = VGroup()
        a7_1 = Arrow(cal7.get_top(), bs7b.get_bottom(), buff=0.08, color=ALT_YELLOW,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        a7_1b= Arrow(bs7b.get_top(), msc7b.get_bottom(), buff=0.08, color=ALT_YELLOW,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        ag7.add(a7_1, a7_1b)
        self.play(Create(a7_1), Create(a7_1b), FadeIn(stexts7[0]), run_time=0.6)
        self.wait(0.2)

        vlr7g= SurroundingRectangle(vlr7b, color=ACCENT_RED, stroke_width=2.5, buff=0.08)
        a7_2 = Arrow(msc7b.get_left(), vlr7b.get_right(), buff=0.08, color=ACCENT_RED,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        ag7.add(a7_2)
        self.play(Create(a7_2), Create(vlr7g), FadeIn(stexts7[1]), run_time=0.55)
        self.wait(0.2)

        cross7= Arrow(vlr7b.get_left(), hlr7a.get_right(), buff=0.1, color=ACCENT_BLUE,
                      stroke_width=2.5, max_tip_length_to_length_ratio=0.28)
        crl7  = Text("Query HLR-A", font_size=11, color=ACCENT_BLUE,
                     weight=BOLD).move_to(cross7.get_center()+UP*0.25)
        ag7.add(cross7)
        self.play(Create(cross7), FadeIn(crl7), FadeIn(stexts7[2]), run_time=0.65)
        self.wait(0.2)

        try:
            shield7 = SVGMobject(UTILS+"shield.svg").scale(0.38)
        except Exception:
            shield7 = RegularPolygon(n=5, color=ACCENT_GRN, fill_opacity=0.4).scale(0.28)
        shield7.move_to(hlr7a.get_center()+LEFT*0.55)
        auth7l = Text("Auth ✓", font_size=12, color=ACCENT_GRN,
                      weight=BOLD).next_to(shield7, DOWN, buff=0.07)
        hlr7g  = SurroundingRectangle(hlr7a, color=ACCENT_GRN, stroke_width=2.5, buff=0.08)
        self.play(FadeIn(shield7, scale=0.5), FadeIn(auth7l),
                  Create(hlr7g), FadeIn(stexts7[3]), run_time=0.65)
        self.wait(0.2)

        a7_5 = Arrow(msc7b.get_bottom(), bs7b.get_top(), buff=0.08, color=ACCENT_PURP,
                     stroke_width=2, max_tip_length_to_length_ratio=0.3)
        ag7.add(a7_5)
        self.play(Create(a7_5), FadeIn(stexts7[4]), run_time=0.5)
        self.wait(0.2)

        self.play(FadeIn(stexts7[5]), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(VGroup(hdr7, hx7a, hx7b, hl7a, hl7b,
                                 bs7a, bs7b, hlr7a, msc7a, vlr7b, msc7b,
                                 cal7, vtag, ag7, vlr7g, crl7,
                                 shield7, auth7l, hlr7g, stexts7),
                          shift=UP*0.3), run_time=0.6)

        # ── Scene 8: Summary ─────────────────────────────────────────
        t8  = Text("Summary — All 4 Cases", font_size=38, weight=BOLD, color=SOFT_WHITE)
        s8  = Text("Call Establishment in 1G AMPS Cellular Network",
                   font_size=20, color=ACCENT_BLUE)
        hdr8= VGroup(t8, s8).arrange(DOWN, buff=0.20).to_edge(UP, buff=0.42)
        self.play(FadeIn(hdr8, shift=DOWN*0.15))
        self.wait(0.3)

        col_headers = ["Case", "Caller",       "Receiver",          "Mechanism",          "Key Entity"]
        col_x_pos   = [-5.2,   -3.5,            -1.6,                0.6,                  3.2]

        header_row = VGroup(*[
            Text(h, font_size=15, color=ACCENT_BLUE, weight=BOLD).move_to([x, 1.9, 0])
            for h, x in zip(col_headers, col_x_pos)
        ])
        header_line = Line(LEFT*6.4+UP*1.68, RIGHT*6.4+UP*1.68,
                           color=ACCENT_BLUE, stroke_width=1.5)
        self.play(LaggedStart(*[FadeIn(h) for h in header_row], lag_ratio=0.1),
                  Create(header_line), run_time=0.7)

        rows8 = [
            ("1", "Home Cell",        "Same Cell",         "Direct — no routing",     "HLR/VLR",    ACCENT_BLUE),
            ("2", "Home Cell",        "Diff Cell\n(Same MSC)", "Paging + VLR lookup", "VLR+Paging", ACCENT_GRN),
            ("3", "Home Cell",        "Diff MSC\n(Cell 3)", "HLR lookup +\nInter-MSC", "HLR+MSC",  ACCENT_PURP),
            ("4", "Visiting\n(Roam)", "Any Cell",          "VLR → HLR auth",          "VLR→HLR",   ACCENT_RED),
        ]
        row_y8 = [1.05, 0.12, -0.88, -2.00]

        for i, ((case, caller, recv, mech, key, col), y) in enumerate(zip(rows8, row_y8)):
            bg8 = RoundedRectangle(corner_radius=0.1, width=13.0, height=0.82,
                                   color=col, fill_opacity=0.08, stroke_width=0.8).move_to([0, y, 0])
            cells8 = [
                Text(case,   font_size=14, color=col,       weight=BOLD).move_to([col_x_pos[0], y, 0]),
                Text(caller, font_size=13, color=SOFT_WHITE             ).move_to([col_x_pos[1], y, 0]),
                Text(recv,   font_size=13, color=SOFT_WHITE             ).move_to([col_x_pos[2], y, 0]),
                Text(mech,   font_size=12, color=SOFT_WHITE             ).move_to([col_x_pos[3], y, 0]),
                Text(key,    font_size=13, color=col,       weight=BOLD ).move_to([col_x_pos[4], y, 0]),
            ]
            self.play(FadeIn(bg8, shift=RIGHT*0.3),
                      LaggedStart(*[FadeIn(c, shift=RIGHT*0.15) for c in cells8], lag_ratio=0.07),
                      run_time=0.6)
            self.wait(0.18)

        self.wait(0.5)

        final_msg = Text("The network ALWAYS knows where you are.",
                         font_size=24, color=ALT_YELLOW, weight=BOLD).to_edge(DOWN, buff=0.52)
        final_sub = Text("HLR (permanent) + VLR (temporary) = seamless mobility",
                         font_size=16, color=DIM_GREY).next_to(final_msg, DOWN, buff=0.16)
        self.play(FadeIn(final_msg, scale=0.9), run_time=0.65)
        self.play(FadeIn(final_sub, shift=UP*0.15), run_time=0.5)
        self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects), shift=UP*0.3), run_time=0.9)
        self.wait(0.3)