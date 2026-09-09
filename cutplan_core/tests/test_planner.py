import pytest

from cutplan_core import Design, FitException, Material, Part, Planner


@pytest.fixture
def sheet():
    return Material.standard_sheet(45)


@pytest.fixture
def bookshelf():
    return Design.bookshelf("B", 800, 1800, 300, 18, 4)


def test_every_part_copy_is_placed(bookshelf, sheet):
    parts = bookshelf.build_parts()
    plan = Planner().plan(bookshelf, sheet)
    assert len(plan.placed) == sum(p.quantity for p in parts)


def test_all_parts_stay_inside_the_sheet(bookshelf, sheet):
    plan = Planner().plan(bookshelf, sheet)
    for p in plan.placed:
        assert p.x >= 0
        assert p.y >= 0
        assert p.x + p.placed_width <= sheet.sheet_width + 1e-6
        assert p.y + p.placed_height <= sheet.sheet_height + 1e-6


def test_sheets_used_is_at_least_one(bookshelf, sheet):
    plan = Planner().plan(bookshelf, sheet)
    assert plan.sheets_used >= 1


def test_waste_percentage_is_between_zero_and_a_hundred(bookshelf, sheet):
    plan = Planner().plan(bookshelf, sheet)
    assert 0 <= plan.waste_percentage() < 100


def test_cost_equals_sheets_used_times_price(bookshelf, sheet):
    plan = Planner().plan(bookshelf, sheet)
    cost = plan.cost_report()
    assert cost.total_price == plan.sheets_used * 45.0


def test_oversized_part_raises_fit_exception(sheet):
    huge = Design.custom("X", [Part("Worktop", 3000, 1300, 1)])
    with pytest.raises(FitException):
        Planner().plan(huge, sheet)


def test_part_that_only_fits_when_rotated_is_accepted(sheet):
    # 1000 x 2000 is too tall as drawn but fits once turned on its side
    tall = Design.custom("Y", [Part("Batten", 1000, 2000, 1)])
    plan = Planner().plan(tall, sheet)
    assert len(plan.placed) == 1


def test_planner_defaults_to_simple_fit():
    from cutplan_core import SimpleFit
    assert isinstance(Planner().algorithm, SimpleFit)


def test_planner_calls_the_algorithm_it_was_given(bookshelf, sheet):
    calls = {"n": 0}

    class Spy:
        def place(self, parts, material):
            calls["n"] += 1
            return []

    planner = Planner()
    planner.set_algorithm(Spy())
    planner.plan(bookshelf, sheet)
    assert calls["n"] == 1


def test_set_algorithm_rejects_none():
    with pytest.raises(ValueError):
        Planner().set_algorithm(None)


def test_many_shelves_spill_onto_a_second_sheet(sheet):
    # too many shelves for one sheet, sheets_used should go up
    big = Design.bookshelf("Big", 800, 1800, 300, 18, 40)
    plan = Planner().plan(big, sheet)
    assert plan.sheets_used >= 2
    assert len(plan.placed) == sum(p.quantity for p in big.build_parts())
