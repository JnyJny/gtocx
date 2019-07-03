"""
"""

import math
import pytest
from gtocx import Star, Stars, Sol

def test_star_creation():

    for i in range(0, 6):
        args = [0] * i
        with pytest.raises(TypeError):
            s = Star(*args)
    
    star = Star(0, 1, 2, 3, 4, 5, 6)
    assert star.r == 0
    assert star.i == 1
    assert star.omega == 2
    assert star.phi == 3
    assert star.t == 4
    assert star.id == 5
    assert star.theta_f == 6


def test_star_theta_f():

    Sol.t = 90
    x,y,z = Sol.position
    theta_f = math.atan2(y, x)

    assert Sol.theta_f == theta_f
    
