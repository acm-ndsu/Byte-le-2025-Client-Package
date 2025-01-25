from game.commander_clash.character.character import *
from game.common.enums import ObjectType, CountryType, ClassType
from game.common.game_object import GameObject


class TeamManager(GameObject):
    """
    `TeamManager class notes:`

    TeamManager (replacing the Avatar class) inherits from GameObject

    Values:
        Team - list of characters (max of three) with a default generic team
        Score - an int for the current score of this team with a default set to 0

    Methods:
        speed_sort() - returns sorted list of team by fastest to slowest speed
        filter_by_type(class_type) - returns list of characters of the specified ClassType
    """

    ''' 
    The team default has a warning "Default argument value is mutable".
    This is due to the list being mutable and if the Character() default is changed in the future, 
    the default for team in the TeamManager class is also changed. This, for the most part, can be 
    ignored, but reminder to exercise caution when adjusting the Character class for this reason.
    '''

    def __init__(self, team: list[Character] = [GenericTrash(), GenericTrash(), GenericTrash()],
                 country_type: CountryType = CountryType.URODA, team_name: str = ''):
        super().__init__()
        self.object_type: ObjectType = ObjectType.TEAMMANAGER
        self.team: list[Character] = team
        self.country_type = country_type
        self.score: int = 0
        self.team_name: str = team_name
        self.dead_team: list[Character] = []

    # Getters and Setters
    @property
    def team(self) -> list[Character]:
        return self.__team

    @team.setter
    def team(self, team: list[Character]) -> None:
        if team is None or not isinstance(team, list):
            raise ValueError(
                f'{self.__class__.__name__}.team must be a list[Character]. It is a(n) {team.__class__.__name__} '
                f'and has the value of {team}.')
        for i in team:
            if i is None or not isinstance(i, Character):
                raise ValueError(
                    f'{self.__class__.__name__}.team must be a list[Character]. It contains a(n) '
                    f'{i.__class__.__name__} with the value {i}.')
        if len(team) > 3:
            raise ValueError(f'{self.__class__.__name__}.team must be a list[Character] with a length of three or '
                             f'less. It has a length of {len(team)}.')
        self.__team: list[Character] = team

    @property
    def object_type(self) -> ObjectType:
        return self.__object_type

    @object_type.setter
    def object_type(self, object_type: ObjectType) -> None:
        if object_type is None or not isinstance(object_type, ObjectType):
            raise ValueError(
                f'{self.__class__.__name__}.object_type must be an ObjectType. It is a(n) '
                f'{object_type.__class__.__name__} and has the value of {object_type}.')
        self.__object_type: ObjectType = object_type

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, score: int) -> None:
        if score is None or not isinstance(score, int):
            raise ValueError(f'{self.__class__.__name__}.score must be an int. It is a(n) {score.__class__.__name__} '
                             f'and has the value of {score}.')
        self.__score: int = score

    @property
    def team_name(self) -> str | None:
        return self.__team_name

    @team_name.setter
    def team_name(self, team_name: str | None) -> None:
        if team_name is not None and not isinstance(team_name, str):
            raise ValueError(
                f'{self.__class__.__name__}.team_name must be a String or None. It is a(n) '
                f'{team_name.__class__.__name__} and has the value of {team_name}.')
        self.__team_name = team_name

    @property
    def dead_team(self) -> list[Character]:
        return self.__dead_team

    @dead_team.setter
    def dead_team(self, dead_team: list[Character]) -> None:
        if dead_team is None or not isinstance(dead_team, list):
            if dead_team is None or not isinstance(dead_team, list):
                raise ValueError(
                    f'{self.__class__.__name__}.team must be a list[Character]. It is a(n) {dead_team.__class__.__name__} '
                    f'and has the value of {dead_team}.')
            for i in dead_team:
                if i is None or not isinstance(i, Character):
                    raise ValueError(
                        f'{self.__class__.__name__}.team must be a list[Character]. It contains a(n) '
                        f'{i.__class__.__name__} with the value {i}.')
                
        self.__dead_team = dead_team

    # Method to sort team based on character speed, fastest to slowest (descending order)
    def speed_sort(self) -> None:
        """
        Sorts the team by the speed stat and rank type in descending order. If a Leader and a Generic have the same
        speed and are on the same team, the leader will take its action first.
        """
        ...

    # Method to filter the team by a class type
    def filter_by_type(self, class_type: ClassType) -> list[Character]:
        """
        Returns characters from this team that have the specified class_type.
        """
        ...

    def get_active_character(self, ordered_teams: list[tuple[Character | None, Character | None]],
                             active_pair_index: int) -> Character:
        """
        Using the GameBoard's ordered_teams list, this will return the character from this team manager that will next
        take its turn. None is returned if a character cannot take its turn yet.
        """
        ...


    def update_character(self, character: Character) -> None:
        """
        Updates the team with the given character to record any changes if the character is in the TeamManager's team.
        """
        ...

    def get_character(self, name: str = '') -> Character | None:
        """
        Returns a Character based off the given name. If the name is not found in the team, returns None.
        """
        ...

    def organize_dead_characters(self) -> None:
        """
        Moves any characters in the team manager from the team reference to the dead_team reference
        """
        ...

    def everyone_is_defeated(self) -> bool:
        ...

    def everyone_took_action(self) -> bool:
        ...
