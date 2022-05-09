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

from color import Color
from triangle import Triangle
from isosahedron import isosahedron_triangles
from matrix import Matrix, PERSPECTIVE_MATRIX, IDENTITY_MATRIX
from vector import vec3, cross_product
import pygame.draw

CUBE_TRIANGLE_VERTICES = (
    # Front
    (vec3( 1.0,  1.0, -1.0), vec3(-1.0,  1.0, -1.0), vec3(-1.0, -1.0, -1.0)),
    (vec3(-1.0, -1.0, -1.0), vec3( 1.0, -1.0, -1.0), vec3( 1.0,  1.0, -1.0)),

    # Back
    (vec3(-1.0,  1.0,  1.0), vec3( 1.0,  1.0,  1.0), vec3( 1.0, -1.0,  1.0)),
    (vec3( 1.0, -1.0,  1.0), vec3(-1.0, -1.0,  1.0), vec3(-1.0,  1.0,  1.0)),

    # Left
    (vec3(-1.0,  1.0, -1.0), vec3(-1.0,  1.0,  1.0), vec3(-1.0, -1.0,  1.0)),
    (vec3(-1.0, -1.0,  1.0), vec3(-1.0, -1.0, -1.0), vec3(-1.0,  1.0, -1.0)),

    # Right
    (vec3( 1.0,  1.0,  1.0), vec3( 1.0,  1.0, -1.0), vec3( 1.0, -1.0, -1.0)),
    (vec3( 1.0, -1.0, -1.0), vec3( 1.0, -1.0,  1.0), vec3( 1.0,  1.0,  1.0)),

    # Top
    (vec3( 1.0,  1.0,  1.0), vec3(-1.0,  1.0,  1.0), vec3(-1.0,  1.0, -1.0)),
    (vec3(-1.0,  1.0, -1.0), vec3( 1.0,  1.0, -1.0), vec3( 1.0,  1.0,  1.0)),

    # Bottom
    (vec3(-1.0, -1.0,  1.0), vec3( 1.0, -1.0,  1.0), vec3( 1.0, -1.0, -1.0)),
    (vec3( 1.0, -1.0, -1.0), vec3(-1.0, -1.0, -1.0), vec3(-1.0, -1.0,  1.0))
)

cube_triangles = [ Triangle(*vert) for vert in CUBE_TRIANGLE_VERTICES ]

class Mesh(object):
    def __init__(self, color="#fff", outline_color="#666"):
        self.triangles = [ ]

        self.color = Color(color)
        self.outline_color = Color(outline_color)

        self.position = vec3(0.0)
        self.scale = Matrix.scale(1.0, 1.0, 1.0)
        self.rotation = Matrix.rotate(0.0, 0.0, 0.0)

    @classmethod
    def cube(cls, side, *args, **kwargs):
        rv = cls(*args, **kwargs)
        halfside = side / 2
        rv.scale = Matrix.scale(halfside, halfside, halfside)
        rv.triangles = cube_triangles.copy()
        return rv

    @classmethod
    def isosahedron(cls, radius, *args, **kwargs):
        rv = cls(*args, **kwargs)
        halfradius = radius / 2
        rv.scale = Matrix.scale(halfradius, halfradius, halfradius)
        rv.triangles = isosahedron_triangles.copy()
        return rv

    def draw(self, screen, lights=None):
        tris_to_be_drawn = [ ]

        for tri in self.triangles:
            # Apply static rotation.
            new_tri = tri * self.rotation

            # Push back the mesh and apply the perspective matrix.
            new_tri += vec3(0.0, 0.0, -10.0)
            new_tri *= PERSPECTIVE_MATRIX

            # Scale it to size and position it.
            new_tri *= self.scale
            new_tri += self.position

            # Find the normal vector.
            line1 = new_tri.v2 - new_tri.v1
            line2 = new_tri.v3 - new_tri.v1

            normal = cross_product(line1, line2).normalize()

            # If facing camera, append to draw buffer.
            if normal[2] < 0.0:
                tris_to_be_drawn.append(new_tri)

        def zsort(x):
            return max((x.v1[2], x.v2[2], x.v1[2]))

        tris_to_be_drawn.sort(key=zsort)

        for tri in tris_to_be_drawn:
            tri.draw(screen, self.color, self.outline_color)
