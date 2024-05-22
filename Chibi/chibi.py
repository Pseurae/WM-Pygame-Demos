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

# A Chibi widget that can be punted across the screen and
# interacts on click.

import pygame
import pygame.draw
import pygame.time
import pygame.display
import pygame.image
import random
import time
import sys

background_colour = (255, 255, 255)
(width, height) = (1920, 1080)
drag = 0.999
elasticity = 0.55
gravity = (0.0, 0.2)

target_fps = 60

def sign(x): return -1 if x < 0 else 1

idle_image = pygame.image.load("m_sticker_1.png")
idle_image_flipped = pygame.transform.flip(idle_image, True, False)

hover_image = pygame.image.load("m_sticker_2.png")
hover_image_flipped = pygame.transform.flip(hover_image, True, False)

class Chibi(object):
    def random_jump_delay(self):
        return random.random() * 4 + 4

    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.mass_inv = 1.0 / mass

        self.speed_x = 0
        self.speed_y = 0

        self.width = max(idle_image.get_width(), hover_image.get_width())
        self.height = max(idle_image.get_height(), hover_image.get_height())

        self.jump_delay = None
        self.flipped = False # True: Left, False: Right
        self.jump_move = 0

    def interact(self, st):
        if self.jump_delay is None :
            self.jump_delay = st + self.random_jump_delay()

        if self.jump_delay < st:
            if not self.hovered() and self.grounded:
                if self.jump_move > 0:
                    self.jump_move = random.randint(-5, 0)
                elif self.jump_move < 0:
                    self.jump_move = random.randint(0, 5)
                else:
                    self.jump_move = random.randint(-1, 1)

                self.flipped = True if self.jump_move > 0 else False
                self.jump_move = min(max(self.jump_move, -1), 1)

                self.speed_x = 1.0 * self.jump_move
                self.speed_y = -3.0

            self.jump_delay = st + self.random_jump_delay()

    def hovered(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return all([
            mouse_x > self.x,
            mouse_x < self.x + self.width,
            mouse_y > self.y,
            mouse_y < self.y + self.height
        ])

    @property
    def idle_image(self):
        if self.flipped:
            return idle_image_flipped

        return idle_image

    @property
    def hover_image(self):
        if self.flipped:
            return hover_image_flipped

        return hover_image

    @property
    def image(self):
        if self.hovered():
            return self.hover_image

        return self.idle_image

    @property
    def grounded(self):
        return self.y + self.height >= height

    def render_step(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))

    def physics_step(self, gravity, drag, dt):
        def modulate_position(x, y):
            self.x += x * dt
            self.y += y * dt

        def modulate_velocity(x, y):
            self.speed_x += x * dt
            self.speed_y += y * dt

        modulate_velocity(*gravity)
        modulate_position(self.speed_x, self.speed_y)

        self.speed_x *= drag
        self.speed_y *= drag

    def bounce_step(self, restitution):
        def restitute_speed(xsign, ysign):
            self.speed_x = xsign * sign(self.speed_x) * abs(self.speed_x) * restitution
            self.speed_y = ysign * sign(self.speed_y) * abs(self.speed_y) * restitution

        if self.x > width - self.width:
            self.x = width - self.width
            restitute_speed(-1, 1)

        elif self.x < 0:
            self.x = 0
            restitute_speed(-1, 1)

        if self.y > height - self.height:
            self.y = height - self.height
            restitute_speed(1, -1)

        elif self.y < 0:
            self.y = 0
            restitute_speed(1, -1)

g_chibi = Chibi(200, 200, 3.0)
g_chibi.speed_x = 2.0 * (random.random() * 2.0 - 1.0)
g_chibi.speed_y = 2.0 * (random.random() * 2.0 - 1.0)


if __name__ == "__main__":
    pygame.init()

    proggy = pygame.font.Font('ProggyVector Regular.ttf', 12)

    window = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    start_time = None

    pygame.display.set_caption('Chibi Physics')

    is_running = True
    selected_chibi = False
    hold_x = hold_y = 0
    hold_timer = 0

    while is_running:
        dt = clock.tick(target_fps) * 0.001 * target_fps
        (mouse_x, mouse_y) = pygame.mouse.get_pos()

        if start_time is None:
            start_time = time.time()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False

            elif ev.type == pygame.MOUSEBUTTONDOWN:
                selected_chibi = g_chibi.hovered()
                if selected_chibi:
                    (hold_x, hold_y) = (mouse_x - g_chibi.x, mouse_y - g_chibi.y)
                    if g_chibi.grounded: g_chibi.speed_y = -3

            elif ev.type == pygame.MOUSEBUTTONUP:
                selected_chibi = False

        if selected_chibi:
            old_x, old_y = g_chibi.x, g_chibi.y
            g_chibi.x, g_chibi.y = min(max(mouse_x - hold_x, 0), width - g_chibi.width), min(max(mouse_y - hold_y, 0), height - g_chibi.height)

            if old_x != g_chibi.x or old_y != g_chibi.y:
                g_chibi.speed_x, g_chibi.speed_y = (g_chibi.x - old_x) * 0.5, (g_chibi.y - old_y) * 0.5

        window.fill(background_colour)

        position_string = "Bounding Box: {:.02f}, {:.02f}, {:.02f}, {:.02f}".format(g_chibi.x, g_chibi.y, g_chibi.x + g_chibi.width, g_chibi.y + g_chibi.height)
        velocity_string = "Velocity: {:.02f}, {:.02f}".format(g_chibi.speed_x, g_chibi.speed_y)
        delta_t_string = "Delta Time: {:.02f}".format(dt)

        def text_render(screen, *arg):
            y = 0

            for t in arg:
                text_surf = proggy.render(t, False, (0, 0, 0), None)
                screen.blit(text_surf, (0, y))
                y += text_surf.get_height()

        text_render(window, position_string, velocity_string, delta_t_string)

        if not selected_chibi:
            g_chibi.physics_step(gravity, drag, min(dt, 1.0))
            g_chibi.bounce_step(elasticity)
            g_chibi.interact(time.time() - start_time)

        g_chibi.render_step(window)
        pygame.display.flip()

    pygame.quit()
