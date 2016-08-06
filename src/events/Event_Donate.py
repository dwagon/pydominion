#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Donate(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'empires'
        self.desc = "After this turn, put all cards from your deck and discard pile into your hand, trash any number, shuffle your hand into your deck, then draw 5 cards."
        self.name = "Donate"
        self.debtcost = 8

    def hook_endTurn(self, game, player):
        for card in player.deck:
            player.addCard(card, 'hand')
            player.deck.remove(card)
        for card in player.discardpile:
            player.addCard(card, 'hand')
            player.discardpile.remove(card)
        player.plrTrashCard(anynum=True)
        for card in player.hand:
            player.addCard(card, 'deck')
            player.hand.remove(card)
        player.shuffleDeck()
        player.pickUpHand(5)


###############################################################################
class Test_Donate(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Donate'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g.events['Donate']

    def test_play(self):
        """ Perform a Donate """
        self.plr.setHand('Gold', 'Duchy')
        self.plr.setDeck('Copper', 'Silver')
        self.plr.setDiscard('Estate', 'Province')
        self.plr.performEvent(self.card)
        self.plr.test_input = ['Copper', 'Silver', 'Estate', 'Duchy', 'finish']
        self.plr.endTurn()
        self.assertEqual(self.g.trashSize(), 4)
        self.assertIsNotNone(self.plr.inHand('Gold'))
        self.assertIsNotNone(self.plr.inHand('Province'))
        self.assertIsNotNone(self.g.inTrash('Copper'))
        self.assertIsNotNone(self.g.inTrash('Estate'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
