#!/usr/bin/env python

import unittest

import dominion.Card as Card
from dominion import Game, Piles


###############################################################################
class Card_Sculptor(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """Gain a card to your hand costing up to 4. If it's a Treasure, +1 Villager."""
        self.name = "Sculptor"
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        card = player.plr_gain_card(4, destination=Piles.HAND, force=True)
        if card.isTreasure():
            player.output("Gained  villager")
            player.villagers.add(1)


###############################################################################
class Test_Sculptor(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sculptor", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Sculptor")
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)

    def test_gainaction(self):
        self.plr.piles[Piles.DECK].set("Moat")
        self.plr.test_input = ["Get Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)
        self.assertIn("Moat", self.plr.piles[Piles.HAND])
        self.assertLessEqual(self.plr.villagers.get(), 1)

    def test_gaintreasure(self):
        self.plr.piles[Piles.DECK].set("Silver")
        self.plr.test_input = ["Get Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertLessEqual(self.plr.villagers.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
