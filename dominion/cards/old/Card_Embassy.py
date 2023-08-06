#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Embassy(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.desc = "+5 Cards, Discard 3. Everyone gets a silver on purchase"
        self.name = "Embassy"
        self.cost = 5
        self.base = Card.CardExpansion.HINTERLANDS
        self.cards = 5

    def special(self, game, player):
        player.plr_discard_cards(3, force=True)

    def hook_gain_this_card(self, game, player):
        """When you gain this, each other player gains a Silver"""
        for plr in game.player_list():
            if plr != player:
                plr.output("Gained a silver from %s's purchase of Embassy" % player.name)
                plr.gain_card("Silver")
        return {}


###############################################################################
class Test_Embassy(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, oldcards=True, initcards=["Embassy"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g["Embassy"].remove()
        self.plr.deck.set("Estate", "Estate", "Estate", "Estate", "Estate")
        self.plr.hand.set("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.test_input = [
            "discard copper",
            "discard silver",
            "discard gold",
            "finish",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 5 - 3)

    def test_gain(self):
        self.plr.gain_card("Embassy")
        self.assertEqual(self.other.discardpile[-1].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
