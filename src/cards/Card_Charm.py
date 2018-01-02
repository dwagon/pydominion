#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_Charm(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'empire'
        self.desc = "When you play this, choose one: +1 Buy and +2 Coin; or the next time you buy a card this turn, you may also gain a differently named card with the same cost."
        self.name = 'Charm'
        self.cost = 5
        self.buytrigger = False

    def special(self, game, player):
        ans = player.plrChooseOptions(
            "Pick One",
            ("+1 Buy and +2 Coin", True),
            ("Next time you buy a card this turn, you may also gain a differently named card with the same cost.", False)
            )
        if ans:
            player.addBuys(1)
            player.addCoin(2)
        else:
            self.buytrigger = True

    def hook_buyCard(self, game, player, card):
        if not self.buytrigger:
            return
        self.buytrigger = False
        cost = card.cost
        player.plrGainCard(cost=cost, modifier='equal', exclude=[card.name])


###############################################################################
class Test_Charm(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Charm'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Charm'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_choose_one(self):
        self.plr.test_input = ['+1 Buy']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_play_choose_two(self):
        self.plr.test_input = ['next time']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 1)
        self.assertEqual(self.plr.getCoin(), 0)
        self.plr.test_input = ['Get Duchy']
        self.plr.buyCard(self.g['Charm'])
        self.assertIsNotNone(self.plr.inDiscard('Duchy'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF