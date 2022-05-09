# MIT License
#
# Copyright 2022 Adhith Chand Thiruvath (Pseurae)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
# associated documentation files (the "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the 
# following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial 
# portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO 
# EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE 
# USE OR OTHER DEALINGS IN THE SOFTWARE.

import math
from vector import vec3
from triangle import Triangle

GOLDEN_RATIO = (1.0 + math.sqrt(5.0)) / 2.0

i = 1.0 / GOLDEN_RATIO

isosahedron_vertices = [
    vec3(-i,  1.0, 0.0),
    vec3( i,  1.0, 0.0),
    vec3(-i, -1.0, 0.0),
    vec3( i, -1.0, 0.0),

    vec3(0.0, -i,  1.0),
    vec3(0.0,  i,  1.0),
    vec3(0.0, -i, -1.0),
    vec3(0.0,  i, -1.0),

    vec3( 1.0, 0.0, -i),
    vec3( 1.0, 0.0,  i),
    vec3(-1.0, 0.0, -i),
    vec3(-1.0, 0.0,  i)
]

def get_iso_triangle(i, j, k, *args, **kwargs):
    return Triangle(
        isosahedron_vertices[i],
        isosahedron_vertices[j],
        isosahedron_vertices[k],
        *args, **kwargs
    )

isosahedron_triangles = [
    get_iso_triangle(0, 11, 5),
    get_iso_triangle(0, 5, 1),
    get_iso_triangle(0, 1, 7),
    get_iso_triangle(0, 7, 10),
    get_iso_triangle(0, 10, 11),

    get_iso_triangle(1, 5, 9),
    get_iso_triangle(5, 11, 4),
    get_iso_triangle(11, 10, 2),
    get_iso_triangle(10, 7, 6),
    get_iso_triangle(7, 1, 8),

    get_iso_triangle(3, 9, 4),
    get_iso_triangle(3, 4, 2),
    get_iso_triangle(3, 2, 6),
    get_iso_triangle(3, 6, 8),
    get_iso_triangle(3, 8, 9),

    get_iso_triangle(4, 9, 5),
    get_iso_triangle(2, 4, 11),
    get_iso_triangle(6, 2, 10),
    get_iso_triangle(8, 6, 7),
    get_iso_triangle(9, 8, 1),
]

