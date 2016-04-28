#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Magpie(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'adventure'
        self.desc = "+1 Card; +1 Action. Reveal top card if treasure then put in hand"
        self.name = 'Magpie'
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """ Reveal the top card of your deck. If it's a treasure, put it into your
        hand. If it's an Action or Victory card, gain a Magpie """
        c = player.nextCard()
        if c.isTreasure():
            player.output("Putting revealed %s into hand" % c.name)
            player.addCard(c, 'hand')
        else:
            player.addCard(c, 'deck')
            if c.isAction() or c.isVictory():
                player.output("Revealed %s so gaining magpie" % c.name)
                player.gainCard('magpie')


###############################################################################
class Test_Magpie(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['magpie'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['magpie'].remove()

    def test_treasure(self):
        """ Play a magpie with treasure """
        self.plr.setDeck('gold', 'copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.g.print_state()
        # Hand of 5, the card gained and the treasure
        self.assertEqual(self.plr.handSize(), 5 + 1 + 1)
        self.assertTrue(self.plr.inHand('Gold'))

    def test_victory(self):
        """ Play a magpie with treasure """
        self.plr.setDeck('duchy', 'copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        # Hand of 5, the card gained
        self.assertEqual(self.plr.handSize(), 5 + 1)
        self.assertFalse(self.plr.inHand('Duchy'))
        self.assertEqual(self.plr.discardpile[0].name, 'Magpie')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
