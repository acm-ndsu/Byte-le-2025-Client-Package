from __future__ import annotations

from game.commander_clash.character.stats import *
from game.commander_clash.moves.moves import *
from game.commander_clash.moves.moveset import Moveset
from game.common.enums import ObjectType, ClassType, RankType, CountryType
from game.common.game_object import GameObject
from game.config import HEALTH_MODIFIER, GENERIC_TRASH_NAME
from game.utils.vector import Vector


class Character(GameObject):
    """
    This is the superclass of all Character instances. Characters will have 3 stats (health, defense, speed);
    pre-determined moves that will allow for attacking, healing, buffing, and debuffing; and other properties that will
    help with the game mechanics.
    """

    def __init__(self, name: str = '', class_type: ClassType = ClassType.ATTACKER, health: int = 1,
                 attack: AttackStat = AttackStat(), defense: DefenseStat = DefenseStat(),
                 speed: SpeedStat = SpeedStat(), position: Vector | None = None,
                 country_type: CountryType = CountryType.URODA, moveset: Moveset = Moveset()):
        super().__init__()
        self.name: str = name
        self.object_type: ObjectType = ObjectType.CHARACTER
        self.class_type: ClassType = class_type
        self.current_health: int = health * HEALTH_MODIFIER
        self.max_health: int = health * HEALTH_MODIFIER
        self.attack: AttackStat = attack
        self.defense: DefenseStat = defense
        self.speed: SpeedStat = speed
        self.rank_type: RankType = RankType.GENERIC
        self.moveset: Moveset = moveset
        self.special_points: int = 0
        self.position: Vector | None = position
        self.took_action: bool = False
        self.country_type: CountryType = country_type
        self.is_dead: bool = False
        self.selected_move: Move | None = None
        self.index: int = -1

    def __eq__(self, other: Self | int) -> bool:
        if not isinstance(other, self.__class__):
            return False

        # return if all the attributes match for the two characters
        return (self.name == other.name
                and self.object_type == other.object_type
                and self.class_type == other.class_type
                and self.current_health == other.current_health
                and self.max_health == other.max_health
                and self.attack == other.attack
                and self.defense == other.defense
                and self.speed == other.speed
                and self.rank_type == other.rank_type
                and self.moveset == other.moveset
                and self.special_points == other.special_points
                and self.position == other.position
                and self.took_action == other.took_action
                and self.country_type == other.country_type
                and self.is_dead == other.is_dead
                and self.selected_move == other.selected_move)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        if name is None or not isinstance(name, str):
            raise ValueError(f'{self.__class__.__name__}.name must be a string. It is a(n) {name.__class__.__name__} '
                             f'and has the value of {name}')
        self.__name: str = name

    @property
    def class_type(self) -> ClassType:
        return self.__class_type

    @class_type.setter
    def class_type(self, class_type: ClassType) -> None:
        if ClassType is None or not isinstance(class_type, ClassType):
            raise ValueError(f'{self.__class__.__name__}.class_type must be a ClassType. '
                             f'It is a(n) {class_type.__class__.__name__} and has the value of {class_type}')
        self.__class_type: ClassType = class_type

    @property
    def current_health(self) -> int:
        return self.__current_health

    @current_health.setter
    def current_health(self, current_health: int) -> None:
        if current_health is None or not isinstance(current_health, int):
            raise ValueError(f'{self.__class__.__name__}.current_health must be an int. It is a(n) '
                             f'{current_health.__class__.__name__} and has the value of {current_health}')
        if current_health < 0:
            raise ValueError(f'{self.__class__.__name__}.current_health must be a positive int.')

        self.__current_health: int = current_health

    @property
    def max_health(self) -> int:
        return self.__max_health

    @max_health.setter
    def max_health(self, max_health: int) -> None:
        if max_health is None or not isinstance(max_health, int):
            raise ValueError(f'{self.__class__.__name__}.max_health must be an int. It is a(n) '
                             f'{max_health.__class__.__name__} and has the value of {max_health}')
        if max_health < 0:
            raise ValueError(f'{self.__class__.__name__}.max_health must be a positive int.')

        self.__max_health: int = max_health

    @property
    def attack(self) -> AttackStat:
        return self.__attack

    @attack.setter
    def attack(self, attack: AttackStat) -> None:
        if attack is None or not isinstance(attack, AttackStat):
            raise ValueError(f'{self.__class__.__name__}.attack must be an AttackStat. It is a(n) '
                             f'{attack.__class__.__name__} and has the value of {attack}')

        self.__attack: AttackStat = attack

    @property
    def defense(self) -> DefenseStat:
        return self.__defense

    @defense.setter
    def defense(self, defense: DefenseStat) -> None:
        if defense is None or not isinstance(defense, DefenseStat):
            raise ValueError(f'{self.__class__.__name__}.defense must be a DefenseStat. It is a(n) '
                             f'{defense.__class__.__name__} and has the value of {defense}')

        self.__defense: DefenseStat = defense

    @property
    def speed(self) -> SpeedStat:
        return self.__speed

    @speed.setter
    def speed(self, speed: SpeedStat) -> None:
        if speed is None or not isinstance(speed, SpeedStat):
            raise ValueError(f'{self.__class__.__name__}.speed must be a SpeedStat. '
                             f'It is a(n) {speed.__class__.__name__} and has the value of {speed}')

        self.__speed: SpeedStat = speed

    @property
    def special_points(self) -> int:
        return self.__special_points

    @special_points.setter
    def special_points(self, special_points: int) -> None:
        if special_points is None or not isinstance(special_points, int):
            raise ValueError(f'{self.__class__.__name__}.special_points must be an int. It is a(n) '
                             f'{special_points.__class__.__name__} and has the value of {special_points}')

        if special_points < 0:
            raise ValueError(f'{self.__class__.__name__}.special_points must be a positive int.')

        self.__special_points: int = special_points

    @property
    def moveset(self) -> Moveset:
        return self.__moveset

    @moveset.setter
    def moveset(self, moveset: Moveset) -> None:
        if moveset is None or not isinstance(moveset, Moveset):
            raise ValueError(f'{self.__class__.__name__}.moveset must be a Moveset. It is a(n) '
                             f'{moveset.__class__.__name__} and has the value of {moveset}')

        self.__moveset: Moveset = moveset

    @property
    def position(self) -> Vector | None:
        return self.__position

    @position.setter
    def position(self, position: Vector | None) -> None:
        if position is not None and not isinstance(position, Vector):
            raise ValueError(f'{self.__class__.__name__}.position must be a Vector or None. It is a(n) '
                             f'{position.__class__.__name__} and has the value of {position}')

        self.__position: Vector = position

    @property
    def took_action(self) -> bool:
        return self.__took_action

    @took_action.setter
    def took_action(self, took_action: bool) -> None:
        if took_action is None or not isinstance(took_action, bool):
            raise ValueError(f'{self.__class__.__name__}.took_action must be a bool. It is a(n) '
                             f'{took_action.__class__.__name__} and has the value of {took_action}')

        self.__took_action = took_action

    @property
    def country_type(self) -> CountryType:
        return self.__country_type

    @country_type.setter
    def country_type(self, country_type: CountryType) -> None:
        if country_type is None or not isinstance(country_type, CountryType):
            raise ValueError(f'{self.__class__.__name__}.country_type must be a CountryType. '
                             f'It is a(n) {country_type.__class__.__name__} and has the value of {country_type}')
        self.__country_type: CountryType = country_type

    @property
    def is_dead(self) -> bool:
        return self.__is_dead

    @is_dead.setter
    def is_dead(self, is_dead: bool) -> None:
        if is_dead is None or not isinstance(is_dead, bool):
            raise ValueError(f'{self.__class__.__name__}.is_dead must be a bool. It is a(n) '
                             f'{is_dead.__class__.__name__} and has the value of {is_dead}')
        self.__is_dead: bool = is_dead

    @property
    def selected_move(self) -> Move | None:
        return self.__selected_move

    @selected_move.setter
    def selected_move(self, selected_move: Move | None) -> None:
        if selected_move is not None and not isinstance(selected_move, Move):
            raise ValueError(f'{self.__class__.__name__}.selected_move must be a Move or None. It is a(n) '
                             f'{selected_move.__class__.__name__} and has the value of {selected_move}')
        self.__selected_move: Move | None = selected_move

    @property
    def index(self) -> int:
        return self.__index

    @index.setter
    def index(self, index: int) -> None:
        if index is None or not isinstance(index, int):
            raise ValueError(f'{self.__class__.__name__}.index must be an int. It is a(n) '
                             f'{index.__class__.__name__} and has the value of {index}')
        self.__index: int = index

    def get_nm(self):
        ...

    def get_s1(self):
        ...

    def get_s2(self):
        ...

    def get_opposing_country(self) -> CountryType:
        # returns the opposite country based on the given CountryType
        ...

    def is_defeated(self) -> bool:
        ...


