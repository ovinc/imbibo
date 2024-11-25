About
=====

Python 3 package for calculating imbibition and related phenomena, in particular in nanoporous media with water.


Install
=======

```bash
git clone https://github.com/ovinc/imbibo
cd imbibo
pip install -e .
```


Testing
=======

With `pytest`:
```bash
pytest
```

Quick Start
===========
```python
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

pore_liquid.capillary_pressure    # [Pa]
pore_liquid.permeability          # [m^2 / (Pa.s)]
pore_liquid.lw_constant           # Lucas-Washburn constant w [m^2 / s]
```


Misc. info
==========

Module requirements
-------------------

- aquasol (properties of water and solutions)
- helisol (for the `Angle` class for contact angles)


Python requirements
-------------------

Python : >= 3.7 (dataclasses)

Author
------

Olivier Vincent

(ovinc.py@gmail.com)

License
-------

CeCILL-B (equivalent to BSD, see *LICENSE* file).
