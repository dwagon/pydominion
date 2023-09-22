#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Treasuremap(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """Trash this and another copy of Treasure Map from your hand.
            If you do trash two Treasure Maps, gain 4 Gold cards, putting them
            on top of your deck."""
        self.name = "Treasure Map"
        self.cost = 4

    def special(self, game, player):
        player.trash_card(self)
        tmaps = [c for c in player.piles[Piles.HAND] if c.name == "Treasure Map"][:1]
        if not tmaps:
            return
        t = player.plr_trash_card(
            prompt="If you trash another treasure map you can get 4 golds",
            cardsrc=tmaps,
        )
        if t:
            player.output("Gaining 4 Gold")
            for _ in range(4):
                player.gain_card("Gold", destination="topdeck")
        else:
            player.output("Didn't trash two so no Gold")


###############################################################################
class Test_Treasuremap(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Treasure Map"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Treasure Map")

    def test_trash(self):
        """Trash a TM"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.DECK].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["0", "1", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertIn("Treasure Map", self.g.trash_pile)
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 0)

    def test_trash_two(self):
        """Trash 2 TM"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.DECK].set()
        self.plr.piles[Piles.HAND].set("Treasure Map")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["1", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.g.trash_pile.size(), tsize + 2)
        self.assertIn("Treasure Map", self.g.trash_pile)
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 4)
        self.assertIn("Gold", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
