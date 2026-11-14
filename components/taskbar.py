"""
taskbar.py — The Cartoon OS taskbar component.

Simple bottom bar containing only:
  • CARTOON OS branding on the left
  • A DESKTOP home button
"""

import tkinter as tk


# ── palette ───────────────────────────────────────────────────────────────────
BG         = "#202020"   # dark ink bar
FG         = "#FFF4D8"   # cream text
ACCENT     = "#FFD85E"   # butter yellow
HOME_BG    = "#4776FF"
HOME_HOVER = "#3060EE"
HOME_PRESS = "#1E40C8"


class Taskbar(tk.Frame):
    """Bottom taskbar widget."""

    def __init__(self, parent, on_home_click, **kwargs):
        super().__init__(parent, bg=BG, height=40, **kwargs)
        self.pack_propagate(False)
        self._on_home_click = on_home_click
        self._build()

    # ── construction ──────────────────────────────────────────────────────────

    def _build(self):
        # left: branding
        tk.Label(
            self, text=" ◉ CARTOON OS ",
            bg=BG, fg=ACCENT,
            font=("Courier", 11, "bold"),
            padx=8,
        ).pack(side="left", padx=(8, 0))

        # home button
        self._home_btn = tk.Label(
            self, text="⌂  DESKTOP",
            bg=HOME_BG, fg=FG,
            font=("Helvetica", 9, "bold"),
            padx=10, pady=3,
            cursor="hand2",
        )
        self._home_btn.pack(side="left", padx=10, pady=5)
        self._home_btn.bind("<Enter>",           self._home_enter)
        self._home_btn.bind("<Leave>",           self._home_leave)
        self._home_btn.bind("<Button-1>",        self._home_press)
        self._home_btn.bind("<ButtonRelease-1>", self._home_release)

    # ── interactions ──────────────────────────────────────────────────────────

    def _home_enter(self, _e):
        self._home_btn.configure(bg=HOME_HOVER)

    def _home_leave(self, _e):
        self._home_btn.configure(bg=HOME_BG)

    def _home_press(self, _e):
        self._home_btn.configure(bg=HOME_PRESS)

    def _home_release(self, _e):
        self._home_btn.configure(bg=HOME_HOVER)
        self._on_home_click()

    # ── kept for API compatibility with main.py ────────────────────────────────

    def stop_clock(self):
        """No-op — clock was removed. Kept so main.py destroy() still works."""
        pass
