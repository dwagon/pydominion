#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Sage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = """+1 Action. Reveal cards from the top of your deck
        until you reveal one costing 3 or more.
        Put that card into your hand and discard the rest."""
        self.name = 'Sage'
        self.actions = 1
        self.cost = 3

    ###########################################################################
    def special(self, game, player):
        todiscard = []
        while True:
            card = player.nextCard()
            if not card:
                player.output("No card costing 3 or more found")
                break
            player.revealCard(card)
            if card.cost >= 3:
                player.output("Adding %s to hand" % card.name)
                player.addCard(card, 'hand')
                break
            player.output("Discarding %s" % card.name)
            todiscard.append(card)
        for card in todiscard:
            player.discardCard(card)


###############################################################################
class Test_Sage(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Sage'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Sage'].remove()

    def test_play(self):
        """ Pick a card out of the pile """
        self.plr.setDeck('Gold', 'Copper', 'Copper', 'Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertIsNotNone(self.plr.inHand('Gold'))

    def test_exhaust_deck(self):
        """ No good card to pick out of the pile """
        self.plr.setDeck('Copper', 'Copper', 'Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.deckSize(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
