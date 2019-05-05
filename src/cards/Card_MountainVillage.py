#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_MountainVillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'renaissance'
        self.desc = "+2 Actions; Look through your discard pile and put a card from it into your hand; if you can't, +1 Card."
        self.name = 'Mountain Village'
        self.cost = 4
        self.actions = 2

    def special(self, game, player):
        if player.discardSize():
            card = player.cardSel(cardsrc='discard')
            player.discardpile.remove(card[0])
            player.addCard(card[0], 'hand')
        else:
            player.output("No cards in discard pile")
            player.pickupCards(1)


###############################################################################
class Test_MountainVillage(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Mountain Village'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Mountain Village'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_no_discard(self):
        """ Play Mountain Village without a discard card """
        self.plr.setDiscard()
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.handSize(), 6)

    def test_play_discard(self):
        """ Play Mountain Village with a discard card """
        self.plr.setDiscard('Gold', 'Silver')
        self.plr.test_input = ['Gold']
        self.plr.playCard(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.getActions(), 2)
        self.assertIsNotNone(self.plr.inHand('Gold'))
        self.assertIsNone(self.plr.inDiscard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF