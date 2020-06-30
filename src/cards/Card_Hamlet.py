#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_Hamlet(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'cornucopia'
        self.desc = "+1 Card +1 Action. You may discard a card; if you do, +1 Action.  You may discard a card; if you do, +1 Buy."
        self.name = 'Hamlet'
        self.cards = 1
        self.actions = 1
        self.cost = 2

    def special(self, game, player):
        c = player.plrDiscardCards(prompt="Discard a card to gain an action")
        if c:
            player.addActions(1)
        c = player.plrDiscardCards(prompt="Discard card to gain a buy")
        if c:
            player.addBuys(1)


###############################################################################
class Test_Hamlet(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Hamlet'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.card = self.g['Hamlet'].remove()
        self.plr.setHand('Silver', 'Gold')
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a hamlet """
        self.plr.test_input = ['finish selecting', 'finish selecting']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 3)
        self.assertEqual(self.plr.getActions(), 1)

    def test_discard_action(self):
        """ Play a hamlet and discard to gain an action """
        self.plr.test_input = ['discard silver', 'finish selecting']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 2)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.getBuys(), 1)
        self.assertIsNone(self.plr.inHand('Silver'))

    def test_discard_buy(self):
        """ Play a hamlet and discard to gain a buy """
        self.plr.test_input = ['finish selecting', 'discard gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 2)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertIsNone(self.plr.inHand('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
