from __future__ import annotations
from numbers import Number

from vector_alg import Vector


class Vector3D(Vector):
    _components = ["x", "y", "z"]

    def __init__(self, *args):
        super().__init__(*args)
        if self.array.size != 3:
            raise ValueError("Vector3D have exactly 3 components.")
        self.x = self[0]
        self.y = self[1]
        self.z = self[2]

    def size(self) -> int:
        return 3

    def __setattr__(self, name: str, value: Number):
        try:
            index = self._components.index(name)
            super().__setitem__(index, value)
        except ValueError:
            pass
        super().__setattr__(name, value)

    def __setitem__(self, index: int, value: Number):
        try:
            self.__setattr__(self._components[index], value)
        except IndexError:
            raise IndexError("Indices of Vector3D are 0, 1, 2.  You provided {}.".format(index))


def cross(vec_1: Vector3D, vec_2: Vector3D) -> Vector3D:
    """
    Short for cross product of two vectors.
    """
    return Vector3D(vec_1.y * vec_2.z - vec_1.z * vec_2.y,
                    vec_1.z * vec_2.x - vec_1.x * vec_2.z,
                    vec_1.x * vec_2.y - vec_1.y * vec_2.x)
