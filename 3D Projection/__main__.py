"""
Copyright 2022 Adhith Chand Thiruvath (Pseurae)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import pygame
import pygame.draw
import pygame.gfxdraw
import pygame.time
import pygame.display
import pygame.image
import time
import math

from matrix import Matrix
from cube import Cube
from sphere import Sphere

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

CLOCK = pygame.time.Clock()

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Projection')
    
    is_running = True
    cube = Cube(100)
    cube.rotate_x = 45.0
    cube.rotate_y = 45.0
    cube.rotate_z = 45.0

    sphere = Sphere(100, 30, 30)
    sphere.rotate_x = 90.0

    while is_running:
        CLOCK.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False

        window.fill((0,0,0))

        sphere.draw(window, 200, 200)
        pygame.display.update()

        sphere.rotate_x += 0.5
        # cube.rotate_x += 0.5
        # cube.rotate_y += 0.25

    pygame.quit()

