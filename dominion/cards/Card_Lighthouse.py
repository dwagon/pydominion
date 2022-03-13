#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Lighthouse(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.desc = """+1 Action. Now and at the start of your next turn: +1 Coin.
        While this is in play, when another player plays an Attack card, it doesn't affect you."""
        self.name = "Lighthouse"
        self.base = Game.SEASIDE
        self.defense = True
        self.actions = 1
        self.cost = 2

    def duration(self, game, player):
        player.addCoin(1)

    def special(self, game, player):
        player.addCoin(1)


###############################################################################
class Test_Lighthouse(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Lighthouse"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Lighthouse"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.getCoin(), 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
