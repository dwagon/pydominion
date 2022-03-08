#!/usr/bin/env python

import unittest
from dominion import Game, Event


###############################################################################
class Event_Populate(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "Gain one card from each Action Supply pile."
        self.name = "Populate"
        self.cost = 10

    def special(self, game, player):
        for cp in game.cardpiles.values():
            if cp.isAction() and cp.insupply:
                player.output("Gained {} from Populate".format(cp.name))
                player.gainCard(cp)


###############################################################################
class Test_Populate(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            eventcards=["Populate"],
            initcards=[
                "Cellar",
                "Chapel",
                "Moat",
                "Militia",
                "Village",
                "Workshop",
                "Gardens",
                "Mine",
                "Library",
                "Lurker",
            ],
            badcards=["Hostelry", "Border Village", "Inn"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Populate"]

    def test_Populate(self):
        """Use Populate"""
        self.plr.addCoin(10)
        self.plr.performEvent(self.card)
        self.assertIsNotNone(self.plr.in_discard("Moat"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
