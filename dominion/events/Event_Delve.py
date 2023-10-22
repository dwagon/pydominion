#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Delve """

import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Delve(Event.Event):
    """Delve"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "+1 Buy. Gain a Silver."
        self.name = "Delve"
        self.cost = 2

    def special(self, game, player):
        player.buys.add(1)
        player.gain_card("Silver")


###############################################################################
class Test_Delve(unittest.TestCase):
    """Test Delve"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Delve"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Delve"]

    def test_play(self):
        """Perform a Delve"""
        self.plr.coins.add(2)
        bys = self.plr.buys.get()
        self.plr.perform_event(self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Silver"])
        self.assertEqual(self.plr.buys.get(), bys + 1 - 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
