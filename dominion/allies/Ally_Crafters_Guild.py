#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Crafters%27_Guild"""

import unittest
from dominion import Card, Game, Ally


###############################################################################
class Ally_Crafters_Guild(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """At the start of your turn, you may spend 2 Favors to gain a card costing up to $4 onto your deck."""
        self.name = "Crafters' Guild"

    def hook_start_turn(self, game, player):
        if player.favors.get() < 2:
            return
        player.output("Crafters' Guild lets you gain a card for 2 favours")
        card = player.plr_gain_card(4, destination="deck")
        if card:
            player.favors.add(-2)


###############################################################################
class Test_Crafters_Guild(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, ally="Crafters' Guild", initcards=["Underling"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_flag(self):
        self.plr.favors.set(5)
        self.plr.test_input = ["Get Silver"]
        self.plr.start_turn()
        self.assertEqual(self.plr.favors.get(), 3)
        self.assertIn("Silver", self.plr.deck)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
