"""Where one copy of a part ended up: which sheet, its x/y position, and
whether it was rotated 90 degrees to fit."""

from dataclasses import dataclass

from .part import Part


@dataclass(frozen=True)
class PlacedPart:
    part: Part
    sheet_index: int
    x: float
    y: float
    rotated: bool = False

    @property
    def placed_width(self) -> float:
        return self.part.height if self.rotated else self.part.width

    @property
    def placed_height(self) -> float:
        return self.part.width if self.rotated else self.part.height
