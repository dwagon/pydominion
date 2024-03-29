#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Charm"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Charm(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """When you play this, choose one: +1 Buy and +2 Coin; or
            the next time you buy a card this turn, you may also gain a differently
            named card with the same cost."""
        self.name = "Charm"
        self.cost = 5
        self.buy_trigger = False

    def special(self, game, player):
        ans = player.plr_choose_options(
            "Pick One",
            ("+1 Buy and +2 Coin", True),
            (
                "Next time you buy a card this turn, you may also gain a differently named card with the same cost.",
                False,
            ),
        )
        if ans:
            player.buys.add(1)
            player.coins.add(2)
        else:
            self.buy_trigger = True

    def hook_buy_card(self, game, player, card):
        if not self.buy_trigger:
            return
        self.buy_trigger = False
        cost = card.cost
        player.plr_gain_card(cost=cost, modifier="equal", exclude=[card.name])


###############################################################################
class TestCharm(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Charm"], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Charm")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_choose_one(self):
        self.plr.test_input = ["+1 Buy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_play_choose_two(self):
        self.plr.test_input = ["next time"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.test_input = ["Get Duchy"]
        self.plr.coins.set(5)
        self.plr.buy_card("Charm")
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
