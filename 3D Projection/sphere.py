"""
Copyright 2022 Adhith Chand Thiruvath (Pseurae)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import pygame.draw
from matrix import Matrix, PROJECTION_MATRIX
import math

def get_points(r, mw, mh):
    rv = [ ] 

    for i in range(mh + 1):
        lt = (2.0 * math.pi / mh) * i

        for j in range(mw + 1):
            lg = (2.0 * math.pi / mw) * j

            sinlt = math.sin(lt)
            sinlg = math.sin(lg)

            coslt = math.cos(lt)
            coslg = math.cos(lg)

            x = r * sinlt * coslg
            y = r * sinlt * sinlg
            z = r * coslt

            rv.append((x, y, z))

    return rv

SPHERE_POINT_COLOR = (255, 255, 255)

class Sphere(object):
    def __init__(self, radius, map_width, map_height):
        self.radius = radius
        self.points = get_points(radius, map_width, map_height)
        self.rotate_x = 0.0
        self.rotate_y = 0.0
        self.rotate_z = 0.0

    @property
    def rotation_matrix(self):
        return Matrix.rotate(
            math.radians(self.rotate_x),
            math.radians(self.rotate_y),
            math.radians(self.rotate_z)
        )

    def draw(self, window, xpos, ypos):
        for (x, y, z) in self.points:
            x, y = self.rotation_matrix.transform2(x, y, z, 1)
            x += xpos
            y += ypos
            pygame.draw.circle(window, SPHERE_POINT_COLOR, (x, y), 3)
