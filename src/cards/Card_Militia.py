#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
###############################################################################
class Card_Militia(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'dominion'
        self.desc = "+2 coin, Every other player discards down to 3"
        self.name = 'Militia'
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        """ Every other player discards down to 3 cards """
        for plr in player.attackVictims():
            plr.output("%s's Militia: Discard down to 3 cards" % player.name)
            plr.plrDiscardDownTo(3)


###############################################################################
def botresponse(player, kind, args=[], kwargs={}):  # pragma: no cover
    numtodiscard = len(player.hand) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Militia(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Militia', 'Moat'])
        self.g.start_game()
        self.attacker, self.defender = self.g.playerList()
        self.mcard = self.g['Militia'].remove()

    def test_defense(self):
        self.attacker.addCard(self.mcard, 'hand')
        self.defender.addCard(self.g['Moat'].remove(), 'hand')
        self.attacker.playCard(self.mcard)
        self.assertEqual(self.defender.handSize(), 6)   # Normal + moat
        self.assertEqual(self.attacker.getCoin(), 2)

    def test_attack(self):
        self.attacker.addCard(self.mcard, 'hand')
        self.defender.test_input = ['1', '2', '0']
        self.attacker.playCard(self.mcard)
        self.assertEqual(self.defender.handSize(), 3)   # Normal  - 2
        self.assertEqual(self.defender.discardSize(), 2)
        self.assertEqual(self.attacker.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
