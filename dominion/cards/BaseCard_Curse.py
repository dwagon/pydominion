#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Curse(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_VICTORY
        self.base = Game.DOMINION
        self.desc = "-1 VP"
        self.basecard = True
        self.playable = False
        self.purchasable = True
        self.name = "Curse"
        self.cost = 0
        self.victory = -1

    def calc_numcards(self, game):
        if game.numplayers == 1:
            return 10
        return 10 * (game.numplayers - 1)


###############################################################################
class Test_Curse(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Witch"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Curse"].remove()

    def test_play(self):
        self.plr.add_card(self.card, "hand")
        self.plr.playCard(self.card)

    def test_have(self):
        self.plr.add_card(self.card)
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc["Curse"], -1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
