#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Saboteur(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'intrigue'
        self.desc = "Trash other players cards but they get one back"
        self.name = 'Saboteur'
        self.cost = 5

    def special(self, game, player):
        """ Each other player reveals cards from the top of his
            deck until revealing one costing 3 or more. He trashes that
            card and may gain a card costing at most 2 less than it.
            He discards the other revealed cards. """
        for victim in player.attackVictims():
            card = self.pickCard(victim, player)
            if not card:
                continue
            victim.output("%s's saboteur trashed %s" % (player.name, card.name))
            victim.trashCard(card)
            victim.plrGainCard(card.cost - 2)

    def pickCard(self, victim, player):
        for i in range(len(victim.allCards())):
            c = victim.nextCard()
            if c.cost >= 3:
                return c
            victim.output("Saboteur checking and discarding %s" % c.name)
            victim.discardCard(c)
        victim.output("Don't have any suitable cards")
        player.output("%s doesn't have any suitable cards")
        return None


###############################################################################
class Test_Saboteur(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['saboteur'])
        self.plr, self.victim = self.g.players.values()
        self.card = self.g['saboteur'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a saboteur """
        self.victim.test_input = ['1']
        self.victim.setDeck('gold', 'copper', 'estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), 1)
        trashed = self.g.trashpile[0]
        self.assertTrue(trashed.cost >= 3)
        for c in self.victim.discardpile[:-1]:
            self.assertTrue(c.cost < 3)
        self.assertTrue(self.victim.discardpile[-1].cost <= trashed.cost - 2)

    def test_nomatching(self):
        """ Play a saboteur where the victim doesn't have a suitable card """
        self.victim.setDeck('copper', 'copper', 'estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), 0)
        for c in self.victim.discardpile:
            self.assertTrue(c.cost < 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
