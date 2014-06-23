#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Minion(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'intrigue'
        self.desc = "+1 action, Choose +2 gold or discard"
        self.name = 'Minion'
        self.cost = 5
        self.actions = 1

    def special(self, game, player):
        """ Choose one: +2 gold or
            discard your hand, +4 cards and each other player with
            at least 5 card in hand discards his hand and draws 4
            cards """
        attack = player.plrChooseOptions(
            "What do you want to do?",
            ("+2 gold", False),
            ("Discard your hand, +4 cards and each other player with 5 cards discards and draws 4", True))
        if attack:
            self.attack(game, player)
        else:
            player.addGold(2)

    def attack(self, game, player):
        self.dropAndDraw(player)
        for victim in player.attackVictims():
            if len(victim.hand) >= 5:
                self.dropAndDraw(victim)

    def dropAndDraw(self, plr):
        # TODO: Do you discard the minion as well?
        plr.discardHand()
        plr.pickupCards(4)


###############################################################################
class Test_Minion(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['minion', 'moat'])
        self.plr, self.victim = self.g.players.values()
        self.card = self.g['minion'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_gold(self):
        """ Play a minion and gain two gold"""
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getGold(), 2)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(len(self.plr.hand), 5)

    def test_play_discard(self):
        """ Play a minion and discard hand"""
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getGold(), 0)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(len(self.plr.hand), 4)
        # Discard the 5 cards + the minion we added
        self.assertEqual(len(self.plr.discardpile), 5 + 1)
        self.assertEqual(len(self.victim.hand), 4)
        self.assertEqual(len(self.victim.discardpile), 5)

    def test_play_victim_smallhand(self):
        """ Play a minion and discard hand - the other player has a small hand"""
        self.victim.setHand('estate', 'estate', 'estate', 'estate')
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getGold(), 0)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(len(self.plr.hand), 4)
        # Discard the 5 cards + the minion we added
        self.assertEqual(len(self.plr.discardpile), 5 + 1)
        self.assertEqual(len(self.victim.hand), 4)
        self.assertEqual(len(self.victim.discardpile), 0)

    def test_play_defended(self):
        """ Play a minion and discard hand - the other player is defended """
        self.victim.setHand('estate', 'estate', 'estate', 'estate', 'moat')
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getGold(), 0)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(len(self.plr.hand), 4)
        # Discard the 5 cards + the minion we added
        self.assertEqual(len(self.plr.discardpile), 5 + 1)
        self.assertEqual(len(self.victim.hand), 5)
        self.assertEqual(len(self.victim.discardpile), 0)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
