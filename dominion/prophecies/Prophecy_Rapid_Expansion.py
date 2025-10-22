#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Rapid_Expansion"""

import unittest
from typing import Any

from dominion import Card, Game, Prophecy, Player, OptionKeys, PlayArea, Piles

RAPID_EXPANSION = "rapid_expansion"


###############################################################################
class Prophecy_Rapid_Expansion(Prophecy.Prophecy):
    """Rapid Expansion"""

    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "When you gain an Action or Treasure, set it aside, and play it at the start of your next turn."
        self.name = "Rapid Expansion"

    def hook_gain_card(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, Any]:
        if RAPID_EXPANSION not in player.specials:
            player.specials[RAPID_EXPANSION] = PlayArea.PlayArea("Rapid Expansion", game)
        if card.isAction() or card.isTreasure():
            player.output(f"Rapid Expansion: Setting {card} aside")
            player.move_card(card, player.specials[RAPID_EXPANSION])
            player.secret_count += 1
            return {OptionKeys.DONTADD: True}
        return {}

    def hook_start_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        if RAPID_EXPANSION not in player.specials:
            return
        for card in player.specials[RAPID_EXPANSION]:
            player.output(f"Getting {card} from Rapid Expansion")
            player.move_card(card, Piles.HAND)
            player.play_card(card, cost_action=False, move_card=False)
            player.secret_count -= 1
            if card.location == Piles.HAND:
                player.move_card(card, Piles.PLAYED)
        player.specials[RAPID_EXPANSION].empty()

    def debug_dump(self, player: "Player.Player") -> None:
        if RAPID_EXPANSION in player.specials and player.specials[RAPID_EXPANSION]:
            player.output(f"In {self.name}: ({player.secret_count=})")
            for card in player.specials[RAPID_EXPANSION]:
                player.output(f"\t{card}")


###############################################################################
class TestRapidExpansion(unittest.TestCase):
    """Test Rapid Expansion"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, prophecies=["Rapid Expansion"], initcards=["Mountain Shrine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.reveal_prophecy()

    def test_play(self) -> None:
        """Play when prophecy active"""
        self.plr.gain_card("Gold")
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])
        self.plr.end_turn()
        self.plr.start_turn()
        self.g.print_state()
        self.assertIn("Gold", self.plr.piles[Piles.PLAYED])
        self.assertEqual(self.plr.coins.get(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
