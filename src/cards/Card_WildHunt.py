#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_WildHunt(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'gathering']
        self.base = 'empires'
        self.desc = """Choose one: +3 Cards and add 1 VP to the Wild Hunt Supply pile; or gain an Estate, and if you do, take the VP from the pile."""
        self.name = 'Wild Hunt'
        self.cost = 5

    def special(self, game, player):
        give = player.plrChooseOptions(
            "Choose one:",
            ("+3 Cards and add 1 VP to the Wild Hunt Supply pile", True),
            ("Gain an Estate, and if you do, take %d VP from the pile." % game['Wild Hunt'].getVP(), False))
        if give:
            player.pickupCards(3)
            game['Wild Hunt'].addVP()
        else:
            player.gainCard('Estate')
            score = game['Wild Hunt'].drainVP()
            player.output("Gaining %d VP from Wild Hunt" % score)
            player.addScore('Wild Hunt', score)


###############################################################################
class Test_WildHunt(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Wild Hunt'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.card = self.g['Wild Hunt'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_give(self):
        """ Play a Wild Hunt and take the cards"""
        self.plr.test_input = ['Cards']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5 + 3)
        self.assertEqual(self.g['Wild Hunt'].getVP(), 1)

    def test_play_take(self):
        """ Play a Wild Hunt and take the score"""
        self.plr.test_input = ['Gain']
        self.g['Wild Hunt'].addVP(3)
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertIsNotNone(self.plr.inDiscard('Estate'))
        self.assertEqual(self.plr.getScoreDetails()['Wild Hunt'], 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
