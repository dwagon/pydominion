#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Trader(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reaction']
        self.base = 'hinterlands'
        self.desc = """Trash a card from your hand. Gain a number of Silvers equal to its cost in coins.
        When you would gain a card, you may reveal this from your hand. If you do, instead, gain a Silver."""
        self.name = 'Trader'
        self.cost = 4

    def special(self, game, player):
        card = player.plrTrashCard(prompt="Trash a card from your hand. Gain a number of Silvers equal to its cost in coins.")
        if card:
            player.output("Gaining %d Silvers" % card[0].cost)
            for i in range(card[0].cost):
                player.gainCard('Silver')

    def hook_gainCard(self, game, player, card):
        if card.name == 'Silver':
            return {}
        silver = player.plrChooseOptions(
            "From your Trader gain %s or gain a Silver instead?" % card.name,
            ("Still gain %s" % card.name, False),
            ("Instead gain Silver", True))
        if silver:
            return {'replace': 'Silver', 'destination': 'discard'}
        return {}


###############################################################################
class Test_Trader(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Trader'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Trader'].remove()

    def test_play(self):
        """ Play a trader - trashing an estate """
        tsize = self.g.trashSize()
        self.plr.setHand('Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['estate', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardSize(), 2)
        for i in self.plr.discardpile:
            self.assertEqual(i.name, 'Silver')
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.inTrash('Estate'))

    def test_gain(self):
        self.plr.test_input = ['Instead']
        self.plr.addCard(self.card, 'hand')
        self.plr.buyCard(self.g['Gold'])
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertIsNone(self.plr.inDiscard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
