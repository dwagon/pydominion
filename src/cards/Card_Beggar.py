#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Beggar(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reaction']
        self.base = 'darkages'
        self.desc = """Gain 3 Coppers, putting them into your hand.
        When another player plays an Attack card, you may discard this.
        If you do, gain two Silvers, putting one on top of your deck."""
        self.name = 'Beggar'
        self.cost = 2

    def special(self, game, player):
        for i in range(3):
            player.gainCard('Copper', 'hand')

    def hook_underAttack(self, player, game):
        player.output("Gaining silvers as under attack")
        player.gainCard('Silver', 'topdeck')
        player.gainCard('Silver')


###############################################################################
class Test_Beggar(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Beggar', 'Militia'])
        self.g.startGame()
        self.plr, self.attacker = self.g.playerList()
        self.card = self.g['Beggar'].remove()

    def test_play(self):
        """ Play a beggar """
        self.plr.setHand()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 3)
        self.assertIsNotNone(self.plr.inHand('Copper'))

    def test_attack(self):
        """ React to an attack as a beggar """
        self.plr.setHand('Beggar', 'Estate', 'Duchy', 'Province', 'Gold')
        self.plr.test_input = ['Estate', 'Duchy', 'Finish']
        militia = self.g['Militia'].remove()
        self.attacker.addCard(militia, 'hand')
        self.attacker.playCard(militia)
        self.assertEqual(self.plr.deck[-1].name, 'Silver')
        self.assertIsNotNone(self.plr.inDiscard('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF