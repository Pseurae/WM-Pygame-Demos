"""
Copyright 2022 Adhith Chand Thiruvath (Pseurae)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import pygame.draw
from matrix import Matrix, PROJECTION_MATRIX
import math

CUBE_VERTICES = (
    (-1, -1,  1),
    ( 1, -1,  1),
    ( 1,  1,  1),
    (-1,  1,  1),
    (-1, -1, -1),
    ( 1, -1, -1),
    ( 1,  1, -1),
    (-1,  1, -1)
)

CUBE_POINT_COLOR = (255, 255, 255)
CUBE_LINE_COLOR = (220, 220, 220)

class Cube(object):
    def __init__(self, size):
        self.size = size
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
        points = [ ]

        def draw_lines(i, j):
            pygame.draw.line(
                window, 
                CUBE_LINE_COLOR, 
                points[i], 
                points[j]
            )

        for (x, y, z) in CUBE_VERTICES:
            x, y, z = self.rotation_matrix.transform3(x, y, z, 1)
            x, y = PROJECTION_MATRIX.transform2(x, y, z, 1)

            x = xpos + x * self.size
            y = ypos + y * self.size
            points.append((x, y))

        draw_lines(0, 1)
        draw_lines(0, 3)
        draw_lines(0, 4)
        draw_lines(1, 2)
        draw_lines(1, 5)
        draw_lines(2, 6)
        draw_lines(2, 3)
        draw_lines(3, 7)
        draw_lines(4, 5)
        draw_lines(4, 7)
        draw_lines(6, 5)
        draw_lines(6, 7)

        for (x, y) in points:
            pygame.draw.circle(window, CUBE_POINT_COLOR, (x, y), 2)

