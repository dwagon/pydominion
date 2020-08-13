#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Stockpile """

import unittest
import Game
import Card


###############################################################################
class Card_Stockpile(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.desc = """3 Coin; +1 Buy; When you play this, Exile it."""
        self.name = 'Stockpile'
        self.coin = 3
        self.buys = 1
        self.cost = 3

    def special(self, game, player):
        player.exile_card(self)
        player.played.remove(self)


###############################################################################
class Test_Stockpile(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Stockpile'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Stockpile'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_exile('Stockpile'))
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
