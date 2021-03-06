#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Masquerade(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
        self.desc = "+2 cards. Every player passes a card on, and you trash a card"
        self.name = 'Masquerade'
        self.cards = 2
        self.cost = 3

    def special(self, game, player):
        """ Each player passes a card from his hand to the left at
            once. Then you may trash a card from your hand"""
        xfer = {}
        for plr in game.player_list():
            xfer[plr] = self.pickCardToXfer(plr, game)
        for plr in list(xfer.keys()):
            newplr = game.playerToLeft(plr)
            newcrd = xfer[plr]
            newplr.output("You gained a %s from %s" % (newcrd.name, plr.name))
            newplr.addCard(newcrd, 'hand')
        player.plrTrashCard()

    def pickCardToXfer(self, plr, game):
        leftplr = game.playerToLeft(plr).name
        cards = plr.cardSel(
            prompt="Which card to give to %s?" % leftplr, num=1, force=True
        )
        card = cards[0]
        plr.hand.remove(card)
        plr.output("Gave %s to %s" % (card.name, leftplr))
        return card


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    c = player.pick_to_discard(1, keepvic=True)
    return c


###############################################################################
class Test_Masquerade(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Masquerade'])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g['Masquerade'].remove()

    def test_play(self):
        """ Play a masquerade """
        tsize = self.g.trashSize()
        self.other.setHand('Copper', 'Silver', 'Gold')
        self.plr.setHand('Copper', 'Silver', 'Gold')
        self.plr.setDeck('Estate', 'Duchy', 'Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['select silver', 'finish']
        self.other.test_input = ['select gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertTrue(self.plr.in_hand('Gold'))
        self.assertTrue(self.other.in_hand('Silver'))
        self.assertEqual(self.g.trashSize(), tsize)

    def test_play_with_trash(self):
        """ Play a masquerade and trash after """
        tsize = self.g.trashSize()
        self.other.setHand('Copper', 'Silver', 'Gold')
        self.plr.setHand('Copper', 'Silver', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['select gold', 'trash silver']
        self.other.test_input = ['select gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 5 - 1)
        self.assertEqual(self.g.trashSize(), tsize + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
