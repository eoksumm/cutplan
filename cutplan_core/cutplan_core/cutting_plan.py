"""The result of arranging a design's parts onto one or more sheets."""

from dataclasses import dataclass, field
from typing import List

from .cost_report import CostReport
from .material import Material
from .placed_part import PlacedPart


@dataclass(frozen=True)
class CuttingPlan:
    placed: List[PlacedPart] = field(default_factory=list)
    sheets_used: int = 0
    material: Material = None

    def parts_on_sheet(self, index: int) -> List[PlacedPart]:
        return [p for p in self.placed if p.sheet_index == index]

    def waste_percentage(self) -> float:
        bought = self.sheets_used * self.material.sheet_area
        if bought <= 0:
            return 0.0
        used = sum(p.placed_width * p.placed_height for p in self.placed)
        return (1.0 - used / bought) * 100.0

    def cost_report(self) -> CostReport:
        return CostReport(
            sheets_needed=self.sheets_used,
            waste_percent=self.waste_percentage(),
            total_price=self.sheets_used * self.material.price_per_sheet,
        )
