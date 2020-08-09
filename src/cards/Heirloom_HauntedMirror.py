#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Haunted_Mirror(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_TREASURE, Card.TYPE_HEIRLOOM]
        self.base = Game.NOCTURNE
        self.desc = "+1 Coin; When you trash this, you may discard an Action card, to gain a Ghost from its pile."
        self.name = 'Haunted Mirror'
        self.cost = 0
        self.coin = 1
        self.required_cards = [('Card', 'Ghost')]
        self.purchasable = False

    def hook_trashThisCard(self, game, player):
        ac = [_ for _ in player.hand if _.isAction()]
        if not ac:
            player.output("No action cards in hand, no effect")
            return
        td = player.plrDiscardCards(cardsrc=ac)
        if td:
            player.gainCard('Ghost')


###############################################################################
class Test_Haunted_Mirror(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cemetery', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Haunted Mirror'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_trash_nothing(self):
        self.plr.setHand('Copper')
        self.plr.trashCard(self.card)
        self.assertIsNone(self.plr.in_discard('Ghost'))

    def test_trash(self):
        self.plr.setHand('Moat')
        self.plr.test_input = ['Moat']
        self.plr.trashCard(self.card)
        self.assertIsNotNone(self.plr.in_discard('Ghost'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
