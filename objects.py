""" This file contains all game objects classes """

import pygame.draw
from functions import *


class Label:
    """ Label UI object for pygame games. """

    def __init__(self, game, text="", pos=None, font_name="Gill Sans", font_size=100, bold=False, italic=False, smooth=True, foreground=(40, 40, 40), background=None):
        self.game = game

        if pos is None:
            self.pos = [0, 0]
        else:
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
        self.update_text(self.text, self.smooth, self.foreground, self.background)

    def update(self):
        """ Shows the surface of label on a game app display """

        self.game.app.DISPLAY.blit(self.surface, self.pos)

    def update_text(self, text, smooth=None, foreground=None, background=None):
        """ Updates text, smooth, foreground and background values of label and recreates surface of label """

        self.text = str(text)
        if smooth:
            self.smooth = smooth
        if foreground:
            self.foreground = foreground
        if background:
            self.background = background
        self.surface = self.font.render(self.text, self.smooth, self.foreground, self.background)
        self.size = self.surface.get_size()

    def center_x(self, y=0):
        """ Places label at the center of game app screen width """

        self.pos = [(self.game.app.WIDTH - self.size[0]) / 2, y]
        return self

    def center_y(self, x=0):
        """ Places label at the center of game app screen height """

        self.pos = [x, (self.game.app.HEIGHT - self.size[1]) / 2]
        return self

    def center(self):
        """ Places label at the center of game app screen width and height """

        self.pos = [(self.game.app.WIDTH - self.size[0]) / 2,
                    (self.game.app.HEIGHT - self.size[1]) / 2]
        return self

    def percent_x(self, percent=0, y=None):
        """ Places label at given percent on the game app screen width """

        one_percent = self.game.app.WIDTH / 100
        if y is None:
            self.pos = [percent * one_percent, (self.game.app.HEIGHT - self.size[1]) / 2]
        else:
            self.pos = [percent * one_percent, y]
        return self

    def percent_y(self, percent=0, x=None):
        """ Places label at given percent on the game app screen height """

        one_percent = self.game.app.HEIGHT / 100
        if x is None:
            self.pos = [(self.game.app.WIDTH - self.size[0]) / 2, percent * one_percent]
        else:
            self.pos = [x, percent * one_percent]
        return self

    def percent(self, percent_x=0, percent_y=0):
        """ Places label at given percent on the game app screen width and height """

        one_percent_x = self.game.app.WIDTH / 100
        one_percent_y = self.game.app.HEIGHT / 100
        self.pos = [percent_x * one_percent_x, percent_y * one_percent_y]
        return self


class Button(Label):
    """ Button UI object for pygame games. """

    def __init__(self, game, text="", pos=None, font_name="Gill Sans", font_size=60, bold=False, italic=False, smooth=True, foreground=(40, 40, 40), background=None):
        super().__init__(game, text, pos, font_name, font_size, bold, italic, smooth, foreground, background)

        self.counter = 0
        self.counter_max = 50

    def clicked(self, mouse_buttons, mouse_position):
        """ Checks if button is clicked or not """

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


class OptionButton(Button):
    """
    OptionButton UI object for pygame games.
    When clicked, switches current option to next option.
    """

    def __init__(self, game, text="", options=None, pos=None, font_name="Gill Sans", font_size=60, bold=False, italic=False, smooth=True, foreground=(40, 40, 40), background=None, current_option=0):
        if options is None:
            self.options = ["Option 1", "Option 2", "Option 3"]
        else:
            self.options = options
        self.current_option = current_option
        self.static_text = text
        self.text = self.static_text + str(self.options[self.current_option])
        super().__init__(game, self.text, pos, font_name, font_size, bold, italic, smooth, foreground, background)
        self.counter_max = 20

    def clicked(self, mouse_buttons, mouse_position):
        """ Checks if option button is clicked or not """

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
            self.next_option()

    def next_option(self):
        """ Selects next option to display on option button """

        self.current_option += 1
        if self.current_option > len(self.options) - 1:
            self.current_option = 0
        self.text = self.static_text + str(self.options[self.current_option])
        self.update_text(self.text, self.smooth, self.foreground, self.background)

    def get_current_option(self):
        """ Returns current option value """

        return self.options[self.current_option]


