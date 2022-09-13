#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Duplicate(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RESERVE]
        self.base = Game.ADVENTURE
        self.desc = (
            "When you gain a card costing up to 6, you may call this to gain a copy of that card"
        )
        self.name = "Duplicate"
        self.cost = 4
        self.when = ["special"]

    def hook_gain_card(self, game, player, card):
        if not player.reserve["Duplicate"]:
            return {}
        if card.cost > 6:
            return {}
        if not card.purchasable:
            return {}
        if card.potcost:
            return {}
        o = player.plr_choose_options(
            "Call Duplicate on %s" % card.name,
            ("Save for later", False),
            ("Duplicate %s" % card.name, True),
        )
        if o:
            self._duplicate = card
            player.call_reserve(self)
        return {}

    def hook_call_reserve(self, game, player):
        card = self._duplicate
        player.output("Gaining a %s from Duplicate" % card.name)
        player.gain_card(card.name, callhook=False)


###############################################################################
class Test_Duplicate(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Duplicate"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Duplicate"].remove()

    def test_buy(self):
        """Call Duplicate from reserve"""
        self.plr.coins.set(6)
        self.plr.reserve.set("Duplicate")
        self.plr.test_input = ["Gold"]
        self.plr.buy_card(self.g["Gold"])
        self.assertEqual(self.plr.discardpile.size(), 2)
        for i in self.plr.discardpile:
            self.assertEqual(i.name, "Gold")
        self.assertEqual(self.plr.coins.get(), 0)

    def test_buy_non_reserve(self):
        """Buy a card when duplicate just in hand"""
        self.plr.coins.set(6)
        self.plr.reserve.set()
        self.plr.hand.set("Duplicate")
        self.plr.buy_card(self.g["Gold"])
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
