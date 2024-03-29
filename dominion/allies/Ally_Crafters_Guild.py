#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Crafters%27_Guild"""

import unittest
from dominion import Card, Game, Piles, Ally, Player


###############################################################################
class Ally_Crafters_Guild(Ally.Ally):
    def __init__(self) -> None:
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """At the start of your turn, you may spend 2 Favors to gain a card costing up to $4 onto your deck."""
        self.name = "Crafters' Guild"

    def hook_start_turn(self, game: Game.Game, player: Player.Player) -> None:
        if player.favors.get() < 2:
            return
        player.output("Crafters' Guild lets you gain a card for 2 favours")
        if player.plr_gain_card(4, destination=Piles.DECK):
            player.favors.add(-2)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return None


###############################################################################
class TestCraftersGuild(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, allies="Crafters' Guild", initcards=["Underling"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_flag(self) -> None:
        self.plr.favors.set(5)
        self.plr.test_input = ["Get Silver"]
        self.plr.start_turn()
        self.assertEqual(self.plr.favors.get(), 3)
        self.assertIn("Silver", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
