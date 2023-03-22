"""
Origin Game Engine Library.
This file contains all game objects classes .
"""

import pygame.draw
from functions import *


def rotate(image, pos, origin_pos, angle):
    """ Rotate pygame surface to given angle with stable origin position """

    # calculate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(origin_pos[0], -origin_pos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - origin_pos[0] + min_box[0] - pivot_move[0], pos[1] - origin_pos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    return rotated_image, [origin[0] + 25, origin[1] + 25]


class Pos:
    """ Basic class for interpreting something that has position """

    def __init__(self, pos=None):
        if pos is None:
            self.pos = [0, 0]
        else:
            self.pos = pos

    @staticmethod
    def add_pos(pos1: list, pos2: list) -> list:
        """ Adds coordinates """

        return [pos1[0] + pos2[0], pos1[1] + pos2[1]]

    @staticmethod
    def sub_pos(pos1: list, pos2: list) -> list:
        """ Subtracts coordinates """

        return [pos1[0] - pos2[0], pos1[1] - pos2[1]]

    @staticmethod
    def inv_sub_pos(pos1: list, pos2: list) -> list:
        """ Subtracts and inverts coordinates """

        return [pos2[0] - pos1[0], pos2[1] - pos1[1]]

    @staticmethod
    def mul_pos(pos1: list, pos2: list) -> list:
        """ Multiplies coordinates """

        return [pos1[0] * pos2[0], pos1[1] * pos2[1]]

    @staticmethod
    def div_pos(pos1: list, pos2: list) -> list:
        """ Divides coordinates """

        return [pos1[0] / pos2[0], pos1[1] / pos2[1]]

    @staticmethod
    def inv_div_pos(pos1: list, pos2: list) -> list:
        """ Divides and inverts coordinates"""

        return [pos2[0] / pos1[0], pos2[1] / pos1[1]]


class Vector(Pos):
    """ Class that represents vectors """

    def __init__(self, pos1=None, pos2=None):
        super().__init__()
        if pos1 is None:
            self.pos1 = [0, 0]
        else:
            self.pos1 = pos1
        if pos2 is None:
            self.pos2 = [0, 0]
        else:
            self.pos2 = pos2
        self.length = self.get_length()
        self.angle = self.get_angle()

    def get_length(self):
        """ Returns length of a vector """

        return distance_to_obj(self.pos1, self.pos2)

    def get_angle(self):
        """
        Returns vector angle.

        y: vertical size of a vector.
        l: length of a vector.
        """

        y = self.sub_pos(self.pos2, self.pos1)[1]
        length = self.get_length()
        return rad_to_deg(math.sin(y / length))


class Surface(Pos):
    """ Surface class that allows you to set alpha value, colorkey and other cool things to show on pygame window"""

    def __init__(self, game, pos=None, size=None, alpha=255, colorkey=None):
        self.game = game

        super().__init__(pos)
        if size is None:
            self.size = [200, 100]
        else:
            self.size = size
        self.alpha = alpha
        self.colorkey = colorkey

        self.create_surface()

    def create_surface(self):
        """ Creates pygame surface """

        self.surface = pygame.Surface(self.size)
        self.surface.set_alpha(self.alpha)
        self.surface.set_colorkey(self.colorkey)

    def update(self):
        """ Shows the surface on a game app display """

        self.game.app.DISPLAY.blit(self.surface, self.pos)


