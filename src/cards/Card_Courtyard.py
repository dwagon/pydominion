#!/usr/bin/env python

import unittest
from Card import Card


class Card_Courtyard(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "+3 cards. Put a card from hand to top of deck"
        self.name = 'Courtyard'
        self.cards = 3
        self.cost = 2

    def special(self, player, game):
        """ Put a card from your hand on top of your deck """
        options = [{'selector': '0', 'print': "Don't put anything on deck", 'card': None}]
        index = 1
        for c in player.hand:
            sel = "%d" % index
            pr = "Put %s" % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        o = player.userInput(options, "Put which card on top of deck?")
        if not o['card']:
            return
        player.addCard(o['card'], 'deck')
        player.hand.remove(o['card'])
        player.output("Put %s on top of deck" % o['card'].name)


###############################################################################
class Test_Courtyard(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['courtyard'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.cy = self.g['courtyard'].remove()

    def test_play(self):
        self.plr.addCard(self.cy, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.cy)
        self.assertEqual(self.plr.handSize(), 8)

    def test_putcard(self):
        self.plr.setHand('gold')
        self.plr.addCard(self.cy, 'hand')
        self.plr.test_input = ['1']
        self.plr.playCard(self.cy)
        self.assertEqual(self.plr.deck[0].name, 'Gold')
        for c in self.plr.hand:
            self.assertNotEqual(c.name, 'Gold')
        self.assertEqual(self.plr.handSize(), 3)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
