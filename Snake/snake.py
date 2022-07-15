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

# May have bugs. Not gonna fix them as, lore-wise, Jez creates this.
# Also was hastily coded during a power outage and with less than 10%
# of battery backup. Not gonna fix that either.

from random import randrange
import colorsys
import pygame
import pygame.draw
import pygame.time
import pygame.display
import math

game_over_tail_bite = True
game_over_out_of_bounds = True

FOREGROUND = 0
RANDOM = 1
GRADIENT = 2

snake_color_option = FOREGROUND
fruit_color_option = RANDOM

foreground_color = (0, 0, 0)
grid_outline_color = (200, 200, 200)
background_colour = (255, 255, 255)

grid_line_width = 1
grid_size = 20
xcells = 20
ycells = 20

width = xcells * grid_size + (xcells - 1) * grid_line_width
height = ycells * grid_size + (ycells - 1) * grid_line_width

target_fps = 15

def generate_gradients():
    rv = [ ]

    for y in range(ycells):
        rrv = [ ]

        for x in range(xcells):
            theta = math.radians(-45.0)
            norm_x = x / (xcells - 1.0)
            norm_y = y / (ycells - 1.0)

            hue = norm_x * math.cos(theta) - norm_y * math.sin(theta)
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

            rrv.append((
                int(r * 255),
                int(g * 255),
                int(b * 255)
            ))

        rv.append(rrv)

    return rv

gradient_colors = generate_gradients()

class Block(object):
    def __init__(self, x, y, padding, color):
        self.x = x
        self.y = y
        self.padding = padding
        self.color = color

    def __repr__(self):
        return "<Block x: {self.x} y: {self.y}>".format(self=self)

    def place(self, renderer):
        return renderer.cell(self.x, self.y, self.color, self.padding)

class Renderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))

    def __getattr__(self, name):
        if hasattr(self.window, name):
            return getattr(self.window, name)
        else:
            super(Renderer, self).__getattr__(name)

    def grid(self, color):
        for i in range(1, xcells):
            x = i * grid_size + (i - 1) * grid_line_width
            pygame.draw.line(self.window, color, (x, 0), (x, self.height), grid_line_width)

        for i in range(1, ycells):
            y = i * grid_size + (i - 1) * grid_line_width
            pygame.draw.line(self.window, color, (0, y), (self.width, y), grid_line_width)

    def cell(self, x, y, color=foreground_color, padding=(0, 0)):
        if isinstance(padding, (float, int)):
            xpadding = ypadding = padding
        else:
            xpadding, ypadding = padding

        x0 = x * (grid_size + grid_line_width)
        y0 = y * (grid_size + grid_line_width)

        rect = pygame.Rect(x0 + xpadding, y0 + xpadding, grid_size - 2 * xpadding, grid_size - 2 * ypadding)
        return pygame.draw.rect(self.window, color, rect)

def random_color():
    return (randrange(256), randrange(256), randrange(256))

def dep_color(option, x, y):
    if option == FOREGROUND:
        return foreground_color
    elif option == GRADIENT:
        return gradient_colors[y][x]
    elif option == RANDOM:
        return random_color()

    return option

def snake_color(x, y):
    return dep_color(snake_color_option, x, y)

def fruit_color(x, y):
    return dep_color(fruit_color_option, x, y)

def default_snake_body():
    xcenter = xcells // 2
    ycenter = ycells // 2

    rv = [ ]

    for i in range(4):
        y = ycenter + i
        rv.append(Block(
            xcenter,
            y,
            0,
            snake_color(xcenter, y)
        ))

    return rv

def create_fruit():
    x = randrange(1, xcells - 1)
    y = randrange(1, ycells - 1)
    return Block(x, y, 5, fruit_color(x, y))

snake_body = default_snake_body()

class Direction(object):
    Up = (0, -1)
    Down = (0, 1)
    Left = (-1, 0)
    Right = (1, 0)

direction_keys = {
    pygame.K_UP: Direction.Up,
    pygame.K_DOWN: Direction.Down,
    pygame.K_LEFT: Direction.Left,
    pygame.K_RIGHT: Direction.Right,
}

opposites = {
   Direction.Up: Direction.Down,
   Direction.Down: Direction.Up,
   Direction.Left: Direction.Right,
   Direction.Right: Direction.Left
}

if __name__ == "__main__":
    pygame.init()

    renderer = Renderer(width, height)
    clock = pygame.time.Clock()
    start_time = None

    pygame.display.set_caption('Snek')

    is_running = True

    current_direction = Direction.Up
    current_position = [ snake_body[0].x, snake_body[0].y ]

    fruit = create_fruit()

    while is_running:
        direction_change_to = current_direction

        dt = clock.tick(target_fps) * 0.001 * target_fps

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False

            elif ev.type == pygame.KEYDOWN:
                direction_change_to = direction_keys.get(ev.key, direction_change_to)

        if opposites[current_direction]!= direction_change_to:
            current_direction = direction_change_to

        current_position[0] += current_direction[0]
        current_position[1] += current_direction[1]

        if not game_over_out_of_bounds:
            current_position[0] %= xcells
            current_position[1] %= ycells

        x, y = current_position[0], current_position[1]
        new_block = Block(x, y, 0, snake_color(x, y))
        snake_body.insert(0, new_block)

        if x == fruit.x and y == fruit.y:
            fruit = create_fruit()
        else:
            snake_body.pop()

        if game_over_tail_bite:
            for b in snake_body[1:]:
                if x == b.x and y == b.y:
                    is_running = False

        if game_over_out_of_bounds:
            is_out_of_bounds = any([
                x < 0, x > xcells - 1,
                y < 0, y > ycells - 1
            ])

            if is_out_of_bounds:
                is_running = False

        # Render step.
        renderer.fill(background_colour)
        renderer.grid(grid_outline_color)

        fruit.place(renderer)
        for b in snake_body:
            b.place(renderer)

        pygame.display.flip()

    pygame.quit()
