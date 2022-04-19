#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Crafters%27_Guild"""

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_Crafters_Guild(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = """At the start of your turn, you may spend 2 Favors to gain a card costing up to $4 onto your deck."""
        self.name = "Crafters Guild"

    def hook_start_turn(self, game, player):
        if player.get_favors() < 2:
            return
        player.output("Crafters' Guild lets you gain a card for 2 favours")
        card = player.plr_gain_card(4, destination="deck")
        if card:
            player.add_favors(-2)


###############################################################################
class Test_Crafters_Guild(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            ally="Crafters Guild",
            initcards=["Underling"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_flag(self):
        self.plr.set_favors(5)
        self.plr.test_input = ["Get Silver"]
        self.plr.start_turn()
        self.assertEqual(self.plr.get_favors(), 3)
        self.assertIsNotNone(self.plr.in_deck("Silver"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
