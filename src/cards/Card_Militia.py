#!/usr/bin/env python

import unittest
from Card import Card


class Card_Militia(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'dominion'
        self.desc = "+2 gold, Every other player discards down to 3"
        self.name = 'Militia'
        self.gold = 2
        self.cost = 4

    def special(self, game, player):
        """ Every other player discards down to 3 cards """
        for plr in player.attackVictims():
            plr.output("Discard down to 3 cards")
            plr.plrDiscardDownTo(3)


###############################################################################
class Test_Militia(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['militia', 'moat'])
        self.attacker, self.defender = self.g.players.values()
        self.mcard = self.g['militia'].remove()

    def test_defense(self):
        self.attacker.addCard(self.mcard, 'hand')
        self.defender.addCard(self.g['moat'].remove(), 'hand')
        #self.defender.test_input = ['1', '1', '0']
        self.attacker.playCard(self.mcard)
        self.assertEquals(len(self.defender.hand), 6)   # Normal + moat
        self.assertEquals(self.attacker.t['gold'], 2)

    def test_attack(self):
        self.attacker.addCard(self.mcard, 'hand')
        self.defender.test_input = ['1', '2', '0']
        self.attacker.playCard(self.mcard)
        self.assertEquals(len(self.defender.hand), 3)   # Normal  - 2
        self.assertEquals(len(self.defender.discardpile), 2)
        self.assertEquals(self.attacker.t['gold'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
