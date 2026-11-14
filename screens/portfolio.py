"""
portfolio.py — Reusable portfolio screen for CARTOON OS.

Receives a profile dict and renders:
  Hero · About · Skills · Projects · Education · Experience · Contact

Uses a left sidebar for navigation and a scrollable main content area.
"""

import tkinter as tk
import webbrowser
import math



# ── palette ───────────────────────────────────────────────────────────────────
CREAM     = "#FFF4D8"
INK       = "#202020"
COBALT    = "#4776FF"
TOMATO    = "#FF6347"
YELLOW    = "#FFD85E"
GREEN     = "#A8D977"
WHITE     = "#FFFFFF"
LIGHT_BG  = "#F5EDD8"
SIDEBAR_W = 200


# ── section names (order matters) ─────────────────────────────────────────────
SECTIONS = ["Hero", "About", "Skills", "Projects", "Education", "Experience", "Contact"]


class PortfolioScreen(tk.Frame):
    """
    Full-screen portfolio frame.

    Parameters
    ----------
    parent      : tk widget
    profile     : dict — one entry from data/profiles.py
    on_home     : callable — go back to desktop
    on_switch   : callable(direction: int) — switch to prev/next profile (±1)
    """

    def __init__(self, parent, profile: dict, on_home, on_switch, **kwargs):
        super().__init__(parent, bg=CREAM, **kwargs)
        self._profile   = profile
        self._on_home   = on_home
        self._on_switch = on_switch
        self._accent    = profile.get("accent_color", COBALT)
        self._section_frames = {}   # section_name → Frame inside content
        self._active_section = SECTIONS[0]
        self._pulse_job  = None
        self._pulse_dir  = 1
        self._pulse_val  = 0
        self._build()

    # ══════════════════════════════════════════════════════════════════════════
    # Layout skeleton
    # ══════════════════════════════════════════════════════════════════════════

    def _build(self):
        # ── top navigation bar ────────────────────────────────────────────
        self._build_topbar()

        # ── body: sidebar + content ───────────────────────────────────────
        body = tk.Frame(self, bg=CREAM)
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        self._build_content_area(body)

    # ── top bar ───────────────────────────────────────────────────────────────

    def _build_topbar(self):
        acc = self._accent
        bar = tk.Frame(self, bg=INK, height=52)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        # home button
        home_btn = tk.Label(
            bar, text="  ⌂ HOME  ",
            bg=acc, fg=WHITE,
            font=("Helvetica", 10, "bold"),
            cursor="hand2", padx=6, pady=4,
        )
        home_btn.pack(side="left", padx=8, pady=8)
        home_btn.bind("<Button-1>", lambda _e: self._on_home())
        _hover(home_btn, acc, _darken(acc))

        # name in centre
        tk.Label(
            bar, text=self._profile["name"].upper(),
            bg=INK, fg=WHITE,
            font=("Courier", 14, "bold"),
        ).pack(side="left", expand=True)

        # profile switcher arrows
        switch_frame = tk.Frame(bar, bg=INK)
        switch_frame.pack(side="right", padx=8)

        tk.Label(switch_frame, text="PROFILES:", bg=INK, fg="#888888",
                 font=("Courier", 9)).pack(side="left", padx=(0, 4))

        prev_btn = tk.Label(switch_frame, text=" ◀ PREV ",
                            bg="#333333", fg=WHITE, font=("Helvetica", 9, "bold"),
                            cursor="hand2", padx=4, pady=4)
        prev_btn.pack(side="left", padx=2, pady=8)
        prev_btn.bind("<Button-1>", lambda _e: self._on_switch(-1))
        _hover(prev_btn, "#333333", "#555555")

        next_btn = tk.Label(switch_frame, text=" NEXT ▶ ",
                            bg="#333333", fg=WHITE, font=("Helvetica", 9, "bold"),
                            cursor="hand2", padx=4, pady=4)
        next_btn.pack(side="left", padx=2, pady=8)
        next_btn.bind("<Button-1>", lambda _e: self._on_switch(1))
        _hover(next_btn, "#333333", "#555555")

    # ── sidebar ───────────────────────────────────────────────────────────────

    def _build_sidebar(self, parent):
        acc = self._accent
        sb  = tk.Frame(parent, bg=INK, width=SIDEBAR_W)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # avatar area
        av_canvas = tk.Canvas(sb, width=SIDEBAR_W, height=140,
                              bg=INK, highlightthickness=0)
        av_canvas.pack(pady=(20, 10))
        self._draw_sidebar_avatar(av_canvas, acc)
        self._start_avatar_pulse(av_canvas)

        # number badge
        tk.Label(sb, text=f"#{self._profile['number']}",
                 bg=INK, fg=acc, font=("Courier", 10, "bold")).pack()

        # nav buttons
        for section in SECTIONS:
            btn = _NavButton(sb, text=section,
                             accent=acc,
                             command=lambda s=section: self._scroll_to(s))
            btn.pack(fill="x", padx=12, pady=2)
            self._section_frames[section + "_nav"] = btn   # save ref

        # version watermark
        tk.Label(sb, text="\n\nCARTOON OS\nv1.0",
                 bg=INK, fg="#333333", font=("Courier", 8)).pack(side="bottom", pady=8)

    def _draw_sidebar_avatar(self, canvas, accent):
        W, H = SIDEBAR_W, 140
        cx, cy = W // 2, H // 2
        r = 48

        img_rel = self._profile.get("avatar_image")
        self._sidebar_photo = None
        if img_rel:
            import os
            proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            full_path = img_rel if os.path.isabs(img_rel) else os.path.join(proj_dir, img_rel)
            if os.path.exists(full_path):
                try:
                    self._sidebar_photo = tk.PhotoImage(file=full_path)
                    canvas.create_rectangle(cx - 43, cy - 43, cx + 43, cy + 43,
                                            fill=accent, outline=WHITE, width=3, tags="av")
                    canvas.create_image(cx, cy, image=self._sidebar_photo, tags="av")
                    return
                except Exception:
                    pass

        shape = self._profile.get("avatar_shape", "circle")
        if shape == "circle":
            canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                               fill=accent, outline=WHITE, width=3, tags="av")
            canvas.create_oval(cx - 14, cy - 10, cx - 5, cy - 1,
                               fill=WHITE, outline="", tags="av")
            canvas.create_oval(cx + 5,  cy - 10, cx + 14, cy - 1,
                               fill=WHITE, outline="", tags="av")
            canvas.create_arc(cx - 15, cy - 4, cx + 15, cy + 18,
                              start=200, extent=140, style="arc", outline=WHITE, width=2, tags="av")
        elif shape == "square":
            canvas.create_rectangle(cx - r, cy - r, cx + r, cy + r,
                                    fill=accent, outline=WHITE, width=3, tags="av")
            canvas.create_rectangle(cx - 16, cy - 12, cx - 6, cy - 2,
                                    fill=WHITE, outline="", tags="av")
            canvas.create_rectangle(cx + 6,  cy - 12, cx + 16, cy - 2,
                                    fill=WHITE, outline="", tags="av")
            canvas.create_rectangle(cx - 13, cy + 4, cx + 13, cy + 12,
                                    fill=WHITE, outline="", tags="av")
        else:
            pts = [cx, cy - r, cx - r, cy + r // 2, cx + r, cy + r // 2]
            canvas.create_polygon(pts, fill=accent, outline=WHITE, width=3, tags="av")
            canvas.create_oval(cx - 10, cy - 4, cx - 2, cy + 4, fill=WHITE, outline="", tags="av")
            canvas.create_oval(cx + 2,  cy - 4, cx + 10, cy + 4, fill=WHITE, outline="", tags="av")

    def _start_avatar_pulse(self, canvas):
        def _pulse(val, direction):
            # Guard: stop if the canvas (or root) is already destroyed
            try:
                if not canvas.winfo_exists():
                    return
            except Exception:
                return
            # pulse the outer ring
            scale = 1.0 + 0.04 * math.sin(val)
            canvas.delete("pulse_ring")
            r  = int(48 * scale)
            cx = SIDEBAR_W // 2
            cy = 70
            canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline=self._accent, width=2, fill="", tags="pulse_ring",
            )
            self._pulse_job = canvas.after(40, _pulse, val + 0.12, direction)

        _pulse(0, 1)

    # ── main content area ─────────────────────────────────────────────────────

    def _build_content_area(self, parent):
        # scrollable canvas
        outer = tk.Frame(parent, bg=CREAM)
        outer.pack(side="left", fill="both", expand=True)

        self._canvas = tk.Canvas(outer, bg=CREAM, highlightthickness=0)
        vscroll = tk.Scrollbar(outer, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=vscroll.set)

        vscroll.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        # inner frame inside canvas
        self._inner = tk.Frame(self._canvas, bg=CREAM)
        self._window_id = self._canvas.create_window((0, 0), window=self._inner, anchor="nw")

        self._inner.bind("<Configure>", self._on_inner_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)

        # mousewheel & trackpad two-finger scrolling
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Button-4>",   self._on_mousewheel)
        self.bind_all("<Button-5>",   self._on_mousewheel)

        # ── build sections ────────────────────────────────────────────────
        self._build_hero()
        self._build_about()
        self._build_skills()
        self._build_projects()
        self._build_education()
        self._build_experience()
        self._build_contact()

    def _on_inner_configure(self, _e):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, e):
        self._canvas.itemconfig(self._window_id, width=e.width)

    def _on_mousewheel(self, event):
        try:
            if not self._canvas.winfo_exists():
                return
        except Exception:
            return

        if event.num == 4:
            self._canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self._canvas.yview_scroll(1, "units")
        else:
            delta = event.delta
            if delta == 0:
                return
            # macOS trackpad gives small deltas (e.g. ±1 to ±5); traditional wheel gives ±120.
            if abs(delta) >= 120:
                units = -int(delta / 120) * 3
            else:
                units = -delta
            self._canvas.yview_scroll(units, "units")

    # ── scroll to section ─────────────────────────────────────────────────────

    def _scroll_to(self, section_name):
        target = self._section_frames.get(section_name)
        if not target:
            return
        self._inner.update_idletasks()
        self._canvas.update_idletasks()
        y = target.winfo_y()
        total = self._inner.winfo_reqheight()
        if total <= 0:
            return
        fraction = y / total
        self._canvas.yview_moveto(fraction)

    # ══════════════════════════════════════════════════════════════════════════
    # Section builders
    # ══════════════════════════════════════════════════════════════════════════

    # ── Hero ──────────────────────────────────────────────────────────────────

    def _build_hero(self):
        p   = self._profile
        acc = self._accent
        hero = _section_frame(self._inner, tag="Hero", sections_dict=self._section_frames)

        hero.configure(bg=acc)

        # hero canvas for geometric decoration
        hc = tk.Canvas(hero, bg=acc, height=200, highlightthickness=0)
        hc.pack(fill="x")

        def _draw_hero(e):
            hc.delete("all")
            W = e.width
            # background shapes
            hc.create_rectangle(W - 160, 0, W, 200, fill=_darken(acc), outline="")
            hc.create_oval(W - 90, -30, W + 40, 90,  fill=WHITE, outline="", stipple="gray25")
            # name
            hc.create_text(40, 50, text=p["name"],
                           font=("Helvetica", 28, "bold"), fill=WHITE, anchor="w")
            # role
            hc.create_text(40, 90, text=p["role"],
                           font=("Helvetica", 14), fill=WHITE, anchor="w")
            # tagline
            hc.create_text(40, 120, text=f'"{p.get("tagline","")}"',
                           font=("Helvetica", 11, "italic"), fill=WHITE, anchor="w",
                           width=W - 200)
            # profile number
            hc.create_text(W - 80, 100, text=f"#{p['number']}",
                           font=("Courier", 48, "bold"), fill=_darken(acc))

        hc.bind("<Configure>", _draw_hero)

        # contact button row
        btn_row = tk.Frame(hero, bg=acc)
        btn_row.pack(fill="x", padx=24, pady=(0, 16))

        email = p.get("email", "")
        if email:
            _action_btn(btn_row, f"✉  {email}", WHITE, acc,
                        lambda: _open_url(f"mailto:{email}")).pack(side="left", padx=(0, 8))

        for platform, url in p.get("socials", {}).items():
            if url:
                _action_btn(btn_row, f"↗  {platform}", INK, YELLOW,
                            lambda u=url: _open_url(u)).pack(side="left", padx=(0, 8))

    # ── About ─────────────────────────────────────────────────────────────────

    def _build_about(self):
        p = self._profile
        sec = _section_frame(self._inner, tag="About", sections_dict=self._section_frames)

        _section_header(sec, "ABOUT ME", self._accent)

        _text_block(sec, p.get("about", "No biography provided."))

        interests = p.get("interests", [])
        if interests:
            _label(sec, "Areas of Interest", bold=True)
            tags_row = tk.Frame(sec, bg=CREAM)
            tags_row.pack(anchor="w", padx=24, pady=(4, 8))
            for interest in interests:
                _tag_label(tags_row, interest, self._accent)

        goals = p.get("goals", "")
        if goals:
            _label(sec, "Goals", bold=True)
            _text_block(sec, goals)

    # ── Skills ────────────────────────────────────────────────────────────────

    def _build_skills(self):
        p = self._profile
        sec = _section_frame(self._inner, tag="Skills", sections_dict=self._section_frames)
        _section_header(sec, "SKILLS", self._accent)

        skills = p.get("skills", {})
        if not skills:
            _label(sec, "No skills listed yet.")
            return

        # two-column grid of categories
        grid = tk.Frame(sec, bg=CREAM)
        grid.pack(fill="x", padx=24, pady=8)

        category_colors = [self._accent, TOMATO, GREEN, YELLOW, COBALT]
        for col_i, (category, skill_list) in enumerate(skills.items()):
            col = col_i % 2
            row = col_i // 2
            cat_frame = tk.Frame(grid, bg=WHITE, bd=0,
                                 highlightthickness=2, highlightbackground=INK)
            cat_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            grid.grid_columnconfigure(col, weight=1)

            color = category_colors[col_i % len(category_colors)]
            # category header
            cat_hdr = tk.Frame(cat_frame, bg=color)
            cat_hdr.pack(fill="x")
            tk.Label(cat_hdr, text=f"  {category}  ",
                     bg=color, fg=WHITE if _is_dark(color) else INK,
                     font=("Helvetica", 10, "bold"), anchor="w").pack(anchor="w", padx=4, pady=4)

            # skills
            tags_container = tk.Frame(cat_frame, bg=WHITE)
            tags_container.pack(fill="x", padx=8, pady=8)
            for skill in skill_list:
                lbl = tk.Label(tags_container, text=f"  {skill}  ",
                               bg=CREAM, fg=INK, font=("Helvetica", 9),
                               bd=1, relief="solid")
                lbl.pack(side="left", padx=3, pady=3)

    # ── Projects ──────────────────────────────────────────────────────────────

    def _build_projects(self):
        p = self._profile
        sec = _section_frame(self._inner, tag="Projects", sections_dict=self._section_frames)
        _section_header(sec, "PROJECTS", self._accent)

        projects = p.get("projects", [])
        if not projects:
            _label(sec, "No projects listed yet.")
            return

        for proj in projects:
            self._project_card(sec, proj)

    def _project_card(self, parent, proj):
        acc = self._accent
        card = tk.Frame(parent, bg=WHITE,
                        highlightthickness=2, highlightbackground=INK)
        card.pack(fill="x", padx=24, pady=8)

        # shadow effect
        shadow = tk.Frame(parent, bg=CARD_SHADOW_COLOR, height=4)
        shadow.pack(fill="x", padx=28)

        # accent left bar
        accent_bar = tk.Frame(card, bg=acc, width=6)
        accent_bar.pack(side="left", fill="y")

        body = tk.Frame(card, bg=WHITE)
        body.pack(side="left", fill="both", expand=True, padx=12, pady=10)

        # title
        tk.Label(body, text=proj.get("title", "Untitled Project"),
                 bg=WHITE, fg=INK, font=("Helvetica", 13, "bold"),
                 anchor="w").pack(anchor="w")

        # description
        desc = proj.get("description", "")
        if desc:
            tk.Label(body, text=desc, bg=WHITE, fg="#444444",
                     font=("Helvetica", 10), wraplength=600, justify="left",
                     anchor="w").pack(anchor="w", pady=(4, 6))

        # tech tags
        tech_row = tk.Frame(body, bg=WHITE)
        tech_row.pack(anchor="w", pady=(0, 6))
        for t in proj.get("tech", []):
            _tag_label(tech_row, t, acc)

        # links row
        link_row = tk.Frame(body, bg=WHITE)
        link_row.pack(anchor="w")
        repo = proj.get("repo", "")
        live = proj.get("live", "")
        if repo:
            _action_btn(link_row, "GitHub ↗", WHITE, INK,
                        lambda u=repo: _open_url(u)).pack(side="left", padx=(0, 6))
        if live:
            _action_btn(link_row, "Live Demo ↗", WHITE, acc,
                        lambda u=live: _open_url(u)).pack(side="left")

    # ── Education ─────────────────────────────────────────────────────────────

    def _build_education(self):
        p = self._profile
        sec = _section_frame(self._inner, tag="Education", sections_dict=self._section_frames)
        _section_header(sec, "EDUCATION", self._accent)

        edu_list = p.get("education", [])
        if not edu_list:
            _label(sec, "No education details provided.")
            return

        for edu in edu_list:
            row = tk.Frame(sec, bg=LIGHT_BG,
                           highlightthickness=2, highlightbackground=INK)
            row.pack(fill="x", padx=24, pady=6)

            badge = tk.Frame(row, bg=self._accent, width=8)
            badge.pack(side="left", fill="y")

            info = tk.Frame(row, bg=LIGHT_BG)
            info.pack(side="left", fill="both", expand=True, padx=12, pady=10)

            tk.Label(info, text=edu.get("institution", ""),
                     bg=LIGHT_BG, fg=INK, font=("Helvetica", 12, "bold"),
                     anchor="w").pack(anchor="w")
            tk.Label(info, text=edu.get("degree", ""),
                     bg=LIGHT_BG, fg="#333333", font=("Helvetica", 10),
                     anchor="w").pack(anchor="w")
            tk.Label(info, text=edu.get("duration", ""),
                     bg=LIGHT_BG, fg=self._accent, font=("Courier", 9, "bold"),
                     anchor="w").pack(anchor="w", pady=(2, 0))
            details = edu.get("details", "")
            if details:
                tk.Label(info, text=details, bg=LIGHT_BG, fg="#666666",
                         font=("Helvetica", 9), wraplength=600, justify="left",
                         anchor="w").pack(anchor="w", pady=(4, 0))

    # ── Experience ────────────────────────────────────────────────────────────

    def _build_experience(self):
        p = self._profile
        sec = _section_frame(self._inner, tag="Experience", sections_dict=self._section_frames)
        _section_header(sec, "EXPERIENCE", self._accent)

        exp_list = p.get("experience", [])
        if not exp_list:
            _label(sec, "No experience listed yet.")
            return

        for exp in exp_list:
            card = tk.Frame(sec, bg=WHITE,
                            highlightthickness=2, highlightbackground=INK)
            card.pack(fill="x", padx=24, pady=6)

            bar = tk.Frame(card, bg=self._accent, width=8)
            bar.pack(side="left", fill="y")

            body = tk.Frame(card, bg=WHITE)
            body.pack(side="left", fill="both", expand=True, padx=12, pady=10)

            # header row
            hrow = tk.Frame(body, bg=WHITE)
            hrow.pack(fill="x")
            tk.Label(hrow, text=exp.get("org", ""),
                     bg=WHITE, fg=INK, font=("Helvetica", 12, "bold")).pack(side="left")
            tk.Label(hrow, text=f"  |  {exp.get('duration', '')}",
                     bg=WHITE, fg=self._accent, font=("Courier", 9, "bold")).pack(side="left")

            tk.Label(body, text=exp.get("role", ""),
                     bg=WHITE, fg="#444444", font=("Helvetica", 10, "italic"),
                     anchor="w").pack(anchor="w")
            tk.Label(body, text=exp.get("description", ""),
                     bg=WHITE, fg="#555555", font=("Helvetica", 10),
                     wraplength=600, justify="left", anchor="w").pack(anchor="w", pady=(4, 0))

            achievements = exp.get("achievements", [])
            for ach in achievements:
                tk.Label(body, text=f"  ✓  {ach}",
                         bg=WHITE, fg=GREEN, font=("Helvetica", 10),
                         anchor="w").pack(anchor="w")

    # ── Contact ───────────────────────────────────────────────────────────────

    def _build_contact(self):
        p = self._profile
        sec = _section_frame(self._inner, tag="Contact", sections_dict=self._section_frames)
        _section_header(sec, "CONTACT", self._accent)

        contact_box = tk.Frame(sec, bg=self._accent,
                               highlightthickness=2, highlightbackground=INK)
        contact_box.pack(padx=24, pady=12, fill="x")

        inner = tk.Frame(contact_box, bg=self._accent)
        inner.pack(padx=20, pady=20, fill="x")

        email = p.get("email", "")
        if email:
            row = tk.Frame(inner, bg=self._accent)
            row.pack(fill="x", pady=4)
            tk.Label(row, text="✉  Email:", bg=self._accent, fg=WHITE,
                     font=("Helvetica", 11, "bold"), width=12, anchor="w").pack(side="left")
            lnk = tk.Label(row, text=email, bg=self._accent, fg=YELLOW,
                           font=("Helvetica", 11), cursor="hand2")
            lnk.pack(side="left")
            lnk.bind("<Button-1>", lambda _e: _open_url(f"mailto:{email}"))

        for platform, url in p.get("socials", {}).items():
            row = tk.Frame(inner, bg=self._accent)
            row.pack(fill="x", pady=4)
            icon = "🔗"
            if platform.lower() == "github":
                icon = "⎔"
            elif platform.lower() == "linkedin":
                icon = "in"
            tk.Label(row, text=f"{icon}  {platform}:", bg=self._accent, fg=WHITE,
                     font=("Helvetica", 11, "bold"), width=12, anchor="w").pack(side="left")
            if url:
                lnk = tk.Label(row, text=url, bg=self._accent, fg=YELLOW,
                               font=("Helvetica", 10), cursor="hand2")
                lnk.pack(side="left")
                lnk.bind("<Button-1>", lambda _e, u=url: _open_url(u))
            else:
                tk.Label(row, text="—", bg=self._accent, fg=WHITE,
                         font=("Helvetica", 10)).pack(side="left")

        # bottom padding
        tk.Frame(sec, bg=CREAM, height=40).pack()

    # ── cleanup ───────────────────────────────────────────────────────────────

    def destroy(self):
        try:
            self.unbind_all("<MouseWheel>")
            self.unbind_all("<Button-4>")
            self.unbind_all("<Button-5>")
        except Exception:
            pass

        # Unpack immediately so the screen disappears without any visual overlap
        try:
            self.pack_forget()
        except Exception:
            pass

        # Cancel the avatar pulse animation if running.
        if self._pulse_job:
            try:
                self.after_cancel(self._pulse_job)
            except Exception:
                pass
        self._pulse_job = None

        try:
            super().destroy()
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════════════════════
# Helper widgets & utilities
# ══════════════════════════════════════════════════════════════════════════════

