#!/usr/bin/env python

import unittest
from Card import Card


class Card_Throneroom(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "Play action twice"
        self.name = "Throne Room"
        self.cost = 4

    def special(self, game, player):
        """ You may chose an Action card in your hand. Play it twice """
        options = [{'selector': '0', 'print': "Don't play a card", 'card': None}]
        index = 1
        for c in player.hand:
            if not c.isAction():
                continue
            sel = "%d" % index
            pr = "Play %s twice" % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        if index == 1:
            return
        o = player.userInput(options, "Play which action card twice?")
        if not o['card']:
            return
        for i in range(1, 3):
            player.output("Number %d play of %s" % (i, o['card'].name))
            player.playCard(o['card'], discard=False, costAction=False)
        player.discardCard(o['card'])


###############################################################################
class Test_Throneroom(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Throne Room', 'Mine'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_action(self):
        # Test by playing mine twice on a copper. Cu -> Ag -> Au
        self.plr.setHand('Copper', 'Mine')
        card = self.plr.gainCard('Throne Room', 'hand')
        self.plr.test_input = ['1', '1', '1']
        self.plr.playCard(card)
        self.assertEqual(self.plr.hand[0].name, 'Gold')
        self.assertEqual(self.plr.handSize(), 1)
        self.assertEqual(self.plr.discardpile[0].name, 'Mine')
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertEqual(self.plr.getActions(), 0)

    def test_donothing(self):
        self.plr.setHand('Copper', 'Mine')
        card = self.plr.gainCard('Throne Room', 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(card)

    def test_noaction(self):
        self.plr.setHand('Copper', 'Copper')
        card = self.plr.gainCard('Throne Room', 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(card)
        self.assertEqual(self.plr.test_input, ['0'])

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
