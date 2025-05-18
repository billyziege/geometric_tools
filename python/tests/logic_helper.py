# Built-in modules
from numbers import Number


def is_near_on_circle(x: Number, y: Number, fudge: Number, mod: Number) -> bool:
    return (abs(x - y) < fudge) or (abs(x - y - mod) < fudge) or (abs(x - y + mod) < fudge)
