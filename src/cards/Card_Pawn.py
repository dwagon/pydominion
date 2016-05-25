#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Pawn(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "Choose two: +1 card, +1 action, +1 buy, +1 coin"
        self.name = 'Pawn'
        self.cost = 2

    def special(self, game, player):
        """ Choose two: +1 card; +1 action +1 buy; +1 coin. (The
            choices must be different)"""
        selectable = [
            ('card', '+1 card'),
            ('action', '+1 action'),
            ('buy', '+1 buy'),
            ('coin', '+1 coin')
        ]
        chosen = []
        player.output("Pick two options")
        for i in range(2):
            options = []
            index = 1
            for k, v in selectable:
                if k in chosen:
                    continue
                options.append({'selector': '%d' % index, 'print': v, 'opt': k})
                index += 1
            o = player.userInput(options, "What do you want to do?")
            chosen.append(o['opt'])

        for choice in chosen:
            if choice == 'card':
                player.pickupCard()
            elif choice == 'action':
                player.addActions(1)
            elif choice == 'buy':
                player.addBuys(1)
            elif choice == 'coin':
                player.addCoin(1)


###############################################################################
class Test_Pawn(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Pawn'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Pawn'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_card(self):
        """ Play the pawn - select card and action"""
        self.plr.test_input = ['+1 card', '+1 action']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getBuys(), 1)
        self.assertEqual(self.plr.getCoin(), 0)

    def test_play_buy(self):
        """ Play the pawn - select buy and coin"""
        self.plr.test_input = ['+1 buy', '+1 coin']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.getActions(), 0)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
