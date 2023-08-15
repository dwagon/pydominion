#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Fortress(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 Card +2 Actions. When you trash this, put it into your hand."""
        self.name = "Fortress"
        self.cards = 1
        self.actions = 2
        self.cost = 4

    def hook_trashThisCard(self, game, player):
        player.output("Putting Fortress back in hand")
        if self in player.piles[Piles.PLAYED]:
            player.add_card(self, Piles.HAND)
            player.piles[Piles.PLAYED].remove(self)
        if self in player.piles[Piles.HAND]:
            player.add_card(self, Piles.HAND)
            player.piles[Piles.HAND].remove(self)
        if self in game.trashpile:
            player.add_card(self, Piles.HAND)
            game.trashpile.remove(self)
        return {"trash": False}


###############################################################################
class Test_Fortress(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Fortress"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Fortress"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play the card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_trash(self):
        self.plr.trash_card(self.card)
        self.g.print_state()
        self.assertIn("Fortress", self.plr.piles[Piles.HAND])
        self.assertNotIn("Fortress", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
