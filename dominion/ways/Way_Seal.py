#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Card, Game, Way, Piles, Player, OptionKeys


###############################################################################
class Way_Seal(Way.Way):
    def __init__(self) -> None:
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+1 Coin; This turn, when you gain a card, you may put it onto your deck."
        self.name = "Way of the Seal"

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.coins.add(1)

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        mod = {}
        if player.plr_choose_options(
            f"Seal: Where to put {card}?",
            (f"Put {card} on discard", False),
            (f"Put {card} on top of deck", True),
        ):
            player.output(f"Putting {card} on deck due to Way of the Seal")
            mod[OptionKeys.DESTINATION] = Piles.TOPDECK
        return mod


###############################################################################
class TestSeal(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            ways=["Way of the Seal"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Moat")
        self.way = self.g.ways["Way of the Seal"]

    def test_play(self) -> None:
        """Perform a Seal"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["top of deck"]
        self.plr.perform_way(self.way, self.card)
        self.plr.gain_card("Gold")
        self.assertEqual(self.plr.piles[Piles.DECK].top_card().name, "Gold")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
