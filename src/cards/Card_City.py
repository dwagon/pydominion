#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_City(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.PROSPERITY
        self.desc = """+1 card, +2 action; If there are one or more empty Supply
            piles, +1 card. If there are two or more, +1 coin, +1 buy """
        self.name = 'City'
        self.cost = 5
        self.cards = 1
        self.actions = 2

    ###########################################################################
    def special(self, game, player):
        empties = sum([1 for st in game.cardpiles if game[st].is_empty()])
        if empties >= 1:
            player.pickupCard()
        if empties >= 2:
            player.addCoin(1)
            player.addBuys(1)


###############################################################################
class Test_City(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['City', 'Moat', 'Cellar'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.city = self.g['City'].remove()
        self.plr.addCard(self.city, 'hand')

    def test_nostacks(self):
        """ Play a city with no stacks empty """
        self.plr.playCard(self.city)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.hand.size(), 6)

    def test_onestack(self):
        """ Play a city with one stacks empty """
        while True:
            c = self.g['Moat'].remove()
            if not c:
                break
        self.plr.playCard(self.city)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.hand.size(), 7)

    def test_twostack(self):
        """ Play a city with two stacks empty """
        while True:
            c = self.g['Moat'].remove()
            if not c:
                break
        while True:
            c = self.g['Cellar'].remove()
            if not c:
                break
        self.plr.playCard(self.city)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.getCoin(), 1)
        # 1 default + 1 for city
        self.assertEqual(self.plr.get_buys(), 2)
        # 5 for hand, 1 for city, 1 for one stack
        self.assertEqual(self.plr.hand.size(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
