#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Barge """

import unittest
import Game
import Card


###############################################################################
class Card_Barge(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.MENAGERIE
        self.desc = "Either now or at the start of your next turn, +3 Cards and +1 Buy."
        self.name = 'Barge'
        self.cost = 5
        self._choice = 'undef'

    def special(self, game, player):
        choice = player.plrChooseOptions(
            "Pick One",
            ("Now: +3 Cards and +1 Buy", "now"),
            ("Next Turn: +3 Cards and +1 Buy", "then")
        )
        if choice == "now":
            player.pickupCards(3)
            player.addBuys(1)
            self._choice = 'now'
        else:
            self._choice = 'then'

    def duration(self, game, player):
        if self._choice == 'then':
            player.pickupCards(3)
            player.addBuys(1)
        self._choice = 'undef'


###############################################################################
class Test_Barge(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Barge'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Barge'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_this_turn(self):
        self.plr.test_input = ['now']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 3)
        self.assertEqual(self.plr.get_buys(), 1 + 1)

    def test_play_next_turn(self):
        self.plr.test_input = ['next']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_buys(), 1)
        self.assertEqual(self.plr.hand.size(), 5)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 5 + 3)
        self.assertEqual(self.plr.get_buys(), 1 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
