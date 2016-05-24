#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Library(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "Draw up to 7 cards"
        self.name = 'Library'
        self.cost = 5

    def special(self, game, player):
        """ Draw until you have 7 cards in your hand. You may set
        aside action cards drawn this way, as you draw them; discard
        the set aside cards after you finish drawing """
        while(player.handSize() < 7):
            c = player.nextCard()
            if c.isAction():
                if self.discardChoice(player, c):
                    player.addCard(c, 'discard')
                    continue
            player.pickupCard(c)

    def discardChoice(self, plr, card):
        ans = plr.plrChooseOptions(
            "Discard %s from library?" % card.name,
            ('Discard %s' % card.name, True), ('Keep %s' % card.name, False))
        return ans


###############################################################################
class Test_Library(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Library', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Library'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_noactions(self):
        """ Play a library where no actions are drawn """
        self.plr.setDeck('Duchy', 'Copper', 'Gold')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 7)

    def test_actions_discard(self):
        """ Play a library where actions are drawn and discarded"""
        self.plr.setDeck('Duchy', 'Moat', 'Gold')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[-1].name, 'Moat')
        self.assertEqual(self.plr.handSize(), 7)

    def test_actions_keep(self):
        """ Play a library where actions are drawn and kept"""
        self.plr.setDeck('Duchy', 'Moat', 'Gold')
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertTrue(self.plr.discardpile.isEmpty())
        self.assertEqual(self.plr.deck[-1].name, 'Duchy')
        self.assertEqual(self.plr.handSize(), 7)
        self.assertTrue(self.plr.inHand('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
