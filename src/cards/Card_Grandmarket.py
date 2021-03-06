#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Grandmarket(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.PROSPERITY
        self.desc = "+1 card, +1 action, +1 buy, +2 coin"
        self.name = 'Grand Market'
        self.cost = 6
        self.cards = 1
        self.actions = 1
        self.buys = 1
        self.coin = 2

    def hook_allowedToBuy(self, game, player):
        """ You can't buy this if you have any copper in play """
        for c in player.hand + player.played:
            if c.name == 'Copper':
                return False
        return True


###############################################################################
class Test_Grandmarket(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Grand Market'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.gm = self.g['Grand Market'].remove()

    def test_play(self):
        self.plr.addCard(self.gm, 'hand')
        self.plr.playCard(self.gm)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.hand.size(), 6)

    def test_nobuy(self):
        self.plr.setHand('Copper', 'Gold', 'Gold')
        self.plr.addCoin(6)
        self.plr.test_input = ['0']
        self.plr.phase = 'buy'
        options, _ = self.plr.choice_selection()
        for opt in options:
            if opt['name'] == 'Grand Market' and opt['verb'] == 'Buy':   # pragma: no cover
                self.fail("Allowed to buy with copper")

    def test_nobuy_played(self):
        self.plr.setHand('Gold', 'Gold', 'Gold')
        self.plr.setPlayed('Copper')
        self.plr.addCoin(6)
        self.plr.test_input = ['0']
        self.plr.phase = 'buy'
        options, _ = self.plr.choice_selection()
        for opt in options:
            if opt['name'] == 'Grand Market' and opt['verb'] == 'Buy':   # pragma: no cover
                self.fail("Allowed to buy with copper")

    def test_buy(self):
        self.plr.setHand('Gold', 'Gold', 'Gold')
        self.plr.addCoin(6)
        self.plr.test_input = ['0']
        self.plr.phase = 'buy'
        options, _ = self.plr.choice_selection()
        for opt in options:
            if opt['name'] == 'Grand Market' and opt['verb'] == 'Buy':   # pragma: no cover
                break
        else:   # pragma: no cover
            self.fail("Not allowed to buy grand market")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
