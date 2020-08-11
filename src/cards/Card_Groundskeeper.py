#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Groundskeeper(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.EMPIRES
        self.desc = "+1 Card. +1 Action. While this is in play, when you gain a Victory card, +1VP"
        self.name = 'Groundskeeper'
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def hook_gain_card(self, game, player, card):
        if card.isVictory():
            player.addScore('Groundskeeper', 1)
            player.output("Scored 1 from Groundskeeper")
        return {}


###############################################################################
class Test_Groundskeeper(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Groundskeeper'], badcards=['Duchess'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Groundskeeper'].remove()

    def test_play(self):
        """ Play a Groundskeeper """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.plr.setCoin(5)
        self.plr.buyCard(self.g['Duchy'])
        self.assertEqual(self.plr.score['Groundskeeper'], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
