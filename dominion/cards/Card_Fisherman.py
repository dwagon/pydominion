#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Fisherman """

import unittest
from dominion import Game, Card, Piles, Phase, Player


###############################################################################
class Card_Fisherman(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.name = "Fisherman"
        self.coin = 1
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def dynamic_description(self, player: "Player.Player") -> str:
        if player.phase == Phase.BUY:
            return """+1 Card; +1 Action; +1 Coin; During your turns, if your discard pile is empty, 
            this costs 3 Coin less."""
        return "+1 Card; +1 Action; +1 Coin"

    def hook_this_card_cost(self, game: "Game.Game", player: "Player.Player") -> int:
        if player.piles[Piles.DISCARD].is_empty():
            return -3
        return 0


###############################################################################
class TestFisherman(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Fisherman"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Fisherman")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play the card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)

    def test_buy_card(self) -> None:
        """Buy the card"""
        self.plr.piles[Piles.DISCARD].set("Copper")
        self.plr.phase = Phase.BUY
        self.assertEqual(self.plr.card_cost(self.card), 5)
        self.assertIn("During", self.card.description(self.plr))
        self.plr.piles[Piles.DISCARD].set()
        self.assertEqual(self.plr.card_cost(self.card), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
