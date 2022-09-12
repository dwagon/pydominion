#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Port(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ADVENTURE
        self.name = "Port"
        self.cards = 1
        self.actions = 2
        self.cost = 4
        self.numcards = 12

    def desc(self, player):
        if player.phase == "buy":
            return "+1 Card, +2 Actions; When you buy this, gain another Port"
        return "+1 Card, +2 Actions"

    def hook_buy_this_card(self, game, player):
        """Gain another Port"""
        c = player.gain_card("Port")
        if c:
            player.output("Gained a port")
        else:
            player.output("No more ports")


###############################################################################
class Test_Port(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Port"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Port"].remove()

    def test_play(self):
        """Play a port"""
        self.plr.hand.set()
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertEqual(self.plr.get_actions(), 2)

    def test_buy(self):
        """Buy a port"""
        self.plr.discardpile.set()
        self.plr.coins.set(5)
        self.plr.buy_card(self.g["Port"])
        for c in self.plr.discardpile:
            self.assertEqual(c.name, "Port")
        self.assertEqual(self.plr.discardpile.size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
