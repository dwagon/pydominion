#!/usr/bin/env python

import contextlib
import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, NoCardException, Phase, OptionKeys


###############################################################################
class Card_Den_of_Sin(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT, Card.CardType.DURATION]
        self.base = Card.CardExpansion.NOCTURNE
        self.name = "Den of Sin"
        self.cost = 5

    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return """At the start of your next turn, +2 Cards;
                    This is gained to your hand (instead of your discard pile)."""
        return "At the start of your next turn, +2 Cards"

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        for _ in range(2):
            with contextlib.suppress(NoCardException):
                player.pickup_card()
        return {}

    def hook_gain_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        return {OptionKeys.DESTINATION: Piles.HAND}


###############################################################################
class Test_Den_of_Sin(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Den of Sin"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Den of Sin")

    def test_gain(self) -> None:
        self.plr.gain_card("Den of Sin")
        self.assertIn("Den of Sin", self.plr.piles[Piles.HAND])

    def test_duration(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
