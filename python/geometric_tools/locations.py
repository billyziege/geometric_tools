from __future__ import annotations
import numpy as np

from angles import degrees_to_radians, radians_to_degrees
from vector_3d import Vector3D


class Location(object):
    """
    Base class for locations.  Provides the algebra for location..
    """

    @classmethod
    def _from_vector(cls, vec_in: Vector3D) -> Location:
        raise NotImplementedError("Should not be converting locations with the base class.")

    def _vec(self) -> Vector3D:
        """
        Convert to a generic 3D vector.
        """
        return self.ecef()._vec()

    def ecef(self):
        raise NotImplementedError("Should not be converting locations with the base class.")

    def geo(self):
        raise NotImplementedError("Should not be converting locations with the base class.")

    def sph_coords(self):
        raise NotImplementedError("Should not be converting locations with the base class.")

    def __add__(self, other: Vector3D) -> Location:
        """
        Returns a location of the same class type that has been displaced by the input vector.
        """
        if isinstance(other, Vector3D):
            return self.__class__._from_vector(self._vec() + other)
        else:
            raise TypeError("Displacement vector must be a Vector3D.")

    def __radd__(self, other: Vector3D) -> Location:
        """
        Returns a location of the same class type that has been displaced by the input vector.
        """
        if isinstance(other, Vector3D):
            return self.__class__._from_vector(self._vec() + other)
        else:
            raise TypeError("Displacement vector must be a Vector3D.")

    def __sub__(self, other: Location) -> Vector3D:
        """
        Gets the vector between two locations.
        """
        return self._vec() - other._vec()

    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False
        for name, value in self.__dict__.items():
            if callable(value):
                continue
            try:
                if other.__dict__[name] != value:
                    return False
            except KeyError:
                return False
        return True

    def __neq__(self, other):
        return not self.__eq__(other)


class ECEF(Location):
    """
    Acronym of Earth Centered Earth Fixed (frame) location.  All units are km.
    """

    def __init__(self, x_km: float, y_km: float, z_km: float):
        self.x = x_km
        self.y = y_km
        self.z = z_km

    @classmethod
    def _from_vector(cls, vec_in: Vector3D) -> ECEF:
        if not isinstance(vec_in, Vector3D):
            err_msg = "Calling _from_vector with a non Vector3D object.  It was of type {}."
            raise TypeError(err_msg.format(vec_in.__class__.__name__))
        return ECEF(vec_in.x, vec_in.y, vec_in.z)

    def __str__(self):
        return "(" + str(self.x) + " km, " + str(self.y) + " km," + str(self.z) + " km)"

    def _vec(self) -> Vector3D:
        """
        Convert to a generic 3D vector.
        """
        return Vector3D(self.x, self.y, self.z)

    def ecef(self) -> ECEF:
        """
        Overrides base class ecef and just returns self.
        """
        return self

    def sph_coords(self) -> SphCoords:
        """
        Convert to spherical coordinate representation.
        """
        r = self._vec().mag()
        if r == 0:
            return SphCoords(0, 0, 0)
        r_xy = np.sqrt(self.x**2 + self.y**2)
        angle_z = np.acos(r_xy / r)  # angle between x,y plane and vector.
        if self.z > 0:
            theta = np.pi / 2. - angle_z
        else:
            theta = np.pi / 2. + angle_z
        if r_xy == 0:
            return SphCoords(r, theta, 0)
        phi = np.acos(self.x / r_xy)  # phi between 0 an np.pi
        if self.y < 0:  # phi between np.pi and 2 np.pi
            phi = 2. * np.pi - phi
        return SphCoords(r, theta, phi)

    def geo(self):
        """
        Convert to geographic representation.
        """
        return self.sph_coords().geo()


class SphCoords(Location):
    """
    Standard spherical coordinate representation of a location.
    Angle in radians.
    """

    def __init__(self, r_km: float, theta_rad: float, phi_rad: float):
        self.r = r_km
        theta_rad = theta_rad % (2 * np.pi)
        if theta_rad > np.pi:
            theta_rad = (2 * np.pi) - theta_rad
        self.theta = theta_rad
        self.phi = phi_rad % (2 * np.pi)

    @classmethod
    def _from_vector(cls, vec_in: Vector3D) -> SphCoords:
        if not isinstance(vec_in, Vector3D):
            raise TypeError("Calling _from_vector with a non Vector3D object.")
        return ECEF(vec_in.x, vec_in.y, vec_in.z).sph_coords()

    def __str__(self):
        return "(" + str(self.r) + " km, " + str(self.theta) + " rad," + str(self.phi) + " rad)"

    def ecef(self) -> ECEF:
        """
        Convert to ECEF representation.
        """
        x = self.r * np.sin(self.theta) * np.cos(self.phi)
        y = self.r * np.sin(self.theta) * np.sin(self.phi)
        z = self.r * np.cos(self.theta)
        return ECEF(x, y, z)

    def sph_coords(self) -> SphCoords:
        """
        Overrides base class sph_coords and just returns self.
        """
        return self

    def geo(self) -> Geo:
        """
        Convert to geographic representation.
        """
        latitude_deg = 90. - radians_to_degrees(self.theta)
        longitude_deg = radians_to_degrees(self.phi)
        altitude_km = self.r - Geo.Re_km
        return Geo(latitude_deg, longitude_deg, altitude_km)


class Geo(Location):
    """
    Geographic representation of location.
    Angles in degrees; altitude in km above spherical earth
    """
    Re_km = 6378.137  # Radius of the Earth in km.

    def __init__(self, latitude_deg: float, longitude_deg: float, altitude_km: float):
        self.lat = (latitude_deg + 180.) % 360. - 180.  # between -180 and 180
        longitude_deg = (longitude_deg + 90) % 360. - 90
        if longitude_deg > 90:
            longitude_deg = 180. - longitude_deg
        self.lon = longitude_deg   # between -90 and 90
        self.alt = altitude_km

    @classmethod
    def _from_vector(cls, vec_in: Vector3D) -> Geo:
        if not isinstance(vec_in, Vector3D):
            raise TypeError("Calling _from_vector with a non Vector3D object.")
        return ECEF(vec_in.x, vec_in.y, vec_in.z).geo()

    def __str__(self):
        return "(" + str(self.lat) + " deg, " + str(self.lon) + " deg," + str(self.alt) + " km)"

    def ecef(self) -> ECEF:
        """
        Convert to ECEF representation.
        """
        return self.sph_coords().ecef()

    def sph_coords(self) -> SphCoords:
        """
        Converts to SphCoord representation.
        """
        r_km = self.Re_km + self.alt
        theta_rad = degrees_to_radians(90. - self.lat)
        phi_rad = degrees_to_radians(self.lon)
        return SphCoords(r_km, theta_rad, phi_rad)

    def geo(self) -> Geo:
        """
        Overrides base class geo and just returns self.
        """
        return self
