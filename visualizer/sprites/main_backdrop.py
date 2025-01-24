import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from game.utils.vector import Vector


class MainBackdrop(pygame.sprite.Sprite):
    def __init__(self, top_left: Vector):
        super().__init__()
        self.image = pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/main_backdrop.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left.as_tuple()
