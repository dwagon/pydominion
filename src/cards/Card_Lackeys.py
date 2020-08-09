#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Lackeys(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.RENAISSANCE
        self.name = 'Lackeys'
        self.cards = 2
        self.cost = 2

    ###########################################################################
    def desc(self, player):
        if player.phase == "buy":
            return "+2 Cards; When you gain this, +2 Villagers."
        return "+2 Cards"

    ###########################################################################
    def hook_gain_this_card(self, game, player):
        player.gainVillager(2)


###############################################################################
class Test_Lackeys(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Lackeys'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_playCard(self):
        self.card = self.g['Lackeys'].remove()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 7)
        self.assertLessEqual(self.plr.getVillager(), 0)

    def test_gainCard(self):
        self.plr.gainCard('Lackeys')
        self.assertLessEqual(self.plr.getVillager(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
