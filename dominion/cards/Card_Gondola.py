#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Gondola"""

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Gondola(Card.Card):
    """Gondola"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.DURATION]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Either now or at the start of your next turn: +$2. When you gain this,
        you may play an Action card from your hand."""
        self.name = "Gondola"
        self.cost = 4
        self._choice = "undef"

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Gain a copy of a card anyone has in play."""
        choice = player.plr_choose_options(
            "Pick One",
            ("Now: +$2", "now"),
            ("Next Turn: +$2", "then"),
        )
        if choice == "now":
            player.coins.add(2)
            self._choice = "now"
        else:
            self._choice = "then"

    def duration(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        if self._choice == "then":
            player.coins.add(2)
        self._choice = "undef"
        return {}

    def hook_gain_this_card(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        """When you gain this, you may play an Action card from your hand."""
        actions = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        if not actions:
            player.output("No action cards in hand")
            return {}
        choices: list[tuple[str, Any]] = [("Don't play a card", None)]
        for _ in actions:
            choices.append((f"Play {_}", _))
        if card := player.plr_choose_options("Play a card from your hand", *choices):
            player.play_card(card, cost_action=False)

        return {}


###############################################################################
class TestGondola(unittest.TestCase):
    """Test Gondola"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Gondola", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Gondola")

    def test_gain(self) -> None:
        """Gain Card"""
        self.plr.piles[Piles.HAND].set("Silver", "Gold", "Moat")
        self.plr.test_input = ["Play Moat"]
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.gain_card("Gondola")
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 2 - 1)  # -1 for using moat; +2 for playing moat

    def test_gain_no_actions(self) -> None:
        """Gain Card but with no actions"""
        self.plr.piles[Piles.HAND].set("Silver", "Gold")
        self.plr.gain_card("Gondola")
        self.assertIn("No action cards in hand", self.plr.messages)

    def test_play_now(self) -> None:
        """Play Gondola this turn"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Now"]
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)

    def test_play_then(self) -> None:
        """Play Gondola next turn"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Next"]
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
