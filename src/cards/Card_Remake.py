#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_Remake(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'cornucopia'
        self.desc = "Do this twice: Trash a card from your hand, then gain a card costing exactly 1 more than the trashed card."
        self.name = 'Remake'
        self.cost = 4

    def special(self, game, player):
        for i in range(2):
            c = player.plrTrashCard(prompt="Trash a card and gain one costing 1 more")
            if c:
                player.plrGainCard(cost=c[0].cost+1, modifier='equal')


###############################################################################
class Test_Remake(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Remake', 'Moat'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.card = self.g['Remake'].remove()

    def test_playcard(self):
        """ Play a remake """
        self.plr.setHand('Copper', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Trash Estate', 'Get Silver', 'Trash Copper', 'Finish Selecting']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 0)
        self.assertIsNotNone(self.plr.inDiscard('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()


# EOF
