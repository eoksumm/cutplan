"""The sheet stock the parts will be cut from: size, saw kerf and price."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    sheet_width: float
    sheet_height: float
    kerf: float
    price_per_sheet: float

    def __post_init__(self) -> None:
        if self.sheet_width <= 0 or self.sheet_height <= 0:
            raise ValueError("sheet size must be positive")
        if self.kerf < 0 or self.price_per_sheet < 0:
            raise ValueError("kerf and price cannot be negative")

    @staticmethod
    def standard_sheet(price_per_sheet: float) -> "Material":
        """A standard 2440 x 1220 mm sheet (e.g. plywood/MDF) with a 3 mm kerf."""
        return Material(2440, 1220, 3, price_per_sheet)

    @property
    def sheet_area(self) -> float:
        return self.sheet_width * self.sheet_height
