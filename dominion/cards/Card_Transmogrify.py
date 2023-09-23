#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Transmogrify(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RESERVE]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """+1 Action; At the start of your turn, you may call this,
            to trash a card from your hand, gain a card costing up to 1 coin more
            than it, and put that card into your hand"""
        self.name = "Transmogrify"
        self.actions = 1
        self.when = "start"
        self.cost = 4

    def hook_call_reserve(self, game, player):
        tc = player.plr_trash_card(
            printcost=True,
            prompt="Trash a card from you hand. Gain a card costing up to 1 more",
        )
        if tc:
            cost = player.card_cost(tc[0])
            player.plr_gain_card(cost + 1, modifier="less", destination=Piles.HAND)


###############################################################################
class Test_Transmogrify(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Transmogrify"],
            badcards=["Duchess", "Fool's Gold"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.trans = self.g.get_card_from_pile("Transmogrify")
        self.plr.add_card(self.trans, Piles.HAND)

    def test_play(self):
        self.plr.play_card(self.trans)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIsNotNone(self.plr.piles[Piles.RESERVE]["Transmogrify"])

    def test_call(self):
        self.plr.piles[Piles.HAND].set("Duchy", "Estate")
        self.plr.piles[Piles.RESERVE].set("Transmogrify")
        self.plr.test_input = ["trash duchy", "get gold"]
        self.plr.call_reserve("Transmogrify")
        self.assertIn("Duchy", self.g.trash_pile)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
