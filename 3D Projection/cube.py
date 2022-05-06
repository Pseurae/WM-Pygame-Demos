"""
Copyright 2022 Adhith Chand Thiruvath (Pseurae)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import pygame.draw
from shape import Shape
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

class Cube(Shape):
    def __init__(self, size):
        super(Cube, self).__init__(CUBE_VERTICES, 0, 0, 0)
        self.size = size

    def draw(self, window, xpos, ypos):
        points = [ ]

        def draw_lines(i, j):
            pygame.draw.line(
                window, 
                CUBE_LINE_COLOR, 
                points[i], 
                points[j]
            )

        for (x, y, z) in self.iterate_points():
            x = xpos + x * self.size
            y = ypos + y * self.size
            points.append((x, y))

        for i in range(4):
            draw_lines(i, (i + 1) % 4)
            draw_lines(i + 4, (i + 1) % 4 + 4)
            draw_lines(i, i + 4)

        for (x, y) in points:
            pygame.draw.circle(window, CUBE_POINT_COLOR, (x, y), 2)

