#!/usr/bin/env python

import unittest
from cards.Card_Castles import CastleCard


###############################################################################
class Card_OpulentCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = ['action', 'victory', 'castle']
        self.base = 'empires'
        self.cost = 7
        self.desc = """Discard any number of Victory cards. +2 Coin per card discarded. +3VP"""
        self.victory = 3
        self.name = "Opulent Castle"

    def special(self, game, player):
        victcards = [c for c in player.hand if c.isVictory()]
        cards = player.plrDiscardCards(anynum=True, cardsrc=victcards, prompt="Discard any number of Victory cards. +2 Coin per card discarded")
        player.addCoin(len(cards) * 2)


###############################################################################
class Test_OpulentCastle(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Castles'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        while True:
            self.card = self.g['Castles'].remove()
            if self.card.name == 'Opulent Castle':
                break

    def test_play(self):
        """ Play a castle """
        self.plr.setHand('Estate', 'Duchy', 'Province', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['estate', 'duchy', 'province', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getScoreDetails()['Opulent Castle'], 3)
        self.assertEqual(self.plr.getCoin(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
