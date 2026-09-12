"""A Canvas widget that draws a CuttingPlan: one rectangle per sheet, one
smaller rectangle per placed part, roughly to scale."""

import tkinter as tk

_SCALE = 0.18
_GAP = 26
_TOP = 18
_MIN_W = 520
_MIN_H = 420


class SheetView(tk.Canvas):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("width", _MIN_W)
        kwargs.setdefault("height", _MIN_H)
        kwargs.setdefault("highlightthickness", 0)
        super().__init__(master, **kwargs)
        self.plan = None

    def show_plan(self, plan) -> None:
        self.plan = plan
        m = plan.material
        w = int(m.sheet_width * _SCALE) + 4
        h = _TOP + int((m.sheet_height * _SCALE + _GAP) * max(plan.sheets_used, 1)) + 4
        self.config(scrollregion=(0, 0, max(w, _MIN_W), max(h, _MIN_H)))
        self._redraw()

    def clear_plan(self) -> None:
        self.plan = None
        self.delete("all")

    def _redraw(self) -> None:
        self.delete("all")
        if self.plan is None:
            return

        m = self.plan.material
        sheet_w = m.sheet_width * _SCALE
        sheet_h = m.sheet_height * _SCALE

        for s in range(self.plan.sheets_used):
            origin_y = _TOP + s * (sheet_h + _GAP)

            self.create_rectangle(2, origin_y, 2 + sheet_w, origin_y + sheet_h,
                                   fill="#ECEAE5", outline="#333333")
            self.create_text(4, origin_y - 8, text=f"Sheet {s + 1}", anchor="w",
                              fill="#666666", font=("Helvetica", 9))

            for p in self.plan.parts_on_sheet(s):
                x = 2 + p.x * _SCALE
                y = origin_y + p.y * _SCALE
                w = p.placed_width * _SCALE
                h = p.placed_height * _SCALE

                self.create_rectangle(x, y, x + w, y + h, fill="#FFD9B3", outline="#C26A1A")
                label = p.part.label + (" (turned)" if p.rotated else "")
                if len(label) > 22:
                    label = label[:21] + "…"
                self.create_text(x + 4, y + 12, text=label, anchor="w",
                                  fill="#5A3410", font=("Helvetica", 8))
