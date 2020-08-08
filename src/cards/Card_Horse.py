#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Horse """

import unittest
import Game
from Card import Card


###############################################################################
class Card_Horse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = Game.MENAGERIE
        self.desc = "+2 Cards; +1 Action; Return this to its pile."
        self.name = "Horse"
        self.purchasable = False
        self.insupply = False
        self.actions = 1
        self.cards = 2
        self.cost = 0
        self.numcards = 30

    def special(self, game, player):
        player.discardCard(self)
        game['Horse'].add()
        player.played.remove(self)
        player.discardpile.remove(self)


###############################################################################
class Test_Horse(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Horse"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Horse"].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNone(self.plr.in_played('Horse'))
        self.assertEqual(self.plr.handSize(), 5 + 2)
        self.assertEqual(self.plr.get_actions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
