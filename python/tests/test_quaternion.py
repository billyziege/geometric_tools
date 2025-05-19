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
from quaternion import Quaternion, quaternion_rotation
from vector_3d import Vector3D


class QuaternionTests(unittest.TestCase):
    _fudge = 1e-6

    def testInitialization(self):
        q = Quaternion(1, 2, 3, 4)
        self.assertEqual(q[0], 1)
        self.assertEqual(q[1], 2)
        self.assertEqual(q[2], 3)
        self.assertEqual(q[3], 4)

    def testFromRotationAboutAxis(self):
        qs = [Quaternion.from_rotation_about_axis(np.pi / 2., Vector3D(1, 0, 0)),
              Quaternion.from_rotation_about_axis(np.pi, Vector3D(0, 1, 0)),
              Quaternion.from_rotation_about_axis(np.pi / 3., Vector3D(0, 0, 2))]
        exp_qs = [Quaternion(1. / np.sqrt(2.), 1. / np.sqrt(2.), 0, 0),
                  Quaternion(0, 0, 1, 0), Quaternion(np.sqrt(3.) / 2., 0, 0, 1. / 2.)]
        for q, exp_q in zip(qs, exp_qs):
            with self.subTest(q=str(q), exp_q=str(exp_q)):
                self.assertTrue((q - exp_q).mag() < self._fudge)

    def testToAngleAndAxis(self):
        qs = [Quaternion(1. / np.sqrt(2.), 1. / np.sqrt(2.), 0, 0),
              Quaternion(0, 0, 1, 0), Quaternion(np.sqrt(3.) / 2., 0, 0, 1. / 2.)]
        exp_angles = [np.pi / 2., np.pi, np.pi / 3.]
        exp_vecs = [Vector3D(1, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1)]
        for q, exp_angle, exp_vec in zip(qs, exp_angles, exp_vecs):
            angle, vec = q.to_angle_and_unit()
            with self.subTest(q=str(q), exp_angle=str(exp_angle), angle=str(angle)):
                self.assertTrue((angle - exp_angle) < self._fudge)
            with self.subTest(q=str(q), exp_vec=str(exp_vec), vec=str(vec)):
                self.assertTrue((vec - exp_vec).mag() < self._fudge)

    def testFromVector(self):
        vecs = [Vector3D(1, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1)]
        exp_qs = [Quaternion(0, 1, 0, 0), Quaternion(0, 0, 1, 0), Quaternion(0, 0, 0, 1)]
        for vec, exp_q in zip(vecs, exp_qs):
            q = Quaternion.from_vector(vec)
            with self.subTest(q=str(q), exp_q=str(exp_q)):
                self.assertEqual(q, exp_q)

    def testToVector(self):
        qs = [Quaternion(0, 1, 0, 0), Quaternion(0, 0, 1, 0), Quaternion(0, 0, 0, 1)]
        exp_vecs = [Vector3D(1, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1)]
        for q, exp_vec in zip(qs, exp_vecs):
            vec = q.to_vector()
            with self.subTest(vec=str(vec), exp_vec=str(exp_vec)):
                self.assertEqual(vec, exp_vec)

    def testMult(self):
        q1s = [Quaternion(1, 1, 1, 1), Quaternion(1, 0, 0, 0), Quaternion(0, 1, 0, 0)]
        q2s = [Quaternion(1, 1, 1, 1), Quaternion(1, 2, 3, 4), Quaternion(0, 0, 1, 0)]
        q_1x2s = [Quaternion(-2, 2, 2, 2), Quaternion(1, 2, 3, 4), Quaternion(0, 0, 0, -1)]
        q_2x1s = [Quaternion(-2, 2, 2, 2), Quaternion(1, 2, 3, 4), Quaternion(0, 0, 0, 1)]
        for q1, q2, exp_1x2, exp_2x1 in zip(q1s, q2s, q_1x2s, q_2x1s):
            prod_1x2 = q1 * q2
            with self.subTest(prod_1x2=str(prod_1x2), exp_1x2=str(exp_1x2)):
                self.assertEqual(prod_1x2, exp_1x2)
            prod_2x1 = q2 * q1
            with self.subTest(prod_2x1=str(prod_2x1), exp_2x1=str(exp_2x1)):
                self.assertEqual(prod_2x1, exp_2x1)

    def testInv(self):
        qs = [Quaternion(1, 1, 1, 1), Quaternion(1, 2, 3, 4), Quaternion(0, 0, 1, 0)]
        exp_invs = [Quaternion(1, -1, -1, -1), Quaternion(1, -2, -3, -4), Quaternion(0, 0, -1, 0)]
        for q, exp_inv in zip(qs, exp_invs):
            qinv = q.inv()
            with self.subTest(qinv=str(qinv), exp_inv=str(exp_inv)):
                self.assertEqual(qinv, exp_inv)

    def testQuaternionRotation(self):
        rot_angles = [np.pi / 2, np.pi / 4, np.pi]
        axes = [Vector3D(0, 0, 1), Vector3D(1, 0, 0), Vector3D(1, 1, 0)]
        vecs = [Vector3D(1, 0, 1), Vector3D(0, 1, 0), Vector3D(0, 1, 0)]
        exp_rot_vecs = [Vector3D(0, 1, 1), Vector3D(0, np.sqrt(2.) / 2., np.sqrt(2.) / 2.), Vector3D(1, 0, 0)]
        for rot_angle, axis, vec, exp_rot_vec in zip(rot_angles, axes, vecs, exp_rot_vecs):
            rot_vec = quaternion_rotation(rot_angle, axis, vec)
            with self.subTest(rot_vec=str(rot_vec), exp_rot_vec=str(exp_rot_vec)):
                self.assertTrue((rot_vec - exp_rot_vec).mag() < self._fudge)
