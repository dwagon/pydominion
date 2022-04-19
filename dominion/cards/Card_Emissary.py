#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Emissary(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_LIAISON]
        self.base = Game.ALLIES
        self.name = "Emissary"
        self.desc = "+3 Cards; If this made you shuffle (at least one card), +1 Action and +2 Favors."
        self.cards = 3
        self.cost = 5

    def hook_post_shuffle(self, game, player):
        player.add_actions(1)
        player.add_favors(2)


###############################################################################
class Test_Emissary(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Emissary"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Emissary"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the card"""
        self.plr.set_deck("Copper", "Copper")
        self.plr.set_discard("Estate", "Estate", "Estate", "Duchy")
        favs = self.plr.get_favors()
        acts = self.plr.get_actions()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_favors(), favs + 2)
        self.assertEqual(self.plr.get_actions(), acts - 1 + 1)
        self.assertEqual(self.plr.hand.size(), 5 + 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
