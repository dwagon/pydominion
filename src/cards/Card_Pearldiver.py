#!/usr/bin/env python

import unittest
from Card import Card


##########################################################################
class Card_Pearldiver(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'seaside'
        self.desc = "+1 card, +1 action. Put bottom of deck to top"
        self.name = 'Pearl Diver'
        self.cards = 1
        self.actions = 1
        self.cost = 2

    def special(self, game, player):
        """ Look at the bottom card of your deck. You may put it on top """
        bcard = player.deck[0]
        top = player.plrChooseOptions(
            'What to do with bottom card?',
            ("Keep %s on bottom of deck" % bcard.name, False),
            ("Put %s on top of deck" % bcard.name, True))
        if top:
            player.output("Putting %s on top of deck" % bcard.name)
            player.deck.remove(bcard)
            player.addCard(bcard, 'topdeck')
        else:
            pass


###############################################################################
class Test_Pearldiver(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['pearldiver'])
        self.plr = self.g.playerList(0)
        self.pearldiver = self.g['pearldiver'].remove()
        self.plr.addCard(self.pearldiver, 'hand')

    def test_play(self):
        self.plr.setDeck('copper', 'gold', 'province', 'silver', 'duchy')
        self.plr.test_input = ['0']
        self.plr.playCard(self.pearldiver)
        self.assertEquals(self.plr.getActions(), 1)
        self.assertEquals(self.plr.handSize(), 6)

    def test_donothing(self):
        self.plr.setDeck('copper', 'estate', 'gold', 'province', 'silver', 'duchy')
        self.plr.test_input = ['0']
        self.plr.playCard(self.pearldiver)
        self.assertEqual(self.plr.deck[-1].name, 'Silver')
        self.assertEqual(self.plr.deck[0].name, 'Copper')

    def test_putontop(self):
        self.plr.setDeck('copper', 'estate', 'gold', 'province', 'silver', 'duchy')
        self.plr.test_input = ['1']
        self.plr.playCard(self.pearldiver)
        # Duchy gets pulled due to +1 card
        self.assertEqual(self.plr.deck[-1].name, 'Copper')
        self.assertEqual(self.plr.deck[0].name, 'Estate')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
