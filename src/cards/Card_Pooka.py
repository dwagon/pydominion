#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Pooka(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'nocturne'
        self.desc = "You may trash a Treasure other than Cursed Gold from your hand, for +4 Cards."
        self.name = 'Pooka'
        self.cost = 5
        self.heirloom = 'Cursed Gold'

    def special(self, game, player):
        treasures = [_ for _ in player.hand if _.isTreasure() and _.name != 'Cursed Gold']
        tr = player.plrTrashCard(prompt="Trash a treasure from your hand for +4 Cards", cardsrc=treasures)
        if tr:
            player.pickupCards(4)


###############################################################################
class Test_Pooka(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Pooka'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Pooka'].remove()

    def test_play(self):
        """ Play a Pooka """
        self.plr.setHand('Copper', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Copper']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertIsNotNone(self.g.inTrash('Copper'))
        self.assertIsNone(self.g.inTrash('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF