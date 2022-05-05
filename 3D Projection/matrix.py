"""
Copyright 2022 Adhith Chand Thiruvath (Pseurae)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Strictly following RenPy's own implementation for Matrices
# so that there's no need to change field names on porting.
# Plus, RenPy's Matrices are in Cython.

from math import sin, cos, pi, radians

class Matrix(object):
    __slots__ = [
        "xdx", "ydx", "zdx", "wdx",
        "xdy", "ydy", "zdy", "wdy",
        "xdz", "ydz", "zdz", "wdz",
        "xdw", "ydw", "zdw", "wdw",
    ]

    def __init__(self, v=None):
        for i in self.__slots__:
            setattr(self, i, 0)

        if v is None: return 

        l = len(v)

        if l == 4:
            (self.xdx, self.xdy, 
             self.ydx, self.ydy) = v
            self.zdz = 1.0
            self.wdw = 1.0

        elif l == 9:
            (self.xdx, self.xdy, self.xdz,
             self.ydx, self.ydy, self.ydz,
             self.zdx, self.zdy, self.zdz) = v
            self.wdw = 1.0
        elif l == 16:
            (self.xdx, self.xdy, self.xdz, self.xdw,
             self.ydx, self.ydy, self.ydz, self.ydw,
             self.zdx, self.zdy, self.zdz, self.zdw,
             self.wdx, self.wdy, self.wdz, self.wdw) = v
        else:
            raise Exception("Must be a square matrix.")

    def __repr__(self):
        x = y = 0

        rv = "Matrix(["

        while 0 <= y < 4:
            x = 0
            if y:
                rv += "\n        "
            while 0 <= x < 4:
                rv += "{:10.7f}, ".format(self[x * 4 + y])
                x += 1
            y += 1

        return rv + "])"

    def __getitem__(self, i):
        return getattr(self, self.__slots__[i])

    def __setitem__(self, i, val):
        return setattr(self, self.__slots__[i], val)

    def __mul__(self, other):
        if isinstance(other, type(self)):
            return self.__mul_matrix__(other)

        raise TypeError("Cannot multiply a matrix and %r." % type(other))    

    def __mul_matrix__(self, other):
        rv = Matrix(None)

        rv.xdx = other.wdx*self.xdw + other.xdx*self.xdx + other.ydx*self.xdy + other.zdx*self.xdz
        rv.xdy = other.wdy*self.xdw + other.xdy*self.xdx + other.ydy*self.xdy + other.zdy*self.xdz
        rv.xdz = other.wdz*self.xdw + other.xdz*self.xdx + other.ydz*self.xdy + other.zdz*self.xdz
        rv.xdw = other.wdw*self.xdw + other.xdw*self.xdx + other.ydw*self.xdy + other.zdw*self.xdz

        rv.ydx = other.wdx*self.ydw + other.xdx*self.ydx + other.ydx*self.ydy + other.zdx*self.ydz
        rv.ydy = other.wdy*self.ydw + other.xdy*self.ydx + other.ydy*self.ydy + other.zdy*self.ydz
        rv.ydz = other.wdz*self.ydw + other.xdz*self.ydx + other.ydz*self.ydy + other.zdz*self.ydz
        rv.ydw = other.wdw*self.ydw + other.xdw*self.ydx + other.ydw*self.ydy + other.zdw*self.ydz

        rv.zdx = other.wdx*self.zdw + other.xdx*self.zdx + other.ydx*self.zdy + other.zdx*self.zdz
        rv.zdy = other.wdy*self.zdw + other.xdy*self.zdx + other.ydy*self.zdy + other.zdy*self.zdz
        rv.zdz = other.wdz*self.zdw + other.xdz*self.zdx + other.ydz*self.zdy + other.zdz*self.zdz
        rv.zdw = other.wdw*self.zdw + other.xdw*self.zdx + other.ydw*self.zdy + other.zdw*self.zdz

        rv.wdx = other.wdx*self.wdw + other.xdx*self.wdx + other.ydx*self.wdy + other.zdx*self.wdz
        rv.wdy = other.wdy*self.wdw + other.xdy*self.wdx + other.ydy*self.wdy + other.zdy*self.wdz
        rv.wdz = other.wdz*self.wdw + other.xdz*self.wdx + other.ydz*self.wdy + other.zdz*self.wdz
        rv.wdw = other.wdw*self.wdw + other.xdw*self.wdx + other.ydw*self.wdy + other.zdw*self.wdz

        return rv

    @classmethod
    def identity(cls):
        rv = cls(None)
        rv.xdx = 1.0
        rv.ydy = 1.0
        rv.zdz = 1.0
        rv.wdw = 1.0
        return rv

    @classmethod
    def offset(cls, x, y, z):
        rv = cls.identity(None)
        rv.xdw = x
        rv.ydw = y
        rv.zdw = z
        return rv

    @classmethod
    def rotate(cls, x, y, z):
        sinx = sin(x)
        cosx = cos(x)
        siny = sin(y)
        cosy = cos(y)
        sinz = sin(z)
        cosz = cos(z)

        rv = cls(None)

        rv.xdx = cosy * cosz
        rv.xdy = sinx * siny * cosz - cosx * sinz
        rv.xdz = cosx * siny * cosz + sinx * sinz

        rv.ydx = cosy * sinz
        rv.ydy = sinx * siny * sinz + cosx * cosz
        rv.ydz = cosx * siny * sinz - sinx * cosz

        rv.zdx = -siny
        rv.zdy = sinx * cosy
        rv.zdz = cosx * cosy

        rv.wdw = 1

        return rv

    @classmethod
    def screen_projection(cls):
        rv = cls(None)
        rv.xdx = 1
        rv.ydy = 1
        rv.zdz = 0
        rv.wdw = 1
        return rv

    def transform3(self, x, y, z, w):
        newx = x * self.xdx + y * self.xdy + z * self.xdz + w * self.xdw
        newy = x * self.ydx + y * self.ydy + z * self.ydz + w * self.ydw
        newz = x * self.zdx + y * self.zdy + z * self.zdz + w * self.zdw
        return (newx, newy, newz)

    def transform2(self, x, y, z, w):
        newx = x * self.xdx + y * self.xdy + z * self.xdz + w * self.xdw
        newy = x * self.ydx + y * self.ydy + z * self.ydz + w * self.ydw
        return (newx, newy)

IDENTITY_MATRIX = Matrix.identity()
PROJECTION_MATRIX = Matrix.screen_projection()

