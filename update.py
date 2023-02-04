import pygame
from objects import *


class Game:
    def __init__(self, app):
        # put initialisation of objects here
        self.app = app
        self.mode = "main menu"
        self.SKIP_FRAME = False
        self.FIRST_ITERATION = True
        self.WIN = False
        self.LOSE = False

        self.main_menu_objects = []
        self.settings_objects = []
        self.info_objects = []
        self.rules_objects = []

        self.scroll_scale = 40

        # game map variables
        self.game_objects = []
        self.hexagons = []

        self.navigation_speed = 30
        self.hexagon_size = 100
        self.min_hexagon_size = 60
        self.max_hexagon_size = 100
        self.hexagon_grid_length = self.hexagon_size * 2
        self.map_move_reaction = 2
        self.grid_line_width = 5
        self.grid_hex_width = 5
        self.grid_line_color = (50, 50, 50, 255)
        self.grid_hex_color = (20, 20, 20)
        self.grid_hex_outline_color = (50, 50, 50, 255)
        self.player_color = (0, 0, 255)
        self.selected_hexagon_color = (100, 0, 150)
        self.enemy_color = (255, 0, 0)
        self.selected_enemy_hexagon_color = (255, 255, 0)

        # grid map
        self.grid_map_image = pygame.transform.rotate(pygame.image.load("map.png"), 90)
        self.grid_map = [[1 if self.grid_map_image.get_at((x, y)) == (0, 0, 0, 255) else 0 for x in range(self.grid_map_image.get_size()[0])] for y in range(self.grid_map_image.get_size()[1])]
        self.grid_map_size = [len(self.grid_map) * (self.hexagon_size + self.hexagon_grid_length), len(self.grid_map[0]) * (self.hexagon_size + self.hexagon_grid_length)]

        self.background_image = pygame.transform.scale(pygame.image.load("pexels-pixabay-235985.jpg"), [self.app.WIDTH, self.app.HEIGHT])

        self.cords = [-self.grid_map_size[0] / 6,
                      -self.grid_map_size[1] / 6]

        self.counter = 1

        # game variables
        self.max_energy = 40
        self.selected_hexagon = None
        self.selected_enemy_hexagon = None
        self.nearby_pos = []
        self.nearby_hexagons = []
        self.nearby_enemy_hexagons = []
        self.player_hexagons = []
        self.enemy_hexagons = []

        # settings variables
        self.SETTINGS_OBJECTS_CREATED = False
        self.FPS_ENABLED = False
        self.fps_label = Label(self, text="ABOBA", foreground=(0, 255, 0), font_size=40, font_name="Courier").percent(95, 2)

        self.create_main_menu_objects()

    def create_main_menu_objects(self):
        self.game_title_label = Label(self, text="Root Wars").percent_y(10)
        self.play_button = Button(self, text="Play").percent_y(35)
        self.settings_button = Button(self, text="Settings").percent_y(45)
        self.info_button = Button(self, text="Info").percent_y(55)
        self.rules_button = Button(self, text="Rules").percent_y(65)
        self.exit_button = Button(self, text="Exit").percent_y(75)

        self.main_menu_objects.append(self.game_title_label)
        self.main_menu_objects.append(self.play_button)
        self.main_menu_objects.append(self.settings_button)
        self.main_menu_objects.append(self.info_button)
        self.main_menu_objects.append(self.rules_button)
        self.main_menu_objects.append(self.exit_button)

    def create_settings_objects(self):
        if not self.SETTINGS_OBJECTS_CREATED:
            self.fps_button = Button(self, text="Show fps").percent_y(10)
            self.back_button = Button(self, text="Back").percent(8, 8)
            self.info_text = Text(self, text="Key settings\n\n"
                                             "Return to main menu: Escape\n"
                                             "Select your root: Left Mouse Button\n\n").percent_y(30, x=100)

            self.settings_objects.append(self.fps_button)
            self.settings_objects.append(self.back_button)
            self.settings_objects.append(self.info_text)

            self.SETTINGS_OBJECTS_CREATED = True

    def create_rules_objects(self):
        self.info_text = Text(self, text="Rules\n\n"
                                         "To win this game, you need to capture the enemy root.\n"
                                         "Enemy root is dyed red.\n"
                                         "To do this, you need to grow your root.\n"
                                         "Your root is dyed blue.\n\n"
                                         "When you click on your root you can choose up to 6\n"
                                         "positions where root can grow.\n"
                                         "Positions where your root can grow are dyed red.\n\n"
                                         f"Every root has energy. Energy can be from 0 to {self.max_energy}.\n"
                                         f"Root energy is a number on root.\n"
                                         "If root that you clicked has more than 1 energy,\n"
                                         "you can click on available positions\n"
                                         "where root can grow to grow your root.\n\n"
                                         "If root that you clicked has more energy than enemy root,\n"
                                         "you can grow your root on enemy root, enemy root will be destroyed.").percent_y(0)

        self.back_button = Button(self, text="Back").percent(8, 8)

        self.rules_objects.append(self.info_text)
        self.rules_objects.append(self.back_button)

    def create_info_objects(self):
        self.info_text = Text(self, text="Hello\n\n"
                                         "This is a simple RTS (Real Time Strategy) game.\n\n"
                                         "Defeat the enemy root and conquer this hexagon map!\n\n"
                                         "Made on 03.02.23.\n\n"
                                         "Written on Python programming language\n\n"
                                         "using module Pygame that uses SDL.\n\n"
                                         "It was made only by me - Egor Mironov.").percent_y(10)

        self.back_button = Button(self, text="Back").percent(8, 8)

        self.info_objects.append(self.info_text)
        self.info_objects.append(self.back_button)

    def get_pos_for_hex_grid(self, position, size):
        x = position[0]
        y = position[1]
        should_offset = y % 2 == 0
        width = pow(3, 0.5) * size
        height = 2 * size

        horizontal_distance = width
        vertical_distance = height * (3 / 4)

        offset = width / 2 if should_offset else 0

        pos = [
            x * horizontal_distance + offset,
            y * vertical_distance
        ]

        if self.grid_map[x][y]:
            return pos
        else:
            return None

    def add_hexagon(self, x, y, color, outline_color):
        if y % 2 == 0:
            if x % 3 == 0:
                pos = self.get_pos_for_hex_grid(position=[x, y], size=self.hexagon_size)
                if pos is not None:
                    self.hexagons.append(Hexagon(self, pos=pos,
                                                 hexagon_size=[self.hexagon_size, self.hexagon_size],
                                                 hex_pos=[x, y],
                                                 color=color,
                                                 outline_color=outline_color,
                                                 foreground=(100, 100, 100)))
        elif (x + 1) % 3 == 0:
            pos = self.get_pos_for_hex_grid(position=[x, y], size=self.hexagon_size)
            if pos is not None:
                self.hexagons.append(Hexagon(self, pos=pos,
                                             hexagon_size=[self.hexagon_size, self.hexagon_size],
                                             hex_pos=[x, y],
                                             color=color,
                                             outline_color=outline_color,
                                             foreground=(100, 100, 100)))

    def create_hex_grid(self):
        # generate hexagon grid map
        for y in range(len(self.grid_map)):
            for x in range(len(self.grid_map)):
                self.add_hexagon(x, y, self.grid_hex_color, self.grid_hex_outline_color)

    def create_hex_grid_lines(self, i):
        for j, p in enumerate(self.player.pos_list):
            pos1 = [p[0] + i.pos[0] + self.cords[0],
                    p[1] + i.pos[1] + self.cords[1]]
            pos3 = [round(pos1[0] + math.sin(deg_to_rad(j * 60 + 120)) * (self.hexagon_grid_length)),
                    round(pos1[1] + math.cos(deg_to_rad((j * 60 + 120))) * (self.hexagon_grid_length))]
            x = 1
            y = 1
            if pos3[0] - x >= 0 and pos3[1] - y >= 0 and pos3[0] < self.app.WIDTH and pos3[1] < self.app.HEIGHT:
                if self.app.DISPLAY.get_at([pos3[0] - x, pos3[1] - y]) == self.grid_hex_outline_color:
                    pygame.draw.line(self.app.DISPLAY, self.grid_hex_outline_color, pos1, pos3, 5)

    def create_game_objects(self):
        # create objects
        self.win_label = Label(self, text="You win!", foreground=(50, 50, 50)).center()
        self.lose_label = Label(self, text="You lose!", foreground=(50, 50, 50)).center()
        self.back_button = Button(self, text="Menu").percent(8, 8)

        self.lines_surface = pygame.Surface((self.app.WIDTH, self.app.HEIGHT))
        self.lines_surface.set_colorkey((0, 0, 0))

        self.create_hex_grid()

        for i in self.hexagons:
            if isinstance(i, Hexagon):
                if i.hex_pos == [8, 15]:
                    self.player = i
                if i.hex_pos == [8, 1]:
                    self.enemy = i
        self.player.set_color(self.player_color)
        self.player.set_energy(1)

        self.enemy.set_color(self.enemy_color)
        self.enemy.set_energy(1)

        self.selected_hexagon = None

        self.cords = [-1385 + self.app.WIDTH / 2 - Hexagon.surface_size[0], -2250 + self.app.HEIGHT / 2 - Hexagon.surface_size[1]]

    def change_mode(self, mode):
        def clear():
            self.game_objects.clear()
            self.nearby_hexagons.clear()
            self.player_hexagons.clear()
            self.hexagons.clear()
            self.main_menu_objects.clear()
            self.info_objects.clear()
            self.rules_objects.clear()

        if mode == "main menu":
            self.mode = mode
            clear()
            self.create_main_menu_objects()
        if mode == "settings":
            self.mode = mode
            clear()
            self.create_settings_objects()
        elif mode == "info":
            self.mode = mode
            clear()
            self.create_info_objects()
        elif mode == "game":
            self.mode = mode
            clear()
            self.create_game_objects()
        elif mode == "rules":
            self.mode = mode
            clear()
            self.create_rules_objects()

    def select_hexagon(self, obj):
        self.selected_hexagon = obj
        self.selected_hexagon.set_color(self.selected_hexagon_color)

    def select_enemy_hexagon(self, obj):
        self.selected_enemy_hexagon = obj
        self.selected_enemy_hexagon.set_color(self.selected_enemy_hexagon_color)

    def create_player_hexagon(self, obj):
        self.selected_hexagon.set_energy(self.selected_hexagon.energy - 1)
        obj.set_color(self.player_color)
        obj.set_energy(1)
        self.player_hexagons.append(obj)
        self.selected_hexagon = obj

    def create_enemy_hexagon(self, obj):
        self.selected_enemy_hexagon.set_energy(self.selected_enemy_hexagon.energy - 1)
        obj.set_color(self.enemy_color)
        obj.set_energy(1)
        self.enemy_hexagons.append(obj)
        self.selected_enemy_hexagon = obj

    def get_nearby_hexagons_for_enemy(self):
        self.selected_enemy_hexagon = random.choice([self.enemy] + self.enemy_hexagons)
        self.nearby_enemy_hexagons.clear()
        for j, p in enumerate(self.player.pos_list):
            pos1 = [p[0] + self.selected_enemy_hexagon.pos[0] + self.cords[0],
                    p[1] + self.selected_enemy_hexagon.pos[1] + self.cords[1]]
            pos2 = [round(pos1[0] + math.sin(deg_to_rad(j * 60 + 120)) * (self.hexagon_grid_length + 20)),
                    round(pos1[1] + math.cos(deg_to_rad((j * 60 + 120))) * (self.hexagon_grid_length + 20))]

            for obj in self.hexagons:
                if touched(obj.pos[0] + self.cords[0] + Hexagon.surface_size[0] / 2, Hexagon.surface_size[0] / 2, pos2[0], 1,
                           obj.pos[1] + self.cords[1] + Hexagon.surface_size[0] / 2, Hexagon.surface_size[0] / 2, pos2[1], 1) and obj not in self.enemy_hexagons:
                    color = (0, 255, 0)
                    # pygame.draw.line(self.app.DISPLAY, color, pos1, pos2, 10)
                    # self.nearby_pos.append([pos1, pos2, obj, color])
                    # obj.set_color((0, 255, 0))
                    self.nearby_enemy_hexagons.append(obj)

    def get_nearby_hexagons_for_player(self):
        if self.selected_hexagon is not None:
            # locate nearby hexagons by pos
            self.nearby_hexagons.clear()
            self.nearby_pos.clear()
            for j, p in enumerate(self.player.pos_list):
                pos1 = [p[0] + self.selected_hexagon.pos[0] + self.cords[0],
                        p[1] + self.selected_hexagon.pos[1] + self.cords[1]]
                pos2 = [round(pos1[0] + math.sin(deg_to_rad(j * 60 + 120)) * (self.hexagon_grid_length + 20)),
                        round(pos1[1] + math.cos(deg_to_rad((j * 60 + 120))) * (self.hexagon_grid_length + 20))]
                # if pos2[0] - x >= 0 and pos2[1] - y >= 0 and pos2[0] < self.app.WIDTH and pos2[1] < self.app.HEIGHT:
                #     if self.app.DISPLAY.get_at([pos2[0] - x, pos2[1] - y]) == self.grid_hex_outline_color:
                # pygame.draw.rect(self.app.DISPLAY, (255, 255, 0), pygame.Rect(pos2, [10, 10]))
                for obj in self.hexagons:
                    if touched(obj.pos[0] + self.cords[0] + Hexagon.surface_size[0] / 2, Hexagon.surface_size[0] / 2, pos2[0], 1,
                               obj.pos[1] + self.cords[1] + Hexagon.surface_size[0] / 2, Hexagon.surface_size[0] / 2, pos2[1], 1) and obj not in self.player_hexagons:
                        color = (0, 255, 0)
                        # pygame.draw.line(self.app.DISPLAY, color, pos1, pos2, 10)
                        self.nearby_pos.append([pos1, pos2, obj, color])
                        obj.set_color((0, 255, 0))
                        self.nearby_hexagons.append(obj)
                    # else:
                    #     color = (255, 0, 0)
                    #     pygame.draw.line(self.app.DISPLAY, color, pos1, pos2, 10)

    # def draw_nearby_hex_lines(self):
    #     pass
    # print(len(self.nearby_hexagons))
    # pygame.draw.line(self.app.DISPLAY, (255, 0, 0),
    #                  [self.nearby_pos[0][0][0] + self.cords[0], self.nearby_pos[0][0][1] + self.cords[1]],
    #                  [self.nearby_pos[0][1][1] + self.cords[0], self.nearby_pos[0][1][1] + self.cords[1]], 5)
    # for i, obj in enumerate(self.nearby_hexagons):
    # for j, p in enumerate(self.nearby_pos):
    #     pos1 = [p[j][0] + self.nearby_hexagons[j].pos[0] + self.cords[0],
    #             p[j][1] + self.nearby_hexagons[j].pos[1] + self.cords[1]]
    #     pos2 = [round(pos1[0] - math.sin(deg_to_rad(j * 60 + 120)) * (self.hexagon_grid_length * 2 - 20)),
    #             round(pos1[1] - math.cos(deg_to_rad((j * 60 + 120))) * (self.hexagon_grid_length * 2 - 20))]
    #     pygame.draw.line(self.app.DISPLAY, (0, 255, 0), pos1, pos2, 10)

    def update(self, mouse_buttons, mouse_position, events, keys):
        # put game code here

        if self.mode == "main menu":
            # self.app.DISPLAY.fill((0, 0, 0))
            self.app.DISPLAY.blit(self.background_image, (0, 0))

            for obj in self.main_menu_objects:
                obj.update()

            if self.play_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("game")
            if self.settings_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("settings")
            if self.info_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("info")
            if self.rules_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("rules")
            if self.exit_button.clicked(mouse_buttons, mouse_position):
                self.app.RUN = False

        if self.mode == "settings":
            # self.app.DISPLAY.fill((0, 0, 0))
            self.app.DISPLAY.blit(self.background_image, (0, 0))

            for obj in self.settings_objects:
                obj.update()

            for event in events:
                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0 and self.info_text.pos[1] > -self.info_text.size[1]:
                        self.info_text.update_y(self.info_text.pos[1] + event.y * self.scroll_scale, 100)
                    elif event.y > 0 and self.info_text.pos[1] < self.info_text.size[1] - self.scroll_scale:
                        self.info_text.update_y(self.info_text.pos[1] + event.y * self.scroll_scale, 100)

            if self.fps_button.clicked(mouse_buttons, mouse_position):
                self.FPS_ENABLED = not self.FPS_ENABLED
                if self.FPS_ENABLED:
                    self.fps_button.update_text("Hide fps")
                else:
                    self.fps_button.update_text("Show fps")
            if self.back_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("main menu")

        if self.mode == "info":
            # self.app.DISPLAY.fill((0, 0, 0))
            self.app.DISPLAY.blit(self.background_image, (0, 0))

            for obj in self.info_objects:
                obj.update()

            if self.back_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("main menu")

        if self.mode == "rules":
            self.app.DISPLAY.blit(self.background_image, (0, 0))

            for obj in self.rules_objects:
                obj.update()

            for event in events:
                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0 and self.info_text.pos[1] > -self.info_text.size[1]:
                        self.info_text.update_y(self.info_text.pos[1] + event.y * self.scroll_scale)
                    elif event.y > 0 and self.info_text.pos[1] < self.info_text.size[1] - self.scroll_scale:
                        self.info_text.update_y(self.info_text.pos[1] + event.y * self.scroll_scale)

            if self.back_button.clicked(mouse_buttons, mouse_position):
                self.change_mode("main menu")

        if self.mode == "game":
            # self.app.DISPLAY.fill((0, 0, 0))  # sky color: (0, 157, 255) # grass color: (50, 255, 20)
            self.app.DISPLAY.blit(self.background_image, (0, 0))

            # print(len(self.hexagons), len(self.nearby_hexagons), len(self.player_hexagons), len(self.nearby_pos))

            if not self.WIN:
                for event in events:
                    # if event.type == pygame.MOUSEWHEEL:
                    #     self.hexagon_size += event.y * 2
                    #     if self.hexagon_size > self.max_hexagon_size:
                    #         self.hexagon_size = self.max_hexagon_size
                    #     elif self.hexagon_size < self.min_hexagon_size:
                    #         self.hexagon_size = self.min_hexagon_size
                    #     self.hexagon_grid_length = self.hexagon_size * 2
                    #     self.grid_map_size = [len(self.grid_map) * (self.hexagon_size + self.hexagon_grid_length), len(self.grid_map[0]) * (self.hexagon_size + self.hexagon_grid_length)]
                    #
                    #     for obj in self.hexagons:
                    #         size = [self.hexagon_size, self.hexagon_size]
                    #         pos = self.get_pos_for_hex_grid(obj.hex_pos, self.hexagon_size)
                    #         obj.zoom(size, pos)

                    if event.type == pygame.MOUSEBUTTONDOWN and not self.FIRST_ITERATION:
                        # set colors
                        for i, obj in enumerate(self.hexagons):
                            if obj == self.player or obj in self.player_hexagons:
                                obj.set_color(self.player_color)
                            elif obj == self.enemy or obj in self.enemy_hexagons:
                                obj.set_color(self.enemy_color)
                            elif obj in self.nearby_hexagons:
                                obj.set_color(self.grid_hex_color)
                            else:
                                obj.set_color(self.grid_hex_color)
                        # player logic
                        for i, obj in enumerate(self.hexagons):
                            if touched(obj.pos[0] + self.cords[0] + Hexagon.surface_size[0] / 2, Hexagon.surface_size[0] / 2, mouse_position[0], 1,
                                       obj.pos[1] + self.cords[1] + Hexagon.surface_size[0] / 2, Hexagon.surface_size[0] / 2, mouse_position[1], 1):
                                if obj == self.player or obj in self.player_hexagons and obj.energy > 1:
                                    self.select_hexagon(obj)
                                    # pygame.draw.rect(self.app.DISPLAY, (255, 0, 0), pygame.Rect([obj.pos[0] + self.cords[0] + Hexagon.surface_size[0] / 2,
                                    #                                                             obj.pos[1] + self.cords[1] + Hexagon.surface_size[0] / 2],
                                    #                                                             [Hexagon.surface_size[0] / 2,
                                    #                                                              Hexagon.surface_size[0] / 2]))
                                    self.get_nearby_hexagons_for_player()
                                if obj in self.nearby_hexagons and self.selected_hexagon is not None and self.selected_hexagon.energy > 1:
                                    if obj == self.enemy or obj in self.enemy_hexagons:
                                        # print(obj.energy, self.selected_hexagon.energy)
                                        energy = self.selected_hexagon.energy - 1
                                        obj.set_energy(obj.energy - energy)
                                        self.selected_hexagon.set_energy(self.selected_hexagon.energy - energy)
                                        if obj.energy <= 0:
                                            if obj == self.enemy:
                                                self.WIN = True
                                                break
                                            else:
                                                self.enemy_hexagons.remove(obj)
                                                self.player_hexagons.append(obj)
                                                obj.set_energy(-obj.energy)
                                                obj.set_color(self.player_color)
                                    else:
                                        self.create_player_hexagon(obj)
                                        self.select_hexagon(obj)
                                        self.get_nearby_hexagons_for_player()
                                    break
                    # elif event.type == pygame.MOUSEBUTTONUP and not self.FIRST_ITERATION:
                    #     for i, obj in enumerate(self.hexagons):
                    #         if not touched(obj.pos[0] + self.cords[0] + Hexagon.surface_size[0] / 2, Hexagon.surface_size[0] / 2, mouse_position[0], 1,
                    #                    obj.pos[1] + self.cords[1] + Hexagon.surface_size[0] / 2, Hexagon.surface_size[0] / 2, mouse_position[1], 1):
                    #             if obj not in self.nearby_hexagons or self.selected_hexagon is None:
                    #                 obj.set_color(self.grid_hex_color)
                    # print(self.selected_hexagon)

                    # if event.type == pygame.MOUSEBUTTONDOWN and not self.FIRST_ITERATION:
                    #     for i, obj in enumerate(self.hexagons):
                    #         if touched(obj.pos[0] + self.cords[0] + Hexagon.surface_size[0] / 2, Hexagon.surface_size[0] / 2, mouse_position[0], 1,
                    #                    obj.pos[1] + self.cords[1] + Hexagon.surface_size[0] / 2, Hexagon.surface_size[0] / 2, mouse_position[1], 1):
                    #             # if obj.hex_pos == self.player.hex_pos:
                    #             if self.selected_hexagon is None:
                    #                 self.selected_hexagon = obj
                    #                 self.get_nearby_hexagons()
                    #             # if obj in self.nearby_hexagons:
                    #             print(321)
                    #             if self.selected_hexagon.energy > 1 and obj not in self.player_hexagons:
                    #                 print(self.selected_hexagon)
                    #                 self.selected_hexagon.set_energy(self.selected_hexagon.energy - 1)
                    #                 obj.set_color((0, 0, 255))
                    #                 obj.set_energy(1)
                    #                 print(123)
                    #                 self.selected_hexagon = obj
                    #                 print(self.selected_hexagon)
                    #                 self.player_hexagons.append(obj)
                    #                 break
                    #         elif obj.hex_pos != self.player.hex_pos and obj not in self.player_hexagons:
                    #             obj.set_color(self.grid_hex_color)
                    #             self.selected_hexagon = None
                    #         else:
                    #             obj.set_color(self.player_color)
                    #             self.selected_hexagon = None

            # user input handling
            if keys[pygame.K_ESCAPE]:
                self.change_mode("main menu")

            # game map navigation
            # top
            if mouse_position[1] - self.map_move_reaction < 0 and self.cords[1] < self.grid_map_size[1] / 8:
                self.cords[1] += self.navigation_speed * self.app.delta_time * self.app.MAX_FPS
            # bottom
            if mouse_position[1] + self.map_move_reaction > self.app.HEIGHT and self.cords[1] > -self.grid_map_size[1] / 2:
                self.cords[1] -= self.navigation_speed * self.app.delta_time * self.app.MAX_FPS
            # left
            if mouse_position[0] - self.map_move_reaction < 0 and self.cords[0] < self.grid_map_size[0] / 8:
                self.cords[0] += self.navigation_speed * self.app.delta_time * self.app.MAX_FPS
            # right
            if mouse_position[0] + self.map_move_reaction > self.app.WIDTH and self.cords[0] > -self.grid_map_size[0] / 2:
                self.cords[0] -= self.navigation_speed * self.app.delta_time * self.app.MAX_FPS

            # self.draw_nearby_hex_lines()

            # show grid hexagons
            for i, obj in enumerate(self.hexagons):
                # show grid lines:
                self.create_hex_grid_lines(obj)

                # pygame.draw.rect(self.app.DISPLAY, (255, 0, 0), pygame.Rect([obj.pos[0] + self.cords[0] + Hexagon.surface_size[0] / 2,
                #                                                              obj.pos[1] + self.cords[1] + Hexagon.surface_size[0] / 2],
                #                                                             [Hexagon.surface_size[0] / 2, Hexagon.surface_size[0] / 2]))
                obj.update(mouse_buttons, mouse_position, events, keys)

                # if mouse_buttons[0]:

                # else:
                #     self.selected_hexagon = None

            if not self.WIN and not self.LOSE:
                # increase player energy by one every second
                if self.counter % 120 == 0:
                    for obj in self.player_hexagons:
                        if obj.energy < self.max_energy:
                            obj.set_energy(obj.energy + 1)
                    if self.player.energy < self.max_energy:
                        self.player.set_energy(self.player.energy + 1)

                    if self.counter % 160 == 0:
                        # bot logic
                        self.get_nearby_hexagons_for_enemy()
                        # print(len(self.enemy_hexagons), len(self.nearby_enemy_hexagons), self.selected_enemy_hexagon.hex_pos)
                        for obj in self.hexagons:
                            if obj in self.nearby_enemy_hexagons and self.selected_enemy_hexagon is not None and self.selected_enemy_hexagon.energy > 1:
                                # print(213)
                                # self.create_enemy_hexagon(obj)
                                if obj in self.player_hexagons:
                                    energy = self.selected_enemy_hexagon.energy - 1
                                    obj.set_energy(obj.energy - energy)
                                    self.selected_enemy_hexagon.set_energy(self.selected_enemy_hexagon.energy - energy)
                                    if obj.energy <= 0:
                                        # if obj == self.enemy:
                                        #     print("YOU WIN!")
                                        #     self.change_mode("main menu")
                                        #     break
                                        # else:
                                        self.player_hexagons.remove(obj)
                                        self.enemy_hexagons.append(obj)
                                        obj.set_energy(-obj.energy)
                                        obj.set_color(self.enemy_color)
                                        # self.select_enemy_hexagon(obj)
                                else:
                                    self.create_enemy_hexagon(obj)
                                break

                        for obj in [self.enemy] + self.enemy_hexagons:
                            # increasing energy
                            if obj.energy < self.max_energy:
                                obj.set_energy(obj.energy + 1)
                        # if self.enemy.energy < self.max_energy:
                        #     self.enemy.set_energy(self.enemy.energy + 1)

            if self.WIN:
                self.win_label.update()
                self.back_button.update()

                if self.back_button.clicked(mouse_buttons, mouse_position):
                    self.change_mode("main menu")

                if self.counter % 12 == 0:
                    self.selected_hexagon = random.choice(self.hexagons)
                    self.selected_hexagon.set_color(self.player_color)

            if self.LOSE:
                self.lose_label.update()
                self.back_button.update()

                if self.back_button.clicked(mouse_buttons, mouse_position):
                    self.change_mode("main menu")

                if self.counter % 12 == 0:
                    self.selected_hexagon = random.choice(self.hexagons)
                    self.selected_hexagon.set_color(self.enemy_color)

            # win
            if len(self.player_hexagons) == len(self.hexagons) - 1:
                self.WIN = True
            # lose
            if self.player in self.enemy_hexagons:
                self.LOSE = True

            self.counter += 1
            if self.counter > 60:
                self.counter = 0

            if self.FIRST_ITERATION and self.counter % 30 == 0:
                self.FIRST_ITERATION = False

        # things that settings change
        if self.FPS_ENABLED:
            self.fps_label.update_text(round(self.app.CLOCK.get_fps()))
            self.fps_label.update()
