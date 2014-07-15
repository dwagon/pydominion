#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Mystic(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "+2 coin, +1 action, guess top card to get it"
        self.name = 'Mystic'
        self.actions = 1
        self.coin = 2
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
            player.addCard(c, 'topdeck')


###############################################################################
class Test_Mystic(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['mystic'])
        self.plr = list(self.g.players.values())[0]
        self.card = self.g['mystic'].remove()

    def test_play(self):
        """ No guess should still get results """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_good(self):
        """ When the guess is good the card should move to the hand """
        self.plr.addCard(self.card, 'hand')
        self.plr.setDeck('gold')
        self.plr.test_input = ['%d' % self.goldnum()]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertTrue(self.plr.inHand('Gold'))
        self.assertEqual(self.plr.deck, [])

    def test_bad(self):
        """ When the guess is bad the card should stay on the deck """
        self.plr.addCard(self.card, 'hand')
        self.plr.setDeck('province')
        self.plr.test_input = ['%d' % self.goldnum()]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertTrue(not self.plr.inHand('Gold'))
        self.assertTrue(not self.plr.inHand('Province'))
        self.assertEqual(self.plr.deck[-1].name, 'Province')

    def goldnum(self):
        index = 1
        for c in sorted(self.g.cardTypes()):
            if c.name == 'Gold':
                goldnum = index
            index += 1
        return goldnum


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
