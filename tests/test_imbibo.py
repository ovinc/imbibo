"""Tests for the imbibo module."""

from imbibo import Water, Liquid, Temperature, PoreLiquid, PorousMedium


def test_imbibo_temperature():
    T = Temperature(C=25)
    assert T.K == 298.15


def test_imbibo_water():
    water = water = Water(temperature=25)
    assert round(water.psat) == 3170


def test_imbibo_pore_liquid_water():
    """Test package for water"""
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
        radius_corr_hydraulic=-0.31e-9,
    )

    assert round(pore_liquid.lw_constant * 1e9, 1) == 8.3


def test_imbibo_pore_liquid_squalane():
    """Test package for squalane"""
    squalane = Liquid(surface_tension=28.15e-3, viscosity=0.0311)
    posi = PorousMedium(pore_radius=4.39e-9, porosity=0.574, tortuosity=2.6)
    pore_liquid = PoreLiquid(liquid=squalane, porous_medium=posi)
    assert round(pore_liquid.c_l, 1) == 3.6
