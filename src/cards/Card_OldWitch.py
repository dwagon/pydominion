#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_OldWitch(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'renaissance'
        self.desc = """+3 Cards; Each other player gains a Curse and may trash a Curse from their hand."""
        self.required_cards = ['Curse']
        self.cards = 3
        self.name = 'Old Witch'
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        for pl in player.attackVictims():
            player.output("{} got cursed".format(pl.name))
            pl.output("{}'s Old Witch cursed you".format(player.name))
            pl.gainCard('Curse')
            tr = pl.inHand('Curse')
            if tr:
                c = pl.plrTrashCard(cardsrc=[tr], prompt="You may trash a Curse")
                if c:
                    player.output("{} trashed a Curse".format(pl.name))


###############################################################################
def botresponse(player, kind, args=[], kwargs={}):  # pragma: no cover
    return kwargs['cardsrc']


###############################################################################
class Test_OldWitch(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Old Witch'])
        self.g.startGame()
        self.plr, self.vic = self.g.playerList()
        self.card = self.g['Old Witch'].remove()

    def test_play(self):
        self.plr.setHand()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 3)
        self.assertIsNotNone(self.vic.inDiscard('Curse'))

    def test_has_curse(self):
        self.vic.setHand('Curse')
        self.plr.addCard(self.card, 'hand')
        self.vic.test_input = ['Trash Curse']
        self.plr.playCard(self.card)
        self.assertIsNone(self.vic.inHand('Curse'))
        self.assertIsNotNone(self.g.inTrash('Curse'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF