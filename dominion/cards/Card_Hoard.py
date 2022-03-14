#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Hoard(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.PROSPERITY
        self.desc = (
            "+2 coin; While this is in play, when you buy a Victory card, gain a Gold"
        )
        self.name = "Hoard"
        self.playable = False
        self.coin = 2
        self.cost = 6

    def hook_buy_card(self, game, player, card):
        """When this is in play, when you buy a Victory card, gain a Gold"""
        if card.isVictory():
            player.output("Gaining Gold from Hoard")
            player.add_card(game["Gold"].remove())


###############################################################################
class Test_Hoard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Hoard"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Hoard"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertTrue(self.plr.discardpile.is_empty())

    def test_buy_victory(self):
        self.plr.play_card(self.card)
        self.plr.buy_card(self.g["Estate"])
        self.assertEqual(self.plr.discardpile.size(), 2)
        for c in self.plr.discardpile:
            if c.name == "Gold":
                break
        else:  # pragma: no cover
            self.fail("Didn't pickup gold")

    def test_buy_nonvictory(self):
        self.plr.play_card(self.card)
        self.plr.buy_card(self.g["Copper"])
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertEqual(self.plr.discardpile[-1].name, "Copper")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
