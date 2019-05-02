#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_RoyalBlacksmith(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'empires'
        self.desc = """+5 Cards. Reveal your hand; discard the Coppers."""
        self.name = 'Royal Blacksmith'
        self.debtcost = 8
        self.cards = 5

    def special(self, game, player):
        count = 0
        for card in player.hand:
            player.revealCard(card)
            if card.name == 'Copper':
                player.discardCard(card)
                count += 1
        player.output("Discarding %d coppers" % count)


###############################################################################
class Test_RoyalBlacksmith(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Royal Blacksmith'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Royal Blacksmith'].remove()

    def test_play(self):
        """ Play an Royal Blacksmith"""
        self.plr.setDeck('Silver', 'Province', 'Estate', 'Copper', 'Gold', 'Silver')
        self.plr.setHand('Copper', 'Silver', 'Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 3 - 2 + 5)
        self.assertIsNotNone(self.plr.inDiscard('Copper'))
        self.assertIsNone(self.plr.inHand('Copper'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
