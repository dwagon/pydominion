#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Countinghouse(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """Look through the discard pile, reveal any number of
            copper cards from it, and put them into your hand."""
        self.name = "Counting House"
        self.cost = 5

    def special(self, game, player):
        count = 0
        for card in player.piles[Piles.DISCARD]:
            if card.name == "Copper":
                player.move_card(card, Piles.HAND)
                count += 1
        player.output(f"Picked up {count} coppers")


###############################################################################
class Test_Countinghouse(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Counting House"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.ch = self.g.get_card_from_pile("Counting House")
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.ch, Piles.HAND)

    def test_pullcoppers(self):
        self.plr.piles[Piles.DISCARD].set("Copper", "Gold", "Duchy", "Copper")
        self.plr.play_card(self.ch)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        for c in self.plr.piles[Piles.HAND]:
            self.assertEqual(c.name, "Copper")
        self.assertNotIn("Copper", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
