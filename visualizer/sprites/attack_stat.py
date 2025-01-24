import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

from game.utils.vector import Vector


class AttackStat(pygame.sprite.Sprite):
    """
    This class is for loading an image for the attack stat for each character on the visualizer. It includes an image
    for when it is neutral, buffed, and debuffed. Implemented in character_info_template.py.
    """

    def __init__(self, top_left: Vector):
        super().__init__()
        self.images: dict[str | int, pygame.Surface] = {
            0: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/attack_stat/attack_neutral.png')),
            1: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/attack_stat/attack_buff.png')),
            2: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/attack_stat/attack_debuff.png')),
        }

        self.image: pygame.Surface = self.images[0]
        self.attack_stat: str | int = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left.as_tuple()

    @property
    def attack_stat(self) -> str | int:
        return self.__attack_stat

    @attack_stat.setter
    def attack_stat(self, attack_stat: str | int) -> None:
        self.__attack_stat = attack_stat
        self.image = self.images[attack_stat]
