#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Fortuneteller(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = [Card.ACTION, Card.ATTACK]
        self.base = Game.CORNUCOPIA
        self.desc = """2 Coin. Each other player reveals cards from the top of his deck
        until he reveals a Victory or Curse card. He puts it on top and discards the other revealed cards."""
        self.name = 'Fortune Teller'
        self.coin = 2
        self.cost = 3

    def special(self, game, player):
        for plr in player.attackVictims():
            while True:
                card = plr.nextCard()
                plr.revealCard(card)
                if not card:
                    break
                if card.isVictory() or card.name == 'Curse':
                    plr.addCard(card, 'topdeck')
                    plr.output("%s's Fortune Teller put %s on top of your deck" % (player.name, card.name))
                    break
                plr.output("%s's Fortune Teller discarded your %s" % (player.name, card.name))
                plr.discardCard(card)


###############################################################################
class Test_Fortuneteller(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Fortune Teller'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g['Fortune Teller'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Fortune Teller """
        self.vic.setDeck('Duchy', 'Silver', 'Copper')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertIsNotNone(self.vic.in_discard('Silver'))
        self.assertIsNotNone(self.vic.in_discard('Copper'))
        self.assertEqual(self.vic.deck[-1].name, 'Duchy')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
