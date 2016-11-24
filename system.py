# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 19:20:05 2016

@author: em1715
"""
# @todo STOP EACH COLLISION FROM HAPPENING TWICE!
import heapq

import objects

from core import close, FRAMERATE


class System:
    """Contain all the objects; keep track of time; trigger animation;
    calculate, queue and trigger collisions; calculate and store state
    variables.
    """

    def __init__(self, balls, container):
        """Initialise the system with objects

        Args:
            balls: list, objects.Ball to include in system
            container: objects.Container for system

        Defines:
            self._balls: list of balls in system
            self._container: the container
            self._objects: All objects in system (balls + container)
            self._collisions: a heap of the next collisions with
                format [time_to_collision, (object1, object2)]
        """
        # input checking
        if type(balls) is not list:
            raise TypeError("balls is not of type list")
        if isinstance(container, objects.Container) is False:
            raise TypeError("container is not instance of Container")
        self._balls = balls
        self._container = container
        self._objects = self._balls[:]
        self._objects.append(self._container)
        self._collisions = []
        self._time = 0.
        self._frame = 0

    def init_figure(self, figure):
        """Generate starting collisions heap, then initialise animation.
        @todo initialise animation
        """
        print "init_figure called"
        ret = []
        for i, ball in enumerate(self._balls):
            collTimes = []
            for other in self._objects[i:]:
                if other == ball:
                    continue
                time_to_coll = ball.time_to_collision(other)
                if time_to_coll is not None:
                    collTimes.append([time_to_coll, (ball, other)])
                # print collTimes
            if len(collTimes) > 0:
                heapq.heappush(self._collisions, min(collTimes))
        # draw the figures
        figure.add_artist(self._container.getPatch())
        for ball in self._balls:
            figure.add_patch(ball.getPatch())
            ret.append(ball.getPatch())
        return ret

    def next_frame(self, f):
        """Called by matplotlib.animation.FuncAnimation()

        @todo draws next frame of animation.
        If the next collision occurs before the next frame, call collide
        instead.
        Args:
            f: int, framenumber
        """
        # DEBUGGING
        print "next frame f =", f
        for ball in self._balls:
            print "Begin ball:"
            print "vel =", ball.getVel()
            print "pos =", ball.getPos()
            print "End ball"
        # /DEBUGGING





        patches = []
        self.check_collide()
        step = (f / FRAMERATE) - self._time
        self.tick(step)
        for ball in self._balls:
            patches.append(ball.getPatch())
        self._frame = f
        return patches

    def collide(self):
        """@todo perform queued collision, then calculate and queue
        next collision"""
        next_coll = heapq.heappop(self._collisions)
        obj1, obj2 = next_coll[1]
        obj1.collide(obj2, True)
        for obj in [obj1, obj2]:
            if isinstance(obj, objects.Container):
                continue
            collTimes = []
            for other in self._objects:
                if obj == other:
                    continue
                time_to_coll = obj.time_to_collision(other)
                if time_to_coll is not None:
                    if close(time_to_coll, 0) is False:
                        time_to_coll += self._time
                        collTimes.append(
                            [time_to_coll, (obj, other)]
                        )
            if len(collTimes) > 0:
                heapq.heappush(self._collisions, min(collTimes))

    def check_collide(self):
        """ """
        print "collisions", self._collisions
        t = self._time
        f = self._frame
        print "time", t
        print "frame", f
        # time at the next frame
        t_1 = (f + 1) / FRAMERATE
        dt = 1 / FRAMERATE
        print "dt =", dt
        next_coll_t = self._collisions[0][0]
        if next_coll_t <= t_1:
            step = next_coll_t - t
            self.tick(step)
            self.collide()
            self.check_collide()
            return None
        else:
            return None

    def tick(self, step):
        for ball in self._balls:
            ball.move(step)
        self._time += step
