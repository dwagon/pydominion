#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Fortress(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = (
            """+1 Card +2 Actions. When you trash this, put it into your hand."""
        )
        self.name = "Fortress"
        self.cards = 1
        self.actions = 2
        self.cost = 4

    def hook_trashThisCard(self, game, player):
        player.output("Putting Fortress back in hand")
        if self in player.played:
            player.add_card(self, "hand")
            player.played.remove(self)
        if self in player.hand:
            player.add_card(self, "hand")
            player.hand.remove(self)
        if self in game.trashpile:
            player.add_card(self, "hand")
            game.trashpile.remove(self)
        return {"trash": False}


###############################################################################
class Test_Fortress(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Fortress"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Fortress"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.get_actions(), 2)

    def test_trash(self):
        self.plr.trash_card(self.card)
        self.g.print_state()
        self.assertIsNotNone(self.plr.in_hand("Fortress"))
        self.assertIsNone(self.g.in_trash("Fortress"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
