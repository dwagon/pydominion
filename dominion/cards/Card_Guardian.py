#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Guardian"""
import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Guardian(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT, Card.CardType.DURATION]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """Until your next turn, when another player plays an
            Attack card, it doesn't affect you. At the start of your next turn,
            +1 Coin."""
        self.name = "Guardian"
        self.defense = True
        self.cost = 2

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        player.coins.add(1)
        return {}

    def hook_gain_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        return {OptionKeys.DESTINATION: Piles.HAND}


###############################################################################
class TestGuardian(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Guardian"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Guardian")

    def test_gain(self) -> None:
        self.plr.gain_card("Guardian")
        self.assertIn("Guardian", self.plr.piles[Piles.HAND])

    def test_duration(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
