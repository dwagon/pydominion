#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Guildmaster(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.base = Card.CardExpansion.ALLIES
        self.name = "Guildmaster"
        self.coin = 3
        self.desc = "+$3; This turn, when you gain a card, +1 Favor."
        self.cost = 5

    def hook_gain_card(self, game, player, card):
        player.favors.add(1)


###############################################################################
class Test_Guildmaster(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Guildmaster"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Guildmaster"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play the card"""
        coin = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coin + 3)
        favs = self.plr.favors.get()
        self.plr.gain_card("Copper")
        self.assertEqual(self.plr.favors.get(), favs + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
