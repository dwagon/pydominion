#!/usr/bin/env python

import unittest
from Card import Card


class Card_Bureaucrat(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'dominion'
        self.desc = "Gain a silver"
        self.name = 'Bureaucrat'
        self.cost = 4

    def special(self, game, player):
        """ Gain a silver card and put it on top of your deck. Each
        other player reveals a victory card from his hand and puts
        it on his deck (or reveals a hand with no victory cards)
        """
        player.gainCard('silver', 'topdeck')
        player.output("Added silver to deck")

        for pl in player.attackVictims():
            for c in pl.hand:
                if c.isVictory():
                    pl.addCard(c, 'topdeck')
                    pl.output("Moved %s to deck due to Bureaucrat played by %s" % (c.name, player.name))
                    player.output("Player %s moved a %s to the top" % (pl.name, c.name))
                    break
            player.output("Player %s has no victory cards in hand" % pl.name)


###############################################################################
class Test_Bureaucrat(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['bureaucrat', 'moat'])
        self.plr = self.g.players.values()[0]
        self.victim = self.g.players.values()[1]
        self.bcard = self.g['bureaucrat'].remove()
        self.plr.addCard(self.bcard, 'hand')

    def test_hasvictory(self):
        self.victim.setHand('estate', 'copper', 'copper')
        self.victim.setDeck('silver')
        self.plr.playCard(self.bcard)
        self.assertEquals(self.victim.deck[-1].name, 'Estate')
        self.assertEquals(self.plr.deck[-1].name, 'Silver')

    def test_novictory(self):
        self.victim.setHand('copper', 'copper', 'copper')
        self.victim.setDeck('province')
        self.plr.setDeck('province')
        self.plr.playCard(self.bcard)
        self.assertEquals(self.victim.deck[-1].name, 'Province')
        self.assertEquals(self.plr.deck[-1].name, 'Silver')

    def test_defense(self):
        self.victim.setHand('estate', 'duchy', 'moat')
        self.victim.setDeck('province')
        self.plr.setDeck('province')
        self.plr.playCard(self.bcard)
        self.assertEquals(self.victim.deck[-1].name, 'Province')
        self.assertEquals(self.plr.deck[-1].name, 'Silver')

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
