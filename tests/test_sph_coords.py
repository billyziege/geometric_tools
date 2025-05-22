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
from locations import ECEF, SphCoords
from vector_3d import Vector3D


class SphCoordsTests(unittest.TestCase):
    _fudge = 1e-6

    def testInitialization(self):
        sph = SphCoords(1, 2, 3)
        self.assertEqual(sph.r, 1)
        self.assertEqual(sph.theta, 2)
        self.assertEqual(sph.phi, 3)

    def testInitializationModulo(self):
        sph_coords = SphCoords(1, 1.75 * np.pi, 3.1 * np.pi)
        exp_sph_coords = SphCoords(1, 0.25 * np.pi, 1.1 * np.pi)
        self.assertTrue((sph_coords - exp_sph_coords).mag() < self._fudge)

    def testConversionSphCoords(self):
        sph_coords = SphCoords(1, 2, 3)
        converted_sph_coords = sph_coords.sph_coords()
        self.assertEqual(sph_coords, converted_sph_coords)

    def testConversionVector3D(self):
        sph_coords = ECEF(1, 2, 3).sph_coords()
        exp_vec = Vector3D(1, 2, 3)
        self.assertTrue((exp_vec - sph_coords._vec()).mag() < self._fudge)

    def testAdd(self):
        sph_coords = ECEF(1, 2, 3).sph_coords()
        vec = Vector3D(0, 2, -3)
        exp_sph_coords = ECEF(1, 4, 0).sph_coords()
        self.assertTrue(((sph_coords + vec) - exp_sph_coords).mag() < self._fudge)
        self.assertTrue(((vec + sph_coords) - exp_sph_coords).mag() < self._fudge)

    def testSutraction(self):
        sph_coords_1 = ECEF(1, 2, 3).sph_coords()
        sph_coords_2 = ECEF(1, 4, 0).sph_coords()
        exp_vec = Vector3D(0, 2, -3)
        self.assertTrue(((sph_coords_2 - sph_coords_1) - exp_vec).mag() < self._fudge)
        self.assertTrue(((sph_coords_1 - sph_coords_2) + exp_vec).mag() < self._fudge)

    def testConversionECEF(self):
        sph_coords = [SphCoords(1, 0, 0), SphCoords(1, 1, 1), SphCoords(1, 1, -1),
                      SphCoords(3, 0, 0), SphCoords(1, 1, 0), SphCoords(3, -1, 1)]
        for sph in sph_coords:
            dbl_converted_sph = sph.ecef().sph_coords()
            with self.subTest(sph=str(sph), converted=str(dbl_converted_sph)):
                self.assertTrue((dbl_converted_sph - sph).mag() < self._fudge)

    def testConversionGeo(self):
        sph_coords = [SphCoords(1, 0, 0), SphCoords(1, 1, 1), SphCoords(1, 1, -1),
                      SphCoords(3, 0, 0), SphCoords(1, 1, 0), SphCoords(3, -1, 1)]
        for sph in sph_coords:
            dbl_converted_sph = sph.geo().sph_coords()
            with self.subTest(sph=str(sph), converted=str(dbl_converted_sph)):
                self.assertTrue((dbl_converted_sph - sph).mag() < self._fudge)

    def testFromVector(self):
        vecs = [Vector3D(1, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1), Vector3D(0, 0, -1), Vector3D(1, 1, 0),
                Vector3D(0, 1, 1)]
        exp_sphs = [ECEF(1, 0, 0).sph_coords(), ECEF(0, 1, 0).sph_coords(), ECEF(0, 0, 1).sph_coords(),
                    ECEF(0, 0, -1).sph_coords(), ECEF(1, 1, 0).sph_coords(), ECEF(0, 1, 1).sph_coords()]
        for vec, exp_sph in zip(vecs, exp_sphs):
            sph = SphCoords._from_vector(vec)
            with self.subTest(sph_coords=str(sph), exp_sph_coords=str(exp_sph)):
                self.assertTrue((exp_sph - sph).mag() < self._fudge)

    def testFromVectorIncorrect(self):
        not_vecs = [1, "one", ECEF(1, 1, 1), SphCoords(1, 0, 1)]
        for element in not_vecs:
            with self.subTest(element=str(element)):
                with self.assertRaises(TypeError):
                    SphCoords._from_vector(element)
