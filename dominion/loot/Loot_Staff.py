#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Staff"""
import unittest
from typing import Any

from dominion import Loot, Card, Game, Piles, Player


###############################################################################
class Loot_Staff(Loot.Loot):
    """Staff"""

    def __init__(self):
        Loot.Loot.__init__(self)
        self.cardtype = [Card.CardType.LOOT, Card.CardType.TREASURE]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "$3; +1 Buy; You may play an Action from your hand."
        self.name = "Staff"
        self.coin = 3
        self.buys = 1
        self.cost = 7
        self.pile = "Loot"

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """You may play an Action from your hand."""
        actions: list[tuple[str, Any]] = [(f"Play {_}", _) for _ in player.piles[Piles.HAND] if _.isAction()]
        if not actions:
            player.output("No applicable cards")
            return
        actions.insert(0, ("Play nothing", None))
        if play := player.plr_choose_options("Staff: Play a card from your hand", *actions):
            player.play_card(play, cost_action=False, discard=False)


###############################################################################
class TestStaff(unittest.TestCase):
    """Test Staff"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Cursed"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        # Remove all other cards from loot pile, so we know what we will draw
        mods = 1
        while mods > 0:
            mods = 0
            for loot in self.g.card_piles["Loot"]:
                if loot.name != "Staff":
                    self.g.card_piles["Loot"].remove(loot.name)
                    mods += 1

    def test_playing(self):
        """Test playing a staff"""
        self.plr.piles[Piles.HAND].set("Moat")
        staff = self.g.get_card_from_pile("Loot", "Staff")
        self.plr.add_card(staff, Piles.HAND)
        self.plr.test_input = ["Moat"]
        self.plr.play_card(staff)
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
