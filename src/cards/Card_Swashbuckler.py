#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Swashbuckler(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'renaissance'
        self.desc = """+3 Cards. If your discard pile has any cards in it: +1 Coffers, then if you have at least 4 Coffers tokens, take the Treasure Chest."""
        self.name = 'Swashbuckler'
        self.needsartifacts = True
        self.cards = 3
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        if player.discardSize() >= 1:
            player.output("Gained a coffer")
            player.gainCoffer(1)
        if player.getCoffer() >= 4:
            player.output("Gained the Treasure Chest")
            player.assign_artifact('Treasure Chest')


###############################################################################
class Test_Swashbuckler(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Swashbuckler'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Swashbuckler'].remove()

    def test_play_no_discard(self):
        self.plr.setDiscard()
        card = self.g['Swashbuckler'].remove()
        self.plr.addCard(card, 'hand')
        self.plr.playCard(card)
        self.assertEqual(self.plr.getCoffer(), 0)

    def test_play_discard(self):
        self.plr.setDiscard('Copper')
        card = self.g['Swashbuckler'].remove()
        self.plr.addCard(card, 'hand')
        self.plr.playCard(card)
        self.assertEqual(self.plr.getCoffer(), 1)

    def test_play_coffers(self):
        self.plr.gainCoffer(3)
        self.plr.setDiscard('Copper')
        card = self.g['Swashbuckler'].remove()
        self.plr.addCard(card, 'hand')
        self.plr.playCard(card)
        self.assertIsNotNone(self.plr.has_artifact('Treasure Chest'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF