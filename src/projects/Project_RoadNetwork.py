#!/usr/bin/env python

import unittest
from Project import Project


###############################################################################
class Project_RoadNetwork(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "When another player gains a Victory card, +1 Card."
        self.name = "Road Network"
        self.cost = 5

    def hook_allPlayers_gainCard(self, game, player, owner, card):
        if card.isVictory() and owner != player:
            owner.pickupCards(1)
            owner.output("Road Network gives card due to {} picking up {}".format(player.name, card.name))


###############################################################################
class Test_RoadNetwork(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initprojects=['Road Network'], badcards=["Duchess"])
        self.g.startGame()
        self.plr, self.other = self.g.playerList()

    def test_victory(self):
        self.plr.assign_project('Road Network')
        self.plr.setDeck('Gold')
        self.other.gainCard('Duchy')
        self.assertEqual(self.plr.handSize(), 5 + 1)
        self.assertIsNotNone(self.plr.inHand('Gold'))

    def test_not_victory(self):
        self.plr.assign_project('Road Network')
        self.plr.setDeck('Gold')
        self.other.gainCard('Copper')
        self.assertEqual(self.plr.handSize(), 5)
        self.assertIsNone(self.plr.inHand('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
