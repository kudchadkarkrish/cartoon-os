"""
profile_card.py — Reusable profile card widget for the CARTOON OS desktop.

Each card is a Canvas-based component that supports:
  • Cartoon avatar (drawn with Canvas primitives)
  • Profile number, name, role
  • Hover elevation + color shift
  • Press feedback
  • Animated arrow indicator
"""

import tkinter as tk


# ── palette ───────────────────────────────────────────────────────────────────
CARD_BG      = "#FFFFFF"
CARD_BORDER  = "#202020"
CARD_SHADOW  = "#C8BBAA"
TEXT_DARK    = "#202020"
TEXT_MID     = "#555555"
CREAM        = "#FFF4D8"


class ProfileCard(tk.Frame):
    """
    A single profile card for the desktop screen.

    Parameters
    ----------
    parent       : tk widget
    profile      : dict  — one entry from data/profiles.py
    on_click     : callable  — called with profile dict when card is activated
    """

    CARD_W = 260
    CARD_H = 320

    def __init__(self, parent, profile: dict, on_click, **kwargs):
        super().__init__(parent, bg=CREAM, **kwargs)
        self._profile   = profile
        self._on_click  = on_click
        self._accent    = profile.get("accent_color", "#4776FF")
        self._hovering  = False
        self._arrow_job = None
        self._arrow_y   = 0
        self._arrow_dir = 1

        self._build()

    # ── construction ──────────────────────────────────────────────────────────

    def _build(self):
        W, H = self.CARD_W, self.CARD_H

        # shadow offset frame
        self._shadow = tk.Frame(self, bg=CARD_SHADOW, width=W, height=H)
        self._shadow.place(x=5, y=5)

        # main canvas
        self._cv = tk.Canvas(
            self,
            width=W, height=H,
            bg=CARD_BG,
            highlightthickness=3,
            highlightbackground=CARD_BORDER,
        )
        self._cv.place(x=0, y=0)

        # total frame size = card + shadow bleed
        self.configure(width=W + 6, height=H + 6)

        self._draw_card()
        self._bind_events()

    def _draw_card(self):
        cv = self._cv
        cv.delete("all")
        W, H = self.CARD_W, self.CARD_H
        acc = self._accent

        # ── accent header strip ────────────────────────────────────────────
        cv.create_rectangle(0, 0, W, 68, fill=acc, outline="")

        # profile number badge
        cv.create_rectangle(10, 10, 50, 38, fill=CARD_BG, outline=CARD_BORDER, width=2)
        cv.create_text(30, 24, text=self._profile["number"],
                       font=("Courier", 11, "bold"), fill=CARD_BORDER)

        # ── avatar area ───────────────────────────────────────────────────
        cx, cy = W // 2, 118
        shape  = self._profile.get("avatar_shape", "circle")
        img_rel = self._profile.get("avatar_image")
        self._avatar_img = None
        has_img = False
        if img_rel:
            import os
            proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            full_path = img_rel if os.path.isabs(img_rel) else os.path.join(proj_dir, img_rel)
            if os.path.exists(full_path):
                try:
                    self._avatar_img = tk.PhotoImage(file=full_path)
                    r = 42
                    cv.create_rectangle(cx - r + 3, cy - r + 3, cx + r + 3, cy + r + 3,
                                        fill=CARD_SHADOW, outline="")
                    cv.create_rectangle(cx - r, cy - r, cx + r, cy + r,
                                        fill=acc, outline=CARD_BORDER, width=3)
                    cv.create_image(cx, cy, image=self._avatar_img)
                    has_img = True
                except Exception:
                    has_img = False

        if not has_img:
            self._draw_avatar(cv, cx, cy, shape, acc)

        # Dynamic font scaling to guarantee name fits on a single line
        name = self._profile["name"]
        name_font = ("Helvetica", 14, "bold")
        try:
            from tkinter import font as tkfont
            for sz in (14, 13, 12, 11, 10):
                f = tkfont.Font(family="Helvetica", size=sz, weight="bold")
                if f.measure(name) <= W - 28:
                    name_font = ("Helvetica", sz, "bold")
                    break
        except Exception:
            name_font = ("Helvetica", 12, "bold") if len(name) > 16 else ("Helvetica", 14, "bold")

        # Dynamic font for role
        role = self._profile.get("role", "")
        role_font = ("Helvetica", 10)
        try:
            from tkinter import font as tkfont
            for sz in (10, 9, 8):
                f = tkfont.Font(family="Helvetica", size=sz)
                if f.measure(role) <= W - 28:
                    role_font = ("Helvetica", sz)
                    break
        except Exception:
            role_font = ("Helvetica", 9) if len(role) > 24 else ("Helvetica", 10)

        # ── name ──────────────────────────────────────────────────────────
        cv.create_text(
            W // 2, 178,
            text=name,
            font=name_font,
            fill=TEXT_DARK,
            width=W - 20,
            justify="center",
        )

        # ── role ──────────────────────────────────────────────────────────
        cv.create_text(
            W // 2, 200,
            text=role,
            font=role_font,
            fill=TEXT_MID,
            width=W - 20,
            justify="center",
        )

        # ── divider ───────────────────────────────────────────────────────
        cv.create_line(30, 218, W - 30, 218, fill="#DDDDDD", width=2)

        # ── tagline ───────────────────────────────────────────────────────
        cv.create_text(
            W // 2, 238,
            text=f'"{self._profile.get("tagline", "")}"',
            font=("Helvetica", 9, "italic"),
            fill=TEXT_MID,
            width=W - 24,
            justify="center",
        )

        # ── "VIEW PORTFOLIO" button area ──────────────────────────────────
        btn_y = H - 44
        cv.create_rectangle(
            20, btn_y, W - 20, btn_y + 30,
            fill=acc, outline=CARD_BORDER, width=2,
        )
        cv.create_text(
            W // 2 - 8, btn_y + 15,
            text="VIEW PORTFOLIO",
            font=("Helvetica", 9, "bold"),
            fill=CARD_BG,
        )
        cv.addtag_withtag("btn_area", cv.find_all()[-1])
        cv.addtag_withtag("btn_area", cv.find_all()[-2])

        # animated arrow (stored item id)
        self._arrow_item = cv.create_text(
            W // 2 + 60, btn_y + 15,
            text="→", font=("Helvetica", 10, "bold"), fill=CARD_BG,
        )

    def _draw_avatar(self, cv, cx, cy, shape, accent):
        r = 42
        if shape == "circle":
            cv.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill=accent, outline=CARD_BORDER, width=3,
            )
            # simple face
            cv.create_oval(cx - 12, cy - 8, cx - 4,  cy,      fill=CARD_BG, outline="")
            cv.create_oval(cx + 4,  cy - 8, cx + 12, cy,      fill=CARD_BG, outline="")
            cv.create_arc( cx - 14, cy - 4, cx + 14, cy + 20,
                           start=200, extent=140, style="arc", outline=CARD_BG, width=2)
        elif shape == "square":
            cv.create_rectangle(
                cx - r, cy - r, cx + r, cy + r,
                fill=accent, outline=CARD_BORDER, width=3,
            )
            # pixel eyes
            cv.create_rectangle(cx - 14, cy - 10, cx - 6, cy - 2, fill=CARD_BG, outline="")
            cv.create_rectangle(cx + 6,  cy - 10, cx + 14, cy - 2, fill=CARD_BG, outline="")
            cv.create_rectangle(cx - 12, cy + 6, cx + 12, cy + 14, fill=CARD_BG, outline="")
        else:  # triangle
            pts = [cx, cy - r, cx - r, cy + r // 2, cx + r, cy + r // 2]
            cv.create_polygon(pts, fill=accent, outline=CARD_BORDER, width=3)
            cv.create_oval(cx - 10, cy - 2, cx - 2, cy + 6,  fill=CARD_BG, outline="")
            cv.create_oval(cx + 2,  cy - 2, cx + 10, cy + 6, fill=CARD_BG, outline="")

    # ── events ────────────────────────────────────────────────────────────────

    def _bind_events(self):
        for widget in (self, self._cv):
            widget.bind("<Enter>",         self._on_enter)
            widget.bind("<Leave>",         self._on_leave)
            widget.bind("<Button-1>",      self._on_press)
            widget.bind("<ButtonRelease-1>", self._on_release)

    def _on_enter(self, _e):
        self._hovering = True
        self._cv.configure(highlightbackground=self._accent)
        self._shadow.configure(bg=self._accent)
        self._start_arrow_anim()

    def _on_leave(self, _e):
        self._hovering = False
        self._cv.configure(highlightbackground=CARD_BORDER)
        self._shadow.configure(bg=CARD_SHADOW)
        self._stop_arrow_anim()

    def _on_press(self, _e):
        # slight "press down" effect: shift canvas right/down
        self._cv.place(x=2, y=2)
        self._shadow.place(x=3, y=3)

    def _on_release(self, _e):
        self._cv.place(x=0, y=0)
        self._shadow.place(x=5, y=5)
        if self._hovering:
            self._on_click(self._profile)

    # ── arrow animation ───────────────────────────────────────────────────────

    def _start_arrow_anim(self):
        self._stop_arrow_anim()
        self._arrow_x    = 0
        self._arrow_max  = 6
        self._arrow_dir  = 1
        self._animate_arrow()

    def _animate_arrow(self):
        if not self._hovering:
            return
        dx = self._arrow_dir * 2
        self._cv.move(self._arrow_item, dx, 0)
        self._arrow_x += dx
        if abs(self._arrow_x) >= self._arrow_max:
            self._arrow_dir *= -1
        self._arrow_job = self.after(80, self._animate_arrow)

    def _stop_arrow_anim(self):
        if self._arrow_job:
            self.after_cancel(self._arrow_job)
            self._arrow_job = None
        # reset arrow to home x
        try:
            coords = self._cv.coords(self._arrow_item)
            if coords:
                self._cv.move(self._arrow_item, -self._arrow_x if hasattr(self, "_arrow_x") else 0, 0)
        except Exception:
            pass
        self._arrow_x = 0
