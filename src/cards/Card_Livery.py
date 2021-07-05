#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Livery """

import unittest
import Game
import Card


###############################################################################
class Card_Livery(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.desc = """+3 Coins; This turn, when you gain a card costing 4 Coins or more, gain a Horse."""
        self.name = "Livery"
        self.coin = 3
        self.cost = 5
        self.required_cards = [("Card", "Horse")]

    def hook_cleanup(self, game, player):
        for card in player.stats["gained"]:
            if card.cost > 4:
                player.output("Gained a Horse from Livery")
                player.gainCard("Horse")


###############################################################################
class Test_Livery(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Livery"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Livery"].remove()
        self.plr.addCard(self.card, "hand")

    def test_playcard_cost0(self):
        """Play a livery and gain something worth 0"""
        self.plr.playCard(self.card)
        self.plr.gainCard("Copper")
        self.plr.test_input = ["end phase", "end phase"]
        self.plr.turn()
        self.assertIsNone(self.plr.in_discard("Horse"))

    def test_playcard_cost6(self):
        """Play a livery and gain something worth 6"""
        self.plr.playCard(self.card)
        self.plr.gainCard("Province")
        self.plr.test_input = ["end phase", "end phase"]
        self.plr.turn()
        self.assertIsNotNone(self.plr.in_discard("Horse"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
