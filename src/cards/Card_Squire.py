#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Squire(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = """+1 Coin. Choose one: +2 Actions; or +2 Buys; or gain a Silver.
        When you trash this, gain an Attack card."""
        self.name = 'Squire'
        self.cost = 2
        self.coin = 1

    def special(self, game, player):
        choice = player.plrChooseOptions(
            "Choose one.",
            ("+2 Actions", 'actions'),
            ("+2 Buys", 'buys'),
            ("Gain a Silver", 'silver')
            )
        if choice == 'actions':
            player.addActions(2)
        elif choice == 'buys':
            player.addBuys(2)
        elif choice == 'silver':
            player.gainCard('Silver')

    def hook_trashThisCard(self, game, player):
        attacks = []
        for cp in game.cardpiles.values():
            if cp.isAttack() and cp.purchasable:
                attacks.append(cp)
        cards = player.cardSel(
            prompt="Gain an attack card",
            cardsrc=attacks
            )
        player.gainCard(cards[0])


###############################################################################
class Test_Squire(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Squire', 'Militia'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Squire'].remove()

    def test_play_actions(self):
        """ Play a Squire - gain actions"""
        self.plr.test_input = ['action']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.getBuys(), 1)
        self.assertIsNone(self.plr.inDiscard('Silver'))

    def test_play_buys(self):
        """ Play a Squire - gain buys"""
        self.plr.test_input = ['buys']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 0)
        self.assertEqual(self.plr.getBuys(), 3)
        self.assertIsNone(self.plr.inDiscard('Silver'))

    def test_play_silver(self):
        """ Play a Squire - gain Silver"""
        self.plr.test_input = ['silver']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 0)
        self.assertEqual(self.plr.getBuys(), 1)
        self.assertIsNotNone(self.plr.inDiscard('Silver'))

    def test_trash(self):
        """ Trash a Squire """
        self.plr.test_input = ['militia']
        self.plr.trashCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Militia'))

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF