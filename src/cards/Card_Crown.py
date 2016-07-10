#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Crown(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'treasure']
        self.base = 'empires'
        self.desc = """If it's your Action phase, you may play an Action from your hand twice.
        If it's your Buy phase, you may play a Treasure from your hand twice."""
        self.name = 'Crown'
        self.cost = 5

    def special(self, game, player):
        if player.phase == 'action':
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
class Test_Crown(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Crown'])
        self.g.startGame()
        self.plr, self.other = self.g.playerList()
        self.card = self.g['Crown'].remove()

    def test_play(self):
        self.other.setHand('Copper', 'Silver', 'Gold')
        self.plr.setHand('Duchy', 'Province', 'Gold', 'Silver', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.other.test_input = ['Copper', 'Silver', 'Finish']
        self.plr.test_input = ['Duchy', 'Province', 'Finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5 + 2 - 2)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.other.handSize(), 3 - 2 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
