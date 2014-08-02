#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Spy(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'dominion'
        self.desc = "+1 cards, reveal next card and optionally discard it"
        self.name = 'Spy'
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """ Each player (including you) reveals the top of his deck and either discards it or puts it back, your choice"""
        self.spyOn(player, player)
        for pl in player.attackVictims():
            self.spyOn(player, pl)

    def spyOn(self, attacker, victim):
        c = victim.nextCard()
        vicname = "your" if attacker == victim else "%s's" % victim.name
        discard = attacker.plrChooseOptions(
            "Discard %s card?" % vicname,
            ("Keep %s on deck" % c.name, False), ("Discard %s" % c.name, True))
        if discard:
            victim.addCard(c, 'discard')
        else:
            victim.addCard(c, 'topdeck')


###############################################################################
class Test_Spy(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['spy', 'moat'])
        self.g.startGame()
        self.attacker, self.defender = self.g.playerList()
        self.attacker.setDeck('estate', 'province', 'duchy')
        self.defender.setDeck('estate', 'gold')

    def test_moat(self):
        self.defender.setHand('moat')
        scard = self.attacker.gainCard('spy', 'hand')
        self.attacker.test_input = ['0']
        self.attacker.playCard(scard)
        self.assertEquals(self.attacker.deck[-1].name, 'Province')
        self.assertEquals(self.defender.deck[-1].name, 'Gold')

    def test_undefended(self):
        scard = self.attacker.gainCard('spy', 'hand')
        self.attacker.test_input = ['0', '0']
        self.attacker.playCard(scard)
        self.assertEquals(self.attacker.deck[-1].name, 'Province')
        self.assertEquals(self.defender.deck[-1].name, 'Gold')

    def test_discards(self):
        scard = self.attacker.gainCard('spy', 'hand')
        self.attacker.test_input = ['1', '1']
        self.attacker.playCard(scard)
        self.assertEquals(self.attacker.deck[-1].name, 'Estate')
        self.assertEquals(self.defender.deck[-1].name, 'Estate')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
