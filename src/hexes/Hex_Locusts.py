#!/usr/bin/env python

import unittest
import Card
import Game
from Hex import Hex


###############################################################################
class Hex_Locusts(Hex):
    def __init__(self):
        Hex.__init__(self)
        self.cardtype = Card.TYPE_HEX
        self.base = Game.NOCTURNE
        self.desc = """Trash the top card of your deck. If it's Copper or Estate,
            gain a Curse. Otherwise, gain a cheaper card that shares a type with it."""
        self.name = "Locusts"
        self.purchasable = False
        self.required_cards = ['Curse']

    def special(self, game, player):
        nxt = player.nextCard()
        if nxt.name in ('Copper', 'Estate'):
            player.output("Gaining a curse because your next card is {}".format(nxt.name))
            player.gainCard('Curse')
        else:
            player.output("Gain a card costing {} because your next card is {}".format(nxt.cost-1, nxt.name))
            types = {
                Card.TYPE_VICTORY: nxt.isVictory(),
                Card.TYPE_TREASURE: nxt.isTreasure(),
                Card.TYPE_ACTION: nxt.isAction(),
                }
            player.plrGainCard(cost=nxt.cost-1, types=types)
        player.output("Trashing your {}".format(nxt.name))
        player.trashCard(nxt)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    if 'Silver' in [_.name for _ in kwargs['cardsrc']]:
        return ['Silver']
    if 'Duchy' in [_.name for _ in kwargs['cardsrc']]:
        return ['Duchy']
    if 'Copper' in [_.name for _ in kwargs['cardsrc']]:
        return ['Copper']
    if 'Estate' in [_.name for _ in kwargs['cardsrc']]:
        return ['Estate']
    return [kwargs['cardsrc'][0].name]


###############################################################################
class Test_Locusts(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cursed Village'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for h in self.g.hexes[:]:
            if h.name != "Locusts":
                self.g.hexes.remove(h)

    def test_curse(self):
        """ Locusts to gain a Curse """
        self.plr.setDeck('Estate')
        self.plr.gainCard('Cursed Village')
        self.assertIsNotNone(self.plr.in_discard('Curse'))
        self.assertIsNotNone(self.g.in_trash('Estate'))

    def test_gain(self):
        """ Locusts to gain a cheaper card """
        self.plr.setDeck('Duchy')
        self.plr.test_input = ['Get Estate']
        self.plr.gainCard('Cursed Village')
        self.assertIsNone(self.plr.in_discard('Curse'))
        self.assertIsNotNone(self.plr.in_discard('Estate'))
        self.assertIsNotNone(self.g.in_trash('Duchy'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
