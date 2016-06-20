#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Mandarin(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'hinterlands'
        self.desc = """+3 Coins.  Put a card from your hand on top of your deck.
        When you gain this, put all Treasures you have in play on top of your deck in any order."""
        self.name = 'Mandarin'
        self.coin = 3
        self.cost = 5

    def special(self, game, player):
        card = player.cardSel(force=True, cardsrc='hand', prompt="Put a card from your on top of your deck")
        player.addCard(card[0], 'topdeck')
        player.hand.remove(card[0])

    def hook_gainThisCard(self, game, player):
        for card in player.played[:]:
            if card.isTreasure():
                player.output("Putting %s on to deck" % card.name)
                player.addCard(card, 'topdeck')
                player.played.remove(card)
        return {}


###############################################################################
class Test_Mandarin(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Mandarin'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Mandarin'].remove()

    def test_play(self):
        """ Play the card """
        self.plr.setHand('Gold', 'Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 3)
        self.assertEqual(self.plr.deck[-1].name, 'Gold')

    def test_gain(self):
        """ Gain the card """
        self.plr.setPlayed('Gold', 'Duchy')
        self.plr.gainCard('Mandarin')
        self.assertEqual(self.plr.deck[-1].name, 'Gold')
        self.assertIsNotNone(self.plr.inPlayed('Duchy'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
