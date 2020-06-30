#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_Quarry(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'prosperity'
        self.desc = "+1 Coin. While this is in play, Action cards cost 2 less, but not less than 0."
        self.name = 'Quarry'
        self.coin = 1
        self.cost = 4

    def hook_cardCost(self, game, player, card):
        if self in player.played and card.isAction():
            return -2
        return 0


###############################################################################
class Test_Quarry(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Quarry', 'Moat'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.card = self.g['Quarry'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a quarry """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.cardCost(self.g['Gold']), 6)
        self.assertEqual(self.plr.cardCost(self.g['Moat']), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()


# EOF
