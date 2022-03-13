#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_RoyalBlacksmith(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.EMPIRES
        self.desc = """+5 Cards. Reveal your hand; discard the Coppers."""
        self.name = "Royal Blacksmith"
        self.debtcost = 8
        self.cards = 5

    def special(self, game, player):
        count = 0
        for card in player.hand:
            player.reveal_card(card)
            if card.name == "Copper":
                player.discardCard(card)
                count += 1
        player.output("Discarding %d coppers" % count)


###############################################################################
class Test_RoyalBlacksmith(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Royal Blacksmith"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Royal Blacksmith"].remove()

    def test_play(self):
        """Play an Royal Blacksmith"""
        self.plr.set_deck("Silver", "Province", "Estate", "Copper", "Gold", "Silver")
        self.plr.set_hand("Copper", "Silver", "Duchy")
        self.plr.add_card(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 3 - 2 + 5)
        self.assertIsNotNone(self.plr.in_discard("Copper"))
        self.assertIsNone(self.plr.in_hand("Copper"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
