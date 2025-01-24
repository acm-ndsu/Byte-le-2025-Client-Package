from game.commander_clash.character.character import Character
from game.commander_clash.generation.character_generation import *
from game.common.enums import SelectLeader, SelectGeneric, ClassType


def validate_team_selection(
        enums: tuple[SelectGeneric, SelectLeader, SelectGeneric]) -> list[Character]:
    """
    Checks if the given tuple has SelectLeader, SelectGeneric, SelectGeneric. If any of the characters are not the class
    they should be, it will be replaced with a Generic Attacker
    """

    # create a dict to map all the selection enums to their ClassType
    classes_map: dict[SelectLeader | SelectGeneric, ClassType] = {
        SelectLeader.ANAHITA: ClassType.HEALER,
        SelectLeader.BERRY: ClassType.HEALER,
        SelectLeader.FULTRA: ClassType.ATTACKER,
        SelectLeader.NINLIL: ClassType.ATTACKER,
        SelectLeader.IRWIN: ClassType.TANK,
        SelectLeader.CALMUS: ClassType.TANK,
        SelectGeneric.GEN_ATTACKER: ClassType.ATTACKER,
        SelectGeneric.GEN_HEALER: ClassType.HEALER,
        SelectGeneric.GEN_TANK: ClassType.TANK,
        SelectGeneric.GEN_TRASH: ClassType.ATTACKER
    }

    # a reference for what will become Generic Trash; will always being a Generic Attacker
    generic_trash_enum: SelectGeneric = SelectGeneric.GEN_TRASH

    # unpack the given tuple of Selection enums to be individual objects
    selection1, selection2, selection3 = enums

    # check for misplaced enums (e.g., SelectGeneric is where SelectLeader should be in the given in tuple)
    if not isinstance(selection1, SelectGeneric):
        selection1 = generic_trash_enum
    if not isinstance(selection2, SelectLeader):
        selection2 = generic_trash_enum
    if not isinstance(selection3, SelectGeneric):
        selection3 = generic_trash_enum

    # if all 3 selections are Generic Trash, differentiate names, assign index values, and return
    if selection1 == selection2 == selection3 == generic_trash_enum:
        characters: list[Character] = [generate_generic_trash(), generate_generic_trash(), generate_generic_trash()]

        # make the names unique
        __differentiate_names(characters)

        for x in range(0, 3):
            characters[x].index = x

        return characters

    # if all 3 characters are the same ClassType, replace the selection 2 IF selections 1 & 3 are NOT generic trash
    if (classes_map[selection1] == classes_map[selection2] == classes_map[selection3]
            and
            (selection1.value != SelectGeneric.GEN_TRASH.value and selection2.value != SelectGeneric.GEN_TRASH.value)):
        selection2 = SelectGeneric.GEN_TRASH

        gen1, trash, gen2 = [__convert_to_character(member) for member in [selection1, selection2, selection3]]

        characters: list[Character] = [gen1, trash, gen2]

        # make the names unique
        __differentiate_names(characters)

        for x in range(0, 3):
            characters[x].index = x

        return characters

    # reevaluate the enums after checking for misplaced enums
    valid_team: tuple[SelectLeader | SelectGeneric, SelectLeader | SelectGeneric,
                      SelectLeader | SelectGeneric] = (selection1, selection2, selection3)
    classes: list[ClassType | None] = [classes_map.get(member, None) for member in valid_team
                                       if member.value != SelectGeneric.GEN_TRASH.value]

    # count occurrences of each class by mapping the ClassType to an int representing the count
    class_counts = {ClassType.ATTACKER: 0, ClassType.HEALER: 0, ClassType.TANK: 0}
    for cls in classes:
        if cls in class_counts:
            class_counts[cls] += 1

    # resolve classes that are represented too often
    for cls, count in class_counts.items():
        if count > 2:
            for i in range(len(classes)):
                if classes[i] == cls:
                    # make the tuple of valid_team enums a list to handle it better
                    valid_team: list[SelectLeader | SelectGeneric] = list(valid_team)
                    valid_team[i] = generic_trash_enum
                    classes[i] = classes_map[generic_trash_enum]

                    # convert back to a tuple to maintain integrity
                    valid_team = tuple(valid_team)

                    break

    gen1, leader, gen2 = [__convert_to_character(member) for member in valid_team]

    characters: list[Character] = [gen1, leader, gen2]

    # make the names unique
    __differentiate_names(characters)

    for x in range(0, 3):
        characters[x].index = x

    # return a list of the characters in the order they would appear in the GameBoard
    return characters

def __convert_to_character(enum: SelectGeneric | SelectLeader):
    """
    A helper method that calls the appropriate character generation mehtod based on the given enum.
    """
    match enum:
        case SelectLeader.ANAHITA:
            return generate_anahita()
        case SelectLeader.BERRY:
            return generate_berry()
        case SelectLeader.FULTRA:
            return generate_fultra()
        case SelectLeader.NINLIL:
            return generate_ninlil()
        case SelectLeader.CALMUS:
            return generate_calmus()
        case SelectLeader.IRWIN:
            return generate_irwin()
        case SelectGeneric.GEN_ATTACKER:
            return generate_generic_attacker()
        case SelectGeneric.GEN_HEALER:
            return generate_generic_healer()
        case SelectGeneric.GEN_TANK:
            return generate_generic_tank()
        case SelectGeneric.GEN_TRASH:
            return generate_generic_trash()


def __differentiate_names(characters: list[Character]) -> None:
    """
    A helper method that will append an incrementing int to a character's name if there is a duplicate. The number
    starts at 2.
    """

    num: int = 2
    names: list[str] = []

    for character in characters:
        if character.name in names:
            character.name += f' {num}'
            num += 1

        names.append(character.name)
