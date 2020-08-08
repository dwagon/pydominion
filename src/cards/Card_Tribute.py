#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Tribute(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = """ The player to your left reveals then discards the top
            2 cards of his deck. For each differently named card revealed,
            if is an Action card, +2 actions; treasure card, +2 coin;
            victory card, +2 cards """
        self.name = 'Tribute'
        self.cost = 5

    def special(self, game, player):
        victim = game.playerToLeft(player)
        cards = []
        for _ in range(2):
            card = victim.nextCard()
            victim.revealCard(card)
            cards.append(card)
        cardname = None
        for c in cards:
            player.output("Looking at %s from %s" % (c.name, victim.name))
            victim.output("%s's Tribute discarded %s" % (player.name, c.name))
            victim.addCard(c, 'discard')
            if c.name == cardname:
                player.output("Duplicate - no extra")
                continue
            cardname = c.name
            if c.isAction():
                player.output("Gained two actions")
                player.addActions(2)
            elif c.isTreasure():
                player.output("Gained two coin")
                player.addCoin(2)
            elif c.isVictory():
                player.output("Gained two cards")
                player.pickupCards(2)


###############################################################################
class Test_Tribute(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Tribute'])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g['Tribute'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a tribute """
        self.victim.setDeck('Copper', 'Estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.handSize(), 7)
        self.assertEqual(self.victim.discard_size(), 2)

    def test_same(self):
        """ Victim has the same cards for Tribute"""
        self.victim.setDeck('Tribute', 'Tribute')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.handSize(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
