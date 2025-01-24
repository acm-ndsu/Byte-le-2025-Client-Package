import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from game.utils.vector import Vector


class GameBackdrop(pygame.sprite.Sprite):
    def __init__(self, top_left: Vector):
        super().__init__()
        self.images: dict[str | int, pygame.Surface] = {
            0: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/game_backdrops/spring.png')),
            1: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/game_backdrops/summer.png')),
            2: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/game_backdrops/fall.png')),
            3: pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/game_backdrops/winter.png')),
        }

        self.image: pygame.Surface = self.images[0]
        self.season: int = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left.as_tuple()

    @property
    def season(self) -> int:
        return self.__season

    @season.setter
    def season(self, season: int) -> None:
        self.__season = season
        self.image = self.images[season]
