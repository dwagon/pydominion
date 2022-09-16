#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Trappers%27_Lodge"""

import unittest
from dominion import Card, Game, Ally


###############################################################################
class Ally_Trappers_Lodge(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """When you gain a card, you may spend a Favor to put it onto your deck."""
        self.name = "Trappers Lodge"

    def hook_gain_card(self, game, player, card):
        if not player.favors.get():
            return {}
        opt = player.plr_choose_options(
            "Use Trappers Lodge to put it onto your deck for a favour?",
            ("Do nothing", False),
            ("Put on to deck", True),
        )
        if opt:
            player.favors.add(-1)
            return {"destination": "topdeck"}
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return []


###############################################################################
class Test_Trappers_Lodge(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, ally="Trappers Lodge", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_gain_card(self):
        """Add to top deck"""
        self.plr.deck.set("Copper", "Copper")
        self.plr.favors.set(2)
        self.plr.test_input = ["Put on to deck"]
        self.plr.gain_card("Estate")
        self.assertEqual(self.plr.deck.top_card().name, "Estate")
        self.assertEqual(self.plr.favors.get(), 1)

    def test_keep(self):
        """Do nothing"""
        self.plr.deck.set("Copper", "Copper")
        self.plr.favors.set(2)
        self.plr.test_input = ["Do nothing"]
        self.plr.gain_card("Estate")
        self.assertNotEqual(self.plr.deck.top_card().name, "Estate")
        self.assertIn("Estate", self.plr.discardpile)
        self.assertEqual(self.plr.favors.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
