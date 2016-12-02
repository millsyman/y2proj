# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 11:52:01 2016

@author: em1715
"""
import numpy as _np
import matplotlib.pyplot as _plt

import core
from core import close


class Ball:
    """Ball class, represents a hard sphere in the system

    Methods:
        get_pos()
        get_vel()
        get_radius()
        get_mass()
        get_patch()
        set_pos(new_pos)
        set_vel(new_vel)
        move(step)
        time_to_collision(other)
        collide(other)


    """

    def __init__(self, mass=1, radius=1, pos=[0, 0, 0], vel=[0, 0, 0]):
        """Initialise Ball

        args:
            mass: float
            radius: float
            pos: numpy.array, 3 component Cartesian position vector
            vel: numpy.array, 3 component Cartesian velocity vector
        """

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
        if type(pos) not in (list, _np.array, _np.ndarray):
            raise TypeError(
                "pos is type {}, should be list or numpy array".format(
                    type(pos)
                )
            )
        if len(pos) != 3:
            raise ValueError("pos has length {}, should be 3".format(len(pos)))
        if type(vel) not in (list, _np.array, _np.ndarray):
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

    def __repr__(self):
        return ("""Ball(mass={0._mass}, radius={0._radius}, pos={0._pos},\
 vel={0._vel})""".format(self))

    def get_pos(self):
        """
        Return position as numpy array with 3 components [x, y, z]

        x, y, z are floats.
        """
        return self._pos

    def get_vel(self):
        """
        Return velocity as numpy array with 3 components [v_x, v_y, v_z]

        v_x, v_y, v_z are floats.
        """
        return self._vel

    def get_radius(self):
        """Return radius as a float"""
        return self._radius

    def get_mass(self):
        """Return mass as float"""
        return self._mass

    def get_patch(self):
        """Return matplotlib.pyplot.Circle representing Ball

        Circle centred on position of Ball, with radius equal to radius
        of Ball.
        """
        return self._patch

    def set_pos(self, new_pos):
        """Update position to *new_pos*

        *new_pos* is list or numpy.array: [x, y, z]; x, y, z are floats
        """
        if type(new_pos) not in (list, _np.array, _np.ndarray):
            raise TypeError(
                "new_pos is type {}, should be list or numpy array".format(
                    type(new_pos)
                )
            )
        self._pos = _np.array(new_pos)
        self._patch.center = self._pos[:-1]

    def set_vel(self, new_vel):
        """Update position to *new_vel*

        *new_vel* is list or numpy.array: [v_x, v_y, v_z];
        v_x, v_y, v_z are floats
        """
        if type(new_vel) not in (list, _np.array, _np.ndarray):
            raise TypeError(
                "new_vel is type {}, should be list or numpy array".format(
                    type(new_vel)
                )
            )
        self._vel = _np.array(new_vel)

    def move(self, step):
        """Move Ball to where it should be in *step* seconds

        *step* is float
        """
        if type(step) not in (int, float):
            raise TypeError(
                "step is type {}, should be int or float".format(type(step))
            )
        if step < 0:
            raise ValueError("step is {}, should be positive".format(step))
        pos = self.get_pos()
        vel = self.get_vel()
        new_pos = pos + (vel * step)
        self.set_pos(new_pos)

    def time_to_collision(self, other):
        """Return time until collision with *other* in seconds.

        *other* is Ball or Container.
        Retun time as float. If Ball does not collide with *other*,
        return None.
        """
        r1 = self.get_pos()
        core.logging.debug("r1 {}".format(r1))
        v1 = self.get_vel()
        core.logging.debug("v1 {}".format(v1))
        rad1 = self.get_radius()
        core.logging.debug("rad1 {}".format(rad1))
        r2 = other.get_pos()
        core.logging.debug("r2 {}".format(r2))
        v2 = other.get_vel()
        core.logging.debug("v2 {}".format(v2))
        rad2 = other.get_radius()
        core.logging.debug("rad2 {}".format(rad2))
        # Define a, b, c of the quadratic equation in dt
        a = _np.dot((v1 - v2), (v1 - v2))
        a = float(a)
        b = 2 * _np.dot((r1 - r2), (v1 - v2))
        b = float(b)
        c = _np.dot((r1 - r2), (r1 - r2)) - ((rad1 + rad2) * (rad1 + rad2))
        dt1 = (-b + _np.sqrt(_np.complex(b * b - 4 * a * c))) / (2 * a)
        dt2 = (-b - _np.sqrt(_np.complex(b * b - 4 * a * c))) / (2 * a)
        if _np.imag(dt1) != 0:
            return None
        minimum = min(dt1, dt2)
        if minimum > 0 and not close(minimum, 0):
            return float(minimum)
        maximum = max(dt1, dt2)
        if maximum > 0:
            return float(maximum)
        else:
            return None

    def collide(self, other):
        """Carry out collision with *other*

        *other* is Ball or Container.
        Update velocity of Ball and *other* as result of the collision.
        """
        Pos = self.get_pos()
        Vel = self.get_vel()
        Mass = self.get_mass()
        if isinstance(other, Container):
            r_norm = Pos / _np.sqrt(_np.dot(Pos, Pos))
            u_perp = _np.dot(Vel, r_norm) * r_norm
            v_para = Vel - u_perp
            v_perp = -u_perp
            dp = 2 * Mass * u_perp
            other.add_momentum(dp)
            v = v_perp + v_para
            self.set_vel(v)
        else:
            oPos = other.get_pos()
            oVel = other.get_vel()
            oMass = other.get_mass()

            r = oPos - Pos
            r = r / _np.sqrt(_np.dot(r, r))
            u1_perp = _np.dot(Vel, r) * r
            u2_perp = _np.dot(oVel, -r) * -r
            v1_para = Vel - u1_perp
            v2_para = oVel - u2_perp
            v1_perp = (((u1_perp * (Mass - oMass) + (2 * oMass * u2_perp))) /
                       (Mass + oMass))
            v2_perp = (((2 * Mass * u1_perp) + (u2_perp * (oMass - Mass))) /
                       (Mass + oMass))
            v1 = v1_perp + v1_para
            v2 = v2_perp + v2_para
            self.set_vel(v1)
            other.set_vel(v2)


class Container:
    """
    Spherical container for objects of type Ball. Has infinite mass.
    """

    def __init__(self, radius):
        """Initialise the container with parameters

        Args:
            radius: float. Radius of container.
        """
        if type(radius) not in (int, float):
            raise TypeError(
                "radius is type {}, should be int or float".format(
                    type(radius)
                )
            )
        if radius <= 0:
            raise ValueError("radius is {}, should be positive".format(radius))

        self._radius = float(radius)
        self._patch = _plt.Circle((0, 0), self._radius, fill=False)
        self._momentum = _np.array([0., 0., 0.])

    def get_pos(self):
        """Return zero vector for use with collisions"""
        return _np.array([0, 0, 0])

    def get_vel(self):
        """Return zero vector for use with collisions"""
        return _np.array([0, 0, 0])

    def get_radius(self):
        """Return negative radius as float.

        Radius is negative to allow interoperability with standard
        Ball.time_to_collision()
        """
        return - self._radius

    def get_patch(self):
        """Return matplotlib.pyplot.Circle displaying Container"""
        return self._patch

    def add_momentum(self, dp):
        # input checking
        self._momentum += dp

    def get_momentum(self):
        return self._momentum
