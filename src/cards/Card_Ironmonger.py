#!/usr/bin/env python

import unittest
from Card import Card


class Card_Ironmonger(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "+1 card, +1 action, reveal top card. Hijinks follow"
        self.name = 'Iron Monger'
        self.cost = 4
        self.actions = 1
        self.cards = 1

    def special(self, player, game):
        """ Reveal the top card of your deck; you may discard it.
            Either way, if it is an... Action card, +1 Action; Treasure
            Card, +1 gold; Victory Card, +1 card """
        card = player.nextCard()
        options = [
            {'selector': '0', 'print': 'Put back %s' % card.name, 'discard': False},
            {'selector': '1', 'print': 'Discard %s' % card.name, 'discard': True}
        ]
        o = player.userInput(options, "What to do with %s" % card.name)
        if o['discard']:
            player.discardCard(card)
        else:
            player.addCard(card, 'topdeck')
        if card.isVictory():
            player.pickupCard()
        if card.isAction():
            player.t['actions'] += 1
        if card.isTreasure():
            player.t['gold'] += 1


###############################################################################
class Test_Ironmonger(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['ironmonger'])
        self.plr = self.g.players.values()[0]
        self.im = self.g['ironmonger'].remove()
        self.plr.addCard(self.im, 'hand')

    def test_play(self):
        self.plr.test_input = ['0']
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.t['actions'], 1)
        # 5 for hand, +1 for ironmonger and another potential +1 for action
        self.assertIn(len(self.plr.hand), [6, 7])

    def test_victory(self):
        self.plr.test_input = ['0']
        self.plr.setDeck('duchy', 'estate')
        self.plr.playCard(self.im)
        self.assertEqual(len(self.plr.hand), 7)

    def test_treasure(self):
        self.plr.test_input = ['0']
        self.plr.setDeck('copper', 'gold')
        self.plr.playCard(self.im)
        self.assertEqual(len(self.plr.hand), 6)
        self.assertEqual(self.plr.t['gold'], 1)

    def test_action(self):
        self.plr.test_input = ['0']
        self.plr.setDeck('ironmonger', 'ironmonger')
        self.plr.playCard(self.im)
        self.assertEqual(len(self.plr.hand), 6)
        self.assertEqual(self.plr.t['actions'], 2)

    def test_discard(self):
        self.plr.test_input = ['1']
        self.plr.setDeck('ironmonger', 'gold')
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.discardpile[0].name, 'Iron Monger')

    def test_putback(self):
        self.plr.test_input = ['0']
        self.plr.setDeck('copper', 'gold')
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.deck[0].name, 'Copper')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
