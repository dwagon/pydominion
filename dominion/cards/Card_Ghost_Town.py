#!/usr/bin/env python

import contextlib
import unittest
from dominion import Card, Game, Piles, Player, NoCardException, OptionKeys, Phase


###############################################################################
class Card_Ghost_Town(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT, Card.CardType.DURATION]
        self.base = Card.CardExpansion.NOCTURNE
        self.name = "Ghost Town"
        self.cost = 3

    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return """At the start of your next turn, +1 Card and +1 Action. This
                is gained to your hand (instead of your discard pile)."""
        return "At the start of your next turn, +1 Card and +1 Action."

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        return {OptionKeys.DESTINATION: Piles.HAND}

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        with contextlib.suppress(NoCardException):
            player.pickup_card()
        player.add_actions(1)
        return {}


###############################################################################
class TestGhostTown(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Ghost Town"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.gtown = self.g.get_card_from_pile("Ghost Town")

    def test_play_card(self) -> None:
        """Play Ghost Town"""
        self.plr.add_card(self.gtown, Piles.HAND)
        self.plr.play_card(self.gtown)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_gain(self) -> None:
        self.plr.gain_card("Ghost Town")
        self.assertNotIn("Ghost Town", self.plr.piles[Piles.DISCARD])
        self.assertIn("Ghost Town", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
