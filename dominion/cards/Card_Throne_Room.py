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
        options: list[dict[str, Any]] = [{"selector": "0", "print": "Don't play a card", "card": None}]
        index = 1
        for card in player.playable_actions():
            options.append({"selector": f"{index}", "print": f"Play {card} twice", "card": card})
            index += 1
        if index == 1:
            return
        o = player.user_input(options, "Play which action card twice?")
        if not o["card"]:
            return
        player.output(f"Play 1 of {o['card']}")
        player.play_card(o["card"], discard=False, cost_action=False)
        player.output(f"Play 2 of {o['card']}")
        player.play_card(o["card"], cost_action=False)


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
