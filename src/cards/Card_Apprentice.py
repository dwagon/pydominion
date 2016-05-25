#!/usr/bin/env python

import unittest
from Card import Card


class Card_Apprentice(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "+1 action, Trash a card, +1 card per cost, +2 cards if it is a potion"
        self.name = 'Apprentice'
        self.cost = 5
        self.actions = 1

    def special(self, game, player):
        """ Trash a card from your hand. +1 Card per coin it costs.
            +2 Cards if it has potion it its cost """
        tc = player.plrTrashCard()
        if not tc:
            return
        c = tc[0]
        numcards = c.cost
        if c.potcost:
            numcards += 2
        player.pickupCards(numcards)


###############################################################################
class Test_Apprentice(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Apprentice', 'Familiar'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.apprentice = self.g['Apprentice'].remove()

    def test_trashNone(self):
        self.plr.addCard(self.apprentice, 'hand')
        self.plr.test_input = ['finish']
        self.plr.playCard(self.apprentice)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertTrue(self.g.trashpile.isEmpty())

    def test_trashCard(self):
        self.plr.setHand('Silver')
        self.plr.addCard(self.apprentice, 'hand')
        self.plr.test_input = ['silver']
        self.plr.playCard(self.apprentice)
        self.assertEqual(self.plr.handSize(), self.g.trashpile[-1].cost)

    def test_trashPotion(self):
        self.plr.setHand('Familiar')
        self.plr.addCard(self.apprentice, 'hand')
        self.plr.test_input = ['Familiar']
        self.plr.playCard(self.apprentice)
        self.assertEqual(self.plr.handSize(), self.g.trashpile[-1].cost + 2)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
