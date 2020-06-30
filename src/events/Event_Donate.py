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
        self.cost = 0
        self.debtcost = 8

    def hook_endTurn(self, game, player):
        for area in (player.hand, player.deck, player.played, player.discardpile):
            for card in area[:]:
                player.addCard(card, 'hand')
                area.remove(card)
        player.plrTrashCard(anynum=True, prompt="Donate allows you to trash any cards")
        player.discardHand()
        player.pickupCards(5)


###############################################################################
class Test_Donate(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Donate'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events['Donate']

    def test_with_treasure(self):
        """ Use Donate """
        tsize = self.g.trashSize()
        self.plr.setHand('Gold', 'Estate', 'Copper', 'Copper')
        self.plr.setDiscard('Province', 'Estate', 'Copper', 'Copper')
        self.plr.setDeck('Silver', 'Estate', 'Copper', 'Copper')
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.debt, 8)
        self.plr.test_input = ['Gold', 'Province', 'Silver', 'finish']
        self.plr.endTurn()
        self.g.print_state()
        self.assertIsNotNone(self.g.inTrash('Gold'))
        self.assertIsNotNone(self.g.inTrash('Province'))
        self.assertIsNotNone(self.g.inTrash('Silver'))
        self.assertIsNone(self.plr.inDeck('Gold'))
        self.assertEqual(self.g.trashSize(), tsize + 3)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.discardSize(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
