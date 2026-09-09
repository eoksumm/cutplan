"""How many sheets, how much waste, and what it costs."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CostReport:
    sheets_needed: int
    waste_percent: float
    total_price: float
