#!/usr/bin/env python

import contextlib
import unittest
from typing import Any

from dominion import Game, Card, Piles, NoCardException, Player, OptionKeys


###############################################################################
class Card_Hireling(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+1 Card forever"
        self.name = "Hireling"
        self.cost = 6
        self.permanent = True

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        with contextlib.suppress(NoCardException):
            player.pickup_card()
        return {}


###############################################################################
class Test_Hireling(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Hireling"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Hireling")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_hireling(self) -> None:
        """Play a hireling"""
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertNotIn("Hireling", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