class ColorOptionButton(OptionButton):
    """
    ColorOptionButton UI object for pygame games.
    When clicked, switches current option to next option.
    Option represents RGB color. Option example: (255, 0, 0).
    """

    def __init__(self, game, text="", color_rect_size=None, options=None, pos=None, font_name="Gill Sans", font_size=60, bold=False, italic=False, smooth=True,
                 foreground=(40, 40, 40), background=None, current_option=0, outline=5):
        super().__init__(game, text, options, pos, font_name, font_size, bold, italic, smooth, foreground, background, current_option)
        self.text = self.static_text
        self.outline = outline
        self.update_text(self.text, self.smooth, self.foreground, self.background)
        if options is None:
            self.options = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        else:
            self.options = options
        if color_rect_size is None:
            self.color_rect_size = [self.font_size * 2, self.font_size + 10]
        else:
            self.color_rect_size = color_rect_size

    def update(self):
        """ Shows the surface of label on a game app display and the rectangle with picked color option """

        pygame.draw.rect(self.game.app.DISPLAY, self.options[self.current_option], pygame.Rect([self.pos[0] + self.size[0], self.pos[1]], self.color_rect_size))
        pygame.draw.rect(self.game.app.DISPLAY, self.foreground, pygame.Rect([self.pos[0] + self.size[0], self.pos[1]], self.color_rect_size), self.outline)
        self.game.app.DISPLAY.blit(self.surface, self.pos)

    def next_option(self):
        """ Selects next option to display on color option button """

        self.current_option += 1
        if self.current_option > len(self.options) - 1:
            self.current_option = 0
        self.text = self.static_text
        self.update_text(self.text, self.smooth, self.foreground, self.background)


class Text(Label):
    """
    Text UI object for pygame games.
    This widget allows you to create multiple lines text.
    """

    def __init__(self, game, text="", pos=None, font_name="Gill Sans", font_size=60, bold=False, italic=False, smooth=True, foreground=(40, 40, 40), background=None, line_height=None):
        super().__init__(game, text, pos, font_name, font_size, bold, italic, smooth, foreground, background)

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
        """ Places Text at given percent on the game app screen height """

        one_percent = self.game.app.HEIGHT / 100
        if x is None:
            self.pos_list = [[(self.game.app.WIDTH - self.size_list[i][0]) / 2, percent * one_percent + i * self.line_height] for i in range(self.lines)]
        else:
            self.pos_list = [[x, percent * one_percent + i * self.line_height] for i in range(self.lines)]
        return self

    def update_y(self, y, x=None):
        """ Updates Text position at given percent on the game app screen height """

        self.pos[1] = y
        if x is None:
            self.pos_list = [[(self.game.app.WIDTH - self.size_list[i][0]) / 2, y + i * self.line_height] for i in range(self.lines)]
        else:
            self.pos_list = [[x, y + i * self.line_height] for i in range(self.lines)]

    def update(self):
        """ Shows the surface of Text on a game app display """

        [self.game.app.DISPLAY.blit(self.surface_list[i], self.pos_list[i]) for i in range(self.lines)]


