import pytest

from cutplan_core import Material


@pytest.mark.parametrize("width,height", [(0, 1000), (-1, 1000), (1000, 0), (1000, -1)])
def test_material_rejects_non_positive_sheet_size(width, height):
    with pytest.raises(ValueError):
        Material(width, height, 3, 45)


def test_material_rejects_negative_kerf():
    with pytest.raises(ValueError):
        Material(2440, 1220, -1, 45)


def test_material_rejects_negative_price():
    with pytest.raises(ValueError):
        Material(2440, 1220, 3, -1)


def test_material_accepts_zero_kerf_and_price_boundary():
    m = Material(2440, 1220, 0, 0)
    assert m.kerf == 0
    assert m.price_per_sheet == 0


def test_standard_sheet_dimensions():
    m = Material.standard_sheet(45)
    assert (m.sheet_width, m.sheet_height, m.kerf, m.price_per_sheet) == (2440, 1220, 3, 45)


def test_sheet_area():
    m = Material(1000, 500, 0, 0)
    assert m.sheet_area == 500_000
