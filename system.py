# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 19:20:05 2016

@author: em1715
"""
# @todo STOP EACH COLLISION FROM HAPPENING TWICE!
import heapq

import objects

import core
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
        """
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
        """
        Generate collisions heap, then draw objects in starting positions.

        Args:
        figure: matplotlib.pyplot.axes object. Axes to draw objects on.
        """
        core.logging.debug("called init_func")
        ret = []
        for i, ball in enumerate(self._balls):
            collTimes = []
            for other in self._objects[i:]:
                if other == ball:
                    continue
                time_to_coll = ball.time_to_collision(other)
                if time_to_coll is not None:
                    collTimes.append([time_to_coll, (ball, other)])
            if len(collTimes) > 0:
                heapq.heappush(self._collisions, min(collTimes))
        # draw the figures
        figure.add_artist(self._container.getPatch())
        for ball in self._balls:
            figure.add_patch(ball.getPatch())
            ret.append(ball.getPatch())
        core.logging.log(15,
                         "init returned collisions {}".format(self._collisions)
                         )
        return ret

    def next_frame(self, f):
        """Called by matplotlib.animation.FuncAnimation()

        Advance time to when frame *f* occurs, carry out any collisions
        on the way. Draw objects for frame *f*.
        Args:
            f: int, framenumber
        """
        # # DEBUGGING # #
        # print "next frame f =", f
        # for ball in self._balls:
        #     print "Begin ball:"
        #     print "vel =", ball.getVel()
        #     print "pos =", ball.getPos()
        #     print "End ball"
        # # /DEBUGGING # #
        core.logging.debug("called next_frame with frame {}".format(f))
        core.logging.debug("container at {}".format(self._container.getPos()))
        core.logging.debug("container vel {}".format(self._container.getVel()))
        patches = []
        self.check_collide()
        step = (f / FRAMERATE) - self._time
        self.tick(step)
        for obj in self._objects:
            patches.append(obj.getPatch())
        self._frame = f
        return patches

    def collide(self):
        """Perform next collision, then update the queue."""
        core.logging.log(11, self._collisions)
        core.logging.log(11, "time is {}".format(self._time))
        core.logging.log(11, "frame is {}".format(self._frame))
        core.logging.log(11, "objects: {}".format(self._objects))
        next_coll = heapq.heappop(self._collisions)
        core.logging.log(11, "next_coll = {}".format(next_coll))
        obj1, obj2 = next_coll[1]
        obj1.collide(obj2)
        # First, recalculate for all the objects obj1 or obj2
        # collide with in the queue
        to_remove = []
        to_add = [obj1, obj2]
        for index, collision in enumerate(self._collisions):
            if obj1 in collision[1]:
                if obj2 in collision[1]:
                    to_remove.append(index)
                else:
                    # pick out the object that is not obj1
                    obj = [i for i in collision[1] if i is not obj1][0]
                    to_remove.append(index)
                    to_add.append(obj)
            elif obj2 in collision[1]:
                obj = [i for i in collision[1] if i is not obj2][0]
                to_remove.append(index)
                to_add.append(obj)
        # Then find what they actually collide with next
        to_remove.reverse()
        for index in to_remove:
            self._collisions.pop(index)
        heapq.heapify(self._collisions)
        for obj in to_add:
            self.next_collides(obj)

    def check_collide(self):
        """Check to see if two objects collide before the next frame.

        If the next collision occurs before the next frame it will be
        executed.
        """
        core.logging.debug("self._collisions {}".format(self._collisions))
        t = self._time
        f = self._frame
        # time at the next frame
        t_1 = (f + 1) / FRAMERATE
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
        """Advances time by an increment *step*"""
        # Stop the balls from sneaking inside each other due to rounding errors
        if step > 1E-10:
            step -= 1E-10
        for obj in self._objects:
            obj.move(step)
        self._time += step

    def next_collides(self, obj):
        """
        Find what an object next collides with, and add it to the queue
        """
        core.logging.log(11, "next_collides on {}".format(obj))
        collTimes = []
        for other in self._objects:
            core.logging.log(11, "other is {}".format(other))
            if obj == other:
                core.logging.log(11, "continuing")
                continue
            time_to_coll = obj.time_to_collision(other)
            if time_to_coll is not None:
                if close(time_to_coll, 0) is False:
                    time_to_coll += self._time
                    collTimes.append(
                        [time_to_coll, (obj, other)]
                    )
            core.logging.log(11, "collTimes = {}".format(collTimes))
        if len(collTimes) > 0:
            heapq.heappush(self._collisions, min(collTimes))
