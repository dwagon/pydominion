#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Pawn(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "Choose two: +1 card, +1 action, +1 buy, +1 gold"
        self.name = 'Pawn'
        self.cost = 2

    def special(self, game, player):
        """ Choose two: +1 card; +1 action +1 buy; +1 gold. (The
            choices must be different)"""
        selectable = [
            ('card', '+1 card'),
            ('action', '+1 action'),
            ('buy', '+1 buy'),
            ('gold', '+1 gold')
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
                player.t['actions'] += 1
            elif choice == 'buy':
                player.t['buys'] += 1
            elif choice == 'gold':
                player.t['gold'] += 1


###############################################################################
class Test_Pawn(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['pawn'])
        self.plr = self.g.players[0]
        self.card = self.g['pawn'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_card(self):
        """ Play the pawn - select card and action"""
        self.plr.test_input = ['1', '1']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 6)
        self.assertEqual(self.plr.t['actions'], 1)
        self.assertEqual(self.plr.t['buys'], 1)
        self.assertEqual(self.plr.t['gold'], 0)

    def test_play_buy(self):
        """ Play the pawn - select buy and gold"""
        self.plr.test_input = ['3', '3']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 5)
        self.assertEqual(self.plr.t['actions'], 0)
        self.assertEqual(self.plr.t['buys'], 2)
        self.assertEqual(self.plr.t['gold'], 1)


###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF
