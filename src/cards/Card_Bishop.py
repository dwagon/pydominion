#!/usr/bin/env python

import unittest
from Card import Card


class Card_Bishop(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.desc = "Trash a card for VP"
        self.name = 'Bishop'
        self.gold = 1
        self.victory = 1
        self.cost = 4

    def special(self, game, player):
        """ Trash a card from your hand. +VP equal to half its cost
        in coins, rounded down. Each other player may trash a card
        from his hand """
        for plr in game.players.values():
            if plr == player:
                self.trashOwnCard(game, player)
            else:
                self.trashOtherCard(game, player, plr)

    def trashOwnCard(self, game, player):
        player.output("Gain VP worth half the cost of the card you trash")
        tc = player.plrTrashCard(printcost=True)
        if not tc:
            return
        card = tc[0]
        points = int(card.cost / 2)
        player.addScore('bishop', points)
        player.output("Trashing %s for %d points" % (card.name, points))

    def trashOtherCard(self, game, player, plr):
        plr.output("%s's bishop lets you trash a card" % player.name)
        plr.plrTrashCard()


###############################################################################
class Test_Bishop(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['bishop'])
        self.plr, self.other = self.g.players.values()
        self.bishop = self.g['bishop'].remove()

    def test_play(self):
        self.plr.addCard(self.bishop, 'hand')
        self.plr.test_input = ['0']
        self.other.test_input = ['0']
        self.plr.playCard(self.bishop)
        self.assertEqual(self.plr.getGold(), 1)

    def test_trash(self):
        self.plr.setHand('gold')
        self.plr.addCard(self.bishop, 'hand')
        self.plr.test_input = ['1']
        self.other.test_input = ['0']
        self.plr.playCard(self.bishop)
        self.assertEqual(self.plr.score['bishop'], 3)
        self.assertEqual(self.plr.hand, [])
        self.assertEqual(self.g.trashpile[0].name, 'Gold')

    def test_bothtrash(self):
        self.plr.setHand('gold')
        self.other.setHand('province')
        self.plr.addCard(self.bishop, 'hand')
        self.plr.test_input = ['1']
        self.other.test_input = ['1']
        self.plr.playCard(self.bishop)
        self.assertEqual(self.plr.score['bishop'], 3)
        self.assertEqual(self.plr.hand, [])
        self.assertEqual(self.other.hand, [])
        self.assertEqual(self.g.trashSize(), 2)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
