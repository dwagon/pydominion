#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Mystic(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "+2 gold, +1 action, guess top card to get it"
        self.name = 'Mystic'
        self.actions = 1
        self.gold = 2
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        """" Name a card. Reveal the top card of your deck. If it's
            the named card, put it into your hand """
        options = [{'selector': '0', 'print': 'No guess', 'card': None}]
        index = 1
        for c in sorted(game.cardTypes()):
            sel = "%s" % index
            options.append({'selector': sel, 'print': "Guess %s" % c.name, 'card': c})
            index += 1
        o = player.userInput(options, "Guess the top card")
        if not o['card']:
            return
        c = player.nextCard()
        if o['card'].name == c.name:
            player.output("You guessed correctly")
            player.addCard(c, 'hand')
        else:
            player.output("You chose poorly - it was a %s" % c.name)
            player.addCard(c, 'deck')


###############################################################################
class Test_Mystic(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['mystic'])
        self.plr = self.g.players[0]
        self.card = self.g['mystic'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.t['actions'], 1)
        self.assertEqual(self.plr.t['gold'], 2)

    def test_good(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.setDeck('gold')
        index = 1
        for c in sorted(self.g.cardTypes()):
            if c.name == 'Gold':
                goldnum = index
            index += 1
        self.plr.test_input = ['%d' % goldnum]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.t['actions'], 1)
        self.assertEqual(self.plr.t['gold'], 2)
        self.assertTrue(self.plr.inHand('Gold'))

    def test_bad(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.setDeck('province')
        index = 1
        for c in sorted(self.g.cardTypes()):
            if c.name == 'Gold':
                goldnum = index
            index += 1
        self.plr.test_input = ['%d' % goldnum]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.t['actions'], 1)
        self.assertEqual(self.plr.t['gold'], 2)
        self.assertTrue(not self.plr.inHand('Gold'))
        self.assertTrue(not self.plr.inHand('Province'))


###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF
