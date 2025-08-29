#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Captain(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.REACTION,
            Card.CardType.COMMAND,
        ]
        self.base = Card.CardExpansion.PROMO
        self.desc = """Now and at the start of your next turn:
            Play a non-Duration, non-Command Action card from the Supply costing
            up to 4 Coin, leaving it there."""
        self.name = "Captain"
        self.cost = 6

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        special_sauce(game, player)

    def duration(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, str]:
        special_sauce(game, player)
        return {}


def special_sauce(game: "Game.Game", player: "Player.Player") -> None:
    options: list[tuple[str, Any]] = [("None", None)]
    for name in game.get_action_piles(4):
        card = game.card_instances[name]
        if card.isDuration():
            continue
        if card.isCommand():
            continue
        options.append((f"Play {name}", card))

    if action := player.plr_choose_options("What action card do you want to imitate?", *options):
        player.output(f"Playing {action} through Captain")
        player.card_benefits(action)


###############################################################################
class TestCaptain(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Captain", "Workshop", "Bureaucrat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Captain")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_bureaucrat(self) -> None:
        """Make the Captain be a Bureaucrat"""
        self.plr.test_input = ["Bureaucrat"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DECK])

    def test_play_market(self) -> None:
        """Make the Captain be a Workshop"""
        self.plr.test_input = ["Play Workshop", "Get Bureaucrat"]
        self.plr.play_card(self.card)
        self.assertNotIn("Workshop", self.plr.piles[Piles.DISCARD])
        self.assertIn("Bureaucrat", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
