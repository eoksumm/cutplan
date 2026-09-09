"""A single named, numeric input to a Design (e.g. width = 800 mm)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Parameter:
    name: str
    value: float
    unit: str = ""

    @staticmethod
    def mm(name: str, value: float) -> "Parameter":
        return Parameter(name, value, "mm")

    @staticmethod
    def count(name: str, value: float) -> "Parameter":
        return Parameter(name, value, "")
