#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Duplicate(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RESERVE]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "When you gain a card costing up to 6, you may call this to gain a copy of that card"
        self.name = "Duplicate"
        self.cost = 4
        self.when = ["special"]
        self._duplicate = None

    def hook_gain_card(self, game, player, card):
        if not player.piles[Piles.RESERVE]["Duplicate"]:
            return {}
        if card.cost > 6:
            return {}
        if not card.purchasable:
            return {}
        if card.potcost:
            return {}
        o = player.plr_choose_options(
            f"Call Duplicate on {card}?",
            ("Save for later", False),
            (f"Duplicate {card}", True),
        )
        if o:
            self._duplicate = card
            player.call_reserve(self)
        else:
            self._duplicate = None
        return {}

    def hook_call_reserve(self, game, player):
        card = self._duplicate
        player.output(f"Gaining a {card} from Duplicate")
        player.gain_card(card.name, callhook=False)


###############################################################################
class TestDuplicate(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Duplicate"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Duplicate"].remove()

    def test_buy(self):
        """Call Duplicate from reserve"""
        self.plr.coins.set(6)
        self.plr.piles[Piles.RESERVE].set("Duplicate")
        self.plr.test_input = ["Gold"]
        self.plr.buy_card(self.g["Gold"])
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        for i in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(i.name, "Gold")
        self.assertEqual(self.plr.coins.get(), 0)

    def test_buy_non_reserve(self):
        """Buy a card when duplicate just in hand"""
        self.plr.coins.set(6)
        self.plr.piles[Piles.RESERVE].set()
        self.plr.piles[Piles.HAND].set("Duplicate")
        self.plr.buy_card(self.g["Gold"])
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
