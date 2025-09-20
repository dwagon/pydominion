#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Whens


###############################################################################
class Card_Coinoftherealm(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.RESERVE]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+1 Coin; Call for +2 Actions"
        self.name = "Coin of the Realm"
        self.coin = 1
        self.cost = 2
        self.when = Whens.POSTACTION

    def hook_call_reserve(self, game, player):
        """Directly after resolving an action you may call this for +2 Actions"""
        player.add_actions(2)


###############################################################################
class Test_Coinoftherealm(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Coin of the Realm"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Coin of the Realm")

    def test_play(self):
        """Play a coin of the realm"""
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.piles[Piles.RESERVE].size(), 1)
        self.assertIn("Coin of the Realm", self.plr.piles[Piles.RESERVE])

    def test_call(self):
        """Call from Reserve"""
        self.plr.actions.set(0)
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        c = self.plr.call_reserve("Coin of the Realm")
        self.assertEqual(c.name, "Coin of the Realm")
        self.assertEqual(self.plr.actions.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
