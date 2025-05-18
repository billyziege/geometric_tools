"""
Encodes the basic algebraic rules for vector algebra.
"""
from __future__ import annotations
from numbers import Number

import numpy as np


class Vector(object):

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], np.ndarray):
            self.array = args[0]
            return
        self.array = np.array(args)

    def size(self) -> int:
        return self.array.size

    def _size_eq(self, other: Vector) -> bool:
        return self.size() == other.size()

    def __add__(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.__class__(self.array + other.array)

    def __sub__(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.__class__(self.array - other.array)

    def __mul__(self, other: Number) -> Vector:
        if not isinstance(other, Number):
            return NotImplemented
        return self.__class__(other * self.array)

    def __rmul__(self, other: Number) -> Vector:
        if not isinstance(other, Number):
            raise TypeError("You can only use a scalar for rmul.")
        return self.__class__(other * self.array)

    def __neg__(self) -> Vector:
        return -1 * self

    def __truediv__(self, other: Number) -> Vector:
        return 1. / other * self

    def __eq__(self, other: Vector) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        if not self._size_eq(other):
            return False
        return np.all(self.array == other.array)

    def __neq__(self, other: Vector) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return not self.__eq__(other)

    def __str__(self) -> str:
        return "(" + ", ".join([str(x) for x in self.array]) + ")"

    def __getitem__(self, index: int) -> Number:
        return self.array[index]

    def __setitem__(self, index: int, value: Number):
        self.array[index] = value

    def mag(self) -> Number:
        """ Short for magnitude.  The L2 norm. """
        return np.sqrt(dot(self, self))


def dot(vec_1: type[Vector], vec_2: type[Vector]) -> Number:
    """ Short for dot/inner product of two vectors. """
    return (vec_1.array * vec_2.array).sum()
