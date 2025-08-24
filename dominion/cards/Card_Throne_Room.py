#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Throne_Room"""
import unittest
from typing import Any

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_ThroneRoom(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "You may play an Action card from your hand twice."
        self.name = "Throne Room"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """You may choose an Action card in your hand. Play it twice"""
        choices: list[tuple[str, Any]] = [(f"Play {_} twice", _) for _ in player.playable_actions()]
        if not choices:
            player.output("No suitable cards")
            return
        choices.insert(0, ("Don't play a card", None))

        if choice := player.plr_choose_options("Play which action card twice?", *choices):
            player.output(f"Play 1 of {choice}")
            player.play_card(choice, discard=False, cost_action=False)
            player.output(f"Play 2 of {choice}")
            player.play_card(choice, cost_action=False)


###############################################################################
class TestThroneRoom(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Throne Room", "Mine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_action(self) -> None:
        # Test by playing mine twice on a copper. Cu -> Ag -> Au
        self.plr.piles[Piles.HAND].set("Copper", "Mine")
        card = self.plr.gain_card("Throne Room", Piles.HAND)
        assert card is not None
        self.plr.test_input = ["Play Mine", "Upgrade Copper", "Get Silver", "Upgrade Silver", "Get Gold"]
        self.plr.play_card(card)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Mine", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Mine", self.plr.piles[Piles.HAND])
        self.assertEqual(self.plr.actions.get(), 0)

    def test_do_nothing(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Mine")
        card = self.plr.gain_card("Throne Room", Piles.HAND)
        assert card is not None
        self.plr.test_input = ["0"]
        self.plr.play_card(card)

    def test_no_action(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Copper")
        card = self.plr.gain_card("Throne Room", Piles.HAND)
        assert card is not None
        self.plr.test_input = ["0"]
        self.plr.play_card(card)
        self.assertEqual(self.plr.test_input, ["0"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
