#!/usr/bin/env python

import unittest
import Card
import Game


###############################################################################
class Card_Cavalry(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.name = 'Cavalry'
        self.cost = 4
        self.required_cards = [('Card', 'Horse')]

    def desc(self, player):
        if player.phase == Card.TYPE_ACTION:
            return "Gain 2 Horses."
        return """Gain 2 Horses. When you gain this, +2 Cards, +1 Buy,
            and if it's your Buy phase return to your Action phase."""

    def special(self, game, player):
        player.gainCard('Horse')
        player.gainCard('Horse')

    def hook_gain_this_card(self, game, player):
        if player.phase == 'buy':
            player.phase = Card.TYPE_ACTION
        player.pickupCards(2)
        player.addBuys(1)


###############################################################################
class Test_Cavalry(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cavalry'], badcards=['Duchess'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Cavalry'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_buys(), 1)
        self.assertIsNotNone(self.plr.in_discard('Horse'))

    def test_gain(self):
        self.plr.phase = 'buy'
        self.plr.gainCard('Cavalry')
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_buys(), 1 + 1)
        self.assertEqual(self.plr.hand.size(), 5 + 2)
        self.assertEqual(self.plr.phase, Card.TYPE_ACTION)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
