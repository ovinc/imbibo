"""Description of liquids for the imbibo package"""

from aquasol import water
from aquasol.constants import R

from .temperature import Temperature


class Liquid:

    def __init__(
        self,
        surface_tension: float,
        viscosity: float,
    ):
        """Surface_Tension [N/m], Viscosity [Pa.s]"""
        self.surface_tension = surface_tension
        self.viscosity = viscosity

    def kelvin_humidity(self, capillary_pressure: float) -> float:
        """Optional kelvin humidity calculation from capillary pressure [Pa]"""
        raise NotImplementedError(f'Kelvin Humidity not implemented for {self}')

    def __repr__(self):
        return f'{self.__class__.__name__} [gamma={self.surface_tension}, eta={self.viscosity}]'


class Water(Liquid):

    def __init__(
        self,
        temperature: float = 25
    ):
        """Water properties. Temperature in °C"""
        self.temperature = Temperature(C=temperature)
        super().__init__(
            viscosity=water.viscosity(T=self.temperature.C),
            surface_tension=water.surface_tension(T=self.temperature.C),
        )
        self._define_other_properties()

    def _define_other_properties(self) -> None:
        """Other properties defined for convenience"""
        self.air_diffusivity = water.diffusivity_in_air(T=self.temperature.C)
        self.density = water.density_atm(T=self.temperature.C)
        self.psat = water.vapor_pressure(T=self.temperature.C)
        self.vm = water.molar_volume(T=self.temperature.C)
        self.epsilon = self.vm * self.psat / (R * self.temperature.K)

    @property
    def kelvin_humidity(self, capillary_pressure: float) -> float:
        return water.kelvin_humidity(
            T=self.temperature.C,
            P=capillary_pressure,
            out='aw',
        )

