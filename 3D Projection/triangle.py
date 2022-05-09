# MIT License

# Copyright 2022 Adhith Chand Thiruvath (Pseurae)

# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation the rights to use, copy, 
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to 
# the following conditions:

# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pygame.draw
from matrix import Matrix
from vector import vec3
from color import Color

class Triangle(object):
    def __init__(self, v1, v2, v3):
        self.v1 = vec3(v1)
        self.v2 = vec3(v2)
        self.v3 = vec3(v3)

    def __repr__(self):
        return "<Triangle {} {} {}>".format(*self.get_vertices())

    def __mul_homogenous__(self, m):
        *v1, w1 = m.transform4(*self.v1, 0)
        *v2, w2 = m.transform4(*self.v2, 0)
        *v3, w3 = m.transform4(*self.v3, 0)

        if w1 != 0: v1 = vec3(v1) / w1
        if w2 != 0: v2 = vec3(v2) / w2
        if w2 != 0: v3 = vec3(v3) / w3

        return Triangle(v1, v2, v3)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.__mul_homogenous__(other)

        elif isinstance(other, (float, int)):
            v1 = self.v1 * other
            v2 = self.v2 * other
            v3 = self.v3 * other

            return Triangle(v1, v2, v3)

        raise NotImplementedError("__mul__ for implemented for %r." % type(other))

    def __add__(self, other):
        if isinstance(other, (float, int, vec3)):
            v1 = self.v1 + other
            v2 = self.v2 + other
            v3 = self.v3 + other

            return Triangle(v1, v2, v3)

        raise NotImplementedError("__add__ for implemented for %r." % type(other))

    def draw(self, screen, color, outline_color):
        color = Color(color)
        outline_color = Color(outline_color)

        v1, v2, v3 = self.get_vertices()

        pygame.draw.polygon(screen, color, (
            v1[:2], v2[:2], v3[:2]
        ))

        pygame.draw.line(screen, outline_color, v1[:2], v2[:2], 2)
        pygame.draw.line(screen, outline_color, v2[:2], v3[:2], 2)
        pygame.draw.line(screen, outline_color, v3[:2], v1[:2], 2)

    def get_vertices(self):
        return (self.v1, self.v2, self.v3) 
