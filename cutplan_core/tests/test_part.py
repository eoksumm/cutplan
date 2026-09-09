import pytest

from cutplan_core import Part


@pytest.mark.parametrize("width,height", [(0, 100), (-5, 100), (100, 0), (100, -5)])
def test_part_rejects_non_positive_size(width, height):
    with pytest.raises(ValueError):
        Part("X", width, height, 1)


def test_part_rejects_zero_quantity():
    with pytest.raises(ValueError):
        Part("X", 100, 100, 0)


def test_part_rejects_negative_quantity():
    with pytest.raises(ValueError):
        Part("X", 100, 100, -1)


def test_part_accepts_quantity_of_one_boundary():
    p = Part("X", 100, 100, 1)
    assert p.quantity == 1


def test_part_string_representation():
    p = Part("Shelf", 300.0, 664.0, 4)
    assert str(p) == "Shelf  300 x 664  x4"
