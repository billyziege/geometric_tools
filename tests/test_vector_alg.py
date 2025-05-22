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
from vector_alg import Vector, dot


class VectorAlgTests(unittest.TestCase):

    def testInitializationEmpty(self):
        vec_1 = Vector()
        self.assertEqual(vec_1.array.size, 0)

    def testInitialize123(self):
        vec_1 = Vector(1, 2, 3)
        self.assertTrue(np.all(vec_1.array == np.array([1, 2, 3])))

    def testInitializeVector(self):
        vec_1 = Vector(1, 2, 3)
        vec_2 = Vector(vec_1)
        self.assertTrue(vec_1, vec_2)

    def testStr(self):
        vec = Vector(1, 2, 3)
        self.assertEqual(str(vec), "(1, 2, 3)")

    def testSetItem(self):
        vec = Vector(1, 2, 3)
        vec[0] = 0
        vec[1] = -1
        vec[2] = -2
        self.assertEqual(vec[0], 0)
        self.assertEqual(vec[1], -1)
        self.assertEqual(vec[2], -2)

    def testSize(self):
        values = []
        for i in range(5):
            values.append(i)
            vec = Vector(*values)
            with self.subTest(size=i + 1):
                self.assertEqual(vec.size(), i + 1)

    def testIndex(self):
        values = [1, 2, 3, 4]
        vec = Vector(*values)
        for i, value in enumerate(values):
            with self.subTest(index=i):
                self.assertEqual(vec[i], value)

    def testEqual(self):
        vec_1 = Vector(1, 2, 3)
        vec_2 = Vector(1, 2, 3)
        self.assertEqual(vec_1, vec_2)

    def testNotEqual(self):
        ref_vec = Vector(1, 2, 3)
        test_vecs = [Vector(0, 2, 3), Vector(1, 0, 3), Vector(1, 2, 0), Vector(1, 2, 3, 4)]
        for vec in test_vecs:
            with self.subTest(vec=vec, ref_vec=ref_vec):
                self.assertNotEqual(ref_vec, vec)

    def testAdd(self):
        vec_1 = Vector(1, 2)
        vec_2 = Vector(2, 2)
        sum_vec = Vector(3, 4)
        self.assertEqual(vec_1 + vec_2, sum_vec)

    def testSubtract(self):
        vec_1 = Vector(1, 2)
        vec_2 = Vector(2, 2)
        diff_vec = Vector(-1, 0)
        self.assertEqual(vec_1 - vec_2, diff_vec)

    def testLeftScale(self):
        vec_1 = Vector(1, 2)
        scaled_vec = Vector(2, 4)
        self.assertEqual(vec_1 * 2, scaled_vec)

    def testRightScale(self):
        vec_1 = Vector(1, 2)
        scaled_vec = Vector(2, 4)
        self.assertEqual(2 * vec_1, scaled_vec)

    def testNegative(self):
        vec_1 = Vector(1, 2)
        vec_2 = Vector(-1, -2)
        self.assertEqual(-vec_1, vec_2)

    def testDivide(self):
        vec_1 = Vector(2, 4)
        vec_2 = Vector(1, 2)
        self.assertEqual(vec_1 / 2, vec_2)

    def testDivideByZero(self):
        vec_1 = Vector(2, 4)
        with self.assertRaises(Exception):
            vec_1 / 0

    def testDot(self):
        ref_vec = Vector(1, 1)
        test_vectors = [Vector(1, 0), Vector(0, 1), Vector(1, 1), Vector(1, -1)]
        exp_dots = [1, 1, 2, 0]
        for vec, exp_dot in zip(test_vectors, exp_dots):
            with self.subTest(vec=vec):
                self.assertEqual(dot(ref_vec, vec), exp_dot)
                self.assertEqual(dot(vec, ref_vec), exp_dot)

    def testMag(self):
        test_vectors = [Vector(1, 0), Vector(0, 1), Vector(3, 4), Vector(0, 0)]
        exp_mags = [1, 1, 5, 0]
        for vec, exp_mag in zip(test_vectors, exp_mags):
            with self.subTest(vec=vec):
                self.assertEqual(vec.mag(), exp_mag)
