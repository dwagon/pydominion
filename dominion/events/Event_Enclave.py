#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Enclave """

import unittest
from dominion import Game, Event


###############################################################################
class Event_Enclave(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "Gain a Gold. Exile a Duchy from the Supply."
        self.name = "Enclave"
        self.cost = 8

    def special(self, game, player):
        player.gainCard("Gold")
        player.exile_card("Duchy")


###############################################################################
class Test_Enclave(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            eventcards=["Enclave"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Enclave"]

    def test_Enclave(self):
        """Use Enclave"""
        self.plr.addCoin(8)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.in_discard("Gold"))
        self.assertIsNotNone(self.plr.in_exile("Duchy"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
