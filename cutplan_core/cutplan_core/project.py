"""A Design and the Material it was planned against. What gets saved to a file."""

from dataclasses import dataclass

from .design import Design
from .material import Material


@dataclass
class Project:
    design: Design
    material: Material
