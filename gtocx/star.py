""" a Star drived from Point
"""

import math

from typing import List
from dataclasses import dataclass, field
from .point import Point

@dataclass
class Star(Point):
    id: int
    theta_f: float
    t_colonized: float = -1
    
    @classmethod
    def from_csv(cls, filename: str) -> List:
        """
        :param str filename:
        """
        stars = []
        with open(filename) as data_file:
            for line in data_file.readlines():
                try:                
                    ndx, R, i, o, p, t = list(map(float, line.strip().split(",")))
                    i = math.radians(i)
                    o = math.radians(o)
                    p = math.radians(p)
                    t = math.radians(t)
                except ValueError:
                    continue
                stars.append(cls(R, i, o, p, 0, int(ndx), t))
        return stars


