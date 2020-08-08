#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Patrol(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = """+3 Cards; Reveal the top 4 cards of your deck.
            Put the Victory cards and Curses into your hand.
            Put the rest back in any order."""
        self.name = 'Patrol'
        self.cards = 3
        self.cost = 5

    def special(self, game, player):
        cards = set()
        for _ in range(4):
            c = player.nextCard()
            player.revealCard(c)
            if c is None:
                break
            if c.isVictory() or c.name == 'Curse':
                player.addCard(c, 'hand')
                player.output("Patrol adding {}".format(c.name))
            else:
                cards.add(c)
        for c in cards:
            player.output("Putting {} back on deck".format(c.name))
            player.addCard(c, 'topdeck')


###############################################################################
class Test_Patrol(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Patrol'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Patrol'].remove()

    def test_play(self):
        self.plr.setHand()
        self.plr.addCard(self.card, 'hand')
        self.plr.setDeck('Duchy', 'Province', 'Silver', 'Gold', 'Copper', 'Copper', 'Gold')
        self.plr.playCard(self.card)
        self.g.print_state()
        self.assertIsNotNone(self.plr.in_hand('Province'))
        self.assertIsNotNone(self.plr.in_hand('Duchy'))
        self.assertIsNone(self.plr.in_hand('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
