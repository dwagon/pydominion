#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Swindler(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'intrigue'
        self.desc = "+2 gold. Other players trash top card and gain one with the same cost"
        self.name = 'Swindler'
        self.cost = 3
        self.gold = 2

    def special(self, game, player):
        """ Each other player trashed the top card of his deck and
            gains a card with the same cost that you choose """

        for victim in player.attackVictims():
            card = victim.pickupCard()
            victim.trashCard(card)
            player.output("Pick which card %s will get" % victim.name)
            c = victim.plrGainCard(card.cost, modifier='equal', chooser=player, force=True)
            victim.output("%s picked a %s to replace your trashed %s" % (player.name, c.name, card.name))


###############################################################################
class Test_Swindler(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['swindler', 'moat'])
        self.plr, self.victim = self.g.players.values()
        self.card = self.g['swindler'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play the Swindler """
        self.victim.setHand('moat')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getGold(), 2)

    def test_defended(self):
        """ Swindle a defended player """
        self.victim.setHand('moat')
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashpile, [])

    def test_attack(self):
        """ Swindle an undefended player """
        self.victim.setDeck('gold')
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashpile[0].name, 'Gold')
        self.assertEqual(self.g.trashSize(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
