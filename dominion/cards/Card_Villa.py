#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Villa"""

import unittest
from typing import Optional, Any

from dominion import Card, Game, Piles, Player, OptionKeys, Phase


###############################################################################
class Card_Villa(Card.Card):
    """Villa"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Villa"
        self.cost = 4
        self.actions = 2
        self.buys = 1
        self.coin = 1

    def dynamic_description(self, player: Player.Player) -> str:
        """Variable desc"""
        if player.phase == Phase.ACTION:
            return "+2 Actions; +1 Buy; +1 Coin"
        return """+2 Actions; +1 Buy; +1 Coin; When you gain this, put it into
            your hand, +1 Action, and if it's your Buy phase return to your
            Action phase."""

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, Any]:
        if player.phase == Phase.BUY:
            player.phase = Phase.ACTION
        player.add_actions(1)
        return {OptionKeys.DESTINATION: Piles.HAND}


###############################################################################
class Test_Villa(unittest.TestCase):
    """Test Villa"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Villa"], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Villa")

    def test_play(self) -> None:
        """Test playing a villa"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_gain(self) -> None:
        """Test gaining a villa"""
        self.plr.phase = Phase.BUY
        self.plr.gain_card("Villa")
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.phase, Phase.ACTION)
        self.assertIn("Villa", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
