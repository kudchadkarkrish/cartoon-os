"""
desktop.py — The CARTOON OS main desktop screen.

Layout (all pack, no mixing):
  DesktopScreen (tk.Frame)
    ├── header row         side=top, fill=x
    ├── colour bar Canvas  side=top, fill=x
    ├── sub-headline Label side=top
    ├── hint Label         side=bottom
    └── cards_area Frame   side=top, fill=both, expand=True
          ├── deco_wrap Frame   [place relx=0 rely=0 relwidth=1 relheight=1]
          │     └── deco_canvas Canvas [pack fill=both expand=True]
          └── cards_wrap Frame  [place relx=0.5 rely=0.5 anchor=center]
                └── ProfileCard × 3  [grid row=0 col=0/1/2]

deco_wrap is lowered below cards_wrap using Frame.lower() (widget-stacking,
not Canvas.lower() which is the canvas-item API and crashes with no args).
"""

import tkinter as tk
import math
import random

from components.profile_card import ProfileCard


# ── palette ───────────────────────────────────────────────────────────────────
CREAM  = "#FFF4D8"
INK    = "#202020"
COBALT = "#4776FF"
TOMATO = "#FF6347"
YELLOW = "#FFD85E"
GREEN  = "#A8D977"
WHITE  = "#FFFFFF"

random.seed(42)   # reproducible decoration positions


# ── decoration helpers ────────────────────────────────────────────────────────

