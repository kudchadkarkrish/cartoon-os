# CARTOON OS — Portfolio Application

A quirky, animated fictional operating-system portfolio built entirely with
**Python 3 + Tkinter**. No third-party packages required.

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Python      | 3.8+    |
| Tkinter     | bundled with Python |

Verify your setup:

```bash
python3 --version
python3 -c "import tkinter; print(tkinter.TkVersion)"
```

---

## Running the Application

```bash
cd cartoon-os
python3 main.py
```

That's it. No `pip install`, no virtual environment, no internet required.

---

## Project Structure

```
cartoon-os/
├── main.py                  # Entry point — launches the window
├── data/
│   └── profiles.py          # ✏️  All portfolio data lives here
├── screens/
│   ├── desktop.py           # Main desktop screen (cards + background)
│   └── portfolio.py         # Reusable portfolio screen (all sections)
├── components/
│   ├── profile_card.py      # Interactive profile card widget
│   └── taskbar.py           # Persistent bottom taskbar + live clock
└── assets/
    └── README.md
```

---

## Customising Profile Information

Open `data/profiles.py` and edit the relevant dictionary.

**You never need to touch any UI code to change content.**

```python
PROFILES = [
    {
        "name":   "Tanmay Rai",
        "role":   "Computer Science Student",
        "email":  "tanmay@example.com",
        "skills": { "Languages": ["Python", "C", "Java"], ... },
        ...
    },
    ...
]
```

---

## Features

- **Cartoon Desktop** — animated floating stars, geometric decorations, stick-figure doodle
- **Three Profile Cards** — hover effects, press feedback, bouncing arrow animation
- **Live Taskbar Clock** — updates every second via `after()`
- **Portfolio Sections** — Hero · About · Skills · Projects · Education · Experience · Contact
- **Smooth Transitions** — screen swap with minimal flicker
- **Scrollable Content** — mousewheel + scrollbar support
- **Profile Switching** — PREV / NEXT arrows in the portfolio header
- **URL Opening** — GitHub / LinkedIn links open in your default browser
- **No External Dependencies** — pure Python standard library

---

## Colour Palette

| Name           | Hex       |
|----------------|-----------|
| Cream (BG)     | `#FFF4D8` |
| Primary Ink    | `#202020` |
| Cobalt Blue    | `#4776FF` |
| Tomato Red     | `#FF6347` |
| Butter Yellow  | `#FFD85E` |
| Fresh Green    | `#A8D977` |

---

## Viva Talking Points

1. **MVC-style separation** — data in `profiles.py`, logic in `screens/`, UI components in `components/`
2. **Reusable layout** — one `PortfolioScreen` class serves all three profiles
3. **Animation without threads** — `after()` schedules callbacks on the Tkinter event loop
4. **Canvas drawing** — all illustrations drawn programmatically (no image files)
5. **Event binding** — `bind()` for hover/click, `after_cancel()` to prevent stale callbacks

---

*Built as a college project demonstration — CARTOON OS v1.0*
