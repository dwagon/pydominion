#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Cave_Dwellers """

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_CaveDwellers(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = """At the start of your turn, you may spend a Favor to discard a card, then draw a card. Repeat as desired."""
        self.name = "Cave Dwellers"

    def hook_start_turn(self, game, player):
        for _ in range(player.get_favors()):
            doit = player.plr_choose_options(
                    "Cave Dwellers:",
                    ("Do nothing", False),
                    ("Spend a favor to discard and draw a card?", True)
                    )
            if doit:
                player.plr_discard_cards()
                player.pickup_card()
                player.add_favors(-1)
            else:
                break


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return []


###############################################################################
class Test_CaveDwellers(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            ally="Cave Dwellers",
            initcards=["Underling"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        """Play card"""
        self.plr.set_deck("Copper", "Copper", "Copper", "Copper")
        self.plr.set_hand("Estate", "Duchy", "Gold")
        self.plr.set_favors(2)
        self.plr.test_input = ["Spend", "Discard Estate", "Spend", "Discard Duchy"]
        self.plr.start_turn()
        self.assertEqual(self.plr.get_favors(), 2 - 2)
        self.assertIsNone(self.plr.in_hand("Estate"))
        self.assertIsNotNone(self.plr.discardpile["Duchy"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
