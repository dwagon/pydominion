#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Ducat(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'renaissance'
        self.buys = 1
        self.name = 'Ducat'
        self.cost = 2

    ###########################################################################
    def desc(self, player):
        if player.phase == 'buy':
            return "+1 Coffers; +1 Buy; When you gain this, you may trash a Copper from your hand."
        else:
            return "+1 Coffers; +1 Buy"

    ###########################################################################
    def special(self, game, player):
        player.gainCoffer()

    ###########################################################################
    def hook_gainThisCard(self, game, player):
        cu = player.inHand('Copper')
        if cu:
            player.plrTrashCard(cardsrc=[cu], num=1)
        else:
            player.output("No Coppers")


###############################################################################
class Test_Ducat(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Ducat'])
        self.g.start_game()
        self.plr = self.g.playerList(0)

    def test_play(self):
        card = self.g['Ducat'].remove()
        self.plr.setCoffer(0)
        self.plr.addCard(card, 'hand')
        self.plr.playCard(card)
        self.assertEqual(self.plr.getCoffer(), 1)
        self.assertEqual(self.plr.getBuys(), 1+1)

    def test_gain_trash(self):
        self.plr.test_input = ['Copper']
        self.plr.setHand('Copper')
        self.plr.gainCard('Ducat')

    def test_gain_nothing(self):
        self.plr.setHand('Silver')
        self.plr.gainCard('Ducat')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
