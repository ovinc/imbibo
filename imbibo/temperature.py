"""Temperature management"""


class Temperature:
    """Class to describe and convert temperatures between Celsius and Kelvin"""

    def __init__(self, C=None, K=None):
        """Input C for Celsius and K for Kelvin"""
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

