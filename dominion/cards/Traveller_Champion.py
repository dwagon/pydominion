#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Champion(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.ADVENTURE
        self.desc = "For the rest of the game +1 Action / Action; Defense"
        self.name = "Champion"
        self.permanent = True
        self.purchasable = False
        self.defense = True
        self.numcards = 5
        self.cost = 6

    def hook_postAction(self, game, player, card):
        player.add_actions(1)


###############################################################################
class Test_Champion(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Page", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Champion"].remove()

    def test_champion(self):
        """Play a champion"""
        self.plr.add_card(self.card, Card.TYPE_DURATION)
        self.assertEqual(self.plr.get_actions(), 1)
        moat = self.g["Moat"].remove()
        self.plr.add_card(moat, "hand")
        self.plr.play_card(moat)
        self.assertEqual(self.plr.get_actions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
