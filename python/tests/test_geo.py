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
from locations import ECEF, Geo
from vector_3d import Vector3D


class SphCoordsTests(unittest.TestCase):
    _fudge = 1e-6

    def testInitialization(self):
        geo = Geo(1, 2, 3)
        self.assertEqual(geo.lat, 1)
        self.assertEqual(geo.lon, 2)
        self.assertEqual(geo.alt, 3)

    def testInitializationModulo(self):
        geo= Geo(190, -100, 3)
        exp_geo = Geo(-170, -80, 3)
        self.assertTrue((geo - exp_geo).mag() < self._fudge)

    def testConversionGeo(self):
        geo = Geo(1, 2, 3)
        converted_geo = geo.geo()
        self.assertEqual(geo, geo)

    def testConversionVector3D(self):
        geo = ECEF(1, 2, 3).geo()
        exp_vec = Vector3D(1, 2, 3)
        self.assertTrue((exp_vec - geo._vec()).mag() < self._fudge)

    def testAdd(self):
        geo = ECEF(1, 2, 3).geo()
        vec = Vector3D(0, 2, -3)
        exp_geo = ECEF(1, 4, 0).geo()
        self.assertTrue(((geo + vec) - exp_geo).mag() < self._fudge)
        self.assertTrue(((vec + geo) - exp_geo).mag() < self._fudge)

    def testSutraction(self):
        geo_1 = ECEF(1, 2, 3).geo()
        geo_2 = ECEF(1, 4, 0).geo()
        exp_vec = Vector3D(0, 2, -3)
        self.assertTrue(((geo_2 - geo_1) - exp_vec).mag() < self._fudge)
        self.assertTrue(((geo_1 - geo_2) + exp_vec).mag() < self._fudge)

    def testConversionECEF(self):
        geos = [Geo(1, 0, 0), Geo(1, 1, 1), Geo(1, 1, -1), Geo(0, 0, 20200),
                Geo(3, 0, 0), Geo(1, 1, 0), Geo(3, -1, 1)]
        for geo in geos:
            dbl_converted_geo = geo.ecef().geo()
            with self.subTest(geo=str(geo), converted=str(dbl_converted_geo)):
                self.assertTrue((dbl_converted_geo - geo).mag() < self._fudge)

    def testConversionSphCoords(self):
        geos = [Geo(1, 0, 0), Geo(1, 1, 1), Geo(1, 1, -1), Geo(0, 0, 20200),
                Geo(3, 0, 0), Geo(1, 1, 0), Geo(3, -1, 1)]
        for geo in geos:
            dbl_converted_geo = geo.sph_coords().geo()
            with self.subTest(geo=str(geo), converted=str(dbl_converted_geo)):
                self.assertTrue((dbl_converted_geo - geo).mag() < self._fudge)

    def testFromVector(self):
        vecs = [Vector3D(1, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1), Vector3D(0, 0, -1), Vector3D(1, 1, 0),
                Vector3D(0, 1, 1)]
        exp_geos = [ECEF(1, 0, 0).geo(), ECEF(0, 1, 0).geo(), ECEF(0, 0, 1).geo(),
                    ECEF(0, 0, -1).geo(), ECEF(1, 1, 0).geo(), ECEF(0, 1, 1).geo()]
        for vec, exp_geo in zip(vecs, exp_geos):
            geo = Geo._from_vector(vec)
            with self.subTest(geo=str(geo), exp_geo=str(exp_geo)):
                self.assertTrue((exp_geo - geo).mag() < self._fudge)

    def testFromVectorIncorrect(self):
        not_vecs = [1, "one", ECEF(1, 1, 1), Geo(1, 0, 1)]
        for element in not_vecs:
            with self.subTest(element=str(element)):
                with self.assertRaises(TypeError):
                    Geo._from_vector(element)