class Generic(Character):
    """
    A class used to help with inheritance and polymorphism for the Generic Characters. This will not have any
    functionality.
    """

    def __init__(self, name: str = '', class_type: ClassType = ClassType.ATTACKER, health: int = 1,
                 attack: AttackStat = AttackStat(), defense: DefenseStat = DefenseStat(),
                 speed: SpeedStat = SpeedStat(), position: Vector | None = None,
                 country_type: CountryType = CountryType.URODA, moveset: Moveset = Moveset()):
        super().__init__(name, class_type, health, attack, defense, speed,
                         position, country_type, moveset)

        self.rank_type: RankType = RankType.GENERIC


class GenericAttacker(Generic):
    def __init__(self, name: str = '', class_type: ClassType = ClassType.ATTACKER, health: int = 1,
                 attack: AttackStat = AttackStat(), defense: DefenseStat = DefenseStat(),
                 speed: SpeedStat = SpeedStat(), position: Vector | None = None,
                 country_type: CountryType = CountryType.URODA, moveset: Moveset = Moveset()):
        super().__init__(name, class_type, health, attack, defense, speed,
                         position, country_type, moveset)

        # Object type given in char_position_generation based on country as well
        self.class_type: ClassType = ClassType.ATTACKER



class GenericHealer(Generic):
    def __init__(self, name: str = '', class_type: ClassType = ClassType.HEALER, health: int = 1,
                 attack: AttackStat = AttackStat(), defense: DefenseStat = DefenseStat(),
                 speed: SpeedStat = SpeedStat(), position: Vector | None = None,
                 country_type: CountryType = CountryType.URODA, moveset: Moveset = Moveset()):
        super().__init__(name, class_type, health, attack, defense, speed,
                         position, country_type, moveset)

        # Object type given in char_position_generation based on country as well
        self.class_type: ClassType = ClassType.HEALER


