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
import pygame.time
import pygame.display
import pygame.image
import time
from random import randrange
from itertools import product

background_colour = (0, 0, 0)
width, height = 400, 400

class Node(object):
    def __init__(self, size, pos, color):
        self.size = size
        self.pos = pos
        self.color = color

    def __repr__(self):
        return f"<Node Position: {self.pos} Color: {self.color}>"

    def draw(self, window):
        x, y = self.pos[0] - self.size / 2, self.pos[1] - self.size / 2
        rect = pygame.Rect(x, y, self.size, self.size)
        pygame.draw.rect(window, background_colour, rect)
        pygame.draw.rect(window, self.color, rect, 1)

    def connect(self, window, other):
        pygame.draw.line(window, self.color, self.pos, other.pos, 1)

def lazy_flatten(l):
    for i in l:
        if type(i) is type(l):
            yield from lazy_flatten(i)
        else:
            yield i

class NodeNetwork(object):
    node_size = 40.0
    node_spacing = 20.0

    def __init__(self, input_node_num=3, proc_node_grid=(3, 3), output_node_num=1, 
            draw_all_lines=False, input_node_color=(255, 255, 255), 
            proc_node_color=(255, 255, 255), output_node_color=(255, 255, 255)):

        self.input_node_num = input_node_num
        self.draw_all_lines = draw_all_lines

        self.connection_lines = None

        if isinstance(proc_node_grid, (int, float)):
            self.proc_node_grid = (proc_node_grid,)
        else:
            self.proc_node_grid = proc_node_grid

        self.proc_node_num = len(self.proc_node_grid)

        self.output_node_num = output_node_num

        self.width, self.height = self.calculate_dimens()

        self.input_nodes = self.create_node_list(0, self.input_node_num, input_node_color)
        self.proc_nodes = [ 
            self.create_node_list(i + 1, self.proc_node_grid[i], proc_node_color) 
            for i in range(self.proc_node_num) ] # Nested list

        self.output_nodes = self.create_node_list(
            self.proc_node_num + 1, self.output_node_num, output_node_color)

    def calculate_dimens(self):
        max_rows = max(self.input_node_num, 
            max(self.proc_node_grid), 
            self.output_node_num)

        columns = 2 + self.proc_node_num

        height = self.get_required_space(max_rows)
        width = self.get_required_space(columns)
        return width, height

    def get_required_space(self, s):
        return s * (self.node_size + self.node_spacing)

    def create_node_list(self, x, n, color=(255, 255, 255)):
        rv = [ ]

        padding = self.height - self.get_required_space(n)
        x = self.get_required_space(x) + self.node_size / 2

        for i in range(n):
            y = self.get_required_space(i) + (self.node_size + padding) / 2
            rv.append(Node(self.node_size, (x, y), color))

        return rv

    def render_surf(self):
        rv = pygame.Surface((self.width, self.height))

        nodes = [ self.input_nodes, *self.proc_nodes, self.output_nodes ]          

        if self.draw_all_lines:
            for i in range(len(nodes) - 1):
                for n1, n2 in product(nodes[i], nodes[i + 1]):
                    n1.connect(rv, n2)

        elif self.connection_lines is not None:
            for line in self.connection_lines:
                if len(line) != len(nodes):
                    continue

                for i in range(len(line) - 1):
                    l1, l2 = line[i], line[i + 1]
                    nodes[i][l1].connect(rv, nodes[i + 1][l2])

        for i in lazy_flatten(nodes):
            i.draw(rv)

        return rv

start_time = time.time()
update_delay = 0.1

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((width, height), pygame.HWSURFACE)

    is_running = True

    node_network = NodeNetwork(3, 4, 2)
    update_time = 0.0

    while is_running:
        st = time.time() - start_time

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False

        window.fill(background_colour) 

        if update_time < st:
            node_network.connection_lines = [
                [ randrange(0, i) for i in (3, 4, 2) ],
                [ randrange(0, i) for i in (3, 4, 2) ],
            ]

            update_time = st + update_delay

        window.blit(node_network.render_surf(), (0, 0))

        pygame.display.update()

    pygame.quit()

