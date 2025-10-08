#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Lighthouse"""
import unittest

from dominion import Game, Piles, Card, Player, OptionKeys


###############################################################################
class Card_Lighthouse(Card.Card):
    """Lighthouse"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.desc = """+1 Action. +$1. At the start of your next turn, +$1.
        Until then, when another player plays an Attack card, it doesn't affect you."""
        self.name = "Lighthouse"
        self.base = Card.CardExpansion.SEASIDE
        self.defense = True
        self.actions = 1
        self.cost = 2

    def duration(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, str]:
        player.coins.add(1)
        return {}

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        player.coins.add(1)


###############################################################################
class TestLighthouse(unittest.TestCase):
    """Test Lighthouse"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Lighthouse"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Lighthouse")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Test play"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
