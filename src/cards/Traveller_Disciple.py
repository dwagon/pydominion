#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Disciple(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'traveller']
        self.base = 'adventure'
        self.desc = """You may play an Action card from your hand twice. Gain a copy of it"""
        self.name = 'Disciple'
        self.purchasable = False
        self.numcards = 5
        self.cost = 5

    def special(self, game, player):
        """ You may play an Action card from your hand twice. Gain a copy of it"""
        actions = [c for c in player.hand if c.isAction()]
        if not actions:
            player.output("No suitable actions to perform")
            return
        cards = player.cardSel(cardsrc=actions)
        if not cards:
            return
        card = cards[0]
        for i in range(1, 3):
            player.output("Number %d play of %s" % (i, card.name))
            player.playCard(card, discard=False, costAction=False)
        player.addCard(card, 'played')
        player.hand.remove(card)
        if card.purchasable:
            c = player.gainCard(card.name)
            if c:
                player.output("Gained a %s from Disciple" % c.name)

    def hook_discardThisCard(self, game, player):
        """ Replace with Teacher """
        player.replace_traveller(self, 'Teacher')


###############################################################################
class Test_Disciple(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Peasant', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Disciple'].remove()

    def test_play_no_actions(self):
        """ Play a disciple with no actions available"""
        self.plr.setHand('Copper', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.playedSize(), 1)

    def test_play_actions(self):
        """ Play a disciple with an action available"""
        self.plr.setHand('Copper', 'Estate', 'Moat')
        self.plr.test_input = ['moat']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.playedSize(), 2)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertIsNotNone(self.plr.inDiscard('Moat'))

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
