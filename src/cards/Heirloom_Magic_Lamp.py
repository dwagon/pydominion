#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_MagicLamp(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['treasure', 'heirloom']
        self.base = 'nocturne'
        self.desc = "When you play this, if there are at least 6 cards that you have exactly 1 copy of in play, trash this. If you do, gain 3 Wishes from their pile."
        self.name = 'Magic Lamp'
        self.cost = 0
        self.coin = 1
        self.purchasable = False
        self.required_cards = [('Card', 'Wish')]

    def special(self, game, player):
        cards = []
        for c in player.played:
            if player.played.count(c) == 1:
                cards.append(c)
        if len(cards) >= 6:
            player.trashCard(self)
            for i in range(3):
                player.gainCard('Wish')


###############################################################################
class Test_MagicLamp(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Secret Cave'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Magic Lamp'].remove()

    def test_play_gain(self):
        """ Play a Magic Lamp to gain 3 Wishes """
        self.plr.addCard(self.card, 'hand')
        self.plr.setPlayed('Copper', 'Silver', 'Gold', 'Duchy', 'Estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertIsNotNone(self.plr.inDiscard('Wish'))

    def test_play_fail(self):
        """ Play a Magic Lamp but don't gain wishes """
        self.plr.addCard(self.card, 'hand')
        self.plr.setPlayed('Copper', 'Silver', 'Gold', 'Estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertIsNone(self.plr.inDiscard('Wish'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
