#!/usr/bin/env python

import unittest
import Game
from Event import Event


###############################################################################
class Event_Raid(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = "Gain a Silver per Silver that you have in play. Each other player puts his -1 Card token on his deck"
        self.name = "Raid"
        self.cost = 5

    def special(self, game, player):
        """ Gain a Silver per Silver that you have in play. Each other player
        puts his -1 Card token on his deck"""
        for victim in player.attackVictims():
            victim.card_token = True
            victim.output("-1 Card token active due to Raid event by %s" % player.name)
        count = 0
        for c in player.hand + player.played:
            if c.name == 'Silver':
                player.gainCard('Silver')
                count += 1
        player.output("Gained %d Silvers from Raid" % count)


###############################################################################
class Test_Raid(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, eventcards=['Raid'], initcards=['Militia'])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.events['Raid']

    def test_play(self):
        """ Perform a Raid """
        self.plr.addCoin(5)
        self.plr.setHand('Silver', 'Silver')
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.buys, 0)
        self.assertEqual(self.plr.discardpile.size(), 2)
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Silver')
        self.assertTrue(self.victim.card_token)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
