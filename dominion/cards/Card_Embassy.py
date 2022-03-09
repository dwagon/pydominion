#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Embassy(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.desc = "+5 Cards, Discard 3. Everyone gets a silver on purchase"
        self.name = "Embassy"
        self.cost = 5
        self.base = Game.HINTERLANDS
        self.cards = 5

    def special(self, game, player):
        player.plrDiscardCards(3, force=True)

    def hook_gain_this_card(self, game, player):
        """When you gain this, each other player gains a Silver"""
        for plr in game.player_list():
            if plr != player:
                plr.output(
                    "Gained a silver from %s's purchase of Embassy" % player.name
                )
                plr.gainCard("Silver")
        return {}


###############################################################################
class Test_Embassy(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Embassy"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g["Embassy"].remove()
        self.plr.setDeck("Estate", "Estate", "Estate", "Estate", "Estate")
        self.plr.setHand("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        self.plr.test_input = [
            "discard copper",
            "discard silver",
            "discard gold",
            "finish",
        ]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 5 - 3)

    def test_gain(self):
        self.plr.gainCard("Embassy")
        self.assertEqual(self.other.discardpile[-1].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
