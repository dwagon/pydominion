#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Paddock """

import unittest
import Game
from Card import Card


###############################################################################
class Card_Paddock(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = Game.MENAGERIE
        self.desc = """+2 Coin; Gain 2 Horses. +1 Action per empty Supply pile."""
        self.name = 'Paddock'
        self.coin = 2
        self.cost = 5
        self.required_cards = [('Card', 'Horse')]

    def special(self, game, player):
        player.gainCard('Horse')
        player.gainCard('Horse')
        empties = sum([1 for st in game.cardpiles if game[st].is_empty()])
        player.addActions(empties)


###############################################################################
class Test_Paddock(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Paddock', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Paddock'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard_one_stack(self):
        while True:
            c = self.g['Moat'].remove()
            if not c:
                break
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNotNone(self.plr.in_discard('Horse'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
