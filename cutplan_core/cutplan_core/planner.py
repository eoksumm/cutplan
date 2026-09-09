"""Asks a CutAlgorithm to arrange a Design's parts on a Material.

Planner only depends on the CutAlgorithm interface, not on SimpleFit
directly. A different algorithm can be swapped in with set_algorithm(),
without changing anything here.
"""

from .cut_algorithm import CutAlgorithm
from .cutting_plan import CuttingPlan
from .design import Design
from .material import Material
from .simple_fit import SimpleFit


class Planner:
    def __init__(self) -> None:
        self._algorithm: CutAlgorithm = SimpleFit()

    def set_algorithm(self, algorithm: CutAlgorithm) -> None:
        if algorithm is None:
            raise ValueError("algorithm cannot be None")
        self._algorithm = algorithm

    @property
    def algorithm(self) -> CutAlgorithm:
        return self._algorithm

    def plan(self, design: Design, material: Material) -> CuttingPlan:
        parts = design.build_parts()
        placed = self._algorithm.place(parts, material)

        sheets_used = 0
        for p in placed:
            sheets_used = max(sheets_used, p.sheet_index + 1)
        return CuttingPlan(placed, sheets_used, material)
