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
from locations import ECEF
from vector_3d import Vector3D


class ECEFTests(unittest.TestCase):
    _fudge = 1e-6

    def testInitialization(self):
        ecef = ECEF(1, 2, 3)
        self.assertEqual(ecef.x, 1)
        self.assertEqual(ecef.y, 2)
        self.assertEqual(ecef.z, 3)

    def testConversionEcef(self):
        ecef = ECEF(1, 2, 3)
        converted_ecef = ecef.ecef()
        self.assertEqual(ecef, converted_ecef)

    def testConversionVector3D(self):
        ecef = ECEF(1, 2, 3)
        vec = Vector3D(1, 2, 3)
        converted_ecef = ecef._vec()
        self.assertTrue(vec == converted_ecef)

    def testAdd(self):
        ecef = ECEF(1, 2, 3)
        vec = Vector3D(0, 2, -3)
        exp_ecef = ECEF(1, 4, 0)
        self.assertTrue(ecef + vec == exp_ecef)
        self.assertTrue(vec + ecef == exp_ecef)

    def testSutraction(self):
        ecef_1 = ECEF(1, 2, 3)
        ecef_2 = ECEF(1, 4, 0)
        exp_vec = Vector3D(0, 2, -3)
        self.assertTrue(ecef_2 - ecef_1 == exp_vec)
        self.assertTrue(ecef_1 - ecef_2 == -exp_vec)

    def testConversionSphCoords(self):
        ecefs = [ECEF(1, 0, 0), ECEF(0, 1, 0), ECEF(0, 0, 1), ECEF(0, 0, -1), ECEF(1, 1, 0), ECEF(0, 1, 1)]
        for ecef in ecefs:
            dbl_converted_ecef = ecef.sph_coords().ecef()
            with self.subTest(ecef=str(ecef), converted=str(dbl_converted_ecef)):
                self.assertTrue((dbl_converted_ecef - ecef).mag() < self._fudge)

    def testConversionGeo(self):
        ecefs = [ECEF(1, 0, 0), ECEF(0, 1, 0), ECEF(0, 0, 1), ECEF(0, 0, -1), ECEF(1, 1, 0), ECEF(0, 1, 1)]
        for ecef in ecefs:
            dbl_converted_ecef = ecef.geo().ecef()
            with self.subTest(ecef=str(ecef), converted=str(dbl_converted_ecef)):
                self.assertTrue((dbl_converted_ecef - ecef).mag() < self._fudge)

    def testFromVector(self):
        vecs = [Vector3D(1, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1), Vector3D(0, 0, -1), Vector3D(1, 1, 0),
                Vector3D(0, 1, 1)]
        exp_ecefs = [ECEF(1, 0, 0), ECEF(0, 1, 0), ECEF(0, 0, 1), ECEF(0, 0, -1), ECEF(1, 1, 0), ECEF(0, 1, 1)]
        for vec, exp_ecef in zip(vecs, exp_ecefs):
            ecef = ECEF._from_vector(vec)
            with self.subTest(ecef=str(ecef), exp_ecef=str(exp_ecef)):
                self.assertTrue((exp_ecef - ecef).mag() < self._fudge)

    def testFromVectorIncorrect(self):
        not_vecs = [1, "one", ECEF(1, 1, 1)]
        for element in not_vecs:
            with self.subTest(element=str(element)):
                with self.assertRaises(TypeError):
                    ECEF._from_vector(element)
