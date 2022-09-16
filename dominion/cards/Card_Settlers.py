#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Settlers(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Settlers"
        self.cards = 1
        self.actions = 1
        self.cost = 2
        self.desc = """+1 Card +1 Action. Look through your discard pile. You may reveal a Copper from it and put it into your hand."""

    def special(self, game, player):
        cu = player.discardpile["Copper"]
        if cu:
            player.add_card(cu, "hand")
            player.discardpile.remove(cu)
            player.reveal_card(cu)
            player.output("Pulled Copper from discard into hand")
        else:
            player.output("No Copper in discard")


###############################################################################
class Test_Settlers(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Settlers"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Settlers"].remove()

    def test_play(self):
        """Play a Settlers and pull a copper"""
        self.plr.discardpile.set("Gold", "Silver", "Copper")
        self.plr.hand.set("Gold", "Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.plr.hand)
        self.assertNotIn("Copper", self.plr.discardpile)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.hand.size(), 2 + 1 + 1)

    def test_play_nocopper(self):
        """Play a Settlers and pull a copper"""
        self.plr.deck.set("Gold", "Silver")
        self.plr.discardpile.set("Gold", "Silver", "Duchy")
        self.plr.hand.set("Gold", "Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertNotIn("Copper", self.plr.hand)
        self.assertEqual(self.plr.hand.size(), 2 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
