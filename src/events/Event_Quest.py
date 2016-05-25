#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Quest(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'adventure'
        self.desc = "Discard stuff to gain a gold"
        self.name = "Quest"
        self.cost = 0

    def special(self, game, player):
        """ You may discard an attack, two curses or six cards. If you do, gain a gold"""
        player.output("Discard any number of cards")
        player.output("If you discard an Attack Card or Two Curses or Six Cards you gain a Gold")
        discards = player.plrDiscardCards(anynum=True)
        attack_flag = False
        curses = 0
        for c in discards:
            if c.isAttack():
                attack_flag = True
            if c.name == 'Curse':
                curses += 1
        if len(discards) >= 6 or attack_flag or curses >= 2:
            player.gainCard('Gold')


###############################################################################
class Test_Quest(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Quest'], initcards=['Witch'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g.events['Quest']

    def test_with_attack(self):
        """ Use Quest with an attack card """
        self.plr.setHand('Witch')
        self.plr.test_input = ['witch', 'finish']
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.discardSize(), 2)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertIsNotNone(self.plr.inDiscard('Witch'))

    def test_with_curses(self):
        """ Use Quest with two curse cards """
        self.plr.setHand('Curse', 'Curse')
        self.plr.test_input = ['1', '2', 'finish']
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.discardSize(), 3)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertIsNotNone(self.plr.inDiscard('Curse'))

    def test_with_six_cards(self):
        """ Use Quest with six cards """
        self.plr.setHand('Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper')
        self.plr.test_input = ['1', '2', '3', '4', '5', '6', 'finish']
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.discardSize(), 7)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertIsNotNone(self.plr.inDiscard('Copper'))

    def test_with_five_cards(self):
        """ Use Quest with five cards """
        self.plr.setHand('Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Copper')
        self.plr.test_input = ['1', '2', '3', '4', '5', 'finish']
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.discardSize(), 5)
        self.assertIsNone(self.plr.inDiscard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
