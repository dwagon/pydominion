#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Conspirator(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
        self.desc = """+2 coin. If you've played 3 or more actions this turn (counting
            this); +1 card, +1 action """
        self.name = 'Conspirator'
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        if self.numActionsPlayed(player) >= 3:
            player.pickupCard()
            player.addActions(1)

    def numActionsPlayed(self, player):
        return sum([1 for c in player.played if c.isAction()])


###############################################################################
class Test_Conspirator(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Conspirator', 'Witch'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Conspirator'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play the conspirator with not enough actions """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.get_actions(), 0)
        self.assertEqual(self.plr.handSize(), 5)

    def test_actions(self):
        """ Play the conspirator with enough actions """
        self.plr.setPlayed('Witch', 'Witch', 'Witch')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.handSize(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
