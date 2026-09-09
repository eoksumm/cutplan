"""Interface for anything that can arrange Parts onto sheets of Material.
Planner only talks to this, never to SimpleFit directly."""

from abc import ABC, abstractmethod
from typing import List

from .material import Material
from .part import Part
from .placed_part import PlacedPart


class CutAlgorithm(ABC):
    @abstractmethod
    def place(self, parts: List[Part], material: Material) -> List[PlacedPart]:
        """Arrange every copy of every part onto one or more sheets.

        Raises FitException if a part cannot be made to fit on an empty sheet
        at all (in either orientation), regardless of how many sheets are used.
        """