CARD_SHADOW_COLOR = "#C8BBAA"


def _section_frame(parent, tag: str, sections_dict: dict) -> tk.Frame:
    """Create and register a section container."""
    frame = tk.Frame(parent, bg=CREAM)
    frame.pack(fill="x", pady=(0, 4))
    sections_dict[tag] = frame
    return frame


def _section_header(parent, title: str, accent: str):
    hdr = tk.Frame(parent, bg=CREAM)
    hdr.pack(fill="x", padx=24, pady=(16, 8))

    tk.Label(hdr, text=title,
             bg=CREAM, fg=INK, font=("Courier", 18, "bold")).pack(side="left")

    # accent dot separator
    tk.Label(hdr, text="  ●",
             bg=CREAM, fg=accent, font=("Helvetica", 14, "bold")).pack(side="left")

    # full-width underline
    line = tk.Canvas(parent, bg=CREAM, height=4, highlightthickness=0)
    line.pack(fill="x", padx=24)
    line.bind("<Configure>", lambda e: (
        line.delete("all"),
        line.create_rectangle(0, 0, e.width, 4, fill=accent, outline=""),
        line.create_rectangle(e.width // 3, 0, e.width, 4, fill=CREAM, outline=""),
    ))


def _text_block(parent, text: str):
    tk.Label(parent, text=text,
             bg=CREAM, fg="#333333", font=("Helvetica", 11),
             wraplength=700, justify="left", anchor="w").pack(
        anchor="w", padx=24, pady=(4, 8))


def _label(parent, text: str, bold: bool = False):
    font = ("Helvetica", 11, "bold") if bold else ("Helvetica", 11)
    tk.Label(parent, text=text, bg=CREAM, fg=INK, font=font,
             anchor="w").pack(anchor="w", padx=24, pady=(6, 2))


def _tag_label(parent, text: str, accent: str):
    fg = WHITE if _is_dark(accent) else INK
    lbl = tk.Label(parent, text=f"  {text}  ",
                   bg=accent, fg=fg,
                   font=("Helvetica", 9, "bold"),
                   padx=2, pady=2)
    lbl.pack(side="left", padx=3, pady=2)


def _action_btn(parent, text: str, fg: str, bg: str, command) -> tk.Label:
    btn = tk.Label(parent, text=text,
                   bg=bg, fg=fg,
                   font=("Helvetica", 9, "bold"),
                   cursor="hand2",
                   padx=8, pady=5,
                   bd=0, relief="flat",
                   highlightthickness=1,
                   highlightbackground=INK)
    btn.bind("<Button-1>", lambda _e: command())
    _hover(btn, bg, _darken(bg))
    return btn


def _hover(widget, normal_bg: str, hover_bg: str):
    widget.bind("<Enter>", lambda _e: widget.configure(bg=hover_bg))
    widget.bind("<Leave>", lambda _e: widget.configure(bg=normal_bg))


def _open_url(url: str):
    try:
        webbrowser.open(url)
    except Exception:
        pass


def _darken(hex_color: str, factor: float = 0.80) -> str:
    """Return a slightly darker version of a hex color."""
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def _is_dark(hex_color: str) -> bool:
    """Return True when the color is perceptually dark (white text preferred)."""
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        return luminance < 140
    except Exception:
        return True


class _NavButton(tk.Frame):
    """Sidebar navigation button with active-state highlight."""

    def __init__(self, parent, text: str, accent: str, command, **kwargs):
        super().__init__(parent, bg=INK, cursor="hand2", **kwargs)
        self._accent   = accent
        self._command  = command
        self._active   = False
        self._normal_bg = INK
        self._hover_bg  = "#2A2A2A"

        self._lbl = tk.Label(
            self, text=f"  {text}",
            bg=INK, fg="#AAAAAA",
            font=("Helvetica", 10),
            anchor="w", pady=6,
        )
        self._lbl.pack(fill="x")

        for w in (self, self._lbl):
            w.bind("<Enter>",    self._on_enter)
            w.bind("<Leave>",    self._on_leave)
            w.bind("<Button-1>", self._on_click)

    def _on_enter(self, _e):
        if not self._active:
            self._lbl.configure(bg=self._hover_bg, fg=WHITE)
            self.configure(bg=self._hover_bg)

    def _on_leave(self, _e):
        if not self._active:
            self._lbl.configure(bg=INK, fg="#AAAAAA")
            self.configure(bg=INK)

    def _on_click(self, _e):
        self._command()

    def set_active(self, active: bool):
        self._active = active
        if active:
            self._lbl.configure(bg=self._accent, fg=WHITE, font=("Helvetica", 10, "bold"))
            self.configure(bg=self._accent)
        else:
            self._lbl.configure(bg=INK, fg="#AAAAAA", font=("Helvetica", 10))
            self.configure(bg=INK)
