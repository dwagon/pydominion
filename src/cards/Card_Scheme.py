#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Scheme(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'hinterlands'
        self.desc = """+1 Card +1 Action; At the start of Clean-up this turn,
        you may choose an Action card you have in play. If you discard it from play
        this turn, put it on your deck."""
        self.name = 'Scheme'
        self.cards = 1
        self.actions = 1
        self.cost = 3

    def hook_cleanup(self, game, player):
        actions = [c for c in player.played if c.isAction()]
        card = player.cardSel(
            cardsrc=actions,
            prompt="Select an action to put back on your deck"
            )
        if card:
            player.addCard(card[0], 'topdeck')
            player.played.remove(card[0])


###############################################################################
class Test_Scheme(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Scheme', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Scheme'].remove()

    def test_play(self):
        """ Play a scheme """
        self.plr.addCard(self.card, 'hand')
        self.plr.setPlayed('Moat')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 1)
        self.plr.test_input = ['moat']
        self.plr.cleanupPhase()
        self.g.print_state()
        self.assertIsNotNone(self.plr.inHand('Moat'))
        self.assertIsNotNone(self.plr.inDiscard('Scheme'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
