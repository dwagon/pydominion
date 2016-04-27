#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Advisor(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'guilds'
        self.desc = "+1 action, +3 cards, plr to left discards one of them"
        self.name = 'Advisor'
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """ Reveal the top 3 cards of your deck. The player to your
            left chooses one of them to them. Discard that card. Put
            the other cards into your hand"""
        cards = []
        choser = game.playerToLeft(player)
        for i in range(3):
            cards.append(player.nextCard())
        options = []
        index = 1
        for c in cards:
            sel = '%d' % index
            options.append({'selector': sel, 'print': 'Discard %s' % c.name, 'card': c})
            index += 1
        o = choser.userInput(options, 'Pick a card of %s to discard' % player.name)
        for c in cards:
            if c == o['card']:
                player.output("%s discarded %s" % (choser.name, o['card'].name))
                player.discardCard(o['card'])
            else:
                player.pickupCard(card=c)


###############################################################################
class Test_Advisor(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['advisor'])
        self.g.startGame()
        self.plr, self.plr2 = self.g.playerList()
        self.acard = self.g['advisor'].remove()
        self.plr.addCard(self.acard, 'hand')

    def test_defended(self):
        self.plr.setDeck('copper', 'silver', 'gold')
        self.plr2.test_input = ['discard gold']
        self.plr.playCard(self.acard)
        self.assertEqual(self.plr.getActions(), 1)
        for c in self.plr.hand:
            if c.name == 'Gold':    # pragma: no cover
                self.fail()
        self.assertEquals(self.plr.handSize(), 7)
        self.assertEquals(self.plr.discardpile[-1].name, 'Gold')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
