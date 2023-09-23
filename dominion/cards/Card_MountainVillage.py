#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_MountainVillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "+2 Actions; Look through your discard pile and put a card from it into your hand; if you can't, +1 Card."
        self.name = "Mountain Village"
        self.cost = 4
        self.actions = 2

    def special(self, game, player):
        if player.piles[Piles.DISCARD].size():
            card = player.card_sel(
                cardsrc="discard",
                force=True,
                prompt="Look through your discard pile and put a card from it into your hand",
            )
            player.piles[Piles.DISCARD].remove(card[0])
            player.add_card(card[0], Piles.HAND)
        else:
            player.output("No cards in discard pile")
            player.pickup_cards(1)


###############################################################################
class Test_MountainVillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Mountain Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Mountain Village")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_no_discard(self):
        """Play Mountain Village without a discard card"""
        self.plr.piles[Piles.DISCARD].set()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)

    def test_play_discard(self):
        """Play Mountain Village with a discard card"""
        self.plr.piles[Piles.DISCARD].set("Gold", "Silver")
        self.plr.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
