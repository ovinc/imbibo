"""Tests for the imbibo module."""

from imbibo import Water, Temperature, PoreLiquid, PorousMedium


def test_imbibo_temperature():
    T = Temperature(C=25)
    assert T.K == 298.15


def test_imbibo_water():
    water = water = Water(temperature=25)
    assert round(water.psat) == 3170


def test_imbibo_pore_liquid():
    """Test package"""
    water = Water(temperature=25)

    porous_silicon = PorousMedium(
        pore_radius=2e-9,
        porosity=0.4,
        tortuosity=4.5,
    )

    pore_liquid = PoreLiquid(
        liquid=water,
        porous_medium=porous_silicon,
        contact_angle=25,
        slip_length=-0.31e-9,
    )

    assert round(pore_liquid.lw_constant * 1e9, 1) == 8.3

