# CutPlan

A desktop app and a small, reusable library for planning cutting layouts for
DIY builds made from sheet material (plywood, MDF, etc.).

**Module:** B144 Software Design and Modelling
**Team:** Eren Oksum, Meric Olcan Polat

## Why two packages

The project is split into two Python packages so the library and the GUI
can be built and tested separately.

[`cutplan_core`](cutplan_core) is the GUI-free library - it turns
measurements into parts, arranges them on sheets, works out
sheets/waste/cost, and saves/loads projects as JSON. It only depends on
the standard library. [`cutplan_app`](cutplan_app) is the Tkinter
desktop GUI, built on top of `cutplan_core`.

`cutplan_core` doesn't import `tkinter` anywhere, and its tests run fine
with no GUI toolkit installed. `cutplan_app` could be deleted and
`cutplan_core` would still work on its own.

## Quick start

```bash
# 1. install the library
cd cutplan_core
python3 -m pip install -e ".[test]"

# 2. install the desktop app (depends on cutplan_core)
cd ../cutplan_app
python3 -m pip install -e .

# 3. run it
python3 -m cutplan_app.main
# or, if your PATH includes the pip scripts dir:
cutplan
```

## Troubleshooting: blank/black window on macOS

If the desktop app opens as a black window with only the two file buttons
visible, your `python3` is probably Apple's system Python, which links
against Tcl/Tk 8.5. That version doesn't handle macOS Dark Mode properly
and renders plain Tk widgets as invisible black-on-black. Check with:

```bash
python3 -c "import tkinter; print(tkinter.TkVersion)"   # 8.5 = broken, 8.6+ = fine
```

Fix: install a Python built against Tk 8.6+, e.g. via Homebrew
(`brew install python-tk@3.11`), then reinstall the two packages under
that interpreter:

```bash
/opt/homebrew/opt/python@3.11/bin/python3.11 -m pip install -e cutplan_core -e cutplan_app
/opt/homebrew/opt/python@3.11/bin/python3.11 -m cutplan_app.main
```

## Running the tests

```bash
cd cutplan_core
pytest --cov=cutplan_core --cov-report=term-missing
```

## Repository layout

```
cutplan/
├── cutplan_core/        the reusable library (its own package + tests)
└── cutplan_app/         the Tkinter desktop app (depends on cutplan_core)
```
