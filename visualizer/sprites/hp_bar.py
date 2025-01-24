import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from game.utils.vector import Vector


class HPBar(pygame.sprite.Sprite):
    """
    This class is for loading the images for the health of a character.
    Implemented in character_info_template.py.
    """

    def __init__(self, top_left: Vector):
        super().__init__()
        self.images: dict[str | int, pygame.Surface] = {
            0: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/hp_bar/hp_bar_0.png')),
            1: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/hp_bar/hp_bar_1.png')),
            2: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/hp_bar/hp_bar_2.png')),
            3: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/hp_bar/hp_bar_3.png')),
            4: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/hp_bar/hp_bar_4.png')),
            5: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/hp_bar/hp_bar_5.png')),
            6: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/hp_bar/hp_bar_6.png')),
            7: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/hp_bar/hp_bar_7.png')),
            8: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/hp_bar/hp_bar_8.png')),
            9: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/hp_bar/hp_bar_9.png')),
            10: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/hp_bar/hp_bar_10.png')),
        }

        self.image: pygame.Surface = self.images[0]
        self.hp: str | int = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left.as_tuple()

    @property
    def hp(self) -> str | int:
        return self.__hp

    @hp.setter
    def hp(self, hp: str | int) -> None:
        self.__hp = hp
        self.image = self.images[hp]
