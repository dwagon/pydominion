#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Amulet(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.ADVENTURE
        self.desc = "Now and next turn - Choose 1: +1 Coin, trash card, gain silver"
        self.name = 'Amulet'
        self.cost = 3

    def special(self, game, player):
        self.amulet_special(game, player)

    def duration(self, game, player):
        self.amulet_special(game, player)

    def amulet_special(self, game, player):
        """ Now and at the start of your next turn, choose one: +1 Coin;
            or trash a card from your hand; or gain a Silver """
        choice = player.plrChooseOptions(
            "Pick one",
            ('Gain a coin', 'coin'),
            ('Trash a card', 'trash'),
            ('Gain a silver', 'silver'))
        if choice == 'coin':
            player.addCoin(1)
        if choice == 'trash':
            player.plrTrashCard(num=1)
        if choice == 'silver':
            player.gainCard('Silver')


###############################################################################
class Test_Amulet(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Amulet'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Amulet'].remove()
        self.plr.setHand('Duchy')
        self.plr.addCard(self.card, 'hand')

    def test_play_coin(self):
        """ Play an amulet with coin """
        self.plr.test_input = ['coin', 'coin']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertIsNone(self.plr.in_discard('Silver'))
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertIsNone(self.plr.in_discard('Silver'))

    def test_play_silver(self):
        """ Play an amulet with coin """
        self.plr.test_input = ['silver', 'silver']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard('Silver'))
        self.assertEqual(self.plr.getCoin(), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertIsNotNone(self.plr.in_discard('Silver'))

    def test_play_trash(self):
        """ Play an amulet with trash """
        tsize = self.g.trashSize()
        self.plr.test_input = ['trash', 'duchy', 'finish', 'trash', '1', 'finish']
        self.plr.playCard(self.card)
        self.assertIsNone(self.plr.in_discard('Silver'))
        self.assertIsNotNone(self.g.in_trash('Duchy'))
        self.assertEqual(self.plr.getCoin(), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertIsNone(self.plr.in_discard('Silver'))
        self.assertEqual(self.g.trashSize(), tsize + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
