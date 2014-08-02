#!/usr/bin/env python

import unittest
from Card import Card


class Card_Counterfeit(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'darkages'
        self.desc = "+1 Gold, +1 Buy; May play a treasure twice and trash it"
        self.name = 'Counterfeit'
        self.cost = 5
        self.coin = 1
        self.buys = 1

    def special(self, game, player):
        """ When you play this, you may play a Treasure from your
            hand twice. If you do, trash that Treasure """
        options = [{'selector': '0', 'print': 'Do nothing', 'card': None}]
        index = 1
        for c in player.hand:
            if c.isTreasure():
                sel = '%d' % index
                index += 1
                options.append({'selector': sel, 'print': "Play %s twice" % c.name, 'card': c})
        if index == 1:
            return
        o = player.userInput(options, 'What to do?')
        if not o['card']:
            return
        for i in range(2):
            player.playCard(o['card'], costAction=False, discard=False)
        player.trashCard(o['card'])


###############################################################################
class Test_Counterfiet(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['counterfeit'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['counterfeit'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.getBuys(), 2)

    def test_notreasures(self):
        self.plr.setHand('estate', 'estate', 'estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.test_input, ['0'])

    def test_twice(self):
        self.plr.setHand('gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertTrue(self.plr.hand.isEmpty())
        self.assertEqual(self.g.trashpile[0].name, 'Gold')
        # CF + 2 * Gold
        self.assertEqual(self.plr.getCoin(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
