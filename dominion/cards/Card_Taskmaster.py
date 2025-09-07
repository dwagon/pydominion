#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Taskmaster"""
import unittest
from typing import Any

from dominion import Game, Card, Piles, OptionKeys, Player


###############################################################################
class Card_Taskmaster(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+1 Action, +$1, and if you gain a card costing exactly $5 this turn,
            then at the start of your next turn, repeat this ability."""
        self.name = "Taskmaster"
        self.cost = 3
        self.actions = 1
        self.coin = 1
        self.trigger = False

    def hook_gain_card(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, Any]:
        if card.cost == 5:
            self.trigger = True
        return {}

    def duration(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, str]:
        if self.trigger:
            player.actions.add(1)
            player.coins.add(1)
        self.trigger = False
        return {}


###############################################################################
class Test_Taskmaster(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Taskmaster"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Taskmaster")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_no_gain(self):
        """Play a Taskmaster with no gain"""
        actions = self.plr.actions.get()
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 1 - 1)
        self.assertEqual(self.plr.coins.get(), coins + 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 0)

    def test_play_gain(self):
        """Play a Taskmaster with gain"""
        actions = self.plr.actions.get()
        coins = self.plr.coins.get()
        self.plr.gain_card("Duchy")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 1 - 1)
        self.assertEqual(self.plr.coins.get(), coins + 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
