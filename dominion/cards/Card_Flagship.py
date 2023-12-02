#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Flagship"""

import unittest

from dominion.Game import Game, TestGame
from dominion.Card import Card, CardType, CardExpansion
from dominion import Piles, OptionKeys
from dominion.Player import Player


###############################################################################
class Card_Flagship(Card):
    """Flagship"""

    def __init__(self) -> None:
        Card.__init__(self)
        self.cardtype = [
            CardType.ACTION,
            CardType.DURATION,
            CardType.COMMAND,
        ]
        self.base = CardExpansion.PROSPERITY
        self.desc = "+$2; The next time you play a non-Command Action card, replay it."
        self.coin = 2
        self.name = "Flagship"
        self.cost = 4
        self.permanent = True

    def hook_post_play(
        self, game: Game, player: Player, card: Card
    ) -> dict[OptionKeys, str]:
        """The next time you play a non-Command Action card, replay it."""
        if not card.isAction() or card.isCommand():
            return {}
        player.output(f"Flagship plays {card} again")
        player.play_card(card, cost_action=False, discard=False, post_action_hook=False)
        player.move_card(self, Piles.DISCARD)
        return {}


###############################################################################
class TestFlagship(unittest.TestCase):
    """Test Flagship"""

    def setUp(self) -> None:
        self.g = TestGame(numplayers=1, initcards=["Flagship", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Flagship")

    def test_play_card(self) -> None:
        """Play this card"""
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)
        self.assertIn("Flagship", self.plr.piles[Piles.DURATION])

    def test_play_action(self) -> None:
        """Play an action"""
        moat = self.g.get_card_from_pile("Moat")
        hand_size = self.plr.piles[Piles.HAND].size()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.plr.add_card(moat, Piles.HAND)
        self.plr.play_card(moat)
        self.assertNotIn("Flagship", self.plr.piles[Piles.DURATION])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hand_size + 2 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
