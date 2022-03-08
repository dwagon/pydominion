#!/usr/bin/env python

import unittest
from dominion import Card, Game, Event


###############################################################################
class Event_Summon(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Game.PROMO
        self.desc = """Gain an Action card costing up to 4. Set it asidee
            If you do, then at the start of your next turn, play it"""
        self.name = "Summon"
        self.cost = 5
        self._card = None

    def special(self, game, player):
        """Gain an Action card costing up to 4"""
        player.plrGainCard(4, types={Card.TYPE_ACTION: True}, destination="duration")
        print("Unimplemented")


###############################################################################
# class XTest_Summon(unittest.TestCase):
#    def setUp(self):
#        import Game
#        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Summon'], initcards=['Moat'])
#        self.g.start_game()
#        self.plr = self.g.player_list()[0]
#        self.card = self.g.events['Summon']
#
#    def test_with_summon(self):
#        """ Use Summon """
#        self.plr.addCoin(5)
#        self.plr.test_input = ['moat']
#        self.plr.performEvent(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
