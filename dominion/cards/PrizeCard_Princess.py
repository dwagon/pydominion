#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Princess(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_PRIZE]
        self.base = Game.CORNUCOPIA
        self.name = "Princess"
        self.purchasable = False
        self.cost = 0
        self.desc = (
            "+1 Buy; While this is in play, cards cost 2 less, but not less than 0."
        )
        self.buys = 1

    def hook_cardCost(self, game, player, card):
        return -2


###############################################################################
class Test_Princess(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Tournament"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Princess"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.cardCost(self.g["Gold"]), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
