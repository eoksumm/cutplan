from cutplan_core import Design, Part


def test_bookshelf_builds_four_part_types():
    parts = Design.bookshelf("B", 800, 1800, 300, 18, 4).build_parts()
    assert len(parts) == 4


def test_bookshelf_has_two_side_panels():
    parts = Design.bookshelf("B", 800, 1800, 300, 18, 4).build_parts()
    side = next(p for p in parts if p.label == "Side panel")
    assert side.quantity == 2


def test_bookshelf_shelf_quantity_matches_input():
    parts = Design.bookshelf("B", 800, 1800, 300, 18, 4).build_parts()
    shelf = next(p for p in parts if p.label == "Shelf")
    assert shelf.quantity == 4


def test_bookshelf_with_zero_shelves_omits_the_shelf_part():
    parts = Design.bookshelf("B", 800, 1800, 300, 18, 0).build_parts()
    assert all(p.label != "Shelf" for p in parts)
    assert len(parts) == 3


def test_box_builds_six_panels_total():
    parts = Design.box("X", 600, 400, 400, 12).build_parts()
    assert sum(p.quantity for p in parts) == 6


def test_custom_design_returns_exactly_the_given_parts():
    parts_in = [Part("Shelf", 100, 200, 1)]
    d = Design.custom("C", parts_in)
    assert d.build_parts() == parts_in


def test_param_returns_zero_for_unknown_name():
    d = Design.bookshelf("B", 800, 1800, 300, 18, 4)
    assert d.param("does-not-exist") == 0
