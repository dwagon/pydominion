#!/usr/bin/env python

import unittest
from Card import Card


class Card_Marauder(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'looter']
        self.base = 'darkages'
        self.desc = "Gain a Spoils from the Spoils pile. Each other player gains a Ruins."
        self.name = 'Marauder'
        self.cost = 4
        self.needspoils = True

    def special(self, game, player):
        for plr in player.attackVictims():
            plr.output("Gained a ruin from %s's Marauder" % player.name)
            plr.gainCard('Ruins')
        player.gainCard("Spoils")


###############################################################################
class Test_Marauder(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Marauder'])
        self.g.startGame()
        self.plr, self.victim = self.g.playerList()
        self.card = self.g['Marauder'].remove()

    def test_play(self):
        """ Play a marauder """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Spoils'))
        self.assertTrue(self.victim.discardpile[0].isRuin())


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
