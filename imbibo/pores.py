"""General definitions for the imbibo package"""

from dataclasses import dataclass

from helisol import Angle, cos

from .liquids import Liquid



@dataclass
class PorousMedium:
    pore_radius: float
    porosity: float
    tortuosity: float

    @property
    def intrinsic_permeability(self):
        """Permeability factor [m^2]"""
        phi = self.porosity
        tau = self.tortuosity
        r_p = self.pore_radius
        return phi * r_p**2 / (8 * tau)


class PoreLiquid:
    """Class to describe the dynamics of a liquid in a porous medium"""

    def __init__(
        self,
        liquid: Liquid,
        porous_medium: PorousMedium,
        contact_angle: float = 0,
        radius_corr_hydraulic: float = 0,
        radius_corr_capillary: float = 0,
        initial_filling_fraction: float = 0,
    ):
        self.liquid = liquid
        self.porous_medium = porous_medium
        self.theta = Angle(contact_angle)
        self.radius_corr_hydraulic = radius_corr_hydraulic
        self.radius_corr_capillary = radius_corr_capillary
        self.initial_filling_fraction = initial_filling_fraction

    @property
    def effective_radius_hydraulic(self) -> float:
        """Radius used in Carman-Kozeny equation [m]"""
        r_p = self.porous_medium.pore_radius
        return r_p * (1 + self.radius_corr_hydraulic / r_p)**2

    @property
    def effective_radius_capillary(self) -> float:
        """Radius used in Young-Laplace equation [m]"""
        r_p = self.porous_medium.pore_radius
        return r_p * (1 + self.radius_corr_capillary / r_p)

    @property
    def effective_porosity(self) -> float:
        """Porosity corrected by initial volume fraction"""
        phi = self.porous_medium.porosity
        return phi * (1 - self.initial_filling_fraction)

    @property
    def capillary_pressure(self) -> float:
        """Intrinsic capillary pressure - 2 gamma cos(theta) / r_p [Pa]"""
        gamma = self.liquid.surface_tension
        return - 2 * gamma * cos(self.theta) / self.effective_radius_capillary

    @property
    def kelvin_humidity(self) -> float:
        """Equilibrium humidity of pores, calculated from Kelvin

        Will work only if liquid.kelvin_humidity is implemented"""
        return self.liquid.kelvin_humidity(self.capillary_pressure)

    @property
    def permeability(self) -> float:
        """Permeability kappa [m^2 / (Pa.s)] from Carman-Kozeny"""
        k = self.porous_medium.intrinsic_permeability
        eta = self.liquid.viscosity
        r_eff_h = self.effective_radius_hydraulic
        r_p = self.porous_medium.pore_radius
        return (k / eta) * (r_eff_h / r_p)**2

    @property
    def lw_constant(self) -> float:
        """Lucas-Washburn constant w [m^2 / s] so that L^2 = w t"""
        kappa = self.permeability
        phi_eff = self.effective_porosity
        pc = self.capillary_pressure
        return - 2 * kappa * pc / phi_eff

    @property
    def c_l(self) -> float:
        """Huber's group liquid constant C_l [m / s]"""
        gamma = self.liquid.surface_tension
        eta = self.liquid.viscosity
        return 4 * gamma * cos(self.theta) / eta

    @property
    def c_m(self) -> float:
        """Huber group's material constant C_m [m]

        By equivalence with our analysis,
        C_m = kappa * eta / r_p
        """
        k = self.porous_medium.intrinsic_permeability
        phi = self.porous_medium.porosity
        r_p = self.porous_medium.pore_radius

        r_eff_h = self.effective_radius_hydraulic
        r_eff_c = self.effective_radius_capillary
        phi_eff = self.effective_porosity

        return (k / r_eff_c) * (r_eff_h / r_p)**2 * phi / phi_eff
