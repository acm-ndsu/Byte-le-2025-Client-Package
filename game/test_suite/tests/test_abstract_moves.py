import unittest

from game.commander_clash.moves.abstract_moves import *


class TestAbstractMoves(unittest.TestCase):
    def setUp(self) -> None:
        self.abstract_move: AbstractMove = AbstractMove(TargetType.SINGLE_OPP)
        self.abstract_attack: AbstractAttack = AbstractAttack(damage_points=10)
        self.abstract_heal: AbstractHeal = AbstractHeal(heal_points=10)
        self.abstract_buff: AbstractBuff = AbstractBuff(buff_amount=1)
        self.abstract_debuff: AbstractDebuff = AbstractDebuff(debuff_amount=-1)

    def test_base_setters_errors(self):
        with self.assertRaises(ValueError) as e:
            self.abstract_move.move_type = 12
        self.assertEqual(str(e.exception), f'{self.abstract_move.__class__.__name__}.move_type must be a MoveType. '
                                           f'It is a(n) {int.__name__} and has the value of {12}.')
        with self.assertRaises(ValueError) as e:
            self.abstract_move.move_type = None
        self.assertEqual(str(e.exception), f'{self.abstract_move.__class__.__name__}.move_type must be a MoveType. '
                                           f'It is a(n) NoneType and has the value of {None}.')

        with self.assertRaises(ValueError) as e:
            self.abstract_move.target_type = 12
        self.assertEqual(str(e.exception), f'{self.abstract_move.__class__.__name__}.target_type must be a TargetType. '
                                           f'It is a(n) {int.__name__} and has the value of {12}.')

        with self.assertRaises(ValueError) as e:
            self.abstract_move.target_type = None
        self.assertEqual(str(e.exception), f'{self.abstract_move.__class__.__name__}.target_type must be a TargetType. '
                                           f'It is a(n) NoneType and has the value of {None}.')

        with self.assertRaises(ValueError) as e:
            self.abstract_attack.damage_points = 'hey'
        self.assertEqual(str(e.exception), f'{self.abstract_attack.__class__.__name__}.damage_points must be an int. '
                                           f'It is a(n) {str.__name__} and has the value of hey.')

        with self.assertRaises(ValueError) as e:
            self.abstract_attack.damage_points = None
        self.assertEqual(str(e.exception),
                         f'{self.abstract_attack.__class__.__name__}.damage_points must be an int. '
                         f'It is a(n) NoneType and has the value of None.')

        with self.assertRaises(ValueError) as e:
            self.abstract_heal.heal_points = 'hey'
        self.assertEqual(str(e.exception), f'{self.abstract_heal.__class__.__name__}.heal_points must be an int. '
                                           f'It is a(n) {str.__name__} and has the value of hey.')

        with self.assertRaises(ValueError) as e:
            self.abstract_heal.heal_points = None
        self.assertEqual(str(e.exception),
                         f'{self.abstract_heal.__class__.__name__}.heal_points must be an int. '
                         f'It is a(n) NoneType and has the value of None.')

        with self.assertRaises(ValueError) as e:
            self.abstract_buff.buff_amount = 'hey'
        self.assertEqual(str(e.exception), f'{self.abstract_buff.__class__.__name__}.buff_amount must be an int. '
                                           f'It is a(n) {str.__name__} and has the value of hey.')

        with self.assertRaises(ValueError) as e:
            self.abstract_buff.buff_amount = None
        self.assertEqual(str(e.exception),
                         f'{self.abstract_buff.__class__.__name__}.buff_amount must be an int. '
                         f'It is a(n) NoneType and has the value of None.')

        with self.assertRaises(ValueError) as e:
            self.abstract_debuff.debuff_amount = 'hey'
        self.assertEqual(str(e.exception), f'{self.abstract_debuff.__class__.__name__}.debuff_amount must be an int. '
                                           f'It is a(n) {str.__name__} and has the value of hey.')

        with self.assertRaises(ValueError) as e:
            self.abstract_debuff.debuff_amount = None
        self.assertEqual(str(e.exception),
                         f'{self.abstract_debuff.__class__.__name__}.debuff_amount must be an int. '
                         f'It is a(n) NoneType and has the value of None.')

    def test_abstract_move_json(self):
        data: dict = self.abstract_move.to_json()
        ab_move: AbstractMove = AbstractMove().from_json(data)
        self.assertEqual(self.abstract_move.object_type, ab_move.object_type)
        self.assertEqual(self.abstract_move.target_type, ab_move.target_type)
        self.assertEqual(self.abstract_move.move_type, ab_move.move_type)

    def test_abstract_attack_json(self):
        data: dict = self.abstract_attack.to_json()
        ab_attack: AbstractAttack = AbstractAttack().from_json(data)
        self.assertEqual(self.abstract_attack.object_type, ab_attack.object_type)
        self.assertEqual(self.abstract_attack.target_type, ab_attack.target_type)
        self.assertEqual(self.abstract_attack.move_type, ab_attack.move_type)
        self.assertEqual(self.abstract_attack.damage_points, ab_attack.damage_points)

    def test_abstract_heal_json(self):
        data: dict = self.abstract_heal.to_json()
        ab_heal: AbstractHeal = AbstractHeal().from_json(data)
        self.assertEqual(self.abstract_heal.object_type, ab_heal.object_type)
        self.assertEqual(self.abstract_heal.target_type, ab_heal.target_type)
        self.assertEqual(self.abstract_heal.move_type, ab_heal.move_type)
        self.assertEqual(self.abstract_heal.heal_points, ab_heal.heal_points)

    def test_abstract_buff_json(self):
        data: dict = self.abstract_buff.to_json()
        ab_buff: AbstractBuff = AbstractBuff().from_json(data)
        self.assertEqual(self.abstract_buff.object_type, ab_buff.object_type)
        self.assertEqual(self.abstract_buff.target_type, ab_buff.target_type)
        self.assertEqual(self.abstract_buff.move_type, ab_buff.move_type)
        self.assertEqual(self.abstract_buff.buff_amount, ab_buff.buff_amount)

    def test_abstract_debuff_json(self):
        data: dict = self.abstract_debuff.to_json()
        ab_debuff: AbstractDebuff = AbstractDebuff().from_json(data)
        self.assertEqual(self.abstract_debuff.object_type, ab_debuff.object_type)
        self.assertEqual(self.abstract_debuff.target_type, ab_debuff.target_type)
        self.assertEqual(self.abstract_debuff.move_type, ab_debuff.move_type)
        self.assertEqual(self.abstract_debuff.debuff_amount, ab_debuff.debuff_amount)
