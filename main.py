"""
main.py — CARTOON OS entry point.

Launches the application window, manages screen transitions between
the desktop and individual portfolio screens.

Run with:
    python3 main.py
"""

import tkinter as tk

from data.profiles          import PROFILES
from screens.desktop        import DesktopScreen
from screens.portfolio      import PortfolioScreen
from components.taskbar     import Taskbar


# ── window constants ──────────────────────────────────────────────────────────
WIN_TITLE  = "CARTOON OS  v1.0"
WIN_W      = 1200
WIN_H      = 800
WIN_MIN_W  = 900
WIN_MIN_H  = 600

CREAM      = "#FFF4D8"
INK        = "#202020"


# Fix Python 3.12+ / 3.13+ / 3.14+ / 3.15+ TclError on widget destruction
_orig_misc_destroy = tk.Misc.destroy
def _safe_misc_destroy(self):
    if self._tclCommands is not None:
        for name in list(self._tclCommands):
            try:
                self.tk.deletecommand(name)
            except tk.TclError:
                pass
        self._tclCommands = None
tk.Misc.destroy = _safe_misc_destroy


class CartoonOS(tk.Tk):
    """Root application window and screen manager."""

    def __init__(self):
        super().__init__()
        self._current_screen  = None
        self._taskbar         = None
        self._transition_job  = None
        self._setup_window()
        self._build_shell()
        self.show_desktop()

    # ── window setup ──────────────────────────────────────────────────────────

    def _setup_window(self):
        self.title(WIN_TITLE)
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.minsize(WIN_MIN_W, WIN_MIN_H)
        self.configure(bg=INK)

        # center on screen
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw - WIN_W) // 2
        y  = (sh - WIN_H) // 2
        self.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")

    # ── shell (persistent chrome) ─────────────────────────────────────────────

    def _build_shell(self):
        # Taskbar MUST be packed first (side="bottom") so pack reserves its
        # space before the expanding content frame claims everything.
        self._taskbar = Taskbar(self, on_home_click=self.show_desktop)
        self._taskbar.pack(side="bottom", fill="x")

        # Content area gets all remaining space above the taskbar.
        self._content = tk.Frame(self, bg=CREAM)
        self._content.pack(side="top", fill="both", expand=True)

    # ── screen management ─────────────────────────────────────────────────────

    def _replace_screen(self, new_screen_factory):
        """
        Replace the current screen with a new one immediately, ensuring only
        one profile/screen exists at a time without any overlapping.

        new_screen_factory: callable() → tk.Frame
        """
        if self._transition_job:
            try:
                self.after_cancel(self._transition_job)
            except Exception:
                pass
            self._transition_job = None

        # 1. Unpack and destroy all existing children in self._content
        for child in list(self._content.winfo_children()):
            try:
                child.pack_forget()
            except Exception:
                pass
            try:
                child.destroy()
            except Exception:
                pass

        self._current_screen = None

        # 2. Build and display the new screen
        new = new_screen_factory()
        new.pack(fill="both", expand=True)
        self._current_screen = new

    # ── screens ───────────────────────────────────────────────────────────────

    def show_desktop(self):
        self._replace_screen(
            lambda: DesktopScreen(self._content, on_profile=self._open_profile)
        )

    def _open_profile(self, profile: dict):
        idx = next((i for i, p in enumerate(PROFILES) if p["id"] == profile["id"]), 0)
        self._replace_screen(
            lambda i=idx: PortfolioScreen(
                self._content,
                profile=PROFILES[i],
                on_home=self.show_desktop,
                on_switch=lambda d, i=i: self._switch_profile(i, d),
            )
        )

    def _switch_profile(self, current_idx: int, direction: int):
        new_idx = (current_idx + direction) % len(PROFILES)
        self._replace_screen(
            lambda i=new_idx: PortfolioScreen(
                self._content,
                profile=PROFILES[i],
                on_home=self.show_desktop,
                on_switch=lambda d, i=new_idx: self._switch_profile(i, d),
            )
        )

    # ── cleanup ───────────────────────────────────────────────────────────────

    def destroy(self):
        if self._taskbar:
            self._taskbar.stop_clock()
        if self._transition_job:
            self.after_cancel(self._transition_job)
        super().destroy()


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = CartoonOS()
    app.mainloop()
