#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/War_Chest"""

import unittest
from typing import Any

from dominion import Piles, NoCardException, Card, Game, Player

WAR_CHEST = "war chest"


###############################################################################
class Card_War_Chest(Card.Card):
    """War Chest"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """The player to your left names a card.
        Gain a card costing up to $5 that hasn't been named for War Chest this turn."""
        self.name = "War Chest"
        self.cost = 5

    def hook_start_turn(self, game: Game.Game, player: Player.Player) -> None:
        player.specials[WAR_CHEST] = []

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if WAR_CHEST not in player.specials:
            player.specials[WAR_CHEST] = []

        banned = get_banned_card(game, player)
        player.specials[WAR_CHEST].append(banned)
        card_name = player.plr_choose_options("Pick a card to gain", *generate_war_chest_options(player))
        try:
            player.gain_card(card_name)
        except NoCardException:
            player.output(f"No more {card_name}")


###############################################################################
def get_banned_card(game: Game.Game, player: Player.Player) -> str:
    """Return the banned card that can't be selected"""
    lefty = game.player_to_left(player)
    options = [(f"Pick {card}", card.name) for card in player.cards_under(5) if card.purchasable]
    banned = lefty.plr_choose_options(
        f"Name a card that {player} can't gain from a War Chest this turn",
        *options,
    )
    return banned


###############################################################################
def generate_war_chest_options(player: Player.Player) -> list[tuple[str, str]]:
    """Generate list of options to select cards"""
    options = [
        (f"Gain {card}", card.name)
        for card in player.cards_under(5)
        if card.purchasable and card.name not in player.specials[WAR_CHEST]
    ]
    return options


###############################################################################
def botresponse(  # pragma: no coverage, pylint: disable=unused-argument
    player: Player.Player, kind: str, args: Any = None, kwargs: Any = None
) -> Any:
    """Name a generally useful card"""
    return "Silver"


###############################################################################
class TestWarChest(unittest.TestCase):
    """Test War Chest"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["War Chest"], badcards=["Silver Mine"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g.get_card_from_pile("War Chest")

    def test_play_card(self) -> None:
        """Play this card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.oth.test_input = ["Pick Duchy"]
        self.plr.test_input = ["Gain Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
