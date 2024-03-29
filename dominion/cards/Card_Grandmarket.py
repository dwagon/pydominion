#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Phase


###############################################################################
class Card_Grandmarket(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+1 card, +1 action, +1 buy, +2 coin"
        self.name = "Grand Market"
        self.cost = 6
        self.cards = 1
        self.actions = 1
        self.buys = 1
        self.coin = 2

    def hook_allowed_to_buy(self, game, player):
        """You can't buy this if you have any copper in play"""
        for c in player.piles[Piles.HAND] + player.piles[Piles.PLAYED]:
            if c.name == "Copper":
                return False
        return True


###############################################################################
class Test_Grandmarket(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Grand Market"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.gm = self.g.get_card_from_pile("Grand Market")

    def test_play(self):
        self.plr.add_card(self.gm, Piles.HAND)
        self.plr.play_card(self.gm)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)

    def test_nobuy(self):
        self.plr.piles[Piles.HAND].set("Copper", "Gold", "Gold")
        self.plr.coins.add(6)
        self.plr.test_input = ["0"]
        self.plr.phase = Phase.BUY
        options = self.plr._choice_selection()
        for opt in options:
            if (
                opt["name"] == "Grand Market" and opt["verb"] == "Buy"
            ):  # pragma: no cover
                self.fail("Allowed to buy with copper")

    def test_nobuy_played(self):
        self.plr.piles[Piles.HAND].set("Gold", "Gold", "Gold")
        self.plr.piles[Piles.PLAYED].set("Copper")
        self.plr.coins.add(6)
        self.plr.test_input = ["0"]
        self.plr.phase = Phase.BUY
        options = self.plr._choice_selection()
        for opt in options:
            if (
                opt["name"] == "Grand Market" and opt["verb"] == "Buy"
            ):  # pragma: no cover
                self.fail("Allowed to buy with copper")

    def test_buy(self):
        self.plr.piles[Piles.HAND].set("Gold", "Gold", "Gold")
        self.plr.coins.add(6)
        self.plr.test_input = ["0"]
        self.plr.phase = Phase.BUY
        options = self.plr._choice_selection()
        for opt in options:
            if (
                opt["name"] == "Grand Market" and opt["verb"] == "Buy"
            ):  # pragma: no cover
                break
        else:  # pragma: no cover
            self.fail("Not allowed to buy grand market")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