def _decoration_list(W: int, H: int) -> list:
    """Return descriptor tuples for every background decoration."""
    items = []

    # 4-pointed stars
    for x, y in [
        (80, 80), (140, 200), (W - 90, 110), (W - 150, 320),
        (50, H - 100), (W - 60, H - 130),
        (W // 2 + 220, 60), (W // 2 - 180, H - 80),
    ]:
        items.append(("star", x, y))

    # decorative rings
    for x, y, r, c in [
        (30,           60,  22, COBALT),
        (W - 40,       70,  18, TOMATO),
        (60,       H - 70,  16, GREEN),
        (W - 50,   H - 60,  20, YELLOW),
        (W // 2 - 300, 160, 12, COBALT),
        (W // 2 + 280, H - 120, 14, TOMATO),
    ]:
        items.append(("ring", x, y, r, c))

    # subtle dot grid
    for gx in range(120, W - 80, 90):
        for gy in range(120, H - 80, 90):
            items.append(("dot", gx, gy))

    # outlined rectangles
    for x0, y0, x1, y1, c in [
        (20,      20, 80,      50, YELLOW),
        (W - 90,  30, W - 20,  65, GREEN),
        (25,  H - 80, 75,  H - 30, TOMATO),
        (W - 80, H - 85, W - 25, H - 35, COBALT),
    ]:
        items.append(("rect_outline", x0, y0, x1, y1, c))

    # dashed lines
    for x0, y0, x1, y1 in [
        (100, 140, 130, 140), (90, 150, 130, 150),
        (W - 130, 200, W - 90, 200), (W - 130, 210, W - 100, 210),
    ]:
        items.append(("line", x0, y0, x1, y1))

    # stick-figure doodle
    items.append(("doodle", W - 120, 90))
    return items


def _star_pts(cx: float, cy: float, r: float) -> list:
    pts = []
    for i in range(8):
        angle  = math.pi / 4 * i - math.pi / 2
        radius = r if i % 2 == 0 else r * 0.45
        pts.append(cx + radius * math.cos(angle))
        pts.append(cy + radius * math.sin(angle))
    return pts


# ── main class ────────────────────────────────────────────────────────────────

class DesktopScreen(tk.Frame):
    """
    The main desktop frame shown at launch.

    Parameters
    ----------
    parent     : tk widget
    on_profile : callable — called with profile dict when a card is clicked
    """

    def __init__(self, parent, on_profile, **kwargs):
        super().__init__(parent, bg=CREAM, **kwargs)
        self._on_profile  = on_profile
        self._anim_job    = None   # single after() id for star animation
        self._float_items = []     # list of (base_x, base_y, canvas_id, phase)
        self._deco_canvas = None
        self._build()

    # ── construction ──────────────────────────────────────────────────────────

    def _build(self):
        """
        Build all desktop content using pure pack() on this frame.
        No Canvas overlay on DesktopScreen itself.
        """

        # ── 1. OS heading row ─────────────────────────────────────────────
        hdr = tk.Frame(self, bg=CREAM)
        hdr.pack(side="top", fill="x", padx=40, pady=(30, 0))

        tk.Label(
            hdr, text="CARTOON  OS",
            bg=CREAM, fg=INK, font=("Courier", 38, "bold"),
        ).pack(side="left", anchor="w")

        right = tk.Frame(hdr, bg=CREAM)
        right.pack(side="right", anchor="e")
        tk.Label(right, text="v1.0  STABLE",
                 bg=CREAM, fg="#888888", font=("Courier", 9, "bold")).pack(anchor="e")
        tk.Label(right, text="✦  Welcome back, User",
                 bg=CREAM, fg=COBALT, font=("Helvetica", 12, "bold")).pack(anchor="e")

        # ── 2. Colour-bar underline ───────────────────────────────────────
        bar = tk.Canvas(self, height=6, bg=CREAM, highlightthickness=0)
        bar.pack(side="top", fill="x", padx=40, pady=(4, 0))
        bar.bind("<Configure>", lambda e, c=bar: self._draw_underline(c, e.width))

        # ── 3. Sub-headline ───────────────────────────────────────────────
        tk.Label(
            self, text="SELECT  A  PROFILE  TO  EXPLORE",
            bg=CREAM, fg=INK, font=("Courier", 13, "bold"),
        ).pack(side="top", pady=(14, 4))

        # ── 4. Hint (anchored at the bottom — packed before cards area) ───
        tk.Label(
            self,
            text="✦  Click any profile card to open its portfolio  ✦",
            bg=CREAM, fg="#999999", font=("Helvetica", 10, "italic"),
        ).pack(side="bottom", pady=(0, 10))

        # ── 5. Cards area — fills remaining space ─────────────────────────
        cards_area = tk.Frame(self, bg=CREAM)
        cards_area.pack(side="top", fill="both", expand=True)

        # 5a. Decoration wrapper — placed to fill cards_area entirely.
        #     Frame.lower() is the correct widget-stacking call (not
        #     Canvas.lower() which is the canvas-item API).
        deco_wrap = tk.Frame(cards_area, bg=CREAM)
        deco_wrap.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._deco_canvas = tk.Canvas(deco_wrap, bg=CREAM, highlightthickness=0)
        self._deco_canvas.pack(fill="both", expand=True)
        self._deco_canvas.bind("<Configure>", self._on_deco_resize)

        # 5b. Cards wrapper — centered inside cards_area via place().
        cards_wrap = tk.Frame(cards_area, bg=CREAM)
        cards_wrap.place(relx=0.5, rely=0.5, anchor="center")

        from data.profiles import PROFILES
        for col, profile in enumerate(PROFILES):
            card = ProfileCard(cards_wrap, profile=profile,
                               on_click=self._on_profile)
            card.grid(row=0, column=col, padx=28, pady=10)

        # 5c. Lower the decoration wrapper BEHIND the cards wrapper.
        #     deco_wrap is a tk.Frame, so .lower() is the widget-stacking
        #     method — not the canvas-item method.
        deco_wrap.lower(cards_wrap)

        # ── 6. Print diagnostics after layout has settled ─────────────────
        self.after(300, self._print_diagnostics,
                   cards_area, deco_wrap, cards_wrap)

    # ── colour bar ────────────────────────────────────────────────────────────

    def _draw_underline(self, canvas: tk.Canvas, width: int):
        canvas.delete("all")
        colors = [COBALT, YELLOW, TOMATO, GREEN]
        sw = width // len(colors)
        for i, c in enumerate(colors):
            canvas.create_rectangle(i * sw, 0, (i + 1) * sw, 6, fill=c, outline="")

    # ── decorative background canvas ──────────────────────────────────────────

    def _on_deco_resize(self, event):
        """Redraws all decorations when the canvas is resized."""
        cv = self._deco_canvas
        if cv is None:
            return
        cv.delete("decoration")
        W, H = event.width, event.height
        if W < 10 or H < 10:
            return

        # cancel any running animation
        if self._anim_job:
            self.after_cancel(self._anim_job)
            self._anim_job = None
        self._float_items.clear()

        for item in _decoration_list(W, H):
            kind = item[0]

            if kind == "star":
                _, x, y = item
                iid = self._draw_star(x, y, 10)
                self._float_items.append((x, y, iid, random.random() * 6.28))

            elif kind == "ring":
                _, x, y, r, color = item
                cv.create_oval(x - r, y - r, x + r, y + r,
                               outline=color, width=3, fill="", tags="decoration")

            elif kind == "dot":
                _, x, y = item
                cv.create_oval(x - 3, y - 3, x + 3, y + 3,
                               fill="#DDCCBB", outline="", tags="decoration")

            elif kind == "rect_outline":
                _, x0, y0, x1, y1, color = item
                cv.create_rectangle(x0, y0, x1, y1,
                                    outline=color, width=3, fill="", tags="decoration")

            elif kind == "line":
                _, x0, y0, x1, y1 = item
                cv.create_line(x0, y0, x1, y1,
                               fill=INK, width=2, dash=(4, 4), tags="decoration")

            elif kind == "doodle":
                _, x, y = item
                self._draw_doodle(x, y)

        self._animate_stars(0)

    def _draw_star(self, cx: float, cy: float, r: float) -> int:
        """Draw a 4-pointed star; returns canvas item id."""
        return self._deco_canvas.create_polygon(
            _star_pts(cx, cy, r),
            fill=YELLOW, outline=INK, width=2,
            tags=("decoration", "star_item"),
        )

    def _draw_doodle(self, x: float, y: float):
        cv = self._deco_canvas
        cv.create_oval(x - 14, y - 30, x + 14, y,
                       fill=YELLOW, outline=INK, width=2, tags="decoration")
        cv.create_oval(x - 7,  y - 22, x - 2,  y - 17,
                       fill=INK, outline="", tags="decoration")
        cv.create_oval(x + 2,  y - 22, x + 7,  y - 17,
                       fill=INK, outline="", tags="decoration")
        cv.create_arc(x - 7, y - 16, x + 7, y - 6,
                      start=200, extent=140, style="arc", outline=INK, width=2, tags="decoration")
        cv.create_line(x, y, x, y + 30,         fill=INK, width=2, tags="decoration")
        cv.create_line(x - 18, y + 10, x + 18, y + 14,
                       fill=INK, width=2, tags="decoration")
        cv.create_line(x, y + 30, x - 12, y + 50, fill=INK, width=2, tags="decoration")
        cv.create_line(x, y + 30, x + 12, y + 50, fill=INK, width=2, tags="decoration")
        cv.create_oval(x + 14, y - 46, x + 44, y - 26,
                       fill=WHITE, outline=INK, width=2, tags="decoration")
        cv.create_text(x + 29, y - 36, text="hi!",
                       font=("Helvetica", 8, "bold"), fill=INK, tags="decoration")

    # ── star float animation ──────────────────────────────────────────────────

    def _animate_stars(self, tick: int):
        """Single recurring after() callback — uses one job id, not a list."""
        cv = self._deco_canvas
        if cv is None:
            return
        for bx, by, iid, phase in self._float_items:
            offset_y = math.sin(tick * 0.04 + phase) * 4
            cv.coords(iid, *_star_pts(bx, by + offset_y, 10))
        self._anim_job = self.after(50, self._animate_stars, tick + 1)

    # ── diagnostics ───────────────────────────────────────────────────────────

    def _print_diagnostics(self, cards_area, deco_wrap, cards_wrap):
        """Print widget sizes/mapping after layout has settled (called via after)."""
        targets = [
            ("DesktopScreen", self),
            ("cards_area",    cards_area),
            ("deco_wrap",     deco_wrap),
            ("deco_canvas",   self._deco_canvas),
            ("cards_wrap",    cards_wrap),
        ]
        print("\n======  CARTOON OS desktop diagnostic  ======")
        for name, w in targets:
            try:
                print(f"  {name:16s}  "
                      f"exists={w.winfo_exists()}  "
                      f"mapped={w.winfo_ismapped()}  "
                      f"size={w.winfo_width()}x{w.winfo_height()}  "
                      f"mgr={w.winfo_manager()!r}")
            except Exception as exc:
                print(f"  {name:16s}  ERROR: {exc}")
        print("=============================================\n")

    # ── cleanup ───────────────────────────────────────────────────────────────

    def destroy(self):
        if self._anim_job:
            self.after_cancel(self._anim_job)
            self._anim_job = None
        self._deco_canvas = None
        super().destroy()
