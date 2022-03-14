#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Supplies """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Supplies(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.MENAGERIE
        self.desc = "+1 coin; When you play this, gain a Horse onto your deck."
        self.name = "Supplies"
        self.coin = 1
        self.cost = 2
        self.required_cards = [("Card", "Horse")]

    def special(self, game, player):
        player.gain_card("Horse", "topdeck")


###############################################################################
class Test_Supplies(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Supplies"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Supplies"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a supplies"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.deck[-1].name, "Horse")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
