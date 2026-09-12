"""CutPlan desktop app: a Tkinter GUI built on top of the cutplan_core
library. It reads form input, calls into cutplan_core to do the actual
work, and shows the result.
"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from cutplan_core import Design, FitException, Material, Part, Planner, Project, project_file

from .sheet_view import SheetView

_PRESETS = ("Bookshelf", "Box", "Custom parts")


class CutPlanApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CutPlan")
        self.geometry("1000x680")
        self.minsize(760, 520)

        self.planner = Planner()
        self._loading = False
        self._entries: dict = {}

        self._build_widgets()
        self._refresh_form_mode()
        self._calculate()

    def _build_widgets(self) -> None:
        header = tk.Label(self, text="CutPlan", bg="#2B2B2B", fg="white", anchor="w",
                           padx=12, pady=8, font=("Helvetica", 13, "bold"))
        header.pack(side="top", fill="x")

        body = tk.Frame(self)
        body.pack(side="top", fill="both", expand=True)

        self._build_form(body)
        self._build_centre(body)
        self._build_totals_bar()

    def _build_form(self, parent) -> None:
        form = tk.Frame(parent, padx=16, pady=16, width=340)
        form.pack(side="left", fill="y")

        tk.Label(form, text="What are you building?", font=("Helvetica", 12, "bold")).pack(anchor="w")

        self.preset_var = tk.StringVar(value=_PRESETS[0])
        preset_box = ttk.Combobox(form, textvariable=self.preset_var, values=_PRESETS, state="readonly")
        preset_box.pack(anchor="w", fill="x", pady=(2, 8))
        preset_box.bind("<<ComboboxSelected>>", lambda _e: (self._refresh_form_mode(), self._calculate()))

        self._hint(form, "1 cm = 10 mm,  1 m = 1000 mm  (a 90 cm shelf = 900)").pack(anchor="w", pady=(0, 8))

        self.preset_grid = tk.Frame(form)
        self.width = self._field(self.preset_grid, "Width (mm)", "700", 0)
        self.height = self._field(self.preset_grid, "Height (mm)", "900", 1)
        self.depth = self._field(self.preset_grid, "Depth (mm)", "250", 2)
        self.thickness = self._field(self.preset_grid, "Board thickness (mm)", "18", 3)
        self.shelves = self._field(self.preset_grid, "Number of shelves", "2", 4)
        self.preset_grid.pack(anchor="w", fill="x")

        self.custom_block = tk.Frame(form)
        self._hint(self.custom_block, "One part per line: name, width, height, quantity").pack(anchor="w")
        self.custom_text = tk.Text(self.custom_block, width=32, height=6)
        self.custom_text.insert(
            "1.0",
            "Side panel, 250, 900, 2\n"
            "Top / bottom, 250, 664, 2\n"
            "Shelf, 250, 664, 2\n"
            "Back panel, 700, 900, 1",
        )
        self.custom_text.pack(fill="both", expand=True, pady=(2, 0))
        self.custom_text.bind("<KeyRelease>", lambda _e: self._calculate())

        ttk.Separator(form).pack(fill="x", pady=10)
        tk.Label(form, text="Your sheet material", font=("Helvetica", 12, "bold")).pack(anchor="w")

        material_grid = tk.Frame(form)
        self.sheet_w = self._field(material_grid, "Sheet width (mm)", "2440", 0)
        self.sheet_h = self._field(material_grid, "Sheet height (mm)", "1220", 1)
        self.kerf = self._field(material_grid, "Saw kerf (mm)", "3", 2)
        self.price = self._field(material_grid, "Price per sheet", "45", 3)
        material_grid.pack(anchor="w", fill="x", pady=(4, 10))

        ttk.Separator(form).pack(fill="x", pady=4)
        btns = tk.Frame(form)
        tk.Button(btns, text="Open project…", command=self._open_project).pack(side="left", padx=(0, 8))
        tk.Button(btns, text="Save project…", command=self._save_project).pack(side="left")
        btns.pack(anchor="w", pady=8)

    def _build_centre(self, parent) -> None:
        centre = tk.Frame(parent, padx=10, pady=10)
        centre.pack(side="left", fill="both", expand=True)

        self._hint(centre, "Orange = a part.   Pale space inside a sheet = wasted material.").pack(anchor="w")

        canvas_frame = tk.Frame(centre)
        canvas_frame.pack(fill="both", expand=True, pady=(4, 0))
        vbar = tk.Scrollbar(canvas_frame, orient="vertical")
        self.sheet_view = SheetView(canvas_frame, bg="#FAFAFA", yscrollcommand=vbar.set)
        vbar.config(command=self.sheet_view.yview)
        vbar.pack(side="right", fill="y")
        self.sheet_view.pack(side="left", fill="both", expand=True)

    def _build_totals_bar(self) -> None:
        bar = tk.Frame(self, bg="#EFEFEF", padx=16, pady=6,
                        highlightbackground="#D0D0D0", highlightthickness=1)
        bar.pack(side="bottom", fill="x")

        self.sheets_value = self._card(bar, "SHEETS TO BUY")
        self.waste_value = self._card(bar, "MATERIAL WASTED")
        self.cost_value = self._card(bar, "TOTAL COST")

        self.message = tk.Label(bar, text=" ", bg="#EFEFEF", fg="black", anchor="w")
        self.message.pack(side="left", fill="x", expand=True, padx=(24, 0))

    def _field(self, parent, label: str, default: str, row: int) -> tk.StringVar:
        tk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=3)
        var = tk.StringVar(value=default)
        entry = tk.Entry(parent, textvariable=var, width=10)
        entry.grid(row=row, column=1, sticky="we", padx=(6, 0), pady=3)
        var.trace_add("write", lambda *_args: self._calculate())
        self._entries[id(var)] = entry
        return var

    def _card(self, parent, title: str) -> tk.Label:
        card = tk.Frame(parent, bg="#EFEFEF")
        tk.Label(card, text=title, fg="#777777", font=("Helvetica", 8), bg="#EFEFEF").pack(anchor="w")
        value = tk.Label(card, text="–", font=("Helvetica", 16, "bold"), bg="#EFEFEF", fg="black")
        value.pack(anchor="w")
        card.pack(side="left", padx=(0, 28))
        return value

    @staticmethod
    def _hint(parent, text: str) -> tk.Label:
        return tk.Label(parent, text=text, fg="#777777", font=("Helvetica", 9), wraplength=300, justify="left")

    def _refresh_form_mode(self) -> None:
        kind = self.preset_var.get()
        custom = kind == "Custom parts"
        if custom:
            self.preset_grid.pack_forget()
            self.custom_block.pack(anchor="w", fill="both", expand=True)
        else:
            self.custom_block.pack_forget()
            self.preset_grid.pack(anchor="w", fill="x")

        shelves_entry = self._entries.get(id(self.shelves))
        if shelves_entry is not None:
            shelves_entry.config(state=("disabled" if kind == "Box" else "normal"))

    def _read_design(self) -> Design:
        kind = self.preset_var.get()
        if kind == "Bookshelf":
            return Design.bookshelf(
                "Bookshelf", self._num(self.width), self._num(self.height),
                self._num(self.depth), self._num(self.thickness), int(self._num(self.shelves)),
            )
        if kind == "Box":
            return Design.box(
                "Box", self._num(self.width), self._num(self.height),
                self._num(self.depth), self._num(self.thickness),
            )
        return Design.custom("Custom", self._parse_custom_parts())

    def _read_material(self) -> Material:
        return Material(self._num(self.sheet_w), self._num(self.sheet_h),
                         self._num(self.kerf), self._num(self.price))

    def _parse_custom_parts(self):
        parts = []
        text = self.custom_text.get("1.0", "end")
        for line in text.splitlines():
            row = line.strip()
            if not row:
                continue
            cells = [c.strip() for c in row.split(",")]
            if len(cells) < 3:
                raise ValueError("Each line needs: name, width, height, quantity")
            qty = int(cells[3]) if len(cells) >= 4 else 1
            parts.append(Part(cells[0], float(cells[1]), float(cells[2]), qty))
        if not parts:
            raise ValueError("Add at least one part.")
        return parts

    @staticmethod
    def _num(var: tk.StringVar) -> float:
        return float(var.get().strip())

    def _calculate(self) -> None:
        if self._loading:
            return
        try:
            plan = self.planner.plan(self._read_design(), self._read_material())
            cost = plan.cost_report()

            self.sheet_view.show_plan(plan)
            self.sheets_value.config(text=str(cost.sheets_needed))
            self.waste_value.config(text=f"{cost.waste_percent:.0f}%")
            self.cost_value.config(text=f"{cost.total_price:.2f}")
            self._show_message(" ", "black")
        except FitException as ex:
            self.sheet_view.clear_plan()
            self._blank_totals()
            self._show_message(str(ex), "#B00020")
        except ValueError as ex:
            self.sheet_view.clear_plan()
            self._blank_totals()
            message = "Fill in every box with a number." if "could not convert" in str(ex) else str(ex)
            self._show_message(message, "#B00020")

    def _blank_totals(self) -> None:
        self.sheets_value.config(text="–")
        self.waste_value.config(text="–")
        self.cost_value.config(text="–")

    def _show_message(self, text: str, color: str) -> None:
        self.message.config(text=text, fg=color)

    def _save_project(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save project", defaultextension=".cutplan",
            filetypes=[("CutPlan project", "*.cutplan *.json")],
        )
        if not path:
            return
        try:
            project_file.save(path, Project(self._read_design(), self._read_material()))
            self._show_message(f"Saved {Path(path).name}", "#1A7F37")
        except Exception as ex:
            self._show_message(f"Could not save: {ex}", "#B00020")

    def _open_project(self) -> None:
        path = filedialog.askopenfilename(
            title="Open project", filetypes=[("CutPlan project", "*.cutplan *.json")],
        )
        if not path:
            return
        try:
            project = project_file.load(path)
            self._loading = True
            self._apply_to_form(project)
            self._loading = False
            self._calculate()
        except Exception as ex:
            self._loading = False
            self._show_message(f"Could not open: {ex}", "#B00020")

    def _apply_to_form(self, project: Project) -> None:
        d = project.design
        kind_label = {"BOOKSHELF": "Bookshelf", "BOX": "Box", "CUSTOM": "Custom parts"}[d.kind.name]
        self.preset_var.set(kind_label)
        self._refresh_form_mode()

        if d.kind.name == "CUSTOM":
            lines = [f"{p.label}, {p.width:.0f}, {p.height:.0f}, {p.quantity}" for p in d.build_parts()]
            self.custom_text.delete("1.0", "end")
            self.custom_text.insert("1.0", "\n".join(lines))
        else:
            self.width.set(self._trim(d.param("width")))
            self.height.set(self._trim(d.param("height")))
            self.depth.set(self._trim(d.param("depth")))
            self.thickness.set(self._trim(d.param("thickness")))
            self.shelves.set(self._trim(d.param("shelves")))

        m = project.material
        self.sheet_w.set(self._trim(m.sheet_width))
        self.sheet_h.set(self._trim(m.sheet_height))
        self.kerf.set(self._trim(m.kerf))
        self.price.set(self._trim(m.price_per_sheet))

    @staticmethod
    def _trim(value: float) -> str:
        return str(int(value)) if value == int(value) else str(value)


def main() -> None:
    CutPlanApp().mainloop()


if __name__ == "__main__":
    main()
