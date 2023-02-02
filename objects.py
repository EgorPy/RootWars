import pygame.draw
from functions import *
import random


class Label:
    def __init__(self, game, text, pos=[0, 0], font_name="Gill Sans", font_size=100, bold=False, italic=False, smooth=True, foreground=(40, 40, 40), background=None):
        self.game = game

        self.pos = pos
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.bold = bold
        self.italic = italic
        self.smooth = smooth
        self.foreground = foreground
        self.background = background

        self.font = pygame.font.SysFont(font_name, font_size, bold, italic)
        self.surface = self.font.render(text, smooth, foreground, background)

        self.size = self.surface.get_size()

    def update(self):
        self.game.app.DISPLAY.blit(self.surface, self.pos)

    def update_text(self, text, smooth=None, foreground=None, background=None):
        self.text = str(text)
        if smooth:
            self.smooth = smooth
        if foreground:
            self.foreground = foreground
        if background:
            self.background = background
        self.surface = self.font.render(self.text, self.smooth, self.foreground, self.background)

    def center_x(self, y=0):
        self.pos = [(self.game.app.WIDTH - self.size[0]) / 2, y]
        return self

    def center_y(self, x=0):
        self.pos = [x, (self.game.app.HEIGHT - self.size[1]) / 2]
        return self

    def center(self):
        self.pos = [(self.game.app.WIDTH - self.size[0]) / 2,
                    (self.game.app.HEIGHT - self.size[1]) / 2]
        return self

    def percent_x(self, percent=0, y=None):
        one_percent = self.game.app.WIDTH / 100
        if y is None:
            self.pos = [percent * one_percent, (self.game.app.HEIGHT - self.size[1]) / 2]
        else:
            self.pos = [percent * one_percent, y]
        return self

    def percent_y(self, percent=0, x=None):
        one_percent = self.game.app.HEIGHT / 100
        if x is None:
            self.pos = [(self.game.app.WIDTH - self.size[0]) / 2, percent * one_percent]
        else:
            self.pos = [x, percent * one_percent]
        return self

    def percent(self, percent_x=0, percent_y=0):
        one_percent_x = self.game.app.WIDTH / 100
        one_percent_y = self.game.app.HEIGHT / 100
        self.pos = [percent_x * one_percent_x, percent_y * one_percent_y]
        return self


class Button(Label):
    def __init__(self, game, text, pos=[0, 0], font_name="Gill Sans", font_size=60, bold=False, italic=False, smooth=True, foreground=(40, 40, 40), background=None):
        super().__init__(game, text, pos, font_name, font_size, bold, italic, smooth, foreground, background)

        self.counter = 0
        self.counter_max = 50

    def clicked(self, mouse_buttons, mouse_position):
        x1 = mouse_position[0]
        x2 = self.pos[0]
        w2 = self.size[0]
        y1 = mouse_position[1]
        y2 = self.pos[1]
        h2 = self.size[1]
        if self.counter > 0:
            self.counter -= 1
        if mouse_buttons[0] and touched(x1, 1, x2, w2, y1, 1, y2, h2) and self.counter <= 0:
            self.counter = self.counter_max
            return True
        else:
            return False


class Text(Label):
    def __init__(self, game, text, pos=[0, 0], font_name="Gill Sans", font_size=60, bold=False, italic=False, smooth=True, foreground=(40, 40, 40), background=None, line_height=None):
        super().__init__(game, text, pos, font_name, font_size, bold, italic, smooth, foreground, background)
        # this widget allows you to insert multiple lines text like this: text = "sentence1\sentence2\sentence3"

        if line_height is None:
            self.line_height = font_size
        else:
            self.line_height = line_height

        self.text_list = self.text.split("\n")
        self.lines = len(self.text_list)
        self.surface_list = [self.font.render(i, self.smooth, self.foreground, self.background) for i in self.text_list]
        self.pos_list = [[self.pos[0], self.pos[1] + i * self.line_height] for i in range(len(self.text_list))]
        self.size_list = [self.surface_list[i].get_size() for i in range(self.lines)]

        self.size = [max([self.surface_list[i].get_size()[0] for i in range(self.lines)]), self.lines * self.line_height]

    def percent_y(self, percent=0, x=None):
        one_percent = self.game.app.HEIGHT / 100
        if x is None:
            self.pos_list = [[(self.game.app.WIDTH - self.size_list[i][0]) / 2, percent * one_percent + i * self.line_height] for i in range(self.lines)]
        else:
            self.pos_list = [[x, percent * one_percent + i * self.line_height] for i in range(self.lines)]
        return self

    def update(self):
        [self.game.app.DISPLAY.blit(self.surface_list[i], self.pos_list[i]) for i in range(self.lines)]


