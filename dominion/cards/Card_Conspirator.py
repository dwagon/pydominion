#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Conspirator(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
        self.desc = """+2 coin. If you've played 3 or more actions this turn (counting
            this); +1 card, +1 action """
        self.name = "Conspirator"
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        if self.numActionsPlayed(player) >= 3:
            player.pickup_card()
            player.add_actions(1)

    def numActionsPlayed(self, player):
        return sum([1 for _ in player.played if _.isAction()])


###############################################################################
class Test_Conspirator(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Conspirator", "Witch"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Conspirator"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the conspirator with not enough actions"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertEqual(self.plr.get_actions(), 0)
        self.assertEqual(self.plr.hand.size(), 5)

    def test_actions(self):
        """Play the conspirator with enough actions"""
        self.plr.played.set("Witch", "Witch", "Witch")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
