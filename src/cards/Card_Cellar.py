#!/usr/bin/env python

import unittest
from Card import Card


class Card_Cellar(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+1 action, Discard and redraw cards"
        self.name = 'Cellar'
        self.actions = 1
        self.cost = 2

    def special(self, game, player):
        """ Discard any number of cards, +1 card per card discarded """
        todiscard = []
        prompt = "Select which card(s) to discard?"
        while(1):
            options = [{'selector': '0', 'print': 'Discard no more', 'card': None}]
            index = 1
            for c in player.hand:
                s = "%s" % index
                discstr = "Undiscard" if c in todiscard else "Discard"
                options.append({'selector': s, 'print': '%s %s' % (discstr, c.name), 'card': c})
                index += 1
            o = player.userInput(options, prompt)
            if o['card'] is None:
                break
            if o['card'] in todiscard:
                todiscard.remove(o['card'])
            else:
                todiscard.append(o['card'])

        for c in todiscard:
            player.output("Discarding %s" % c.name)
            player.discardCard(c)
            player.pickupCard()


###############################################################################
class Test_Cellar(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['cellar'])
        self.plr = self.g.players[0]
        self.ccard = self.g['cellar'].remove()

    def test_none(self):
        self.plr.setHand('estate', 'copper', 'silver')
        self.plr.addCard(self.ccard, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.ccard)
        self.assertEquals(len(self.plr.hand), 3)

    def test_one(self):
        self.plr.setHand('estate', 'copper', 'silver')
        self.plr.setDeck('province', 'gold')
        self.plr.addCard(self.ccard, 'hand')
        self.plr.test_input = ['1', '0']
        self.plr.playCard(self.ccard)
        self.assertEquals(self.plr.deck[-1].name, 'Province')
        for c in self.plr.hand:
            if c.name == 'Gold':
                break
        else:
            self.fail()
        self.assertEquals(len(self.plr.hand), 3)


###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF
