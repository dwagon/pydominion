#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Tradingpost(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
        self.desc = "Trash 2 cards for a silver"
        self.name = "Trading Post"
        self.cost = 5

    def special(self, game, player):
        """Trash 2 card from your hand. If you do, gain a Silver card; put it into your hand"""
        num = min(2, player.hand.size())
        trash = player.plr_trash_card(
            num=num, prompt="Trash two cards to gain a silver"
        )
        if len(trash) == 2:
            player.gain_card("Silver", "hand")
            player.add_coins(2)
        else:
            player.output("Not enough cards trashed")


###############################################################################
class Test_Tradingpost(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Trading Post"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Trading Post"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play Trading Post"""
        tsize = self.g.trash_size()
        self.plr.test_input = ["1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.hand)
        self.assertEqual(self.g.trash_size(), tsize + 2)

    def test_trash_little(self):
        """Play a trading post but don't trash enough"""
        tsize = self.g.trash_size()
        self.plr.test_input = ["1", "0"]
        self.plr.play_card(self.card)
        self.assertFalse(self.plr.in_hand("Silver"))
        self.assertEqual(self.g.trash_size(), tsize + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
