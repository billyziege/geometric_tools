from __future__ import annotations
from numbers import Number
from typing import Tuple

import numpy as np

from vector_alg import Vector
from vector_3d import Vector3D


class Quaternion(Vector):
    _fudge = 1e-10

    def __init__(self, q0, q1, q2, q3):
        super().__init__(q0, q1, q2, q3)

    @classmethod
    def from_rotation_about_axis(cls, angle: Number, vec: Vector3D) -> Quaternion:
        if not isinstance(vec, Vector3D):
            raise TypeError("The vector argument must be a Vector3D object.")
        unit = vec.unit()
        cos_half_angle = np.cos(angle / 2.)
        sin_half_angle = np.sin(angle / 2.)
        qvec = sin_half_angle * unit
        return Quaternion(cos_half_angle, qvec.x, qvec.y, qvec.z)

    def to_angle_and_unit(self) -> Tuple[Number, Vector3D]:
        angle = 2. * np.acos(self.array[0])
        sin_half_angle = np.sin(angle / 2.)
        if sin_half_angle == 0:
            raise ValueError("Could not recover unit vector from angle = {}.".format(angle))
        return angle, Vector3D(*list((self.array / sin_half_angle)[1:]))

    @classmethod
    def from_vector(cls, vec: Vector3D) -> Quaternion:
        if not isinstance(vec, Vector3D):
            raise TypeError("The vector argument must be a Vector3D object.")
        return Quaternion(0, vec.x, vec.y, vec.z)

    def to_vector(self) -> Vector3D:
        if abs(self.array[0]) > self._fudge:
            err_msg = "Could not convert the quaternion to a vector as q0 needs to be 0. q0 = {}."
            raise ValueError(err_msg.format(self.q0))
        return Vector3D(*list(self.array[1:]))

    def __mul__(self, other: Quaternion) -> Quaternion:
        if not isinstance(other, Quaternion):
            return super().__mul__(other)
        return Quaternion(self[0] * other[0] - self[1] * other[1] - self[2] * other[2] - self[3] * other[3],
                          self[0] * other[1] + self[1] * other[0] - self[2] * other[3] + self[3] * other[2],
                          self[0] * other[2] + self[2] * other[0] - self[3] * other[1] + self[1] * other[3],
                          self[0] * other[3] + self[3] * other[0] - self[1] * other[2] + self[2] * other[1])

    def inv(self) -> Quaternion:
        return Quaternion(self[0], -self[1], -self[2], -self[3])


def quaternion_rotation(rot_angle, rot_axis: Vector3D, vec: Vector3D) -> Vector3D:
    """
    Rotates vec by rot_angle about the axis along rot_axis.
    """
    rot_q = Quaternion.from_rotation_about_axis(rot_angle, rot_axis)
    qvec = Quaternion.from_vector(vec)
    qvec_rot = rot_q.inv() * qvec * rot_q
    return qvec_rot.to_vector()
