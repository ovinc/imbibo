"""General definitions for the imbibo package"""

from dataclasses import dataclass

from aquasol.water import diffusivity_in_air, kelvin_humidity, molar_volume
from aquasol.water import viscosity, surface_tension, vapor_pressure, density_atm
from aquasol.constants import R

from helisol import Angle, cos


class Temperature:

    def __init__(self, C=None, K=None):
        if C is None and K is None:
            raise ValueError('No temperature value supplied')
        if C is None:
            self.C = K - 273.15
            self.K = K
        else:
            self.C = C
            self.K = C + 273.15

    def __repr__(self):
        return f'Temperature of {self.C}°C [{self.K}K]'


class Water:

    def __init__(self, temperature=25):
        """Water properties. Temperature in °C"""
        self.temperature = Temperature(C=temperature)
        self.air_diffusivity = diffusivity_in_air(T=self.temperature.C)
        self.viscosity = viscosity(T=self.temperature.C)
        self.surface_tension = surface_tension(T=self.temperature.C)
        self.density = density_atm(T=self.temperature.C)
        self.psat = vapor_pressure(T=self.temperature.C)
        self.vm = molar_volume(T=self.temperature.C)
        self.epsilon = self.vm * self.psat / (R * self.temperature.K)


LIQUIDS = {
    'water': Water
}


@dataclass
class PorousMedium:
    pore_radius: float
    porosity: float
    tortuosity: float


class PoreLiquid:
    """Class to describe the dynamics of a liquid in a porous medium"""

    def __init__(
        self,
        liquid,
        porous_medium,
        contact_angle: float = 0,
        slip_length: float = 0,
    ):
        self.liquid = liquid
        self.porous_medium = porous_medium
        self.theta = Angle(contact_angle)
        self.slip_length = slip_length

    @property
    def effective_radius(self):
        rp = self.porous_medium.pore_radius
        return rp * (1 + self.slip_length / rp)**2

    @property
    def capillary_pressure(self):
        gamma = self.liquid.surface_tension
        return - 2 * gamma * cos(self.theta) / self.porous_medium.pore_radius

    @property
    def equilibrium_humidity(self):
        return kelvin_humidity(
            T=self.liquid.temperature.C,
            P=self.capillary_pressure,
            out='aw',
        )

    @property
    def permeability(self):
        phi = self.porous_medium.porosity
        tau = self.porous_medium.tortuosity
        r_eff = self.effective_radius
        eta = self.liquid.viscosity
        return phi * r_eff**2 / (8 * eta * tau)

    @property
    def lw_constant(self):
        kappa = self.permeability
        phi = self.porous_medium.porosity
        pc = self.capillary_pressure
        return - 2 * kappa * pc / phi
