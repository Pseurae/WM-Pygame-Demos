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

import pygame
import pygame.draw
import pygame.gfxdraw
import pygame.time
import pygame.display
import pygame.image
import time
import math

from matrix import Matrix

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

CLOCK = pygame.time.Clock()

from matrix import Matrix
from mesh import Mesh
from vector import vec3
import time
import math

def interact():
    pass

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Projection')
    
    is_running = True
    cube = Mesh.isosahedron(200)
    cube.position = vec3(200, 200, 0.0)
    start_time = time.time()
    rot = 0.0

    while is_running:
        CLOCK.tick(30)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False

        window.fill((0,0,0))

        cube.rotation = Matrix.rotate(math.radians(rot), math.radians(rot), 0)
        cube.draw(window)

        interact()

        pygame.display.update()
        rot += 2.0
        rot %= 360

    pygame.quit()

