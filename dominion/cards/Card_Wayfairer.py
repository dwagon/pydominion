#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Wayfarer """

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Wayfarer(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+3 Cards; You may gain a Silver. This has the same cost as the last other card gained this turn, if any."
        self.name = "Wayfarer"
        self.cards = 3
        self.cost = 6

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            player.gain_card("Silver")
            player.output("Gained a Silver")
        except NoCardException:
            player.output("No more Silver")

    def hook_this_card_cost(self, game: Game.Game, player: Player.Player) -> int:
        if player.stats["gained"]:
            last_cost = player.stats["gained"][0].cost
            delta = -6 + last_cost
            return delta
        return 0


###############################################################################
class TestWayfarer(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Wayfarer"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Wayfarer")
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self) -> None:
        """Play a wayfairer"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 3)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_buy(self) -> None:
        """Buy a wayfairer"""
        cost = self.plr.card_cost(self.card)
        self.assertEqual(cost, 6)
        self.plr.gain_card("Estate")
        cost = self.plr.card_cost(self.card)
        self.assertEqual(cost, 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
