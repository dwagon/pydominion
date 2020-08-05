#!/usr/bin/env python

import unittest
import Game
from Event import Event


###############################################################################
class Event_Annex(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'adventure'
        self.desc = "Look through your discard pile. Shuffle all but up to 5 cards from it into your deck. Gain a Duchy."
        self.name = "Annex"
        self.debtcost = 8

    def special(self, game, player):
        if player.discard_size() <= 5:
            player.output("Not enough cards to choose")
            return
        cards = player.cardSel(
            num=5,
            cardsrc='discard',
            prompt="Select 5 cards to leave in discard pile"
            )
        keep = []
        for card in player.discardpile[:]:
            if card in cards:
                keep.append(card)
            else:
                player.addCard(card, 'deck')
        player.deck.shuffle()
        player.setDiscard()
        for card in keep:
            player.addCard(card, 'discard')
        if player.gainCard('Duchy'):
            player.output("Gained a Duchy")


###############################################################################
class Test_Annex(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Annex'], initcards=['Moat'], badcards=['Duchess'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events['Annex']

    def test_play(self):
        """ Perform Annex """
        self.plr.setDiscard('Gold', 'Silver', 'Copper', 'Province', 'Moat', 'Estate')
        self.plr.test_input = ['Silver', 'Copper', 'Province', 'Moat', 'Estate', 'Finish']
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.debt, 8)
        self.assertIsNotNone(self.plr.inDiscard('Duchy'))
        self.assertIsNone(self.plr.inDiscard('Gold'))
        self.assertIsNotNone(self.plr.in_deck('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
