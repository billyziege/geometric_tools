import numpy as np


def degrees_to_radians(angle_deg: float) -> float:
    return float((angle_deg % 360.) * np.pi / 180.)


def radians_to_degrees(angle_rad: float) -> float:
    return float((angle_rad % (2. * np.pi)) * 180.0 / np.pi)
