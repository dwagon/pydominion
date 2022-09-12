#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Band_of_Nomads"""

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_Band_Nomads(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = "When you gain a card costing $3 or more, you may spend a Favor, for +1 Card, or +1 Action, or +1 Buy."
        self.name = "Band of Nomads"

    def hook_gain_card(self, game, player, card):
        if card.cost < 3:
            return
        chc = player.plr_choose_options(
            "Spend a favor to choose One: ",
            ("Nothing", "none"),
            ("+1 Card", "card"),
            ("+1 Action", "action"),
            ("+1 Buy", "buy"),
        )
        if chc == "nothing":
            return
        player.favors.add(-1)
        if chc == "card":
            player.pickup_card()
        elif chc == "action":
            player.add_actions(1)
        elif chc == "buy":
            player.add_buys(1)


###############################################################################
class Test_Band_Nomads(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, ally="Band of Nomads", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play_card(self):
        """Play and gain a card"""
        self.plr.favors.set(1)
        hndsz = self.plr.hand.size()
        self.plr.test_input = ["+1 Card"]
        self.plr.gain_card("Silver")
        self.assertEqual(self.plr.hand.size(), hndsz + 1)

    def test_play_actions(self):
        """Play and gain an action"""
        self.plr.favors.set(1)
        acts = self.plr.actions.get()
        self.plr.test_input = ["+1 Action"]
        self.plr.gain_card("Silver")
        self.assertEqual(self.plr.actions.get(), acts + 1)

    def test_play_buys(self):
        """Play and gain a buys"""
        self.plr.favors.set(1)
        bys = self.plr.get_buys()
        self.plr.test_input = ["+1 Buy"]
        self.plr.gain_card("Silver")
        self.assertEqual(self.plr.get_buys(), bys + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