class Label(Pos):
    """ Label UI object for pygame games. """

    def __init__(self, game, text="", pos=None, font_name="Segoe UI", font_size=100, bold=False, italic=False,
                 smooth=True, foreground=(200, 200, 200), background=None):
        self.game = game

        super().__init__(pos)
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

    def __init__(self, game, text="", pos=None, font_name="Segoe UI", font_size=60, bold=False, italic=False,
                 smooth=True, foreground=(200, 200, 200), background=None):
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

    def __init__(self, game, text="", options=None, pos=None, font_name="Segoe UI", font_size=60, bold=False,
                 italic=False, smooth=True, foreground=(200, 200, 200), background=None,
                 current_option=0):
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

    def __init__(self, game, text="", color_rect_size=None, options=None, pos=None, font_name="Segoe UI", font_size=60,
                 bold=False, italic=False, smooth=True,
                 foreground=(200, 200, 200), background=None, current_option=0, outline=1):
        super().__init__(game, text, options, pos, font_name, font_size, bold, italic, smooth, foreground, background,
                         current_option)
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

        pygame.draw.rect(self.game.app.DISPLAY, self.options[self.current_option],
                         pygame.Rect([self.pos[0] + self.size[0], self.pos[1]], self.color_rect_size))
        pygame.draw.rect(self.game.app.DISPLAY, self.foreground,
                         pygame.Rect([self.pos[0] + self.size[0], self.pos[1]], self.color_rect_size), self.outline)
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

    def __init__(self, game, text="", pos=None, font_name="Segoe UI", font_size=60, bold=False, italic=False,
                 smooth=True, foreground=(200, 200, 200), background=None, line_height=None):
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

        self.size = [max([self.surface_list[i].get_size()[0] for i in range(self.lines)]),
                     self.lines * self.line_height]

    def percent_y(self, percent=0, x=None):
        """ Places Text at given percent on the game app screen height """

        one_percent = self.game.app.HEIGHT / 100
        if x is None:
            self.pos_list = [
                [(self.game.app.WIDTH - self.size_list[i][0]) / 2, percent * one_percent + i * self.line_height] for i
                in range(self.lines)]
        else:
            self.pos_list = [[x, percent * one_percent + i * self.line_height] for i in range(self.lines)]
        return self

    def update_y(self, y, x=None):
        """ Updates Text position at given percent on the game app screen height """

        self.pos[1] = y
        if x is None:
            self.pos_list = [[(self.game.app.WIDTH - self.size_list[i][0]) / 2, y + i * self.line_height] for i in
                             range(self.lines)]
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
    height_scale = 3

    def __init__(self, game, pos=None, color=(255, 255, 255), outline_color=(10, 10, 10), width=5, hexagon_size=None,
                 hex_pos=None, energy=0,
                 text="", font_name="Segoe UI", font_size=60, bold=False, italic=False, smooth=True,
                 foreground=(40, 40, 40), background=None):
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
            pygame.draw.lines(self.surface, self.outline_color, True, self.pos_list, self.width)
            for i in range(int(self.energy)):
                energy_pos_list = []
                for j in self.pos_list:
                    pos = [j[0] - i * self.height_scale, j[1] - i * self.height_scale]
                    energy_pos_list.append(pos)
                color = [self.color[0] - i * self.height_scale * 2 if self.color[0] != 0 else self.color[0],
                         self.color[1] - i * self.height_scale * 2 if self.color[1] != 0 else self.color[1],
                         self.color[2] - i * self.height_scale * 2 if self.color[2] != 0 else self.color[2]]
                color[0] = 0 if color[0] < 0 else color[0]
                color[1] = 0 if color[1] < 0 else color[1]
                color[2] = 0 if color[2] < 0 else color[2]
                color[0] = 255 if color[0] > 255 else color[0]
                color[1] = 255 if color[1] > 255 else color[1]
                color[2] = 255 if color[2] > 255 else color[2]

                pygame.draw.polygon(self.surface, color, energy_pos_list)
                if i % 5 == 0:
                    pygame.draw.lines(self.surface, self.color, True, energy_pos_list, self.width)
        else:
            pygame.draw.polygon(self.surface, self.color, self.pos_list)
            pygame.draw.lines(self.surface, self.outline_color, True, self.pos_list, self.width)

        self.text_surface = self.font.render(str(self.energy), self.smooth, self.foreground, self.background)

    def update(self):
        """ Shows the surface of Hexagon on a game app display """

        self.game.app.DISPLAY.blit(self.surface, [self.pos[0] + self.game.cords[0], self.pos[1] + self.game.cords[1]])
        if self.energy > 0:
            self.game.app.DISPLAY.blit(self.text_surface, [
                self.pos[0] + self.game.cords[0] + self.surface_size[0] - 50 - self.energy * self.height_scale -
                self.text_surface.get_size()[0] / 2,
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


class Line(Vector):
    """ Line class for the Root Wars grid map. """

    def __init__(self, game, pos1=None, pos2=None, color=(255, 255, 255), width=5):
        self.game = game

        super().__init__(pos1, pos2)
        self.color = color
        self.width = width

    def update(self):
        """ Draws the Line on game app display """

        pygame.draw.line(self.game.app.DISPLAY, self.color,
                         [self.pos1[0] + self.game.cords[0], self.pos1[1] + self.game.cords[1]],
                         [self.pos2[0] + self.game.cords[0], self.pos2[1] + self.game.cords[1]],
                         self.width)


class AnimatedRing(Surface):
    """
    Was the first test version of bloom effect.
    Now it's a simple test object that uses smooth animation.
    """

    surface_size = 300

    def __init__(self, game, pos=None, size=100, color=(0, 155, 255), alpha=255, colorkey=None, angle=0, width=4):
        Surface.__init__(self, game, pos, [self.surface_size, self.surface_size], alpha, colorkey)
        self.angle = angle
        self.color = color
        self.size = size
        self.width = width
        self.counter = 0

        self.acceleration = 20
        self.init_size = 10
        self.max_size = self.size

        self.init_max_size = size
        self.init_color = color

        # self.surface.fill((255, 0, 0))
        self.draw_ring()

    def draw_ring(self):
        """ Draws ring on its surface """

        self.surface.fill(self.colorkey)
        pygame.draw.circle(self.surface, sub_brightness(self.color, 100),
                           [self.surface_size // 2, self.surface_size // 2], self.size // 2 + self.width // 2,
                           self.width * 2)
        pygame.draw.circle(self.surface, self.color, [self.surface_size // 2, self.surface_size // 2], self.size // 2,
                           self.width)

    def draw_circle(self):
        """ Draws circle on its surface """

        self.surface.fill(self.colorkey)
        pygame.draw.circle(self.surface, sub_brightness(self.color, 100),
                           [self.surface_size // 2, self.surface_size // 2], self.size // 2 + self.width * 2)
        pygame.draw.circle(self.surface, self.color, [self.surface_size // 2, self.surface_size // 2], self.size // 2)

    def set_alpha(self, alpha: int):
        """ Sets alpha value of the surface """

        self.alpha = alpha
        self.surface.set_alpha(self.alpha)

    def set_size(self, size):
        """ Sets the size value of the surface """

        self.size = size
        self.draw_ring()

    def update(self):
        """ Shows the surface on a game app display """

        self.game.app.DISPLAY.blit(self.surface, self.pos)

        if self.color[2] < 230:
            self.color = add_brightness(self.color, 8)
        self.draw_ring()

        self.size = (self.counter / (self.counter / 1.1 + 1)) * (self.max_size - self.init_size) + self.init_size
        if self.size > self.max_size:
            self.size = self.max_size
        # self.width = 15 - int(self.size / 10)
        # self.set_alpha(self.size)
        self.set_size(self.size)

        if self.counter < 255:
            self.counter += 1

    def reset(self):
        """ Resets animation properties """

        self.counter = 0
        self.size = self.init_max_size
        self.max_size = self.size
        self.color = self.init_color


class Bloom2(Surface):
    """
    Bloom effects like post-processing.
    Can be implemented in any visual object.
    """

    def __init__(self, game, pos=None, r=50, light_source_r=5, resolution=20, color=(255, 255, 255), alpha=5,
                 colorkey=(0, 0, 0), angle=0):
        Surface.__init__(self, game, pos, [r, r], alpha, colorkey)
        self.angle = angle
        self.color = color
        self.r = r
        self.light_source_r = light_source_r
        self.resolution = resolution
        self.size = [r, r]
        self.intensity = 1
        self.scale = self.r // self.resolution

        self.draw(0)

    def draw(self, r):
        """ Draws bloom light on self surface """

        self.surface.fill(self.colorkey)
        self.surface.set_alpha(self.alpha)
        pygame.draw.circle(self.surface, self.color, [self.r // 2, self.r // 2], self.r // 2 - r)

    def update(self):
        """ Shows the surface on a game app display """

        # rotated_surface, rotated_pos = rotate(self.surface, self.pos, [self.s // 2, self.s // 2], i * self.steps)

        # draw light
        for i in range(self.r // self.scale):
            self.draw(self.r - i * self.scale)
            self.game.app.DISPLAY.blit(self.surface, self.pos)

        # draw light source
        pygame.draw.circle(self.game.app.DISPLAY, add_brightness(self.color, 100),
                           self.add_pos(self.pos, [self.r // 2, self.r // 2]), self.light_source_r)


class Bloom3(Surface):
    """
    Bloom effects like post-processing.
    Can be implemented in any visual object.
    Allows to create glowy lines.
    """

    def __init__(self, game, pos=None, r=50, light_source_r=2, resolution=20, color=(255, 255, 255), alpha=3,
                 colorkey=(0, 0, 0), angle=0):
        Surface.__init__(self, game, pos, [r, r], alpha, colorkey)
        self.angle = angle
        self.color = color
        self.r = r
        self.light_source_r = light_source_r
        self.resolution = resolution
        self.size = [r, r]
        self.intensity = 1
        self.scale = self.r // self.resolution
        self.last_pos = self.pos

        self.draw(0)

    def draw(self, r):
        """ Draws bloom light on self surface """

        self.surface.fill(self.colorkey)
        self.surface.set_alpha(self.alpha)
        pygame.draw.circle(self.surface, self.color, [self.r // 2, self.r // 2], self.r // 2 - r)

    def update(self):
        """ Shows the surface on a game app display """

        # draw light
        for i in range(self.r // self.scale):
            self.draw(self.r - i * self.scale)
            self.game.app.DISPLAY.blit(self.surface, self.sub_pos(self.pos, [self.r // 2, self.r // 2]))

        # draw light source
        pygame.draw.line(self.game.app.DISPLAY, add_brightness(self.color, 100), self.last_pos, self.pos,
                         self.light_source_r * 2)

        self.last_pos = self.pos
