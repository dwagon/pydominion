#!/usr/bin/env python

import unittest
import Game


###############################################################################
class TestToken(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_place_token(self):
        """ Ensure that when we place a token it is there """
        self.assertEquals(self.plr.tokens['Trashing'], None)
        self.plr.place_token('Trashing', 'Copper')
        self.assertNotEquals(self.plr.tokens['Trashing'], None)
        ans = self.plr.which_token('Copper')
        self.assertEquals(ans, ['Trashing'])

    def test_pickup(self):
        """ Ensure we have smaller hand if -Card token in place """
        self.plr.card_token = True
        self.plr.hand.empty()
        self.plr.pickUpHand()
        self.assertEqual(self.plr.handSize(), 4)
        self.assertFalse(self.plr.card_token)

    def test_short_draw(self):
        """ Ensure we draw less if the -Card token is in place"""
        self.plr.card_token = True
        self.plr.setHand()
        moat = self.g['moat'].remove()
        self.plr.addCard(moat, 'hand')
        self.assertEquals(self.plr.handSize(), 1)
        self.plr.playCard(moat)
        # 2 for moat -1 for token
        self.assertEquals(self.plr.handSize(), 2 - 1)
        self.assertFalse(self.plr.card_token)

    def test_action_token(self):
        """ Does the +Action token work """
        self.plr.place_token('+Action', 'Moat')
        moat = self.g['moat'].remove()
        self.plr.addCard(moat, 'hand')
        self.assertEquals(self.plr.getActions(), 1)
        self.plr.playCard(moat)
        self.assertEquals(self.plr.getActions(), 1)

    def test_trashing_token(self):
        """ Does the Trashing token work """
        self.plr.setHand('gold', 'province', 'duchy')
        self.plr.place_token('Trashing', 'Moat')
        self.plr.test_input = ['trash province']
        self.plr.buyCard(self.g['Moat'])
        self.assertEqual(self.g.trashSize(), 1)

    def test_cost_token(self):
        """ Does the -Cost token work """
        self.assertEquals(self.plr.getCoin(), 0)
        self.plr.place_token('-Cost', 'Moat')
        self.plr.buyCard(self.g['Moat'])
        self.assertEquals(self.plr.getCoin(), 0)

    def test_card_token(self):
        """ Does the +Card token work """
        self.plr.setHand()
        self.plr.place_token('+Card', 'Moat')
        moat = self.g['moat'].remove()
        self.plr.addCard(moat, 'hand')
        self.assertEquals(self.plr.handSize(), 1)
        self.plr.playCard(moat)
        # 2 for moat 1 for token
        self.assertEquals(self.plr.handSize(), 2 + 1)

    def test_pluscoin_token(self):
        """ Does the +Coin token work """
        self.plr.place_token('+Coin', 'Moat')
        moat = self.g['moat'].remove()
        self.plr.addCard(moat, 'hand')
        self.assertEquals(self.plr.getCoin(), 0)
        self.plr.playCard(moat)
        self.assertEquals(self.plr.getCoin(), 1)

    def test_buy_token(self):
        """ Does the +Buy token work """
        self.plr.place_token('+Buy', 'Moat')
        moat = self.g['moat'].remove()
        self.plr.addCard(moat, 'hand')
        self.assertEquals(self.plr.getBuys(), 1)
        self.plr.playCard(moat)
        self.assertEquals(self.plr.getBuys(), 2)

    def test_journey_token(self):
        """ Does the Journey token work """
        self.assertTrue(self.plr.journey_token)
        self.plr.flip_journey_token()
        self.assertFalse(self.plr.journey_token)
        self.plr.flip_journey_token()
        self.assertTrue(self.plr.journey_token)

    def test_coin_token(self):
        """ Does the -Coin token work """
        pass    # TODO

    def test_estate_token(self):
        """ Does the Estate token work """
        pass    # TODO


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
