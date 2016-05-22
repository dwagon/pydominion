#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Bishop(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.desc = "Trash a card for VP"
        self.name = 'Bishop'
        self.coin = 1
        self.victory = 1
        self.cost = 4

    def special(self, game, player):
        """ Trash a card from your hand. +VP equal to half its cost
        in coins, rounded down. Each other player may trash a card
        from his hand """
        for plr in game.playerList():
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

    def trashOtherCard(self, game, player, victim):
        victim.output("%s's bishop lets you trash a card" % player.name)
        tc = victim.plrTrashCard()
        if tc:
            victim.output("Trashing %s" % tc[0].name)
        else:
            victim.output("All mine I tell you, all mine")


###############################################################################
def botresponse(player, kind, args=[], kwargs={}):
    # Trash an estate, then a copper else nothing
    es = player.inHand('estate')
    if es:
        return [es]
    cu = player.inHand('copper')
    if cu:
        return [cu]
    else:
        return []


###############################################################################
class Test_Bishop(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['bishop'])
        self.g.startGame()
        self.plr, self.other = self.g.playerList()
        self.bishop = self.g['bishop'].remove()

    def test_play(self):
        self.plr.addCard(self.bishop, 'hand')
        self.plr.test_input = ['finish']
        self.other.test_input = ['finish']
        self.plr.playCard(self.bishop)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_trash(self):
        self.plr.setHand('gold')
        self.plr.addCard(self.bishop, 'hand')
        self.plr.test_input = ['trash gold']
        self.other.test_input = ['finish']
        self.plr.playCard(self.bishop)
        self.assertEqual(self.plr.score['bishop'], 3)
        self.assertTrue(self.plr.hand.isEmpty())
        self.assertEqual(self.g.trashpile[0].name, 'Gold')

    def test_bothtrash(self):
        self.plr.setHand('gold')
        self.other.setHand('province')
        self.plr.addCard(self.bishop, 'hand')
        self.plr.test_input = ['trash gold']
        self.other.test_input = ['trash province']
        self.plr.playCard(self.bishop)
        self.assertEqual(self.plr.score['bishop'], 3)
        self.assertTrue(self.plr.hand.isEmpty())
        self.assertTrue(self.other.hand.isEmpty())
        self.assertEqual(self.g.trashSize(), 2)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
