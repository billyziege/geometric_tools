# Built-in modules
from numbers import Number
import os
import sys
import unittest

# 3rd party
import numpy as np

# This next bit makes sure the resources are available without needing to install.
this_dir = os.path.abspath(os.path.dirname(__file__))
python_dir = os.path.dirname(this_dir)
module_dir = os.path.join(python_dir, "geometric_tools")
if module_dir not in sys.path:
    sys.path.append(module_dir)

# Custom modules
from angles import degrees_to_radians, radians_to_degrees

def is_near_on_circle(x: Number, y: Number, fudge: Number, mod: Number) -> bool:
    return (abs(x - y) < fudge) or (abs(x - y - mod) < fudge) or (abs(x - y + mod) < fudge)

class AnglesTests(unittest.TestCase):
    _fudge = 1e-6

    def testDegRadConversion(self):
        degrees = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
        radians = [0, 1 / 6., 1 / 4., 1 / 3., 1 / 2., 2. / 3., 3. / 4., 5. / 6., 1., 7. / 6.,
                   5 / 4., 4. / 3., 3. / 2., 5. / 3., 7. / 4., 11. / 6, 2.]
        radians = [float(np.pi * x) for x in radians]
        for deg, rad in zip(degrees, radians):
            self.assertTrue(is_near_on_circle(degrees_to_radians(deg), rad, self._fudge, 2. * np.pi))
            self.assertTrue(is_near_on_circle(radians_to_degrees(rad), deg, self._fudge, 360.))

    def testDegModulo(self):
        degrees = np.array([0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360])
        full_rotations = [x * 360. for x in [-2, -1, 2, 3, 81]]
        for full_rot in full_rotations:
            rot_degrees = degrees + full_rot
            rot_degrees = [deg + full_rot for deg in degrees]
            with self.subTest(full_rot=full_rot):
                for rot_deg, deg in zip(list(rot_degrees), list(degrees)):
                    self.assertTrue(is_near_on_circle(degrees_to_radians(rot_deg), degrees_to_radians(deg),
                                                      self._fudge, 2. * np.pi))

    def testRadModulo(self):
        radians = [0, 1 / 6., 1 / 4., 1 / 3., 1 / 2., 2. / 3., 3. / 4., 5. / 6., 1., 7. / 6.,
                   5 / 4., 4. / 3., 3. / 2., 5. / 3., 7. / 4., 11. / 6, 2.]
        radians = [float(np.pi * x) for x in radians]
        full_rotations = [float(x * 2. * np.pi) for x in [-2, -1, 2, 3, 81]]
        for full_rot in full_rotations:
            rot_radians = [rad + full_rot for rad in radians]
            with self.subTest(full_rot=full_rot):
                for rot_rad, rad in zip(list(rot_radians), list(radians)):
                    self.assertTrue(is_near_on_circle(radians_to_degrees(rot_rad), radians_to_degrees(rad),
                                                      self._fudge, 360.))
