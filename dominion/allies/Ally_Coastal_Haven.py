#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Coastal_Haven"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Ally, Player, OptionKeys, PlayArea

HAVEN = "coastal haven"


###############################################################################
class Ally_Coastal_Haven(Ally.Ally):
    """Coastal Haven"""

    def __init__(self) -> None:
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """When discarding your hand in Clean-up, you may spend any number of Favors
                to keep that many cards in hand for next turn (you still draw 5)."""
        self.name = "Coastal Haven"

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        if player.favors.get() == 0:
            return {}
        if HAVEN not in player.specials:
            player.specials[HAVEN] = PlayArea.PlayArea("Coastal Haven", initial=[])
        cards = player.card_sel(
            num=player.favors.get(), prompt="Spend a favor per card to keep in hand for next turn", cardsrc=Piles.HAND
        )
        for card in cards:
            player.move_card(card, player.specials[HAVEN])
            player.secret_count += 1
            player.favors.add(-1)
        return {}

    def hook_start_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        for card in player.specials.get(HAVEN, []):
            player.move_card(card, Piles.HAND)
            player.secret_count -= 1
        player.specials[HAVEN] = PlayArea.PlayArea("Coastal Haven", initial=[])


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover pylint: disable=unused-argument
    """Just make never select anything to keep"""
    return []


###############################################################################
class Test_Coastal_Haven(unittest.TestCase):
    """Test Coastal Haven"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, allies="Coastal Haven", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card(self) -> None:
        """Play ally"""
        self.plr.piles[Piles.HAND].set("Gold", "Silver", "Copper", "Underling", "Duchy", "Province")
        self.plr.test_input = ["Select Gold", "Select Underling", "Finish"]
        self.plr.favors.set(2)
        self.plr.end_turn()
        self.assertEqual(self.plr.favors.get(), 0)
        self.plr.start_turn()
        self.g.print_state()
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Underling", self.plr.piles[Piles.HAND])
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
