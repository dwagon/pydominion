#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Fisherman """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Fisherman(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+1 Card; +1 Action; +1 Coin; During your turns, if your discard pile is empty, this costs 3 Coin less."
        self.name = "Fisherman"
        self.coin = 1
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def hook_this_card_cost(self, game, player):
        if player.discardpile.is_empty():
            return -3
        return 0


###############################################################################
class Test_Fisherman(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Fisherman"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Fisherman"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play the card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.hand.size(), 5 + 1)

    def test_buycard(self):
        """Buy the card"""
        self.plr.discardpile.set("Copper")
        self.assertEqual(self.plr.card_cost(self.card), 5)
        self.plr.discardpile.set()
        self.assertEqual(self.plr.card_cost(self.card), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
