"""A rectangular piece that needs to be cut, and how many copies are needed."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Part:
    label: str
    width: float
    height: float
    quantity: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError(f"part {self.label} has a non-positive size")
        if self.quantity < 1:
            raise ValueError(f"part {self.label} needs quantity >= 1")

    def __str__(self) -> str:
        return f"{self.label}  {self.width:.0f} x {self.height:.0f}  x{self.quantity}"
