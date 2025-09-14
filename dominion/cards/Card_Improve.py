#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, OptionKeys, Player


###############################################################################
class Card_Improve(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """+2 Coin; At the start of Clean-up, you may trash an Action
        card you would discard from play this turn, to gain a card costing exactly
        1 more than it."""
        self.name = "Improve"
        self.cost = 3
        self.coin = 2

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        acts = [_ for _ in player.piles[Piles.HAND] + player.piles[Piles.DISCARD] if _.isAction()]
        if not acts:
            return {}
        tt = player.plr_trash_card(cardsrc=acts, prompt="Trash a card through Improve")
        if not tt:
            return {}
        cost = tt[0].cost
        player.plr_gain_card(cost + 1, modifier="equal")
        return {}


###############################################################################
class Test_Improve(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Improve", "Moat", "Guide"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Improve")
        self.card.player = self.plr

    def test_play(self) -> None:
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.test_input = ["End phase", "End phase", "Trash Moat", "Get Guide"]
        self.plr.turn()
        self.assertIn("Moat", self.g.trash_pile)
        self.assertIn("Guide", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
