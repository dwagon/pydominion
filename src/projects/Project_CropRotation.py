#!/usr/bin/env python

import unittest
from Project import Project


###############################################################################
class Project_CropRotation(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "At the start of your turn, you may discard a Victory card for +2 Cards."
        self.name = "Crop Rotation"
        self.cost = 6

    def hook_startTurn(self, game, player):
        vics = [_ for _ in player.hand if _.isVictory()]
        if vics:
            choices = [("Crop Rotation: Discard nothing", None)]
            for card in vics:
                choices.append(("Crop Rotation: Discard {} for +2 cards".format(card.name), card))
            ans = player.plrChooseOptions("Discard which victory card? ", *choices)
            if ans:
                player.discardCard(ans)
                player.pickupCards(2)
        else:
            player.output("Crop Rotation: No victory cards found")


###############################################################################
class Test_CropRotation(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Crop Rotation'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_play(self):
        self.plr.assign_project('Crop Rotation')
        self.plr.setHand('Estate', 'Province', 'Duchy', 'Copper', 'Copper')
        self.plr.test_input = ['Discard Duchy']
        self.plr.startTurn()
        self.assertEqual(self.plr.handSize(), 5 - 1 + 2)
        self.assertIsNotNone(self.plr.inDiscard('Duchy'))

    def test_discard_nothing(self):
        self.plr.assign_project('Crop Rotation')
        self.plr.setHand('Estate', 'Province', 'Duchy', 'Copper', 'Copper')
        self.plr.test_input = ['Discard nothing']
        self.plr.startTurn()
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.discardSize(), 0)

    def test_no_victory(self):
        self.plr.assign_project('Crop Rotation')
        self.plr.setHand('Silver', 'Silver', 'Silver', 'Copper', 'Copper')
        self.plr.startTurn()
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.discardSize(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
