#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/War Chest"""

import unittest
from typing import Any

from dominion import Piles, NoCardException
from dominion.Card import Card, CardType, CardExpansion
from dominion.Game import Game, TestGame
from dominion.Player import Player

WAR_CHEST = "war chest"


###############################################################################
class Card_WarChest(Card):
    """War Chest"""

    def __init__(self) -> None:
        Card.__init__(self)
        self.cardtype = CardType.TREASURE
        self.base = CardExpansion.PROSPERITY
        self.desc = """The player to your left names a card.
        Gain a card costing up to $5 that hasn't been named for War Chest this turn."""
        self.name = "War Chest"
        self.cost = 5

    def hook_start_turn(self, game: Game, player: Player) -> None:
        player.specials[WAR_CHEST] = []

    def special(self, game: Game, player: Player) -> None:
        if WAR_CHEST not in player.specials:
            player.specials[WAR_CHEST] = []

        lefty = game.player_to_left(player)
        options = [
            (f"Pick {card}", card.name)
            for card in player.cards_under(5)
            if card.purchasable
        ]
        banned = lefty.plr_choose_options(
            f"Name a card that {player.name} can't gain from a War Chest this turn",
            *options,
        )
        player.specials[WAR_CHEST].append(banned)
        card_name = player.plr_choose_options(
            "Pick a card to gain", *self.generate_options(game, player)
        )
        try:
            player.gain_card(card_name)
        except NoCardException:
            player.output(f"No more {card_name}")

    @classmethod
    def generate_options(cls, game: Game, player: Player) -> list[tuple[str, str]]:
        """Generate list of options to select cards"""
        options: list[tuple[str, str]] = []
        for name, _ in game.get_card_piles():
            if name in player.specials[WAR_CHEST]:
                continue
            card = game.card_instances[name]
            if player.card_cost(card) > 5:
                continue
            options.append((f"Get {name}", name))
        return options


###############################################################################
def botresponse(player: Player, kind: str, args: Any = None, kwargs: Any = None) -> Any:
    return "Silver"


###############################################################################
class TestWarChest(unittest.TestCase):
    """Test War Chest"""

    def setUp(self) -> None:
        self.g = TestGame(
            numplayers=2, initcards=["War Chest"], badcards=["Silver Mine"]
        )
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g.get_card_from_pile("War Chest")

    def test_play_card(self) -> None:
        """Play this card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.oth.test_input = ["Pick Duchy"]
        self.plr.test_input = ["Get Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
