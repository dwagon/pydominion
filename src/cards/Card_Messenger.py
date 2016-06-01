#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Messenger(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'adventure'
        self.desc = """+1 Buy, +2 Coin, You may put ypur deck into your discard pile;
        When this is your first buy in a turn, gain a card costing up to 4,
        and each other player gains a copy of it."""
        self.name = 'Messenger'
        self.buys = 1
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        o = player.plrChooseOptions(
            'Put entire deck into discard pile?',
            ('No - keep it as it is', False),
            ('Yes - dump it', True)
            )
        if o:
            for c in player.deck[:]:
                player.addCard(c, 'discard')
                player.deck.remove(c)

    def hook_buyThisCard(self, game, player):
        if player.stats['buys'] == 1:
            player.output("Pick a card for everyone to gain")
            c = player.plrGainCard(4)
            for plr in game.playerList():
                if plr != player:
                    plr.gainCard(c)
                    plr.output("Gained a %s from %s's Messenger" % (c.name, player.name))


###############################################################################
class Test_Messenger(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Messenger'])
        self.g.startGame()
        self.plr, self.other = self.g.playerList()
        self.card = self.g['Messenger'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a Messenger - do nothing"""
        self.plr.test_input = ['No']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_discard(self):
        """ Play a messenger and discard the deck """
        decksize = self.plr.deckSize()
        self.plr.test_input = ['Yes']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.deckSize(), 0)
        self.assertEqual(self.plr.discardSize(), decksize)

    def test_buy(self):
        """ Buy a messenger """
        self.plr.test_input = ['silver']
        self.plr.buyCard(self.g['Messenger'])
        for plr in self.g.playerList():
            self.assertIsNotNone(plr.inDiscard('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
