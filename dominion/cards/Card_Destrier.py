#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Destrier(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.desc = "+2 Cards; +1 Action; During your turns, this costs 1 less per card you've gained this turn."
        self.name = "Destrier"
        self.cards = 2
        self.actions = 1
        self.cost = 6

    def hook_this_card_cost(self, game, player):
        num_gained = len(player.stats["gained"])
        return -num_gained


###############################################################################
class Test_Destrier(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Destrier"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Destrier"].remove()

    def test_play(self):
        self.plr.set_hand()
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
