#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Lackeys(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.name = "Lackeys"
        self.cards = 2
        self.cost = 2

    ###########################################################################
    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return "+2 Cards; When you gain this, +2 Villagers."
        return "+2 Cards"

    ###########################################################################
    def hook_gain_this_card(self, game, player):
        player.villagers.add(2)


###############################################################################
class Test_Lackeys(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Lackeys"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play_card(self):
        self.card = self.g.get_card_from_pile("Lackeys")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertLessEqual(self.plr.villagers.get(), 0)

    def test_gain_card(self):
        self.plr.gain_card("Lackeys")
        self.assertLessEqual(self.plr.villagers.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
