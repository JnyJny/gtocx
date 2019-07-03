"""a spherical coordinate point
"""

from loguru import logger
from dataclasses import dataclass, field
from typing import List
from functools import lru_cache
import math

from .constants import K

@dataclass
class Point:
    r: float
    i: float
    omega: float
    phi: float
    t: float
#    cos_i: float = field(init=False)
#    sin_i: float = field(init=False)
#    cos_omega: float = field(init=False)
#    sin_omega: float = field(init=False)

    def __post_init__(self):
        self.cos_i = math.cos(self.i)
        self.sin_i = math.sin(self.i)
        self.cos_omega = math.cos(self.omega)
        self.sin_omega = math.sin(self.omega)

    @property
    def Vc(self):
        """Vc - circular orbital speed km/s?
        """
        try:
            return self._Vc
        except AttributeError:
            pass
        self._Vc = 1 / sum([k*(self.r**i) for i,k in enumerate(K)])
        return self._Vc

    @property
    def Fc(self):
        """Force directed towards galactic center
        """
        try:
            return self._Fc
        except AttributeError:
            pass
        self._Fc = (self.Vc**2) / self.r
        return self._Fc

    @property
    def n(self):
        """
        """
        try:
            return self._n
        except AttributeError:
            pass
        self._n = self.Vc / self.r
        return self._n

    @property
    def nt_phi(self):
        return (self.n * self.t) + self.phi

    @property
    def x(self):
        """X coordinate at time 't' .

        R[cos(nt+φ) cosΩ − sin(nt+φ) cosi sinΩ]
        """
        a = math.cos(self.nt_phi) * self.cos_omega
        b = math.sin(self.nt_phi) * self.cos_i * self.sin_omega
        return self.r * (a - b)

    @property
    def y(self):
        """Y coordinate at time 't'.

        R[cos(nt+φ)sinΩ + sin(nt+φ) cos i cos Ω]
        """
        a = math.cos(self.nt_phi) * self.sin_omega
        b = math.sin(self.nt_phi) * self.cos_i * self.cos_omega
        return self.r * (a + b)

    @property
    def z(self):
        """Z coordinate at time 't'.

        R[sin(nt + φ) sin i]
        """
        return self.r * (math.sin(self.nt_phi) * self.sin_i)

    @property
    def Vx(self):
        """X velocity component at time 't'.

        vc(R)[−sin(nt+φ)cosΩ−cos(nt+φ)cosisinΩ]
        """
        a = -1 * math.sin(self.nt_phi) * self.cos_omega
        b = math.cos(self.nt_phi) * self.cos_i * self.sin_omega
        return self.Vc * (a - b)

    @property
    def Vy(self):
        """Y velocity component at time 't'.

        vc(R)[−sin(nt+φ)sinΩ+cos(nt+φ)cosicosΩ]
        """
        a = -1 * math.sin(self.nt_phi) * self.sin_omega
        b = math.cos(self.nt_phi * self.cos_i * self.cos_omega)
        return self.Vc * (a + b)

    @property
    def Vz(self):
        """Z velocity component at time 't'.

        vc(R)[cos(nt + φ) sin i]
        """
        return self.Vc * (math.cos(self.nt_phi) * self.sin_i)

    @property
    def position(self):
        """Tuple of (x, y, z) coordinates.
        """
        return (self.x, self.y, self.z)

    @property
    def velocity(self):
        """A tuple of Vx, Vy, Vz.
        """
        return (self.v_x(t), self.v_y(t), self.v_z(t))

    def distance(self, other):
        """Euclidean distance between self and other.
        """
        if self.t != other.t:
            raise ValueError(f"Comparing distance of points at different times")
        dsqr = sum([(b-a)**2 for a,b in zip(self.position, other.position)])
        return dsqr**0.5
