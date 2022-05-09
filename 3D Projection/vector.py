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

import math

class Vector(tuple):

    VEC_LENGTH = 4

    def __repr__(self):
        return "<Vector Length: %s %s>" % (self.VEC_LENGTH, tuple.__repr__(self))

    def __new__(cls, *args):
        l = len(args)

        if l == cls.VEC_LENGTH:
            t = args

        elif l == 1:
            arg = args[0]
            if isinstance(arg, (float, int)):
                t = (arg,) * cls.VEC_LENGTH
            else:
                t = arg

        else:
            raise ValueError(
                "%r cannot have more than %s components." % (cls.__name__, self.VEC_LENGTH)
            )

        return tuple.__new__(cls, tuple(t))

    def __add__(self, other):
        if isinstance(other, (int, float)):
            t = tuple(i + other for i in self)
            return type(self)(*t)

        elif isinstance(other, Vector):
            if self.VEC_LENGTH == other.VEC_LENGTH:
                t = tuple(i + j for i, j in zip(self, other))
                return type(self)(*t)

            else:
                raise Exception("Different vector lengths.")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            t = tuple(i * other for i in self)
            return type(self)(*t)

        elif isinstance(other, Vector):
            if self.VEC_LENGTH == other.VEC_LENGTH:
                t = tuple(i * j for i, j in zip(self, other))
                return type(self)(*t)
            else:
                raise Exception("Different vector lengths.")

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            t = tuple(self[i] - other for i in range(self.VEC_LENGTH))
            return type(self)(*t)

        elif isinstance(other, Vector):
            if self.VEC_LENGTH == other.VEC_LENGTH:
                t = tuple(i - j for i, j in zip(self, other))
                return type(self)(*t)
            else:
                raise Exception("Different vector lengths.")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            t = tuple(self[i] / other for i in range(self.VEC_LENGTH))
            return type(self)(*t)

        elif isinstance(other, Vector):
            if self.VEC_LENGTH == other.VEC_LENGTH:
                t = tuple(i / j for i, j in zip(self, other))
                return type(self)(*t)
            else:
                raise Exception("Different vector lengths.")

    def dot(self, other):
        if isinstance(other, Vector) and other.VEC_LENGTH == self.VEC_LENGTH:
            d = (sum(a * b for a, b in zip(self, other)))
            return d
        else:
            raise TypeError("%r cannot be dot producted with a Vector." % type(other))

    def length(self):
        return math.sqrt(sum(i ** 2 for i in self))

    def normalize(self):
        mag = self.length()

        if mag == 0:
            return type(self)(0.0)
        
        return self / mag

class vec3(Vector):
    VEC_LENGTH = 3

class vec2(Vector):
    VEC_LENGTH = 2

def cross_product(a, b):
    if not isinstance(a, vec3) or not isinstance(b, vec3):
        raise Exception()

    return vec3(
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    )