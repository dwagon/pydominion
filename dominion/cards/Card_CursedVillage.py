#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_CursedVillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DOOM]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+2 Actions. Draw until you have 6 cards in hand. When you gain this, receive a Hex."
        self.name = "Cursed Village"
        self.actions = 2
        self.cost = 5

    def special(self, game, player):
        while player.piles[Piles.HAND].size() < 6:
            player.pickup_card()

    def hook_gain_this_card(self, game, player):
        player.receive_hex()


###############################################################################
class TestCursedVillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cursed Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Cursed Village"].remove()
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play_card(self):
        """Play Cursed Village"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertGreaterEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)

    def test_gain(self):
        self.plr.gain_card("Cursed Village")
        self.assertTrue(self.plr.has_state("Deluded"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
