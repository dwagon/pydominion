#!/usr/bin/env python

import unittest
from Card import Card


class Card_Rabble(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+3 cards. Other players discard cards"
        self.name = 'Rabble'
        self.cost = 5
        self.cards = 3

    def attack(self, victim, attacker):
        cards = []
        for i in range(3):
            c = victim.nextCard()
            if c.isAction() or c.isTreasure():
                victim.output("Discarding %s due to %s's rabble" % (c.cardname, attacker.name))
                attacker.output("%s discarding %s" % (victim.name, c.cardname))
                victim.discardCard(c)
            else:
                cards.append(c)
        # TODO - let victim pick order
        for c in cards:
            victim.output("Putting %s back on deck" % c.cardname)
            attacker.output("%s keeping %s" % (victim.name, c.cardname))
            victim.addCard(c, 'deck')

    def special(self, game, player):
        """ Each other player reveals the top 3 cards of his deck,
            discard the revealed Actions and Treasures, and puts the
            rest back on top in any order he chooses """
        for plr in game.players:
            if plr.hasDefense(player):
                continue
            if plr == player:
                continue
            self.attack(plr, player)


###############################################################################
class Test_Rabble(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['rabble', 'moat'])
        self.attacker = self.g.players[0]
        self.victim = self.g.players[1]
        self.rabble = self.g['rabble'].remove()
        self.moat = self.g['moat'].remove()
        self.attacker.addCard(self.rabble, 'hand')

    def test_defended(self):
        self.victim.addCard(self.moat, 'hand')
        self.attacker.playCard(self.rabble)
        self.assertEqual(len(self.victim.hand), 6)  # 5 + moat
        self.assertEqual(len(self.attacker.hand), 5 + 3)
        self.assertEqual(self.victim.discardpile, [])

    def test_nodefense(self):
        self.victim.setDeck('copper', 'estate', 'rabble')
        self.attacker.playCard(self.rabble)
        self.assertEqual(self.victim.deck[-1].name, 'Estate')
        self.assertEqual(len(self.victim.discardpile), 2)
        self.assertEqual(len(self.attacker.hand), 5 + 3)


###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF
