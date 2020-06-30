#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Tournament(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'cornucopia'
        self.desc = """+1 Action. Each player may reveal a Province from his hand.
        If you do, discard it and gain a Prize (from the Prize pile) or a Duchy,
        putting it on top of your deck. If no-one else does, +1 Card, +1 Coin."""
        self.name = 'Tournament'
        self.needsprize = True
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        found = False
        for plr in game.playerList():
            if plr != player and plr.inHand('Province'):
                found = True
        if player.inHand('Province'):
            player.discardCard(player.inHand('Province'))
            player.gainPrize()
        if not found:
            player.addCoin(1)
            player.pickupCard()


###############################################################################
class Test_Tournament(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Tournament'])
        self.g.start_game()
        self.plr, self.other = self.g.playerList()
        self.card = self.g['Tournament'].remove()

    def test_play(self):
        """ Play a tournament - no provinces """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)

    def test_play_have_province(self):
        """ Play a tournament - self provinces """
        self.plr.test_input = ['Bag']
        self.plr.setHand('Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.handSize(), 1)
        self.assertIsNotNone(self.plr.inDiscard('Bag of Gold'))

    def test_play_all_province(self):
        """ Play a tournament - others have provinces """
        self.other.setHand('Province')
        self.plr.test_input = ['Bag']
        self.plr.setHand('Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.handSize(), 0)
        self.assertIsNotNone(self.plr.inDiscard('Bag of Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
