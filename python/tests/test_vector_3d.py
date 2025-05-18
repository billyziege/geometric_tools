# Built-in modules
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
from vector_3d import Vector3D, cross


class Vector3DTests(unittest.TestCase):

    def testIncorrectInitialization(self):
        lists = [[], [1], [1, 2], [1, 2, 3, 4]]
        for input_l in lists:
            with self.subTest(test_list=input_l):
                with self.assertRaises(ValueError):
                    Vector3D(*input_l)

    def testAccess(self):
        vec = Vector3D(1, 2, 3)
        self.assertEqual(vec.x, 1)
        self.assertEqual(vec.y, 2)
        self.assertEqual(vec.z, 3)

    def testIndexAssignment(self):
        vec = Vector3D(1, 2, 3)
        vec[0] = 0
        vec[1] = -1
        vec[2] = -2
        self.assertEqual(vec.x, 0)
        self.assertEqual(vec.y, -1)
        self.assertEqual(vec.z, -2)

    def testAttributeAssignment(self):
        vec = Vector3D(1, 2, 3)
        vec.x = 0
        vec.y = -1
        vec.z = -2
        self.assertEqual(vec[0], 0)
        self.assertEqual(vec[1], -1)
        self.assertEqual(vec[2], -2)

    def testCross(self):
        ref_vec = Vector3D(1, 0, 0)
        test_vectors = [Vector3D(1, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1), Vector3D(1, 1, 1)]
        exp_vectors = [Vector3D(0, 0, 0), Vector3D(0, 0, 1), Vector3D(0, -1, 0), Vector3D(0, -1, 1)]
        for vec, exp_vec in zip(test_vectors, exp_vectors):
            with self.subTest(vec=vec):
                self.assertEqual(cross(ref_vec, vec), exp_vec)
                self.assertEqual(cross(vec, ref_vec), -exp_vec)
