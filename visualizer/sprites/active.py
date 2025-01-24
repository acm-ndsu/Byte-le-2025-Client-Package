import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from game.utils.vector import Vector


class Active(pygame.sprite.Sprite):
    """
    This class is for the Active game image, that is used to represent when a character is actively taking their turn.
    Used in character_info_template.py.
    """

    def __init__(self, top_left: Vector):
        super().__init__()
        self.image = pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/active.png')).convert()
        self.transparent: bool = False
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left.as_tuple()

    @property
    def transparent(self) -> bool:
        return self.__transparent

    @transparent.setter
    def transparent(self, transparent: bool) -> None:
        self.__transparent = transparent
        self.image.set_alpha(0) if self.__transparent is True else self.image.set_alpha(255)
