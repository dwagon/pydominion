#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Philosophersstone(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TREASURE
        self.base = Game.ALCHEMY
        self.desc = "When you play this, count your deck and discard pile. Worth 1 Coin per 5 cards total between them (rounded down)"
        self.name = "Philosopher's Stone"
        self.cost = 3
        self.required_cards = ['Potion']
        self.potcost = True

    def hook_coinvalue(self, game, player):
        """ When you play this, count your deck and discard pile.
            Worth 1 per 5 cards total between them (rounded down) """
        numcards = player.deckSize() + player.discard_size()
        extracoin = numcards / 5
        player.output("Gained %d coins from Philosopher's Stone" % extracoin)
        return int(extracoin)


###############################################################################
class Test_Philosophersstone(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Philosopher's Stone"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Philosopher's Stone"].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a philosophers stone with not much on"""
        self.plr.setDeck('Estate')
        self.plr.setDiscard('Estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 0)

    def test_play_value(self):
        """ Play a philosophers stone with the full Nicholas Flamel """
        self.plr.setDeck('Estate', 'Estate', 'Estate', 'Estate', 'Silver')
        self.plr.setDiscard('Estate', 'Estate', 'Estate', 'Estate', 'Silver')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