class GenericTank(Generic):
    def __init__(self, name: str = '', class_type: ClassType = ClassType.TANK, health: int = 1,
                 attack: AttackStat = AttackStat(), defense: DefenseStat = DefenseStat(),
                 speed: SpeedStat = SpeedStat(), position: Vector | None = None,
                 country_type: CountryType = CountryType.URODA, moveset: Moveset = Moveset()):
        super().__init__(name, class_type, health, attack, defense, speed,
                         position, country_type, moveset)

        # Object type given in char_position_generation based on country as well
        self.class_type: ClassType = ClassType.TANK


class GenericTrash(Generic):
    def __init__(self, name: str = GENERIC_TRASH_NAME, class_type: ClassType = ClassType.ATTACKER,
                 position: Vector | None = None, country_type: CountryType = CountryType.URODA):
        # No matter what, the stats should be set to 1, even the health
        super().__init__(name, class_type, 1, AttackStat(1), DefenseStat(1), SpeedStat(1),
                         position, country_type)

        self.object_type: ObjectType = ObjectType.GENERIC_TRASH
        self.class_type: ClassType = ClassType.ATTACKER

        # set the moveset here since it'll remain consistent
        self.moveset = Moveset((Debuff('Trashed Attack', TargetType.SELF, 0, None, -5, ObjectType.ATTACK_STAT),
                                Debuff('Trashed Defense', TargetType.SELF, 0, None, -5, ObjectType.DEFENSE_STAT),
                                Debuff('Trashed Speed', TargetType.SELF, 0, None, -5, ObjectType.SPEED_STAT)))


class Leader(Character):
    def __init__(self, name: str = '', class_type: ClassType = ClassType.ATTACKER, health: int = 1,
                 attack: AttackStat = AttackStat(), defense: DefenseStat = DefenseStat(),
                 speed: SpeedStat = SpeedStat(), position: Vector | None = None,
                 country_type: CountryType = CountryType.URODA, moveset: Moveset = Moveset()):
        super().__init__(name, class_type, health, attack, defense, speed,
                         position, country_type, moveset)

        self.rank_type: RankType = RankType.LEADER
