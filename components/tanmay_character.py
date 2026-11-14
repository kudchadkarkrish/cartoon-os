"""
tanmay_character.py — Tanmay Rai's illustrated cartoon mascot widget.

Draws a charming hand-drawn-style cartoon character representing Tanmay Rai
alongside a speech bubble.  Three pose variants are supported:

    pose="hero"     — confident pointer (GitHub area)
    pose="projects" — confused shrug   (Projects section)
    pose="contact"  — friendly wave    (Contact section)

The dialogue strings are stored as module-level constants so they can be
updated without touching any drawing code.

Usage
-----
    TanmayCharacter(parent, line=TANMAY_LINE_GITHUB,   pointing="left",  pose="hero")
    TanmayCharacter(parent, line=TANMAY_LINE_PROJECTS, pointing="right", pose="projects")
    TanmayCharacter(parent, line=TANMAY_LINE_CONTACT,  pointing="right", pose="contact")
"""

import tkinter as tk


# ── Dialogue constants ────────────────────────────────────────────────────────
# Edit ONLY these strings to change what Tanmay says.  Do not rename the
# constants — they are imported by portfolio.py.

TANMAY_LINE_GITHUB   = "psst. my commits are over there."
TANMAY_LINE_PROJECTS = "it worked yesterday. that's all i can tell you."
TANMAY_LINE_CONTACT  = "send a message. i promise i'm less awkward in code."


# ── Palette ───────────────────────────────────────────────────────────────────
COBALT        = "#4776FF"   # hair / accent
COBALT_DARK   = "#2A50CC"   # hair shadow / shirt shadow
SHIRT_BLUE    = "#7AABFF"   # shirt body (lighter cobalt)
SHIRT_DARK    = "#5588DD"   # shirt shadow strip
CREAM         = "#FFF4D8"   # canvas background
INK           = "#202020"   # outlines
WHITE         = "#FFFFFF"   # bubble fill
YELLOW        = "#FFD85E"   # earphone accent
SKIN          = "#FFD9A8"   # face / hands / neck
SKIN_SHADOW   = "#F0B87E"   # face shadow / cheek
CORD_COL      = "#444444"   # earphone wire
SHOE_COL      = "#1A1A1A"   # dark shoes
COLLAR_COL    = "#F5EDD8"   # cream collar


