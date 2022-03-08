#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Inventor(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.desc = "Gain a card costing up to 4, then cards cost 1 less this turn (but not less than 0)."
        self.name = "Inventor"
        self.cost = 4

    def special(self, game, player):
        """Gain a card costing up to 4"""
        player.plrGainCard(4)

    def hook_cardCost(self, game, player, card):
        if self in player.played:
            return -1
        return 0


###############################################################################
class Test_Inventor(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            initcards=["Inventor", "Gardens"],
            badcards=["Blessed Village", "Cemetery"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.inventor = self.g["Inventor"].remove()
        self.plr.addCard(self.inventor, "hand")

    def test_play(self):
        self.plr.test_input = ["Get Gardens"]
        self.assertEqual(self.plr.cardCost(self.g["Gold"]), 6)
        self.plr.playCard(self.inventor)
        self.assertEqual(self.plr.cardCost(self.g["Gold"]), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
