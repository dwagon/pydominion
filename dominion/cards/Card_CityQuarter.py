#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_CityQuarter(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "+2 Actions. Reveal your hand. +1 Card per Action card revealed."
        self.name = "City Quarter"
        self.debtcost = 8
        self.actions = 2
        self.coin = 1

    def special(self, game, player):
        actions = 0
        for c in player.piles[Piles.HAND]:
            player.reveal_card(c)
            if c.isAction():
                actions += 1
        player.output("Revealed %d actions" % actions)
        player.pickup_cards(actions)


###############################################################################
class Test_CityQuarter(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["City Quarter", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("City Quarter")

    def test_play(self):
        """Play a City Quarter"""
        self.plr.piles[Piles.HAND].set("Moat", "Moat", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
