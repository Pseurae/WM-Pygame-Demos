"""
Copyright 2022 Adhith Chand Thiruvath (Pseurae)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from matrix import Matrix, PROJECTION_MATRIX
import math

class Shape(object):
    def __init__(self, points, rot_x, rot_y, rot_z):
        self.points = points
        self.rot_x = rot_x
        self.rot_y = rot_y
        self.rot_z = rot_z

    def rotation_matrix(self):
        return Matrix.rotate(
            math.radians(self.rot_x),
            math.radians(self.rot_y),
            math.radians(self.rot_z)
        )

    def iterate_points(self):
        rot_matrix = self.rotation_matrix()

        for (x, y, z) in self.points:
            x, y, z = rot_matrix.transform3(x, y, z, 1)
            x, y, z = PROJECTION_MATRIX.transform3(x, y, z, 1)
            yield (x, y, z)
