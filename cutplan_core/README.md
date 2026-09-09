# cutplan-core

The reusable library part of CutPlan. Plans cuts for a DIY build made from
sheet material (plywood, MDF, etc). No GUI code in it at all, so it can be
reused by the desktop app, a CLI, whatever.

## What it does

`Design` turns a few measurements into a list of `Part`s
(`Design.bookshelf(...)`, `Design.box(...)`, or `Design.custom(...)` for a
hand-written part list). `Planner` asks a `CutAlgorithm` (default:
`SimpleFit`) to arrange those parts on a `Material`. The result is a
`CuttingPlan`: which sheet each part is on, how many sheets, waste
percentage, and cost. `project_file.save()`/`load()` save and load a
`Project` as JSON.

## Install

```bash
pip install -e .
pip install -e ".[test]"   # for the test suite
```

## Example

```python
from cutplan_core import Design, Material, Planner

design = Design.bookshelf("Bookshelf", width=800, height=1800, depth=300, thickness=18, shelves=4)
material = Material.standard_sheet(price_per_sheet=45)

plan = Planner().plan(design, material)
cost = plan.cost_report()
print(cost.sheets_needed, cost.waste_percent, cost.total_price)
```

## Design patterns

`CutAlgorithm` is an abstract base class (Strategy pattern) - `Planner`
only calls it through that interface, never `SimpleFit` directly, so a
different algorithm can be swapped in later.

`Design.bookshelf()` / `.box()` / `.custom()` are static factory methods
that build a `Design` from raw numbers.

## Tests

```bash
pytest --cov=cutplan_core
```
