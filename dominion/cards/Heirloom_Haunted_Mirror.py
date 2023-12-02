#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Haunted_Mirror(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.HEIRLOOM]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Coin; When you trash this, you may discard an Action card, to gain a Ghost from its pile."
        self.name = "Haunted Mirror"
        self.cost = 0
        self.coin = 1
        self.required_cards = [("Card", "Ghost")]
        self.purchasable = False

    def hook_trash_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, Any]:
        ac = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        if not ac:
            player.output("No action cards in hand, no effect")
            return {}
        if player.plr_discard_cards(cardsrc=ac):
            player.gain_card("Ghost")
        return {}


###############################################################################
class Test_Haunted_Mirror(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Cemetery", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Haunted Mirror")

    def test_play(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_trash_nothing(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.trash_card(self.card)
        self.assertNotIn("Ghost", self.plr.piles[Piles.DISCARD])

    def test_trash(self) -> None:
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.test_input = ["Moat"]
        self.plr.trash_card(self.card)
        self.assertIn("Ghost", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
