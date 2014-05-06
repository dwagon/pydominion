#!/usr/bin/env python

import unittest
from Card import Card


class Card_Herbalist(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "+1 buy, +1 gold, can put treasures on top of deck"
        self.name = 'Herbalist'
        self.cost = 2
        self.buys = 1
        self.gold = 1

    def hook_discardCard(self, game, player):
        """ When you discard this from play, you may put one of
            your Treasures from play on top of your deck """
        options = [{'selector': '0', 'print': 'Do nothing', 'card': None}]
        index = 1
        for c in player.played:
            if c.isTreasure():
                sel = "%d" % index
                options.append({'selector': sel, 'print': 'Put %s' % c.name, 'card': c})
                index += 1
        o = player.userInput(options, "Put a card on the top of your deck?")
        if o['card']:
            player.addCard(o['card'], 'deck')


###############################################################################
class Test_Herbalist(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['herbalist'])
        self.plr = self.g.players[0]
        self.hcard = self.g['herbalist'].remove()

    def test_putnothing(self):
        self.plr.setPlayed('gold', 'estate')
        self.plr.addCard(self.hcard, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.hcard)
        self.plr.discardHand()
        self.assertEqual(len(self.plr.deck), 5)

    def test_putgold(self):
        self.plr.setPlayed('gold', 'estate')
        self.plr.addCard(self.hcard, 'hand')
        self.plr.test_input = ['1']
        self.plr.playCard(self.hcard)
        self.plr.discardHand()
        self.assertEqual(self.plr.deck[-1].name, 'Gold')
        self.assertEqual(len(self.plr.deck), 6)

###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF
