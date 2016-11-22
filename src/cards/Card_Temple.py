#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Temple(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'gathering']
        self.base = 'empires'
        self.desc = """+1 VP. Trash from 1 to 3 differently named cards from your hand. Add 1 VP
        to the Temple Supply pile. When you gain this, take the VP from the
        Temple Supply pile."""
        self.name = 'Temple'
        self.cost = 4

    def special(self, game, player):
        player.addScore('Temple', 1)
        cardnames = set([c.name for c in player.hand])
        cards = [player.inHand(c) for c in cardnames]
        trash = player.plrTrashCard(cardsrc=cards, prompt="Trash up to 3 different cards", num=3)
        if not trash:
            return
        game['Temple'].addVP()

    def hook_gainThisCard(self, game, player):
        score = game['Temple'].drainVP()
        player.output("Gaining %d VP from Temple" % score)
        player.addScore('Temple', score)


###############################################################################
class Test_Temple(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Temple'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Temple'].remove()

    def test_play(self):
        """ Play a Temple """
        self.plr.setHand('Copper', 'Silver', 'Silver', 'Gold', 'Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Copper', 'Silver', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getScoreDetails()['Temple'], 1)
        self.assertIsNotNone(self.g.inTrash('Silver'))

    def test_gain(self):
        """ Gain a Temple """
        self.g['Temple'].addVP(5)
        self.plr.buyCard(self.g['Temple'])
        self.assertEqual(self.plr.getScoreDetails()['Temple'], 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
