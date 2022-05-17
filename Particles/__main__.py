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

import pygame_sdl2
import pygame_sdl2.draw
import pygame_sdl2.time
import pygame_sdl2.display
import pygame_sdl2.image
import time
import random
import math

background_colour = (0, 0, 0)
(width, height) = (400, 400)
drag = 0.999

target_fps = 60

clock = pygame_sdl2.time.Clock()

update_list = [ ]

start_time = last_time = time.time()

class ParticleEmitter(object):
    gravity = -0.5
    damping = 0.9

    def __init__(self):
        # x, y, dir_x, dir_y, zoom
        self.particles = [ ]

    def add(self, x, y):
        theta = random.random() * 2.0 * 3.14
        dir_x = math.cos(theta) * 6.0
        dir_y = math.sin(theta) * 4.0

        self.particles.append([ x, y, dir_x, dir_y, 1.0 ])

    def spawn_at(self, x, y, n):
        for _ in range(n):
            self.add(x, y)

    def update(self):
        self.particles = [ i for i in self.particles if i[4] > 0.0 ]

        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]

            p[3] += self.gravity

            p[2] *= self.damping
            p[3] *= self.damping

            p[4] -= 0.05

    def render(self, window):
        for i in self.particles:
            radius = 10 * i[4]
            pygame_sdl2.draw.circle(window, (255, 255, 255), (i[0], i[1]), radius)

class FanParticleEmitter(ParticleEmitter):
    def __init__(self, angle, fan_angle):
        super(FanParticleEmitter, self).__init__()
        self.angle = math.radians(angle)
        self.fan_angle = math.radians(fan_angle)

    def add(self, x, y):
        theta = random.uniform(self.angle - self.fan_angle / 2.0, self.angle + self.fan_angle / 2.0)
        dir_x = math.cos(theta) * 6.0
        dir_y = math.sin(theta) * 4.0

        self.particles.append([ x, y, dir_x, dir_y, 1.0 ])

class PlaneParticleEmitter(ParticleEmitter):
    def __init__(self, angle, length):
        super(PlaneParticleEmitter, self).__init__()
        self.angle = math.radians(angle)
        self.length = length

    def add(self, x, y):
        halflength = self.length / 2
        offset = halflength * random.random()

        xoff = offset * math.cos(math.pi / 2.0 + self.angle)
        yoff = offset * math.sin(math.pi / 2.0 + self.angle)

        dir_x = math.cos(self.angle) * 6.0
        dir_y = math.sin(self.angle) * 4.0

        sign = random.choice([ -1, 1 ])
        self.particles.append([ x + xoff * sign, y + yoff * sign, dir_x, dir_y, 1.0 ])

if __name__ == "__main__":
    pygame_sdl2.init()

    window = pygame_sdl2.display.set_mode((width, height), pygame_sdl2.HWSURFACE)

    is_running = True
    particles = ParticleEmitter()

    while is_running:
        update_list = [ ]

        dt = time.time() - last_time
        last_time = time.time()

        for ev in pygame_sdl2.event.get():
            if ev.type == pygame_sdl2.QUIT:
                is_running = False

            elif ev.type == pygame_sdl2.MOUSEBUTTONDOWN:
                particles.spawn_at(*pygame_sdl2.mouse.get_pos(), 10)

        window.fill(background_colour)

        particles.render(window)
        particles.update()
        pygame_sdl2.display.update()

        clock.tick(60.0)
        fps = clock.get_fps()
        pygame_sdl2.display.set_caption(f"FPS: {fps:.1f}")

    pygame_sdl2.quit()
