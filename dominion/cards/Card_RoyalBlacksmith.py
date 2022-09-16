#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_RoyalBlacksmith(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """+5 Cards. Reveal your hand; discard the Coppers."""
        self.name = "Royal Blacksmith"
        self.debtcost = 8
        self.cards = 5

    def special(self, game, player):
        count = 0
        for card in player.hand:
            player.reveal_card(card)
            if card.name == "Copper":
                player.discard_card(card)
                count += 1
        player.output("Discarding %d coppers" % count)


###############################################################################
class Test_RoyalBlacksmith(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Royal Blacksmith"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Royal Blacksmith"].remove()

    def test_play(self):
        """Play an Royal Blacksmith"""
        self.plr.deck.set("Silver", "Province", "Estate", "Copper", "Gold", "Silver")
        self.plr.hand.set("Copper", "Silver", "Duchy")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 3 - 2 + 5)
        self.assertIn("Copper", self.plr.discardpile)
        self.assertNotIn("Copper", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
