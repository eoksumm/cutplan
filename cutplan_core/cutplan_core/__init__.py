"""cutplan_core: a small library for planning sheet-material cutting layouts.

No GUI code in here. Give it a Design and a Material and it works out the
parts, arranges them on sheets, and reports how many sheets, how much
waste, and what it costs.
"""

from .cost_report import CostReport
from .cut_algorithm import CutAlgorithm
from .cutting_plan import CuttingPlan
from .design import Design, Kind
from .fit_exception import FitException
from .material import Material
from .parameter import Parameter
from .part import Part
from .placed_part import PlacedPart
from .planner import Planner
from .project import Project
from .simple_fit import SimpleFit
