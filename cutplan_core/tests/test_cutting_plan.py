from cutplan_core import CuttingPlan, Material, Part, PlacedPart


def _plan(placed, sheets_used, material):
    return CuttingPlan(placed=placed, sheets_used=sheets_used, material=material)


def test_waste_percentage_is_zero_when_no_sheets_used():
    plan = _plan([], 0, Material.standard_sheet(10))
    assert plan.waste_percentage() == 0


def test_waste_percentage_with_fully_used_sheet():
    m = Material(1000, 1000, 0, 10)
    part = Part("Square", 1000, 1000, 1)
    placed = [PlacedPart(part, 0, 0, 0)]
    plan = _plan(placed, 1, m)
    assert plan.waste_percentage() == 0


def test_waste_percentage_with_half_used_sheet():
    m = Material(1000, 1000, 0, 10)
    part = Part("HalfSheet", 1000, 500, 1)
    placed = [PlacedPart(part, 0, 0, 0)]
    plan = _plan(placed, 1, m)
    assert plan.waste_percentage() == 50.0


def test_parts_on_sheet_filters_by_index():
    m = Material.standard_sheet(10)
    a = PlacedPart(Part("A", 100, 100, 1), sheet_index=0, x=0, y=0)
    b = PlacedPart(Part("B", 100, 100, 1), sheet_index=1, x=0, y=0)
    plan = _plan([a, b], 2, m)
    assert plan.parts_on_sheet(0) == [a]
    assert plan.parts_on_sheet(1) == [b]


def test_cost_report_fields():
    m = Material(1000, 1000, 0, 25)
    plan = _plan([], 3, m)
    cost = plan.cost_report()
    assert cost.sheets_needed == 3
    assert cost.total_price == 75


def test_placed_part_swaps_dimensions_when_rotated():
    part = Part("Plank", 200, 50, 1)
    placed = PlacedPart(part, 0, 0, 0, rotated=True)
    assert placed.placed_width == 50
    assert placed.placed_height == 200
