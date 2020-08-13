#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Ghost_Town(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_NIGHT, Card.TYPE_DURATION]
        self.base = Game.NOCTURNE
        self.name = 'Ghost Town'
        self.cost = 3

    def desc(self, player):
        if player.phase == 'buy':
            return """At the start of your next turn, +1 Card and +1 Action. This
                is gained to your hand (instead of your discard pile)."""
        return "At the start of your next turn, +1 Card and +1 Action."

    def hook_gain_this_card(self, game, player):
        return {'destination': 'hand'}

    def duration(self, game, player):
        player.pickupCard()
        player.addActions(1)


###############################################################################
class Test_Ghost_Town(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Ghost Town'])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.gtown = self.g['Ghost Town'].remove()

    def test_play_card(self):
        """ Play Ghost Town """
        self.plr.addCard(self.gtown, 'hand')
        self.plr.playCard(self.gtown)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertEqual(self.plr.get_actions(), 2)

    def test_gain(self):
        self.plr.gainCard('Ghost Town')
        self.assertIsNone(self.plr.in_discard('Ghost Town'))
        self.assertIsNotNone(self.plr.in_hand('Ghost Town'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
