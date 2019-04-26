#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Experiment(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'renaissance'
        self.name = 'Experiment'
        self.desc = "+2 Cards; +1 Action; Return this to the Supply. When you gain this, gain another Experiment (that doesn't come with another)."
        self.cost = 3
        self.cards = 2
        self.actions = 1

    ###########################################################################
    def hook_gainThisCard(self, game, player):
        player.gainCard('Experiment', callhook=False)
        player.output("Gained a new experiment")

    ###########################################################################
    def special(self, game, player):
        player.played.remove(self)
        game[self.name].add()
        player.output("Returned experiment to stack")


###############################################################################
class Test_Experiment(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Experiment'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_playCard(self):
        self.card = self.g['Experiment'].remove()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 0 + 1)
        self.assertEqual(self.plr.handSize(), 5 + 2)

    def test_gainCard(self):
        self.plr.gainCard('Experiment')
        count = 0
        for card in self.plr.discardpile:
            if card.name == 'Experiment':
                count += 1
        self.assertEqual(count, 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF