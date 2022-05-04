#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Altar(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """Trash a card from your hand. Gain a card costing up to 5 Coin."""
        self.name = "Altar"
        self.cost = 6

    def special(self, game, player):
        # Trash a card from your hand
        player.plr_trash_card(prompt="Trash a card from your hand", force=True)

        # Gain a card costing up to 5 Coin
        player.plr_gain_card(5)


###############################################################################
class Test_Altar(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Altar", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Altar"].remove()

    def test_play(self):
        """Play an Altar"""
        self.plr.set_hand("Province")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Province", "Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.discardpile)
        self.assertIsNotNone(self.g.in_trash("Province"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
