import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from game.utils.vector import Vector


class SPBar(pygame.sprite.Sprite):
    """
    This class is for loading the images for the special points of a character.
    Implemented in character_info_template.py.
    """
    def __init__(self, top_left: Vector):
        super().__init__()
        self.images: dict[str | int, pygame.Surface] = {
            0: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/sp_bar/sp_bar_0.png')),
            1: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/sp_bar/sp_bar_1.png')),
            2: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/sp_bar/sp_bar_2.png')),
            3: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/sp_bar/sp_bar_3.png')),
            4: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/sp_bar/sp_bar_4.png')),
            5: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/sp_bar/sp_bar_5.png')),
        }

        self.image: pygame.Surface = self.images[0]
        self.sp: str | int = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left.as_tuple()

    @property
    def sp(self) -> str | int:
        return self.__sp

    @sp.setter
    def sp(self, sp: str | int) -> None:
        self.__sp = sp
        self.image = self.images[sp]
