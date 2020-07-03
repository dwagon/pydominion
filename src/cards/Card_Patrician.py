#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Patrician(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'empires'
        self.desc = "+1 Card, +1 Action. Reveal the top card of your deck. If it costs 5 or more, put it into your hand."
        self.name = 'Patrician'
        self.cards = 1
        self.actions = 1
        self.cost = 2

    ###########################################################################
    def special(self, game, player):
        topcard = player.nextCard()
        player.revealCard(topcard)
        if topcard.cost >= 5:
            player.addCard(topcard, 'hand')
            player.output("Adding %s to hand" % topcard.name)
        else:
            player.addCard(topcard, 'topdeck')
            player.output("%s too cheap to bother with" % topcard.name)


###############################################################################
class Test_Patrician(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Patrician'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Patrician'].remove()

    def test_play_cheap(self):
        """ Play the Patrician """
        self.plr.setDeck('Estate', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 1)

    def test_play_good(self):
        """ Play the Patrician """
        self.plr.setDeck('Gold', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 7)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertIsNotNone(self.plr.inHand('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
