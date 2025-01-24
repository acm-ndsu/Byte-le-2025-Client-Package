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
        self.team = sorted(self.team, key=lambda character: (character.speed, character.rank_type.value), reverse=True)

    # Method to filter the team by a class type
    def filter_by_type(self, class_type: ClassType) -> list[Character]:
        """
        Returns characters from this team that have the specified class_type.
        """
        return [character for character in self.team if character.class_type is class_type]

    def get_active_character(self, ordered_teams: list[tuple[Character | None, Character | None]],
                             active_pair_index: int) -> Character:
        """
        Using the GameBoard's ordered_teams list, this will return the character from this team manager that will next
        take its turn. None is returned if a character cannot take its turn yet.
        """

        active_chars: tuple[Character | None, Character | None] = ordered_teams[active_pair_index]

        # index will be 0 if Uroda, 1 if Turpis
        tuple_index_to_use: int = self.country_type.value - 1

        active_char: Character | None = active_chars[tuple_index_to_use]

        return active_char


    def update_character(self, character: Character) -> None:
        """
        Updates the team with the given character to record any changes if the character is in the TeamManager's team.
        """
        for index in range(len(self.team)):
            # if the given character is found based on the unique name the character has, update it in the team manager
            if self.team[index].name == character.name:
                self.team[index] = character

    def get_character(self, name: str = '') -> Character | None:
        """
        Returns a Character based off the given name. If the name is not found in the team, returns None.
        """
        for char in self.team:
            if char.name == name:
                return char

    def organize_dead_characters(self) -> None:
        """
        Moves any characters in the team manager from the team reference to the dead_team reference
        """
        for character in self.team:
            if character.is_dead:
                self.dead_team.append(character)
                self.team.remove(character)

    def everyone_is_defeated(self) -> bool:
        return len(self.dead_team) == 3

    def everyone_took_action(self) -> bool:
        return all([character.took_action for character in self.team])

    # To and From Json
    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['team'] = [character.to_json() for character in self.team]
        data['dead_team'] = [character.to_json() for character in self.dead_team]
        data['country_type'] = self.country_type.value
        data['score'] = self.score
        data['team_name'] = self.team_name
        return data

    def __from_json_helper(self, data: dict) -> Character:
        temp: ObjectType = ObjectType(data['object_type'])

        match temp:
            case ObjectType.CHARACTER:
                return Character().from_json(data)
            case ObjectType.GENERIC_TRASH:
                return GenericTrash().from_json(data)
            case (ObjectType.ANAHITA | ObjectType.BERRY | ObjectType.FULTRA |
                  ObjectType.NINLIL | ObjectType.CALMUS | ObjectType.IRWIN):
                return Leader().from_json(data)
            case ObjectType.URODA_GENERIC_ATTACKER | ObjectType.TURPIS_GENERIC_ATTACKER:
                return GenericAttacker().from_json(data)
            case ObjectType.URODA_GENERIC_HEALER | ObjectType.TURPIS_GENERIC_HEALER:
                return GenericHealer().from_json(data)
            case ObjectType.URODA_GENERIC_TANK | ObjectType.TURPIS_GENERIC_TANK:
                return GenericTank().from_json(data)
            case _:
                raise ValueError(
                    f'The object type of the object is not handled properly. The object type passed in is {temp}.')

    def from_json(self, data: dict) -> Self:
        super().from_json(data)

        # converts each json object in the 'team' to be a Character object and creates a list with them
        self.team = [self.__from_json_helper(obj) for obj in data['team']] if len(data['team']) > 0 else []

        self.dead_team = [self.__from_json_helper(obj)
                          for obj in data['dead_team']] if len(data['dead_team']) > 0 else []

        self.country_type = CountryType(data['country_type'])
        self.score = data['score']
        self.team_name = data['team_name']
        return self
