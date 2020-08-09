#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Cobbler(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_NIGHT, Card.TYPE_DURATION]
        self.base = Game.NOCTURNE
        self.desc = "At the start of your next turn, gain a card to your hand costing up to 4."
        self.name = 'Cobbler'
        self.cost = 5

    def duration(self, game, player):
        player.plrGainCard(4)


###############################################################################
class Test_Cobbler(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cobbler'], badcards=['Blessed Village', 'Cemetery'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Cobbler'].remove()

    def test_duration(self):
        try:
            self.plr.addCard(self.card, 'hand')
            self.plr.playCard(self.card)
            self.plr.end_turn()
            self.plr.test_input = ['1']
            self.plr.start_turn()
            self.assertLessEqual(self.plr.discardpile[0].cost, 4)
        except (AssertionError, IOError, OSError):  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
