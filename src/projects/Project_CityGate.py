#!/usr/bin/env python

import unittest
from Project import Project


###############################################################################
class Project_CityGate(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "At the start of your turn, +1 Card, then put a card from your hand onto your deck."
        self.name = "City Gate"
        self.cost = 3

    def hook_startTurn(self, game, player):
        player.pickupCard()
        card = player.cardSel(force=True, cardsrc='hand', prompt='Put a card from your hand onto your deck')
        player.addCard(card[0], 'topdeck')
        player.hand.remove(card[0])


###############################################################################
class Test_CityGate(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['City Gate'])
        self.g.start_game()
        self.plr = self.g.playerList(0)

    def test_play(self):
        self.plr.assign_project('City Gate')
        self.plr.setDeck('Gold')
        self.plr.setHand('Copper', 'Estate', 'Province', 'Silver', 'Duchy')
        self.plr.test_input = ['Select Province']
        self.plr.startTurn()
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.deck[-1].name, 'Province')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
