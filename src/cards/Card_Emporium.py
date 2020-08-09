#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Emporium(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.EMPIRES
        self.name = 'Emporium'
        self.coin = 1
        self.actions = 1
        self.cards = 1
        self.cost = 5

    ###########################################################################
    def desc(self, player):
        if player.phase == Card.ACTION:
            return "+1 Card, +1 Action, +1 Coin"
        return "+1 Card, +1 Action, +1 Coin. When you gain this, if you have at least 5 Action cards in play, +2VP."

    ###########################################################################
    def hook_gain_this_card(self, game, player):
        count = sum([1 for c in player.played if c.isAction()])
        if count >= 5:
            player.addScore('Emporium', 2)
            player.output("Gained 2VP from Emporium")
        else:
            player.output("No VP as only have {} action cards in play".format(count))


###############################################################################
class Test_Emporium(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Emporium', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Emporium'].remove()

    def test_play(self):
        """ Play the Emporium """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.get_actions(), 1)

    def test_gain_with_actions(self):
        """ Play the Emporium having played lots of actions"""
        self.plr.setPlayed('Moat', 'Moat', 'Moat', 'Moat', 'Moat')
        self.plr.gainCard('Emporium')
        self.assertEqual(self.plr.getScoreDetails()['Emporium'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
