#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Guildmaster(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_LIAISON]
        self.base = Game.ALLIES
        self.name = "Guildmaster"
        self.coin = 3
        self.desc = "+$3; This turn, when you gain a card, +1 Favor."
        self.cost = 5

    def hook_gain_card(self, game, player, card):
        player.add_favors()


###############################################################################
class Test_Guildmaster(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Guildmaster"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Guildmaster"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the card"""
        coin = self.plr.get_coins()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), coin + 3)
        favs = self.plr.get_favors()
        self.plr.gain_card("Copper")
        self.assertEqual(self.plr.get_favors(), favs + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
