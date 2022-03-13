#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Councilroom(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "+4 cards, +1 buy. Everyone else +1 card"
        self.name = "Council Room"
        self.cards = 4
        self.buys = 1
        self.cost = 5

    def special(self, game, player):
        """Each other player draws a card"""
        for pl in game.player_list():
            if pl != player:
                pl.output(
                    "Picking up card due to %s playing a Council Room" % player.name
                )
                pl.pickup_card()


###############################################################################
class Test_Councilroom(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Council Room"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.ccard = self.g["Council Room"].remove()
        self.plr.add_card(self.ccard, "hand")

    def test_play(self):
        self.assertEqual(self.other.hand.size(), 5)
        self.plr.playCard(self.ccard)
        self.assertEqual(self.other.hand.size(), 6)
        self.assertEqual(self.plr.hand.size(), 9)
        self.assertEqual(self.plr.get_buys(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
