#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Werewolf(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'night', 'doom']
        self.base = 'nocturne'
        self.desc = "If it's your Night phase, each other player receives the next Hex.  Otherwise, +3 Cards."
        self.name = 'Werewolf'
        self.cost = 5

    def special(self, game, player):
        for i in range(3):
            player.pickupCard()

    def night(self, game, player):
        for plr in player.attackVictims():
            plr.output("{}'s werewolf hexed you".format(player.name))
            plr.receive_hex()


###############################################################################
class Test_Werewolf(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Werewolf'])
        self.g.startGame()
        self.plr, self.vic = self.g.playerList()
        self.card = self.g['Werewolf'].remove()
        self.plr.addCard(self.card, 'hand')
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play_day(self):
        """ Play a Werewolf during the day """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5 + 3)
        self.assertFalse(self.vic.has_state('Deluded'))

    def test_play_night(self):
        self.plr.phase = 'night'
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertTrue(self.vic.has_state('Deluded'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF