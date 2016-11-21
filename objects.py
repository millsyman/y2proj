# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 11:52:01 2016

@author: em1715
"""
import numpy as _np
import matplotlib.pyplot as _plt


def close(float1, float2=0.):
    """Determine if two floats are close enough to be equal. Return bool."""
    if abs(float1 - float2) <= (100. * _np.finfo(float).eps):
        return True
    else:
        return False


class Ball:
    """"""

    def __init__(self, mass=1, radius=1, pos=[0, 0, 0], vel=[0, 0, 0]):
        """"""

        # type checking
        if type(mass) not in (int, float):
            raise TypeError(
                "mass type {}, should be int or float".format(type(mass))
            )
        if mass < 0:
            raise ValueError(
                "mass is {}, should be positive or zero.".format(mass)
            )
        if type(radius) not in (int, float):
            raise TypeError(
                "radius is type {}, should be int or float".format(
                    type(radius)
                )
            )
        if radius <= 0:
            raise ValueError("radius is {}, should be positive".format(radius))
        if type(pos) not in (list, _np.array):
            raise TypeError(
                "pos is type {}, should be list or numpy array".format(
                    type(pos)
                )
            )
        if len(pos) != 3:
            raise ValueError("pos has length {}, should be 3".format(len(pos)))
        if type(vel) not in (list, _np.array):
            raise TypeError(
                "vel is type {}, should be list or numpy array".format(
                    type(vel)
                )
            )
        if len(vel) != 3:
            raise ValueError("vel has length {}, should be 3".format(len(vel)))

        self._mass = float(mass)
        self._radius = float(radius)
        self._pos = _np.array(pos)
        self._vel = _np.array(vel)
        self._patch = _plt.Circle(self._pos[:-1], self._radius)

    def getPos(self):
        """
        Return position as numpy array with 3 components [x, y, z]
        """
        return self._pos

    def getVel(self):
        """
        Return velocity as numpy array with 3 components [v_x, v_y, v_z]
        """
        return self._vel

    def getRadius(self):
        """Return radius as a float"""
        return self._radius

    def setPos(self, new_pos):
        if type(new_pos) not in (list, _np.array):
            raise TypeError(
                "new_pos is type {}, should be list or numpy array".format(
                    type(new_pos)
                )
            )
        self._pos = _np.array(new_pos)

    def setVel(self, new_vel):
        if type(new_vel) not in (list, _np.array):
            raise TypeError(
                "new_vel is type {}, should be list or numpy array".format(
                    type(new_vel)
                )
            )
        self._vel = _np.array(new_vel)

    def move(self, dt):
        if type(dt) not in (int, float):
            raise TypeError(
                "dt is type {}, should be int or float".format(type(dt))
            )
        if dt <= 0:
            raise ValueError("dt is {}, should be positive".format(dt))
        pos = self.getPos()
        vel = self.getVel()
        new_pos = pos.inner(vel * dt)
        self.setPos(new_pos)

    def time_to_collision(self, other):
        # @todo
        r1 = self.getPos()
        v1 = self.getVel()
        rad1 = self.getRadius()
        r2 = other.getPos()
        v2 = other.getVel()
        rad2 = other.getRadius()
        # Define a, b, c of the quadratic equation in dt
        a = _np.dot((v1 - v2), (v1 - v2))
        a = float(a)
        b = 2 * _np.dot((r1 - r2), (v1 - v2))
        b = float(b)
        c = _np.dot((r1 - r2), (r1 - r2)) - ((rad1 + rad2) * (rad1 + rad2))
        dt1 = (-b + _np.sqrt(_np.complex(b*b - 4*a*c))) / (2*a)
        dt2 = (-b - _np.sqrt(_np.complex(b*b - 4*a*c))) / (2*a)
        if _np.imag(dt1) != 0:
            return None
        minimum = min(dt1, dt2)
        if minimum > 0:
            return float(minimum)
        maximum = max(dt1, dt2)
        if maximum > 0:
            return float(maximum)
        else:
            return None

    def collide(self, other):
        # @todo
        None


class Container:
    """"""

    def __init__(self, radius):
        if type(radius) not in (int, float):
            raise TypeError(
                "radius is type {}, should be int or float".format(
                    type(radius)
                )
            )
        if radius <= 0:
            raise ValueError("radius is {}, should be positive".format(radius))

        self._radius = float(radius)
        self._patch = _plt.Circle((0, 0), self._radius)

    def getPos(self):
        """Return zero vector for use with collisions"""
        return _np.array([0, 0, 0])

    def getVel(self):
        """Return zero vector for use with collisions"""
        return _np.array([0, 0, 0])

    def getRadius(self):
        """Return negative radius as float.

        Radius is negative to allow interoperability with standard
        Ball.time_to_collision()
        """
        return - self._radius