class TanmayCharacter(tk.Frame):
    """
    A self-contained Frame that draws Tanmay's cartoon mascot + speech bubble.

    Parameters
    ----------
    parent   : tk widget
    line     : str   — one of the TANMAY_LINE_* constants
    pointing : str   — "right" (character left, bubble right)
                       "left"  (character right, bubble left)
    pose     : str   — "hero" | "projects" | "contact"
    """

    # Canvas dimensions
    _CW = 340    # total width
    _CH = 160    # total height

    # Character x-zone width (the slot reserved for the character)
    _CHAR_ZONE = 80

    # Gap between character zone and bubble
    _GAP = 6

    def __init__(self, parent, line: str,
                 pointing: str = "right",
                 pose: str = "hero",
                 **kwargs):
        super().__init__(parent, bg=CREAM, **kwargs)
        self._line     = line
        self._pointing = pointing
        self._pose     = pose
        self._blink_job = None  # for blink animation cleanup

        self._cv = tk.Canvas(
            self,
            width=self._CW,
            height=self._CH,
            bg=CREAM,
            highlightthickness=0,
        )
        self._cv.pack()
        self._draw()

        # Kick off idle blink
        self._blink_job = self._cv.after(3500, self._blink_start)

    # ── public cleanup ────────────────────────────────────────────────────────

    def destroy(self):
        if self._blink_job:
            try:
                self._cv.after_cancel(self._blink_job)
            except Exception:
                pass
        self._blink_job = None
        super().destroy()

    # ── layout dispatcher ─────────────────────────────────────────────────────

    def _draw(self):
        cv  = self._cv
        CW  = self._CW
        CH  = self._CH
        gap = self._GAP
        cz  = self._CHAR_ZONE

        if self._pointing == "right":
            # Character on LEFT, bubble on RIGHT
            cx = cz // 2 + 4          # character centre-x
            cy = CH - 22              # character centre-y (bottom-aligned)
            bx = cz + gap
            by = 6
            bw = CW - bx - 4
            bh = CH - 12
            tail_side = "left"
        else:
            # Character on RIGHT, bubble on LEFT
            cx = CW - cz // 2 - 4
            cy = CH - 22
            bw = CW - cz - gap - 8
            bx = 4
            by = 6
            bh = CH - 12
            tail_side = "right"

        self._draw_bubble(cv, bx, by, bw, bh, tail_side)
        self._draw_character(cv, cx, cy)

    # ══════════════════════════════════════════════════════════════════════════
    # Character drawing
    # ══════════════════════════════════════════════════════════════════════════

    def _draw_character(self, cv, cx: int, cy: int):
        """
        Draw Tanmay's full-body cartoon character centred at (cx, bottom=cy).
        cy is the Y of the bottom of the feet.
        """
        pose = self._pose
        # ── measurements (all relative to cx / cy) ────────────────────────
        shoe_h   = 7     # shoe oval height
        leg_h    = 26    # leg height
        torso_h  = 30    # torso height
        neck_h   = 6
        head_r   = 16    # head radius (slightly oval: wider)

        # Y positions (from bottom up)
        shoe_y   = cy                        # bottom of shoes
        hip_y    = shoe_y  - shoe_h - 2      # hip (top of legs)
        chest_y  = hip_y   - leg_h           # bottom of torso
        neck_bot = chest_y - torso_h         # bottom of neck
        neck_top = neck_bot - neck_h
        head_cy  = neck_top - head_r + 4     # head centre y

        # Arm attachment
        arm_y    = chest_y - torso_h // 2 + 4  # shoulder height

        # ── Shoes ─────────────────────────────────────────────────────────
        self._draw_shoes(cv, cx, shoe_y)

        # ── Legs ──────────────────────────────────────────────────────────
        self._draw_legs(cv, cx, hip_y, leg_h)

        # ── Torso (shirt) ─────────────────────────────────────────────────
        self._draw_torso(cv, cx, chest_y, torso_h)

        # ── Arms (pose-dependent) ─────────────────────────────────────────
        if pose == "hero":
            self._draw_arms_hero(cv, cx, arm_y)
        elif pose == "projects":
            self._draw_arms_projects(cv, cx, arm_y)
        else:  # contact
            self._draw_arms_contact(cv, cx, arm_y)

        # ── Neck ──────────────────────────────────────────────────────────
        cv.create_polygon(
            cx - 4, neck_bot,
            cx + 4, neck_bot,
            cx + 3, neck_top,
            cx - 3, neck_top,
            fill=SKIN, outline=INK, width=1,
        )

        # ── Head (draw before hair so hair overlaps top of head) ──────────
        self._draw_head(cv, cx, head_cy, head_r, pose)

        # ── Curly blue hair (drawn ON TOP of head top) ────────────────────
        self._draw_curly_hair(cv, cx, head_cy, head_r)

        # ── Earphones ─────────────────────────────────────────────────────
        self._draw_earphones(cv, cx, head_cy, head_r)

    # ── Body parts ────────────────────────────────────────────────────────────

    def _draw_shoes(self, cv, cx, shoe_y):
        """Two rounded dark shoes."""
        # left shoe
        cv.create_oval(
            cx - 17, shoe_y - 7,
            cx - 2,  shoe_y + 1,
            fill=SHOE_COL, outline=INK, width=1,
        )
        # right shoe
        cv.create_oval(
            cx + 2,  shoe_y - 7,
            cx + 17, shoe_y + 1,
            fill=SHOE_COL, outline=INK, width=1,
        )

    def _draw_legs(self, cv, cx, hip_y, leg_h):
        """Two slightly tapered leg polygons."""
        # left leg
        cv.create_polygon(
            cx - 12, hip_y,
            cx - 4,  hip_y,
            cx - 6,  hip_y + leg_h,
            cx - 14, hip_y + leg_h,
            fill=INK, outline=INK, width=1,
        )
        # right leg
        cv.create_polygon(
            cx + 4,  hip_y,
            cx + 12, hip_y,
            cx + 14, hip_y + leg_h,
            cx + 6,  hip_y + leg_h,
            fill=INK, outline=INK, width=1,
        )
        # trousers highlight stripe
        cv.create_line(cx - 8, hip_y + 4, cx - 8, hip_y + leg_h - 4,
                       fill="#2A2A2A", width=1)
        cv.create_line(cx + 8, hip_y + 4, cx + 8, hip_y + leg_h - 4,
                       fill="#2A2A2A", width=1)

    def _draw_torso(self, cv, cx, chest_y, torso_h):
        """Rounded torso polygon with shirt colour and collar."""
        tw = 16   # half-width at shoulder
        bw = 13   # half-width at hips
        top_y = chest_y - torso_h
        bot_y = chest_y

        # Main shirt body
        cv.create_polygon(
            cx - tw, top_y,
            cx + tw, top_y,
            cx + bw, bot_y,
            cx - bw, bot_y,
            fill=SHIRT_BLUE, outline=INK, width=2,
            smooth=True,
        )

        # Shirt shadow strip (right side)
        cv.create_polygon(
            cx + 6,  top_y + 4,
            cx + tw, top_y,
            cx + bw, bot_y,
            cx + 6,  bot_y,
            fill=SHIRT_DARK, outline="",
        )

        # V-collar (cream)
        cv.create_polygon(
            cx - 5, top_y,
            cx + 5, top_y,
            cx,     top_y + 8,
            fill=COLLAR_COL, outline=INK, width=1,
        )

        # Pocket detail (small rectangle, lower-left of torso)
        px = cx - tw + 4
        py = top_y + torso_h // 2
        cv.create_rectangle(px, py, px + 8, py + 6,
                            fill=SHIRT_DARK, outline=INK, width=1)

    def _draw_arms_hero(self, cv, cx, arm_y):
        """
        Hero pose: right arm extends outward/forward (pointing toward bubble),
        left arm rests down slightly.
        Pointing direction determines which side the bubble is on.
        """
        pointing = self._pointing
        arm_len  = 22
        arm_wid  = 5

        if pointing == "right":
            # Character is on LEFT → right arm points RIGHT toward bubble
            # Right arm: extends to the right and slightly up
            rx0, ry0 = cx + 14, arm_y
            rx1, ry1 = cx + 14 + arm_len, arm_y - 6
            self._draw_arm_polygon(cv, rx0, ry0, rx1, ry1, arm_wid)
            # Hand (pointing right)
            cv.create_oval(rx1 - 5, ry1 - 5, rx1 + 6, ry1 + 4,
                           fill=SKIN, outline=INK, width=1)
            # Finger extended (pointing tip)
            cv.create_line(rx1 + 2, ry1 - 2, rx1 + 10, ry1 - 7,
                           fill=SKIN, width=3, capstyle="round")
            cv.create_oval(rx1 + 8, ry1 - 10, rx1 + 14, ry1 - 4,
                           fill=SKIN, outline=INK, width=1)
        else:
            # Character is on RIGHT → left arm points LEFT toward bubble
            lx0, ly0 = cx - 14, arm_y
            lx1, ly1 = cx - 14 - arm_len, arm_y - 6
            self._draw_arm_polygon(cv, lx0, ly0, lx1, ly1, arm_wid)
            # Hand (pointing left)
            cv.create_oval(lx1 - 6, ly1 - 5, lx1 + 5, ly1 + 4,
                           fill=SKIN, outline=INK, width=1)
            # Finger extended (pointing tip)
            cv.create_line(lx1 - 2, ly1 - 2, lx1 - 10, ly1 - 7,
                           fill=SKIN, width=3, capstyle="round")
            cv.create_oval(lx1 - 14, ly1 - 10, lx1 - 8, ly1 - 4,
                           fill=SKIN, outline=INK, width=1)

        # Opposite arm: relaxed down
        if pointing == "right":
            lx0, ly0 = cx - 14, arm_y
            lx1, ly1 = cx - 18, arm_y + 16
            self._draw_arm_polygon(cv, lx0, ly0, lx1, ly1, arm_wid - 1)
            cv.create_oval(lx1 - 5, ly1 - 4, lx1 + 4, ly1 + 5,
                           fill=SKIN, outline=INK, width=1)
        else:
            rx0, ry0 = cx + 14, arm_y
            rx1, ry1 = cx + 18, arm_y + 16
            self._draw_arm_polygon(cv, rx0, ry0, rx1, ry1, arm_wid - 1)
            cv.create_oval(rx1 - 4, ry1 - 4, rx1 + 5, ry1 + 5,
                           fill=SKIN, outline=INK, width=1)

    def _draw_arms_projects(self, cv, cx, arm_y):
        """
        Projects pose: confused shrug.
        Both arms raised slightly, elbows out, hands up.
        """
        arm_wid = 5

        # Left arm: raised and bent outward
        lshoulder_x, lshoulder_y = cx - 14, arm_y
        lelbow_x,    lelbow_y    = cx - 26, arm_y - 8
        lhand_x,     lhand_y    = cx - 20, arm_y - 22

        # Upper arm segment
        self._draw_arm_polygon(cv, lshoulder_x, lshoulder_y,
                                   lelbow_x, lelbow_y, arm_wid)
        # Forearm segment (bent upward)
        self._draw_arm_polygon(cv, lelbow_x, lelbow_y,
                                   lhand_x, lhand_y, arm_wid - 1)
        # Hand
        cv.create_oval(lhand_x - 5, lhand_y - 5, lhand_x + 4, lhand_y + 4,
                       fill=SKIN, outline=INK, width=1)

        # Right arm: raised and bent outward (mirror)
        rshoulder_x, rshoulder_y = cx + 14, arm_y
        relbow_x,    relbow_y    = cx + 26, arm_y - 8
        rhand_x,     rhand_y    = cx + 20, arm_y - 22

        self._draw_arm_polygon(cv, rshoulder_x, rshoulder_y,
                                   relbow_x, relbow_y, arm_wid)
        self._draw_arm_polygon(cv, relbow_x, relbow_y,
                                   rhand_x, rhand_y, arm_wid - 1)
        cv.create_oval(rhand_x - 4, rhand_y - 5, rhand_x + 5, rhand_y + 4,
                       fill=SKIN, outline=INK, width=1)

    def _draw_arms_contact(self, cv, cx, arm_y):
        """
        Contact pose: friendly wave.
        One arm raised high and open, other arm down naturally.
        """
        arm_wid  = 5
        pointing = self._pointing

        # Wave arm — opposite side to where the bubble is, so wave faces viewer
        if pointing == "right":
            # Bubble on right → wave with RIGHT arm (toward viewer)
            wx0, wy0 = cx + 14, arm_y
            wx1, wy1 = cx + 24, arm_y - 20   # elbow
            wx2, wy2 = cx + 16, arm_y - 36   # hand (raised)
            self._draw_arm_polygon(cv, wx0, wy0, wx1, wy1, arm_wid)
            self._draw_arm_polygon(cv, wx1, wy1, wx2, wy2, arm_wid - 1)
            # Open waving hand (palm oval)
            cv.create_oval(wx2 - 7, wy2 - 6, wx2 + 6, wy2 + 6,
                           fill=SKIN, outline=INK, width=1)
            # Three small fingers
            for i, (fdx, fdy) in enumerate([(-5, -8), (0, -9), (5, -8)]):
                cv.create_oval(wx2 + fdx - 3, wy2 + fdy - 3,
                               wx2 + fdx + 3, wy2 + fdy + 3,
                               fill=SKIN, outline=INK, width=1)

            # Resting left arm
            lx0, ly0 = cx - 14, arm_y
            lx1, ly1 = cx - 19, arm_y + 16
            self._draw_arm_polygon(cv, lx0, ly0, lx1, ly1, arm_wid - 1)
            cv.create_oval(lx1 - 5, ly1 - 4, lx1 + 4, ly1 + 5,
                           fill=SKIN, outline=INK, width=1)
        else:
            # Bubble on left → wave with LEFT arm
            wx0, wy0 = cx - 14, arm_y
            wx1, wy1 = cx - 24, arm_y - 20
            wx2, wy2 = cx - 16, arm_y - 36
            self._draw_arm_polygon(cv, wx0, wy0, wx1, wy1, arm_wid)
            self._draw_arm_polygon(cv, wx1, wy1, wx2, wy2, arm_wid - 1)
            cv.create_oval(wx2 - 6, wy2 - 6, wx2 + 7, wy2 + 6,
                           fill=SKIN, outline=INK, width=1)
            for i, (fdx, fdy) in enumerate([(-5, -8), (0, -9), (5, -8)]):
                cv.create_oval(wx2 + fdx - 3, wy2 + fdy - 3,
                               wx2 + fdx + 3, wy2 + fdy + 3,
                               fill=SKIN, outline=INK, width=1)

            rx0, ry0 = cx + 14, arm_y
            rx1, ry1 = cx + 19, arm_y + 16
            self._draw_arm_polygon(cv, rx0, ry0, rx1, ry1, arm_wid - 1)
            cv.create_oval(rx1 - 4, ry1 - 4, rx1 + 5, ry1 + 5,
                           fill=SKIN, outline=INK, width=1)

    def _draw_arm_polygon(self, cv, x0, y0, x1, y1, half_w):
        """Draw a filled arm segment as a thick tapered polygon."""
        import math
        dx = x1 - x0
        dy = y1 - y0
        length = math.hypot(dx, dy) or 1
        # Perpendicular unit vector
        px = -dy / length
        py =  dx / length
        w0 = half_w        # width at base
        w1 = max(half_w - 2, 2)   # slightly narrower at tip
        pts = [
            x0 + px * w0, y0 + py * w0,
            x1 + px * w1, y1 + py * w1,
            x1 - px * w1, y1 - py * w1,
            x0 - px * w0, y0 - py * w0,
        ]
        cv.create_polygon(pts, fill=SHIRT_BLUE, outline=INK, width=1, smooth=False)

    def _draw_head(self, cv, cx, head_cy, head_r, pose):
        """Draw head oval, facial features (eyes, brows, nose, mouth)."""
        hw = head_r + 2   # slightly wider than tall

        # Slight cheek blush
        cv.create_oval(cx - hw + 2, head_cy + 2, cx - hw + 10, head_cy + 9,
                       fill=SKIN_SHADOW, outline="")
        cv.create_oval(cx + hw - 10, head_cy + 2, cx + hw - 2, head_cy + 9,
                       fill=SKIN_SHADOW, outline="")

        # Head
        cv.create_oval(cx - hw, head_cy - head_r,
                       cx + hw, head_cy + head_r,
                       fill=SKIN, outline=INK, width=2)

        # ── Eyes ──────────────────────────────────────────────────────────
        ex_l = cx - 6
        ex_r = cx + 6
        ey   = head_cy - 3

        if pose == "contact":
            # Happy squint — half-closed arc eyes
            cv.create_arc(ex_l - 5, ey - 3, ex_l + 3, ey + 5,
                          start=30, extent=120, style="arc",
                          outline=INK, width=2)
            cv.create_arc(ex_r - 3, ey - 3, ex_r + 5, ey + 5,
                          start=30, extent=120, style="arc",
                          outline=INK, width=2)
            self._eye_l = None
            self._eye_r = None
        else:
            # Normal oval eyes with pupil
            self._eye_l = cv.create_oval(ex_l - 4, ey - 4, ex_l + 4, ey + 4,
                                          fill=WHITE, outline=INK, width=1)
            self._eye_r = cv.create_oval(ex_r - 4, ey - 4, ex_r + 4, ey + 4,
                                          fill=WHITE, outline=INK, width=1)
            # Pupils (offset slightly based on pose)
            pupil_dx = 1 if pose == "projects" else 0
            pupil_dy = 0
            cv.create_oval(ex_l - 2 + pupil_dx, ey - 2 + pupil_dy,
                           ex_l + 2 + pupil_dx, ey + 2 + pupil_dy,
                           fill=INK, outline="")
            cv.create_oval(ex_r - 2 + pupil_dx, ey - 2 + pupil_dy,
                           ex_r + 2 + pupil_dx, ey + 2 + pupil_dy,
                           fill=INK, outline="")
            # Highlight glint
            cv.create_oval(ex_l - 1 + pupil_dx, ey - 3 + pupil_dy,
                           ex_l + 1 + pupil_dx, ey - 1 + pupil_dy,
                           fill=WHITE, outline="")
            cv.create_oval(ex_r - 1 + pupil_dx, ey - 3 + pupil_dy,
                           ex_r + 1 + pupil_dx, ey - 1 + pupil_dy,
                           fill=WHITE, outline="")

        # Store eye positions for blink
        self._eye_pos = (ex_l, ex_r, ey)

        # ── Eyebrows ──────────────────────────────────────────────────────
        by_base = ey - 7
        if pose == "projects":
            # One brow raised (left), right brow normal
            cv.create_line(ex_l - 5, by_base - 3, ex_l + 4, by_base,
                           fill=INK, width=2, capstyle="round")
            cv.create_line(ex_r - 4, by_base,     ex_r + 5, by_base,
                           fill=INK, width=2, capstyle="round")
        elif pose == "contact":
            # Both brows raised slightly (happy)
            cv.create_arc(ex_l - 5, by_base - 4, ex_l + 5, by_base + 2,
                          start=10, extent=160, style="arc",
                          outline=INK, width=2)
            cv.create_arc(ex_r - 5, by_base - 4, ex_r + 5, by_base + 2,
                          start=10, extent=160, style="arc",
                          outline=INK, width=2)
        else:
            # Hero: confident flat-to-slight-V brows
            cv.create_line(ex_l - 5, by_base, ex_l + 4, by_base - 2,
                           fill=INK, width=2, capstyle="round")
            cv.create_line(ex_r - 4, by_base - 2, ex_r + 5, by_base,
                           fill=INK, width=2, capstyle="round")

        # ── Nose ──────────────────────────────────────────────────────────
        # Small teardrop shape
        cv.create_oval(cx - 2, head_cy + 1, cx + 2, head_cy + 5,
                       fill=SKIN_SHADOW, outline=INK, width=1)

        # ── Mouth / Smile ─────────────────────────────────────────────────
        mouth_y = head_cy + 8
        if pose == "hero":
            # Confident smirk (asymmetric arc)
            cv.create_arc(cx - 7, mouth_y - 2, cx + 7, mouth_y + 6,
                          start=210, extent=120, style="arc",
                          outline=INK, width=2)
        elif pose == "projects":
            # Flat / slight frown (confused)
            cv.create_arc(cx - 6, mouth_y, cx + 6, mouth_y + 5,
                          start=0, extent=180, style="arc",
                          outline=INK, width=2)
        else:
            # Contact: wide friendly smile
            cv.create_arc(cx - 8, mouth_y - 2, cx + 8, mouth_y + 8,
                          start=200, extent=140, style="arc",
                          outline=INK, width=2)

    def _draw_curly_hair(self, cv, cx, head_cy, head_r):
        """
        Draw Tanmay's distinctive blue curly hair as individual curl shapes —
        NOT a blob.  Uses create_arc() to form C-shaped curls layered across
        the top of the head.
        """
        hair_top = head_cy - head_r   # top edge of head

        # Define curls as (centre_x, centre_y, width, height, start_angle, extent, layer)
        # Layer 0 = background, Layer 1 = foreground curl on top
        curls = [
            # Row of base curls (behind / at hairline)
            {"cx": cx - 16, "cy": hair_top + 4,  "w": 16, "h": 14, "s": 40,  "e": 200},
            {"cx": cx - 6,  "cy": hair_top + 1,  "w": 16, "h": 16, "s": 20,  "e": 220},
            {"cx": cx + 4,  "cy": hair_top,       "w": 16, "h": 16, "s": 10,  "e": 200},
            {"cx": cx + 14, "cy": hair_top + 3,   "w": 16, "h": 14, "s": 30,  "e": 200},
            # Second row (slightly higher, tighter curls)
            {"cx": cx - 12, "cy": hair_top - 6,  "w": 13, "h": 12, "s": 60,  "e": 180},
            {"cx": cx,      "cy": hair_top - 8,  "w": 14, "h": 12, "s": 30,  "e": 200},
            {"cx": cx + 11, "cy": hair_top - 5,  "w": 12, "h": 11, "s": 50,  "e": 190},
            # Top flourish curl
            {"cx": cx - 3,  "cy": hair_top - 16, "w": 12, "h": 10, "s": 20,  "e": 220},
        ]

        # Draw filled curl blobs first (blue base)
        for c in curls:
            x0 = c["cx"] - c["w"] // 2
            y0 = c["cy"] - c["h"] // 2
            x1 = c["cx"] + c["w"] // 2
            y1 = c["cy"] + c["h"] // 2
            cv.create_oval(x0, y0, x1, y1,
                           fill=COBALT, outline="")

        # Draw ink outline arcs on top (the individual "curl" contours)
        for c in curls:
            x0 = c["cx"] - c["w"] // 2 - 1
            y0 = c["cy"] - c["h"] // 2 - 1
            x1 = c["cx"] + c["w"] // 2 + 1
            y1 = c["cy"] + c["h"] // 2 + 1
            cv.create_arc(x0, y0, x1, y1,
                          start=c["s"], extent=c["e"],
                          style="arc", outline=COBALT_DARK, width=2)

        # Highlight glints on a couple of curls (small white arc)
        for c in [curls[1], curls[5]]:
            x0 = c["cx"] - c["w"] // 2 + 2
            y0 = c["cy"] - c["h"] // 2 + 2
            x1 = c["cx"] + c["w"] // 2 - 2
            y1 = c["cy"] + c["h"] // 2 - 2
            cv.create_arc(x0, y0, x1, y1,
                          start=60, extent=70,
                          style="arc", outline=WHITE, width=1)

    def _draw_earphones(self, cv, cx, head_cy, head_r):
        """Wired earphones: buds on ears, arc wire over head."""
        bud_rx = head_r + 2   # bud x offset from centre
        bud_y  = head_cy + 1  # bud vertical position (ear level)

        # Left ear bud
        cv.create_oval(cx - bud_rx - 5, bud_y - 4,
                       cx - bud_rx + 1, bud_y + 4,
                       fill=INK, outline="")
        cv.create_oval(cx - bud_rx - 3, bud_y - 2,
                       cx - bud_rx,     bud_y + 2,
                       fill=YELLOW, outline="")

        # Right ear bud
        cv.create_oval(cx + bud_rx - 1, bud_y - 4,
                       cx + bud_rx + 5, bud_y + 4,
                       fill=INK, outline="")
        cv.create_oval(cx + bud_rx,     bud_y - 2,
                       cx + bud_rx + 3, bud_y + 2,
                       fill=YELLOW, outline="")

        # Overhead wire arc
        wire_margin = bud_rx + 4
        cv.create_arc(
            cx - wire_margin, head_cy - head_r - 10,
            cx + wire_margin, head_cy + head_r - 6,
            start=0, extent=180,
            style="arc", outline=CORD_COL, width=2,
        )

        # Dangling cord to pocket area (from left bud downward)
        cord_x = cx - bud_rx - 2
        cv.create_line(cord_x, bud_y + 4,
                       cord_x + 2, bud_y + 16,
                       cx - 6,     bud_y + 22,
                       fill=CORD_COL, width=1, smooth=True)

    # ══════════════════════════════════════════════════════════════════════════
    # Speech bubble
    # ══════════════════════════════════════════════════════════════════════════

    def _draw_bubble(self, cv, bx: int, by: int, bw: int, bh: int,
                     tail_side: str):
        """
        Draw a proper rounded-rectangle speech bubble with a triangular tail.
        Tail points toward the character's mouth area.
        """
        r        = 12       # corner radius
        x0, y0   = bx,      by
        x1, y1   = bx + bw, by + bh

        # Tail dimensions
        tail_len = 16       # how far tail tip extends from bubble edge
        tail_hw  = 9        # half-height of tail base on the edge

        # Tail attaches near the bottom-third of the bubble (mouth height)
        tail_mid_y = y0 + bh * 2 // 3

        # Rounded rectangle corners (8 points per corner, approximated with
        # straight segments is fine because smooth=True rounds them).
        if tail_side == "left":
            # Tail protrudes from left edge
            pts = [
                x0 + r,            y0,            # top-left start
                x1 - r,            y0,            # top-right start
                x1,                y0,            # corner
                x1,                y0 + r,
                x1,                y1 - r,
                x1,                y1,            # corner
                x1 - r,            y1,
                x0 + r,            y1,
                x0,                y1,            # corner
                x0,                y1 - r,
                x0,                tail_mid_y + tail_hw,
                x0 - tail_len,     tail_mid_y,   # tail tip
                x0,                tail_mid_y - tail_hw,
                x0,                y0 + r,
                x0,                y0,            # corner
                x0 + r,            y0,
            ]
        else:
            # Tail protrudes from right edge
            pts = [
                x0 + r,            y0,
                x1 - r,            y0,
                x1,                y0,
                x1,                y0 + r,
                x1,                tail_mid_y - tail_hw,
                x1 + tail_len,     tail_mid_y,   # tail tip
                x1,                tail_mid_y + tail_hw,
                x1,                y1 - r,
                x1,                y1,
                x1 - r,            y1,
                x0 + r,            y1,
                x0,                y1,
                x0,                y1 - r,
                x0,                y0 + r,
                x0,                y0,
                x0 + r,            y0,
            ]

        # Shadow (offset polygon)
        shadow_pts = [p + 3 if i % 2 == 0 else p + 2 for i, p in enumerate(pts)]
        cv.create_polygon(shadow_pts,
                          fill="#CCBBAA", outline="",
                          smooth=True)

        # Main bubble
        cv.create_polygon(pts,
                          fill=WHITE, outline=INK, width=2,
                          smooth=True)

        # ── Dialogue text ──────────────────────────────────────────────────
        # Centre text in the bubble, accounting for tail indent on left side
        tail_indent = tail_len + 4 if tail_side == "left" else 0
        text_x = x0 + tail_indent + (bw - tail_indent) // 2
        text_y = y0 + bh // 2

        wrap_w = bw - tail_indent - 22

        cv.create_text(
            text_x, text_y,
            text=self._line,
            font=("Helvetica", 9, "italic"),
            fill=INK,
            width=max(wrap_w, 60),
            justify="left",
            anchor="center",
        )

    # ══════════════════════════════════════════════════════════════════════════
    # Blink animation
    # ══════════════════════════════════════════════════════════════════════════

    def _blink_start(self):
        """Briefly squish the eye ovals to simulate a blink."""
        if not self._cv.winfo_exists():
            return
        if not hasattr(self, "_eye_l") or self._eye_l is None:
            # Arc eyes (contact pose) — skip blink
            self._blink_job = self._cv.after(4000, self._blink_start)
            return
        try:
            ex_l, ex_r, ey = self._eye_pos
            # Squish eyes to a thin horizontal line
            self._cv.coords(self._eye_l,
                            ex_l - 4, ey - 1, ex_l + 4, ey + 1)
            self._cv.coords(self._eye_r,
                            ex_r - 4, ey - 1, ex_r + 4, ey + 1)
            self._blink_job = self._cv.after(90, self._blink_end)
        except Exception:
            pass

    def _blink_end(self):
        """Restore eyes after blink and schedule the next one."""
        if not self._cv.winfo_exists():
            return
        try:
            ex_l, ex_r, ey = self._eye_pos
            self._cv.coords(self._eye_l,
                            ex_l - 4, ey - 4, ex_l + 4, ey + 4)
            self._cv.coords(self._eye_r,
                            ex_r - 4, ey - 4, ex_r + 4, ey + 4)
        except Exception:
            pass
        self._blink_job = self._cv.after(3800, self._blink_start)
