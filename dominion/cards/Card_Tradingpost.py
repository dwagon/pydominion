#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_TradingPost(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "Trash 2 cards for a silver"
        self.name = "Trading Post"
        self.cost = 5

    def special(self, game, player):
        """Trash 2 card from your hand. If you do, gain a Silver card; put it into your hand"""
        num = min(2, player.piles[Piles.HAND].size())
        trash = player.plr_trash_card(
            num=num, prompt="Trash two cards to gain a silver"
        )
        if trash and len(trash) == 2:
            player.gain_card("Silver", Piles.HAND)
            player.coins.add(2)
        else:
            player.output("Not enough cards trashed")


###############################################################################
class TestTradingPost(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Trading Post"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Trading Post"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play Trading Post"""
        tsize = self.g.trashpile.size()
        self.plr.test_input = ["1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertEqual(self.g.trashpile.size(), tsize + 2)

    def test_trash_little(self):
        """Play a trading post but don't trash enough"""
        tsize = self.g.trashpile.size()
        self.plr.test_input = ["1", "0"]
        self.plr.play_card(self.card)
        self.assertNotIn("Silver", self.plr.piles[Piles.HAND])
        self.assertEqual(self.g.trashpile.size(), tsize + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
