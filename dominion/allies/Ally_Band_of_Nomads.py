#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Band_of_Nomads"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Ally, OptionKeys, Player


###############################################################################
class Ally_Band_Nomads(Ally.Ally):
    """Band of Nomads"""

    def __init__(self) -> None:
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """When you gain a card costing $3 or more, you may spend a Favor,
            for +1 Card, or +1 Action, or +1 Buy."""
        self.name = "Band of Nomads"

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if card.cost < 3 or player.favors.get() <= 0:
            return {}
        chc = player.plr_choose_options(
            "Spend a favor to choose One: ",
            ("Nothing", "none"),
            ("+1 Card", "card"),
            ("+1 Action", "action"),
            ("+1 Buy", "buy"),
        )
        if chc == "nothing":
            return {}
        player.favors.add(-1)
        if chc == "card":
            player.pickup_card()
        elif chc == "action":
            player.add_actions(1)
        elif chc == "buy":
            player.buys.add(1)
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    """Bot Response"""
    return "nothing"


###############################################################################
class Test_Band_Nomads(unittest.TestCase):
    """Test Band of Nomads"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, allies="Band of Nomads", initcards=["Underling"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card(self) -> None:
        """Play and gain a card"""
        self.plr.favors.set(1)
        hndsz = self.plr.piles[Piles.HAND].size()
        self.plr.test_input = ["+1 Card"]
        self.plr.gain_card("Silver")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hndsz + 1)

    def test_play_actions(self) -> None:
        """Play and gain an action"""
        self.plr.favors.set(1)
        acts = self.plr.actions.get()
        self.plr.test_input = ["+1 Action"]
        self.plr.gain_card("Silver")
        self.assertEqual(self.plr.actions.get(), acts + 1)

    def test_play_buys(self) -> None:
        """Play and gain a buys"""
        self.plr.favors.set(1)
        bys = self.plr.buys.get()
        self.plr.test_input = ["+1 Buy"]
        self.plr.gain_card("Silver")
        self.assertEqual(self.plr.buys.get(), bys + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
