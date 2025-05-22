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
from locations import Location
from vector_3d import Vector3D


class LocationBaseClassTests(unittest.TestCase):

    def testDefaultInitialization(self):
        try:
            location = Location()
        except Exception as e:
            self.fail("Location initialization threw an unexpected exception: " + str(e))

    def testImproperUseConversions(self):
        location = Location()
        methods = [Location._vec, Location.ecef, Location.sph_coords, Location.geo]
        for method in methods:
            with self.subTest():
                with self.assertRaises(NotImplementedError):
                    method(location)

    def testFromVector(self):
        location = Location()
        vec = Vector3D(1, 2, 3)
        with self.subTest():
            with self.assertRaises(NotImplementedError):
                location._from_vector(vec)
        with self.subTest():
            with self.assertRaises(NotImplementedError):
                location._from_vector(1)

    def testAdd(self):
        location = Location()
        vec = Vector3D(1, 2, 3)
        with self.assertRaises(NotImplementedError):
            location + vec

    def testSubtract(self):
        location_1 = Location()
        location_2 = Location()
        with self.assertRaises(NotImplementedError):
            location_1 - location_2

    def testEqual(self):
        location_1 = Location()
        location_2 = Location()
        self.assertTrue(location_1 == location_2)
        self.assertFalse(location_1 == 1)

    def testNotEqual(self):
        location_1 = Location()
        location_2 = Location()
        self.assertFalse(location_1 != location_2)
        self.assertTrue(location_1 != 1)
