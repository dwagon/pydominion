#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Followers(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'prize']
        self.base = 'cornucopia'
        self.name = "Followers"
        self.purchasable = False
        self.required_cards = ['Curse']
        self.cost = 0
        self.desc = "+2 Cards. Gain an Estate. Each other player gains a Curse and discards down to 3 cards in hand."
        self.cards = 2

    def special(self, game, player):
        player.gainCard('Estate')
        for plr in player.attackVictims():
            plr.output("%s's Followers cursed you" % player.name)
            plr.gainCard('Curse')
            plr.plrDiscardDownTo(3)


###############################################################################
class Test_Followers(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Tournament'])
        self.g.startGame()
        self.plr, self.victim = self.g.playerList()
        self.card = self.g['Followers'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.victim.setHand('Copper', 'Copper', 'Copper', 'Silver', 'Gold')
        self.victim.test_input = ['silver', 'gold', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5 + 2)
        self.assertEqual(self.victim.handSize(), 3)
        self.assertIsNotNone(self.plr.inDiscard('Estate'))
        self.assertIsNotNone(self.victim.inDiscard('Curse'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF