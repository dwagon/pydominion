#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Cartographer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.desc = """+1 Card; +1 Action; Look at the top 4 cards of your deck.
            Discard any number of them. Put the rest back on top in any order."""
        self.name = 'Cartographer'
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        cards = []
        for _ in range(4):
            c = player.nextCard()
            if c:
                cards.append(c)
        todisc = player.plrDiscardCards(prompt="Discard any number and the rest go back on the top of the deck", anynum=True, cardsrc=cards)
        for card in cards:
            if card not in todisc:
                player.addCard(card, 'topdeck')


###############################################################################
class Test_Cartographer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cartographer'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Cartographer'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.setDeck('Silver', 'Gold', 'Province', 'Duchy', 'Copper')
        self.plr.test_input = ['Province', 'Duchy', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNotNone(self.plr.in_deck('Silver'))
        self.assertIsNotNone(self.plr.in_deck('Gold'))
        self.assertIsNotNone(self.plr.in_discard('Province'))
        self.assertIsNotNone(self.plr.in_discard('Duchy'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
