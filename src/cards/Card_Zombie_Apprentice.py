#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Zombie_Apprentice(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'zombie']
        self.base = 'nocturne'
        self.desc = "You may trash an Action card from your hand for +3 Cards and +1 Action."
        self.name = 'Zombie Apprentice'
        self.cost = 3
        self.insupply = False
        self.purchasable = False
        self.numcards = 1

    def setup(self, game):
        game.trashpile.add(self)

    def special(self, game, player):
        actions = [_ for _ in player.hand if _.isAction()]
        if not actions:
            player.output("No actions to trash")
            return
        tr = player.plrTrashCard(prompt="Trash an action from your hand for +3 Cards and +1 Action", cardsrc=actions)
        if tr:
            player.pickupCards(3)
            player.addActions(1)


###############################################################################
class Test_Zombie_Apprentice(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Zombie Apprentice', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Zombie Apprentice'].remove()

    def test_play_noactions(self):
        tsize = self.g.trashSize()
        self.plr.playCard(self.card, discard=False, costAction=False)
        self.assertIsNotNone(self.g.inTrash('Zombie Apprentice'))
        self.assertEqual(self.g.trashSize(), tsize)

    def test_play_action(self):
        self.plr.setHand('Moat')
        self.plr.test_input = ['Moat']
        self.plr.playCard(self.card, discard=False, costAction=False)
        self.assertEqual(self.plr.handSize(), 3)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertIsNotNone(self.g.inTrash('Zombie Apprentice'))
        self.assertIsNotNone(self.g.inTrash('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF