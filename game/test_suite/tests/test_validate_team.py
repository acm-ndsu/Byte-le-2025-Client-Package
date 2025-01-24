import unittest

from game.commander_clash.character.character import Leader, GenericAttacker, GenericTrash, Character
from game.commander_clash.validate_team import validate_team_selection as validate
from game.common.enums import SelectLeader, SelectGeneric
from game.config import GENERIC_TRASH_NAME


class TestValidateTeam(unittest.TestCase):
    """
    Tests the `validate_team_selection` method and what it returns for valid and invalid team selections.
    """

    def setUp(self):
        self.valid_team: tuple[SelectGeneric, SelectLeader, SelectGeneric] = (SelectGeneric.GEN_ATTACKER,
                                                                              SelectLeader.ANAHITA,
                                                                              SelectGeneric.GEN_ATTACKER)

        self.invalid_team: tuple[SelectLeader, SelectGeneric, SelectLeader] = (SelectLeader.ANAHITA,
                                                                               SelectGeneric.GEN_ATTACKER,
                                                                               SelectLeader.BERRY)

    def test_valid_team(self) -> None:
        result: list[Character] = validate(self.valid_team)

        # test that all the characters are instances of the correct class
        self.assertTrue(isinstance(result[0], GenericAttacker))
        self.assertTrue(isinstance(result[1], Leader))
        self.assertTrue(isinstance(result[2], GenericAttacker))

    def test_invalid_team_leader_gen_leader(self) -> None:
        # returns true if all characters returned from the `validate_team_selection()` are GenericTrash
        team: list[Character] = validate(self.invalid_team)
        self.assertTrue(all([isinstance(character, GenericTrash) for character in team]))

        # check that any duplicate characters have an identifying int next to their name by using the last character
        self.assertEqual(team[0].name[-1], GENERIC_TRASH_NAME[-1])
        self.assertEqual(team[1].name[-1], '2')
        self.assertEqual(team[2].name[-1], '3')

    def test_team_of_one_class_type(self) -> None:
        # if a player tries to make a team with all one class type (e.g., Tank, Tank, Tank), the leader should be
        # replaced with Generic Trash
        self.invalid_team: tuple[SelectGeneric, SelectLeader, SelectGeneric] = (SelectGeneric.GEN_ATTACKER,
                                                                                SelectLeader.FULTRA,
                                                                                SelectGeneric.GEN_ATTACKER)
        team: list[Character] = validate(self.invalid_team)

        # ensure the leader is generic trash and that the other two generics didn't change
        self.assertTrue(isinstance(team[0], GenericAttacker))
        self.assertTrue(isinstance(team[1], GenericTrash))
        self.assertTrue(isinstance(team[2], GenericAttacker))

        # check that any duplicate characters have an identifying int next to their name by using the last character
        self.assertEqual(team[0].name,  'Attacker')
        self.assertEqual(team[1].name, GENERIC_TRASH_NAME)
        self.assertEqual(team[2].name[-1], '2')

    def test_team_of_one_class_type_with_invalid_leader(self) -> None:
        # if given a full team of generics, only the character in the leader slot should change to generic trash
        self.invalid_team: tuple[SelectGeneric, SelectGeneric, SelectGeneric] = (SelectGeneric.GEN_ATTACKER,
                                                                               SelectGeneric.GEN_ATTACKER,
                                                                               SelectGeneric.GEN_ATTACKER)
        team: list[Character] = validate(self.invalid_team)

        # ensure the leader is generic trash and that the other two generics didn't change
        self.assertTrue(isinstance(team[0], GenericAttacker))
        self.assertTrue(isinstance(team[1], GenericTrash))
        self.assertTrue(isinstance(team[2], GenericAttacker))

        # check that any duplicate characters have an identifying int next to their name by using the last character
        self.assertTrue(team[0].name, 'Attacker')
        self.assertTrue(team[1].name, GENERIC_TRASH_NAME)
        self.assertTrue(team[2].name[-1], 2)

    def test_team_of_leader_leader_generic(self) -> None:
        self.invalid_team: tuple[SelectLeader, SelectLeader, SelectGeneric] = (SelectLeader.ANAHITA,
                                                                               SelectLeader.ANAHITA,
                                                                               SelectGeneric.GEN_HEALER)
        team: list[Character] = validate(self.invalid_team)

        # check that the first SelectLeader became generic trash
        self.assertEqual(team[0].name, GENERIC_TRASH_NAME)
        self.assertEqual(team[1].name, 'Anahita')
        self.assertEqual(team[2].name, 'Healer')

