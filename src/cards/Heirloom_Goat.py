#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Goat(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['treasure', 'heirloom']
        self.base = 'nocturne'
        self.desc = "When you play this, you may trash a card from your hand."
        self.name = 'Goat'
        self.cost = 2
        self.coin = 1
        self.purchasable = False

    def special(self, game, player):
        if player.handSize():
            player.plrTrashCard()


###############################################################################
def botresponse(player, kind, args=[], kwargs={}):  # pragma: no cover
    return []


###############################################################################
class Test_Goat(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Pixie'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Goat'].remove()

    def test_play(self):
        self.plr.setHand('Province', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Province']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertIsNotNone(self.g.inTrash('Province'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
