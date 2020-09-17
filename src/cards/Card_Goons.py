#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Goons(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.PROSPERITY
        self.desc = "Other players discard down to 3. +1 VP when buying"
        self.name = 'Goons'
        self.cost = 6
        self.buys = 1
        self.coin = 2

    def special(self, game, player):
        """ Each other player discards down to three cards """
        for plr in player.attackVictims():
            plr.output("Discard down to 3 cards")
            plr.plrDiscardDownTo(3)

    def hook_buyCard(self, game, player, card):
        """ While this card is in play, when you buy a card +1 VP """
        player.output("Scored 1 more from goons")
        player.addScore('Goons', 1)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.hand) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Goons(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Goons', 'Moat'])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g['Goons'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.victim.test_input = ['1', '2', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.victim.hand.size(), 3)

    def test_defended(self):
        self.victim.setHand('Moat', 'Estate', 'Gold', 'Copper')
        self.plr.playCard(self.card)
        self.assertEqual(self.victim.hand.size(), 4)

    def test_buy(self):
        self.victim.setHand('Moat', 'Estate', 'Gold', 'Copper')
        self.plr.playCard(self.card)
        self.plr.buyCard(self.g['Copper'])
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Goons'], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
