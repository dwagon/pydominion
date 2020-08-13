#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Ironworks(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
        self.desc = "Gain a card costing up to 4. If it is an ... Action card, +1 Action; Treasure card, +1 Coin; Victory card, +1 Card"
        self.name = 'Iron Works'
        self.cost = 4

    def special(self, game, player):
        """ Gain a card costing up to 4. If it is an action card:
            +1 action; treasure card +1 coin; victory card, +1 card"""
        c = player.plrGainCard(4, force=True)
        if c.isVictory():
            player.pickupCard()
        if c.isAction():
            player.addActions(1)
        if c.isTreasure():
            player.addCoin(1)


###############################################################################
class Test_Ironworks(unittest.TestCase):
    def setUp(self):
        # Make most of the cards too expensive to ensure we can select what we want
        initcards = ['Iron Works', 'Great Hall', 'Apprentice', 'Bandit Camp',
                     'City', 'Count', 'Duke', 'Library', 'Market', 'Rebuild']
        self.g = Game.Game(quiet=True, numplayers=1, initcards=initcards)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Iron Works'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_great_hall(self):
        """ Use Ironworks to gain a Great Hall """
        self.plr.test_input = ['great']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[-1].name, 'Great Hall')
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.hand.size(), 6)

    def test_play_silver(self):
        """ Use Ironworks to gain a Silver """
        self.plr.test_input = ['Silver']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[-1].name, 'Silver')
        self.assertEqual(self.plr.get_actions(), 0)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.hand.size(), 5)

    def test_play_ironworks(self):
        """ Use Ironworks to gain an Ironworks """
        self.plr.test_input = ['iron']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[-1].name, 'Iron Works')
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.hand.size(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