class Hexagon(Label):
    """
    Hexagon game object.
    Main game object for the Root Wars.
    """

    surface_size = [300, 300]
    height_scale = 1

    def __init__(self, game, pos=None, color=(255, 255, 255), outline_color=(10, 10, 10), width=5, hexagon_size=None, hex_pos=None, energy=0,
                 text="", font_name="Gill Sans", font_size=60, bold=False, italic=False, smooth=True, foreground=(40, 40, 40), background=None, i=None):
        super().__init__(game, text, pos, font_name, font_size, bold, italic, smooth, foreground, background)

        if hex_pos is None:
            self.hex_pos = []
        else:
            self.hex_pos = hex_pos
        self.color = color
        self.outline_color = outline_color
        self.width = width
        if hexagon_size is None:
            self.hexagon_size = [100, 100]
        else:
            self.hexagon_size = [hexagon_size[0] // 2, hexagon_size[1] // 2]
        self.text_surface = self.font.render(self.text, self.smooth, self.foreground, self.background)
        self.i = i

        # game variables
        self.energy = energy

        self.draw_hexagon()

    def draw_hexagon(self):
        """ Draw hexagon on its surface """

        self.text_surface = self.font.render(str(int(self.energy)), self.smooth, self.foreground, self.background)
        self.surface = pygame.Surface(self.surface_size)
        self.surface.set_colorkey((0, 0, 0))

        self.pos_list = [[0, math.cos(deg_to_rad(60)) * self.hexagon_size[1] * 2.9 + self.width]]
        for i in range(1, 6):
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
            for i in range(int(self.energy)):
                energy_pos_list = []
                for j in self.pos_list:
                    pos = [j[0] - i * self.height_scale, j[1] - i * self.height_scale]
                    energy_pos_list.append(pos)
                color = [self.color[0] - i * self.height_scale if self.color[0] != 0 else self.color[0],
                         self.color[1] - i * self.height_scale if self.color[1] != 0 else self.color[1],
                         self.color[2] - i * self.height_scale if self.color[2] != 0 else self.color[2]]
                color[0] = 0 if color[0] < 0 else color[0]
                color[1] = 0 if color[1] < 0 else color[1]
                color[2] = 0 if color[2] < 0 else color[2]
                color[0] = 255 if color[0] > 255 else color[0]
                color[1] = 255 if color[1] > 255 else color[1]
                color[2] = 255 if color[2] > 255 else color[2]

                pygame.draw.polygon(self.surface, color, energy_pos_list)
                if i % 5 == 0:
                    pygame.draw.lines(self.surface, self.outline_color, True, energy_pos_list, self.width)
        else:
            pygame.draw.polygon(self.surface, self.color, self.pos_list)
            pygame.draw.lines(self.surface, self.outline_color, True, self.pos_list, self.width)

        self.text_surface = self.font.render(str(self.energy), self.smooth, self.foreground, self.background)

    def update(self):
        """ Shows the surface of Hexagon on a game app display """

        self.game.app.DISPLAY.blit(self.surface, [self.pos[0] + self.game.cords[0], self.pos[1] + self.game.cords[1]])
        if self.energy > 0:
            self.game.app.DISPLAY.blit(self.text_surface, [self.pos[0] + self.game.cords[0] + self.surface_size[0] - 50 - self.energy * self.height_scale - self.text_surface.get_size()[0] / 2,
                                                           self.pos[1] + self.game.cords[1] + self.surface_size[0] - 90 - self.energy * self.height_scale])

    def zoom(self, size, pos):
        """ Zooms Hexagon size and position """

        self.pos = pos
        self.hexagon_size = [size[0] // 2, size[1] // 2]
        self.draw_hexagon()

    def set_color(self, color):
        """ Sets Hexagon color """

        self.color = color
        self.draw_hexagon()

    def set_outline_color(self, color):
        """ Sets Hexagon outline color """

        self.outline_color = color
        self.draw_hexagon()

    def set_energy(self, energy):
        """ Sets Hexagon energy """

        self.energy = energy
        self.draw_hexagon()


class Line:
    """ Line class for the Root Wars grid map. """

    def __init__(self, game, pos1=None, pos2=None, color=(255, 255, 255), width=5):
        self.game = game

        if pos1 is None:
            self.pos1 = [0, 0]
        else:
            self.pos1 = pos1
        if pos2 is None:
            self.pos2 = [0, 0]
        else:
            self.pos2 = pos2
        self.color = color
        self.width = width

    def update(self):
        """ Draws the Line on game app display """

        pygame.draw.line(self.game.app.DISPLAY, self.color,
                         [self.pos1[0] + self.game.cords[0], self.pos1[1] + self.game.cords[1]],
                         [self.pos2[0] + self.game.cords[0], self.pos2[1] + self.game.cords[1]],
                         self.width)
