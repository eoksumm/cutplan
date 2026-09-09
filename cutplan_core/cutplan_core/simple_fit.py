"""A greedy shelf-packing heuristic: the one CutAlgorithm shipped with this library.

Parts are sorted largest-first, then packed left-to-right into a "shelf" (row).
When a part no longer fits in the current shelf it starts a new shelf above
the current one. If the sheet itself is full it moves on to a new sheet.
Each part may be rotated 90 degrees if that lets it fit.

This is simple and fast rather than optimal: it doesn't always find the
arrangement that uses the fewest sheets, but it's good enough for a rough
cutting plan.
"""

from dataclasses import dataclass
from typing import List, Optional

from .cut_algorithm import CutAlgorithm
from .fit_exception import FitException
from .material import Material
from .part import Part
from .placed_part import PlacedPart

_EPS = 1e-6


@dataclass
class _Unit:
    part: Part
    w: float
    h: float


@dataclass
class _Placement:
    x: float
    y: float
    footprint_w: float
    footprint_h: float
    rotated: bool


class SimpleFit(CutAlgorithm):
    def place(self, parts: List[Part], material: Material) -> List[PlacedPart]:
        sheet_w = material.sheet_width
        sheet_h = material.sheet_height
        kerf = material.kerf

        for p in parts:
            if not self._fits_somehow(p.width, p.height, sheet_w, sheet_h):
                raise FitException(
                    p.label,
                    f'"{p.label}" is {p.width:.0f} x {p.height:.0f} mm and will '
                    f"not fit on a {sheet_w:.0f} x {sheet_h:.0f} mm sheet.",
                )

        units = self._explode(parts)
        units.sort(key=lambda u: (-max(u.w, u.h), -(u.w * u.h)))

        placed: List[PlacedPart] = []
        sheet = 0
        shelf_y = 0.0
        shelf_height = 0.0
        cursor_x = 0.0

        for u in units:
            fit = self._try_row(u, cursor_x, shelf_y, shelf_height, sheet_w, sheet_h, kerf)

            if fit is None:
                next_y = shelf_y + shelf_height + (kerf if shelf_height > 0 else 0)
                fit = self._try_row(u, 0, next_y, 0, sheet_w, sheet_h, kerf)
                if fit is not None:
                    shelf_y = next_y
                    shelf_height = 0.0
                    cursor_x = 0.0

            if fit is None:
                sheet += 1
                shelf_y = 0.0
                shelf_height = 0.0
                cursor_x = 0.0
                fit = self._try_row(u, 0, 0, 0, sheet_w, sheet_h, kerf)

            placed.append(PlacedPart(u.part, sheet, fit.x, fit.y, fit.rotated))
            cursor_x = fit.x + fit.footprint_w
            shelf_height = max(shelf_height, fit.footprint_h)

        return placed

    @staticmethod
    def _try_row(u: _Unit, cursor_x: float, shelf_y: float, shelf_height: float,
                 sheet_w: float, sheet_h: float, kerf: float) -> Optional[_Placement]:
        gap = kerf if cursor_x > 0 else 0
        for rotated in (False, True):
            fw = u.h if rotated else u.w
            fh = u.w if rotated else u.h
            fits_x = cursor_x + gap + fw <= sheet_w + _EPS
            fits_y = shelf_y + max(shelf_height, fh) <= sheet_h + _EPS
            if fits_x and fits_y:
                return _Placement(cursor_x + gap, shelf_y, fw, fh, rotated)
        return None

    @staticmethod
    def _fits_somehow(w: float, h: float, sheet_w: float, sheet_h: float) -> bool:
        return (w <= sheet_w + _EPS and h <= sheet_h + _EPS) or (
            h <= sheet_w + _EPS and w <= sheet_h + _EPS
        )

    @staticmethod
    def _explode(parts: List[Part]) -> List[_Unit]:
        units: List[_Unit] = []
        for p in parts:
            for _ in range(p.quantity):
                units.append(_Unit(p, p.width, p.height))
        return units
