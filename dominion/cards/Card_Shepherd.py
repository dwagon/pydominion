#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Shepherd(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = (
            "+1 action; Discard any number of victory cards +2 cards per card discarded"
        )
        self.name = "Shepherd"
        self.cost = 2
        self.actions = 1
        self.heirloom = "Pasture"

    def special(self, game, player):
        to_discard = player.plr_discard_cards(
            num=0, any_number=True, types={Card.CardType.VICTORY: True}
        )
        if not to_discard:
            return
        player.pickup_cards(2 * len(to_discard))


###############################################################################
class TestShepherd(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Shepherd"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Shepherd")

    def test_play(self):
        """Play a Shepherd"""
        self.plr.piles[Piles.HAND].set("Estate", "Province", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Estate", "Duchy", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
