__author__ = "Egor Mironov"

# started developing 31.01.23

import pygame
import time
from update import *


class App:
    def __init__(self):
        """main initialization"""
        pygame.init()

        self.INIT_WIDTH = 0
        self.INIT_HEIGHT = 0
        self.INIT_DISPLAY_MODE = pygame.FULLSCREEN

        self.init_display(self.INIT_WIDTH, self.INIT_HEIGHT, self.INIT_DISPLAY_MODE)
        pygame.display.set_caption("Root Wars")
        self.CLOCK = pygame.time.Clock()
        self.MAX_FPS = 60
        self.delta_time = 0.01
        self.RUN = True
        self.last_time = time.time()

        self.game = Game(self)

    def init_display(self, display_width, display_height, display_mode):
        """display initialization"""
        pygame.display.quit()
        self.WIDTH = display_width
        self.HEIGHT = display_height
        self.DISPLAY_MODE = display_mode
        self.DISPLAY = pygame.display.set_mode((self.WIDTH, self.HEIGHT), self.DISPLAY_MODE)
        if self.DISPLAY_MODE == pygame.FULLSCREEN:
            self.WIDTH, self.HEIGHT = pygame.display.get_window_size()
        self.H_WIDTH = self.WIDTH / 2
        self.H_HEIGHT = self.HEIGHT / 2

    def run(self):
        """main script loop"""
        while self.RUN:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            for event in events:
                if event.type == pygame.QUIT:
                    self.RUN = False

            mouse_buttons = pygame.mouse.get_pressed()
            mouse_position = list(pygame.mouse.get_pos())
            now_time = time.time()
            self.delta_time = now_time - self.last_time
            self.last_time = now_time

            self.game.update(mouse_buttons, mouse_position, events, keys)

            pygame.display.update()
            self.CLOCK.tick(self.MAX_FPS)


if __name__ == "__main__":
    app = App()
    app.run()