class Hexagon:
    surface_size = [300, 300]
    height_scale = 2

    def __init__(self, game, pos=[0, 0], color=(255, 255, 255), outline_color=(10, 10, 10), width=5, hexagon_size=[100, 100], hex_pos=[], energy=0):
        self.game = game

        self.pos = pos
        self.hex_pos = hex_pos
        self.color = color
        self.outline_color = outline_color
        self.width = width
        self.hexagon_size = [hexagon_size[0] // 2, hexagon_size[1] // 2]

        # game variables
        self.energy = energy

        self.draw_hexagon()

    def draw_hexagon(self):
        self.surface = pygame.Surface(self.surface_size)
        self.surface.set_colorkey((0, 0, 0))

        # self.surface.fill((0, 0, 0))
        # self.surface.fill((255, 255, 255))
        self.pos_list = [[0, math.cos(deg_to_rad(60)) * self.hexagon_size[1] * 2.9 + self.width]]
        for i in range(1, 7):
            p = [
                self.pos_list[i - 1][0] + round(math.sin(deg_to_rad(i * 60)) * self.hexagon_size[0]),
                self.pos_list[i - 1][1] + round(math.cos(deg_to_rad(i * 60)) * self.hexagon_size[1])
            ]
            self.pos_list.append(p)
        for i in self.pos_list:
            i[0] = self.surface_size[0] - i[0] - self.width
            i[1] = self.surface_size[1] - i[1]
        if self.energy > 0:
            pygame.draw.lines(self.surface, self.outline_color, False, self.pos_list, self.width)
            for i in range(self.energy):
                energy_pos_list = []
                for j in self.pos_list:
                    energy_pos_list.append([j[0] - i * self.height_scale, j[1] - i * self.height_scale])
                # if i % height_scale == 0:
                color = [self.color[0] - i * 15 if self.color[0] != 0 else self.color[0],
                         self.color[1] - i * 15 if self.color[1] != 0 else self.color[1],
                         self.color[2] - i * 15 if self.color[2] != 0 else self.color[2]]
                color[0] = 0 if color[0] < 0 else color[0]
                color[1] = 0 if color[1] < 0 else color[1]
                color[2] = 0 if color[2] < 0 else color[2]
                color[0] = 255 if color[0] > 255 else color[0]
                color[1] = 255 if color[1] > 255 else color[1]
                color[2] = 255 if color[2] > 255 else color[2]
                # print(color)
                pygame.draw.polygon(self.surface, color, energy_pos_list)
        else:
            pygame.draw.polygon(self.surface, self.color, self.pos_list)
            pygame.draw.lines(self.surface, self.outline_color, False, self.pos_list, self.width)

    def update(self, mouse_buttons, mouse_position, events, keys):
        self.game.app.DISPLAY.blit(self.surface, [self.pos[0] + self.game.cords[0], self.pos[1] + self.game.cords[1]])

    def zoom(self, size, pos):
        self.pos = pos
        self.hexagon_size = [size[0] // 2, size[1] // 2]
        self.draw_hexagon()

    def set_color(self, color):
        self.color = color
        self.draw_hexagon()

    def set_outline_color(self, color):
        self.outline_color = color
        self.draw_hexagon()

    def set_energy(self, energy):
        self.energy = energy
        self.draw_hexagon()
