#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Bustling_Village"""
import unittest

from dominion import Card, Game, Piles


###############################################################################
class Card_BustlingVillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Bustling Village"
        self.actions = 3
        self.cards = 1
        self.cost = 5
        self.pile = "Settlers"
        self.desc = """+1 Card; +3 Actions; Look through your discard pile.
        You may reveal a Settlers from it and put it into your hand."""

    ###########################################################################
    def special(self, game, player):
        discarded_settlers = player.piles[Piles.DISCARD]["Settlers"]
        if discarded_settlers:
            player.move_card(discarded_settlers, Piles.HAND)
            player.reveal_card(discarded_settlers)
            player.output("Pulled Settlers from discard into hand")
        else:
            player.output("No Settlers in discard")


###############################################################################
class Test_BustlingVillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Settlers", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Settlers", "Bustling Village")

    def test_play_settlers(self):
        """Play a Bustling Village and pull a Settlers"""
        self.plr.piles[Piles.DISCARD].set("Gold", "Silver", "Settlers")
        self.plr.piles[Piles.HAND].set("Gold", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Settlers", self.plr.piles[Piles.HAND])
        self.assertNotIn("Settlers", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.actions.get(), 3)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2 + 1 + 1)

    def test_play_no_settlers(self):
        """Play a Bustling Village and pull no Settlers"""
        self.plr.piles[Piles.DECK].set("Gold", "Silver")
        self.plr.piles[Piles.DISCARD].set("Gold", "Silver", "Duchy")
        self.plr.piles[Piles.HAND].set("Gold", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertNotIn("Bustling Village", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
