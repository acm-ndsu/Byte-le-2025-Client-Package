import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

from game.common.enums import RankType
from game.utils.vector import Vector
from visualizer.templates.info_template import InfoTemplate
from visualizer.templates.character_info_template import CharacterInfoTemplate
from visualizer.utils.text import Text


class TeamInfoTemplate(InfoTemplate):
    def __init__(self, screen: pygame.Surface, topleft: Vector, size: Vector, font: str, color: str,
                 country: int) -> None:
        super().__init__(screen, topleft, size, font, color)
        """
        Displays a Country name and Team name with the font size of 32
        and instantiates the character info templates
        """

        self.country = country
        self.country_text: Text = Text(screen, text=f'{"Uroda" if country == 1 else "Turpis"}',
                                       font_size=32, font_name=self.font, color=self.color,
                                       position=Vector.add_vectors(self.topleft, Vector(x=35, y=15)))

        # Character Info Templates instantiated here, in order of first generic, leader, second generic
        self.character1 = CharacterInfoTemplate(screen, Vector.add_vectors(self.topleft, Vector(x=38, y=56)),
                                                Vector(x=350, y=168),
                                                self.font, self.color, self.country, 0)
        self.character2 = CharacterInfoTemplate(screen, Vector.add_vectors(self.topleft, Vector(x=38, y=237)),
                                                Vector(x=350, y=168),
                                                self.font, self.color, self.country, 1)
        self.character3 = CharacterInfoTemplate(screen, Vector.add_vectors(self.topleft, Vector(x=38, y=418)),
                                                Vector(x=350, y=168),
                                                self.font, self.color, self.country, 2)

    def recalc_animation(self, turn_log: dict) -> None:
        team_name: str = [client['team_name']
                          for client in turn_log['clients']
                          if client['team_manager']['country_type'] == self.country][0]
        team_name = team_name[:20] + '...' if len(team_name) > 20 else team_name
        self.country_text.text = f'{"Uroda" if self.country == 1 else "Turpis"}: {team_name}'
        self.character1.recalc_animation(turn_log)
        self.character2.recalc_animation(turn_log)
        self.character3.recalc_animation(turn_log)

    def render(self) -> None:
        super().render()
        self.country_text.render()
        self.character1.render()
        self.character2.render()
        self.character3.render()
