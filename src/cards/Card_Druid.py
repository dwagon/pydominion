#!/usr/bin/env python

import unittest
import random
from Card import Card
from PlayArea import PlayArea


###############################################################################
class Card_Druid(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'fate']
        self.base = 'nocturne'
        self.desc = "+1 Buy; Receive one of the set-aside Boons"
        self.name = 'Druid'
        self.buys = 1
        self.cost = 2

    def setup(self, game):
        game._druid_area = PlayArea([])
        random.shuffle(game.boons)
        for i in range(3):
            game._druid_area.add(game.boons.pop())

    def special(self, game, player):
        options = []
        for i in range(3):
            sel = '%d' % i
            bn = list(game._druid_area)[i]
            toprint = "Receive {}: {}".format(bn.name, bn.description(player))
            options.append({'selector': sel, 'print': toprint, 'boon': bn})
        b = player.userInput(options, "Which boon? ")
        player.receive_boon(boon=b['boon'], discard=False)


###############################################################################
class Test_Druid(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Druid', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Druid'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a Druid """
        self.plr.test_input = ['0', '0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)

    def test_setaside(self):
        """ Test that we don't get a set aside boon """
        setaside = set([_.name for _ in self.g._druid_area])
        left = set([_.name for _ in self.g.boons])
        if setaside.intersection(left):
            self.fail("Set aside boons not set aside")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF