import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from game.utils.vector import Vector


class Headshot(pygame.sprite.Sprite):
    """
    This class is for loading an image for the headshot of the character, depending on the character.
    Implemented in character_info_template.py.
    """

    def __init__(self, top_left: Vector):
        super().__init__()
        self.images: dict[str | int, pygame.Surface] = {
            'turpis_anahita': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/anahita_headshot.png')),
            'turpis_berry': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/berry_headshot.png')),
            'turpis_ninlil': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/ninlil_headshot.png')),
            'turpis_calmus': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/calmus_headshot.png')),
            'turpis_irwin': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/irwin_headshot.png')),
            'turpis_fultra': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/fultra_headshot.png')),
            'uroda_anahita': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/anahita_headshot.png')),
            'uroda_berry': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/berry_headshot.png')),
            'uroda_ninlil': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/ninlil_headshot.png')),
            'uroda_calmus': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/calmus_headshot.png')),
            'uroda_irwin': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/irwin_headshot.png')),
            'uroda_fultra': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/fultra_headshot.png')),
            'turpis_attacker': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/turpis_generic_attacker_headshot.png')),
            'turpis_tank': pygame.image.load(os.path.join(os.getcwd(),'visualizer/images/staticsprites/headshot/turpis_generic_tank_headshot.png')),
            'turpis_healer': pygame.image.load(os.path.join(os.getcwd(),'visualizer/images/staticsprites/headshot/turpis_generic_healer_headshot.png')),
            'uroda_attacker': pygame.image.load(os.path.join(os.getcwd(),'visualizer/images/staticsprites/headshot/uroda_generic_attacker_headshot.png')),
            'uroda_tank': pygame.image.load(os.path.join(os.getcwd(),'visualizer/images/staticsprites/headshot/uroda_generic_tank_headshot.png')),
            'uroda_healer': pygame.image.load(os.path.join(os.getcwd(),'visualizer/images/staticsprites/headshot/uroda_generic_healer_headshot.png')),
            'uroda_missing': pygame.image.load(os.path.join(os.getcwd(),'visualizer/images/staticsprites/headshot/atleastheshappy.png')),
            'turpis_missing': pygame.image.load(os.path.join(os.getcwd(), 'visualizer/images/staticsprites/headshot/atleastheshappy.png')),
        }

        self.image: pygame.Surface = self.images['uroda_missing']
        self.character: str | int = 'uroda_missing'
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left.as_tuple()

    @property
    def character(self) -> str | int:
        return self.__character

    @character.setter
    def character(self, character: str | int) -> None:
        self.__character = character
        self.image = self.images[character]
