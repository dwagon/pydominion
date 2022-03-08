#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Wish(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.NOCTURNE
        self.desc = "+1 Action; Return this to its pile. If you did, gain a card to your hand costing up to 6."
        self.name = "Wish"
        self.purchasable = False
        self.insupply = False
        self.actions = 1
        self.cost = 0
        self.numcards = 12

    def special(self, game, player):
        dc = player.plrChooseOptions(
            "Return this to gain a card to you hand costing up to 6",
            ("Return", True),
            ("Keep", False),
        )
        if dc:
            player.discardCard(self)
            game["Wish"].add()
            player.played.remove(self)
            player.plrGainCard(cost=6)


###############################################################################
class Test_Wish(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Wish"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Wish"].remove()

    def test_return(self):
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["Return", "Get Gold"]
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard("Gold"))
        self.assertIsNone(self.plr.in_played("Wish"))

    def test_keep(self):
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["Keep"]
        self.plr.playCard(self.card)
        self.assertIsNone(self.plr.in_discard("Gold"))
        self.assertIsNotNone(self.plr.in_played("Wish"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
