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
            plr.output("Discard down to 3 cards")
            plr.plrDiscardDownTo(3)


###############################################################################
def botresponse(hand):
    numtodiscard = len(hand) - 3
    if numtodiscard <= 0:
        return []
    todiscard = []

    # Discard non-treasures first
    for card in hand:
        if not card.isTreasure():
            todiscard.append(card)
    if len(todiscard) >= numtodiscard:
        return todiscard[:2]
    for treas in ('Copper', 'Silver', 'Gold'):
        while len(todiscard) < numtodiscard:
            for card in hand:
                if card.name == treas:
                    todiscard.append(card)
    if len(todiscard) >= numtodiscard:
        return todiscard[:2]
    print "Couldn't find cards to discard from %s" % (", ".join([c.name for c in hand]))


###############################################################################
class Test_Militia(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['militia', 'moat'])
        self.g.startGame()
        self.attacker, self.defender = self.g.playerList()
        self.mcard = self.g['militia'].remove()

    def test_defense(self):
        self.attacker.addCard(self.mcard, 'hand')
        self.defender.addCard(self.g['moat'].remove(), 'hand')
        self.attacker.playCard(self.mcard)
        self.assertEquals(self.defender.handSize(), 6)   # Normal + moat
        self.assertEquals(self.attacker.getCoin(), 2)

    def test_attack(self):
        self.attacker.addCard(self.mcard, 'hand')
        self.defender.test_input = ['1', '2', '0']
        self.attacker.playCard(self.mcard)
        self.assertEquals(self.defender.handSize(), 3)   # Normal  - 2
        self.assertEquals(self.defender.discardSize(), 2)
        self.assertEquals(self.attacker.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
