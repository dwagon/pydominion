#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Masquerade(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "+2 cards. Every player passes a card on, and you trash a card"
        self.name = 'Masquerade'
        self.cards = 2
        self.cost = 3

    def special(self, player, game):
        """ Each player passes a card from his hand to the left at
            once. Then you may trash a card from your hand"""
        xfer = {}
        for plr in game.playerList():
            xfer[plr] = self.pickCardToXfer(plr, game)
        for plr in list(xfer.keys()):
            newplr = game.playerToLeft(plr)
            newcrd = xfer[plr]
            newplr.output("You gained a %s from %s" % (newcrd.name, plr.name))
            newplr.addCard(newcrd, 'hand')
        player.plrTrashCard()

    def pickCardToXfer(self, plr, game):
        index = 1
        options = []
        leftplr = game.playerToLeft(plr).name
        for c in plr.hand:
            sel = "%d" % index
            pr = "Select %s" % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        o = plr.userInput(options, "Which card to give to %s?" % leftplr)
        plr.hand.remove(o['card'])
        plr.output("Gave %s to %s" % (o['card'].name, leftplr))
        return o['card']


###############################################################################
class Test_Masquerade(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['masquerade'])
        self.g.startGame()
        self.plr, self.other = self.g.playerList()
        self.card = self.g['masquerade'].remove()

    def test_play(self):
        """ Play a masquerade """
        self.other.setHand('gold', 'gold', 'gold')
        self.plr.setHand('silver', 'silver', 'silver')
        self.plr.setDeck('silver', 'silver', 'silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['1', '0']
        self.other.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertTrue(self.plr.inHand('gold'))
        self.assertTrue(self.other.inHand('silver'))
        self.assertTrue(self.g.trashpile.isEmpty())

    def test_play_with_trash(self):
        """ Play a masquerade and trash after """
        self.other.setHand('gold', 'gold', 'gold')
        self.plr.setHand('silver', 'silver', 'silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['1', '1']
        self.other.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5 - 1)
        self.assertEqual(self.g.trashSize(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
