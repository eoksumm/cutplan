"""Turns a handful of measurements into the list of Parts that need cutting.

Design.bookshelf / Design.box / Design.custom build a Design from raw
numbers. Design.build_parts() is the one place that turns those numbers
into concrete Part objects, so the app doesn't have to work that out
itself.
"""

from enum import Enum, auto
from typing import List

from .parameter import Parameter
from .part import Part


class Kind(Enum):
    BOOKSHELF = auto()
    BOX = auto()
    CUSTOM = auto()


class Design:
    def __init__(self, name: str, kind: Kind):
        self.name = name
        self.kind = kind
        self.parameters: List[Parameter] = []
        self._custom_parts: List[Part] = []

    @staticmethod
    def bookshelf(name: str, width: float, height: float, depth: float,
                  thickness: float, shelves: int) -> "Design":
        d = Design(name, Kind.BOOKSHELF)
        d.parameters = [
            Parameter.mm("width", width),
            Parameter.mm("height", height),
            Parameter.mm("depth", depth),
            Parameter.mm("thickness", thickness),
            Parameter.count("shelves", shelves),
        ]
        return d

    @staticmethod
    def box(name: str, width: float, height: float, depth: float, thickness: float) -> "Design":
        d = Design(name, Kind.BOX)
        d.parameters = [
            Parameter.mm("width", width),
            Parameter.mm("height", height),
            Parameter.mm("depth", depth),
            Parameter.mm("thickness", thickness),
        ]
        return d

    @staticmethod
    def custom(name: str, parts: List[Part]) -> "Design":
        d = Design(name, Kind.CUSTOM)
        d._custom_parts = list(parts)
        return d

    def build_parts(self) -> List[Part]:
        if self.kind == Kind.BOOKSHELF:
            return self._bookshelf_parts()
        if self.kind == Kind.BOX:
            return self._box_parts()
        return list(self._custom_parts)

    def _bookshelf_parts(self) -> List[Part]:
        w = self.param("width")
        h = self.param("height")
        d = self.param("depth")
        t = self.param("thickness")
        shelves = round(self.param("shelves"))
        inner_width = w - 2 * t

        parts = [
            Part("Side panel", d, h, 2),
            Part("Top / bottom", d, inner_width, 2),
        ]
        if shelves > 0:
            parts.append(Part("Shelf", d, inner_width, shelves))
        parts.append(Part("Back panel", w, h, 1))
        return parts

    def _box_parts(self) -> List[Part]:
        w = self.param("width")
        h = self.param("height")
        d = self.param("depth")
        t = self.param("thickness")
        return [
            Part("Front / back", w, h, 2),
            Part("Left / right", d, h, 2),
            Part("Top / bottom", w - 2 * t, d - 2 * t, 2),
        ]

    def param(self, name: str) -> float:
        for p in self.parameters:
            if p.name == name:
                return p.value
        return 0.0
