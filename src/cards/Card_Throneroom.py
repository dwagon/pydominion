#!/usr/bin/env python

import unittest
from Card import Card


class Card_Throneroom(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "Play action 2 times"
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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['throneroom', 'mine'])
        self.plr = self.g.players[0]

    def test_action(self):
        self.plr.setHand('copper', 'mine')
        self.plr.test_input = ['1', '1', '1']
        self.tcard = self.plr.gainCard('throneroom', 'hand')
        self.plr.playCard(self.tcard)
        self.assertEqual(self.plr.hand[0].name, 'Gold')
        self.assertEqual(len(self.plr.hand), 1)
        self.assertEqual(self.plr.discardpile[0].name, 'Mine')
        self.assertEqual(len(self.plr.discardpile), 1)

###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF
