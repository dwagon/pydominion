#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Engineer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'empires'
        self.desc = """Gain a card costing up to 4 Coin.
        You may trash this. If you do, gain a card costing up to 4 Coin."""
        self.name = 'Engineer'
        self.debtcost = 4
        self.coin = 1

    def special(self, game, player):
        player.plrGainCard(4)
        trash = player.plrChooseOptions(
            "Trash the Engineer?",
            ("Keep the enginner", False),
            ("Trash to gain a card costing up to 4", True))
        if trash:
            player.trashCard(self)
            player.plrGainCard(4)


###############################################################################
class Test_Engineer(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Engineer', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Engineer'].remove()

    def test_play_trash(self):
        """ Play an Engineer and trash it"""
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Get Silver', 'Trash', 'Moat']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertIsNotNone(self.plr.inDiscard('Moat'))
        self.assertIsNotNone(self.g.inTrash('Engineer'))

    def test_play_keep(self):
        """ Play an Engineer and keep it """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Get Silver', 'Keep']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertIsNotNone(self.plr.inPlayed('Engineer'))
        self.assertIsNone(self.g.inTrash('Engineer'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
