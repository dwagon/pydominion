#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Duchess(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.HINTERLANDS
        self.desc = """+2 Coin.  Each player (including you) looks at the top card of his deck, and discards it or puts it back."""
        self.name = 'Duchess'
        self.coin = 2
        self.cost = 2

    def special(self, game, player):
        for plr in game.player_list():
            card = plr.nextCard()
            if plr == player:
                name = 'your'
            else:
                name = "%s's" % player.name
            keep = plr.plrChooseOptions(
                "Due to %s Duchess you can keep or discard the top card" % name,
                ("Keep %s on top of deck" % card.name, True),
                ("Discard %s" % card.name, False))
            if keep:
                plr.addCard(card, 'topdeck')
            else:
                plr.output("Discarding %s" % card.name)
                plr.discardCard(card)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    if 'Estate' in args[0] or 'Duchy' in args[0] or 'Province' in args[0]:
        return False
    return True


###############################################################################
class Test_Duchess(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Duchess'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Duchess'].remove()

    def test_play(self):
        """ Play duchess - keep on deck """
        self.plr.setDeck('Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['keep']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertIsNotNone(self.plr.in_deck('Province'))
        self.assertIsNone(self.plr.in_discard('Province'))

    def test_disacrd(self):
        """ Play duchess - discard """
        self.plr.setDeck('Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['discard']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertIsNone(self.plr.in_deck('Province'))
        self.assertIsNotNone(self.plr.in_discard('Province'))

    def test_buy_duchess(self):
        self.plr.test_input = ['Duchess']
        self.plr.gainCard('Duchy')
        self.assertIsNotNone(self.plr.in_discard('Duchess'))
        self.assertIsNotNone(self.plr.in_discard('Duchy'))

    def test_buy_duchy(self):
        self.plr.test_input = ['No']
        self.plr.gainCard('Duchy')
        self.assertIsNone(self.plr.in_discard('Duchess'))
        self.assertIsNotNone(self.plr.in_discard('Duchy'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
