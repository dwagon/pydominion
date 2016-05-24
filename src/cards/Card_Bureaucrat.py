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
        player.gainCard('Silver', 'topdeck')
        player.output("Added silver to deck")

        for pl in player.attackVictims():
            for c in pl.hand:
                if c.isVictory():
                    pl.addCard(c, 'topdeck')
                    pl.hand.remove(c)
                    pl.output("Moved %s to deck due to Bureaucrat played by %s" % (c.name, player.name))
                    player.output("Player %s moved a %s to the top" % (pl.name, c.name))
                    break
            else:
                player.output("Player %s has no victory cards in hand" % pl.name)


###############################################################################
class Test_Bureaucrat(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Bureaucrat', 'Moat'])
        self.g.startGame()
        self.plr, self.victim = self.g.playerList()
        self.bcard = self.g['Bureaucrat'].remove()
        self.plr.addCard(self.bcard, 'hand')

    def test_hasvictory(self):
        self.victim.setHand('Estate', 'Copper', 'Copper')
        self.victim.setDeck('Silver')
        self.plr.playCard(self.bcard)
        self.assertEquals(self.victim.deck[-1].name, 'Estate')
        self.assertIsNone(self.victim.inHand('Estate'))
        self.assertEquals(self.plr.deck[-1].name, 'Silver')

    def test_novictory(self):
        self.victim.setHand('Copper', 'Copper', 'Copper')
        self.victim.setDeck('Province')
        self.plr.setDeck('Province')
        self.plr.playCard(self.bcard)
        self.assertEquals(self.victim.deck[-1].name, 'Province')
        self.assertEquals(self.plr.deck[-1].name, 'Silver')

    def test_defense(self):
        self.victim.setDeck('Province')
        self.victim.setHand('Estate', 'Duchy', 'Moat')
        self.plr.playCard(self.bcard)
        self.assertEqual(self.plr.deck[-1].name, 'Silver')
        self.assertEquals(self.victim.deck[-1].name, 'Province')
        self.assertIsNotNone(self.victim.inHand('Estate'))

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
