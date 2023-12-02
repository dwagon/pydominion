#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Priest(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.name = "Priest"
        self.desc = "+2 Coin. Trash a card from your hand. For the rest of this turn, when you trash a card, +2 Coin."
        self.cost = 4
        self.coin = 2
        self.in_special = False

    ###########################################################################
    def special(self, game: Game.Game, player: Player.Player) -> None:
        self.in_special = True
        player.plr_trash_card(force=True)
        self.in_special = False

    ###########################################################################
    def hook_trash_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if not self.in_special:
            player.output("Adding 2 from Priest")
            player.coins.add(2)
        return {}


###############################################################################
class TestPriest(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Priest", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Priest")
        self.plr.add_card(self.card, Piles.HAND)
        self.moat = self.g.get_card_from_pile("Moat")
        self.plr.add_card(self.moat, Piles.HAND)
        self.gold = self.g.get_card_from_pile("Gold")
        self.plr.add_card(self.gold, Piles.HAND)

    def test_play_card(self) -> None:
        self.plr.test_input = ["Trash Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Moat", self.g.trash_pile)
        self.plr.trash_card(self.gold)
        self.assertEqual(self.plr.coins.get(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
