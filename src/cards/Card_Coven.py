#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Coven """

import unittest
import Game
from Card import Card


###############################################################################
class Card_Coven(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'menagerie'
        self.desc = """+1 Action; +2 Coin; Each other player Exiles a Curse
            from the Supply. If they can't, they discard their Exiled Curses."""
        self.name = 'Coven'
        self.actions = 1
        self.coin = 2
        self.cost = 5
        self.required_cards = ['Curse']

    def special(self, game, player):
        for plr in player.attackVictims():
            plr.exile_card('Curse')
            if game['Curse'].is_empty():
                num = plr.unexile('Curse')
                plr.output("Unexiled {} Curses from {}'s Coven".format(num, player.name))
            else:
                plr.output("Exiled a Curse from {}'s Coven".format(player.name))


###############################################################################
class Test_Coven(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Coven', 'Moat'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g['Coven'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertIsNotNone(self.vic.in_exile('Curse'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
