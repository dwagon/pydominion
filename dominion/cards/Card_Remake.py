#!/usr/bin/env python

import unittest
import dominion.Card as Card
import dominion.Game as Game


###############################################################################
class Card_Remake(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.CORNUCOPIA
        self.desc = "Do this twice: Trash a card from your hand, then gain a card costing exactly 1 more than the trashed card."
        self.name = "Remake"
        self.cost = 4

    def special(self, game, player):
        for _ in range(2):
            c = player.plrTrashCard(prompt="Trash a card and gain one costing 1 more")
            if c:
                player.plrGainCard(cost=c[0].cost + 1, modifier="equal")


###############################################################################
class Test_Remake(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Remake", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Remake"].remove()

    def test_playcard(self):
        """Play a remake"""
        self.plr.set_hand("Copper", "Estate")
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = [
            "Trash Estate",
            "Get Silver",
            "Trash Copper",
            "Finish Selecting",
        ]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 0)
        self.assertIsNotNone(self.plr.in_discard("Silver"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()


# EOF
