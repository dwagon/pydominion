#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
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
            Card, +1 coin; Victory Card, +1 card """
        card = player.nextCard()
        ans = player.plrChooseOptions(
            "What to do with %s" % card.name,
            ('Put back %s' % card.name, False),
            ('Discard %s' % card.name, True)
        )
        if ans:
            player.discardCard(card)
        else:
            player.addCard(card, 'topdeck')
        if card.isVictory():
            player.pickupCard()
        if card.isAction():
            player.addActions(1)
        if card.isTreasure():
            player.addCoin(1)


###############################################################################
class Test_Ironmonger(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Iron Monger'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.im = self.g['Iron Monger'].remove()
        self.plr.addCard(self.im, 'hand')

    def test_play(self):
        self.plr.test_input = ['put back']
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.getActions(), 1)
        # 5 for hand, +1 for ironmonger and another potential +1 for action
        self.assertIn(self.plr.handSize(), [6, 7])

    def test_victory(self):
        self.plr.test_input = ['put back']
        self.plr.setDeck('Duchy', 'Estate')
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.handSize(), 7)

    def test_treasure(self):
        self.plr.test_input = ['put back']
        self.plr.setDeck('Copper', 'Gold')
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_action(self):
        self.plr.test_input = ['put back']
        self.plr.setDeck('Iron Monger', 'Iron Monger')
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 2)

    def test_discard(self):
        self.plr.test_input = ['discard']
        self.plr.setDeck('Iron Monger', 'Gold')
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.discardpile[0].name, 'Iron Monger')

    def test_putback(self):
        self.plr.test_input = ['put back']
        self.plr.setDeck('Copper', 'Gold')
        self.plr.playCard(self.im)
        self.assertEqual(self.plr.deck[0].name, 'Copper')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
