#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_SecretCave(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.NOCTURNE
        self.desc = "+1 Card; +1 Action; You may discard 3 cards. If you did, then at the start of your next turn, +3 Coin"
        self.name = 'Secret Cave'
        self.cost = 3
        self.actions = 1
        self.cards = 1
        self.heirloom = 'Magic Lamp'
        self._discarded = False

    def special(self, game, player):
        dcs = player.plrDiscardCards(num=3, prompt="If you discard 3 cards next turn gain 3 Coin")
        if dcs:
            self._discarded = True

    def duration(self, game, player):
        if self._discarded:
            player.output("Gained 3 Coin from Secret Cave")
            player.addCoin(3)


###############################################################################
class Test_SecretCave(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Secret Cave'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Secret Cave'].remove()

    def test_play_keep(self):
        """ Play a Secret Cave """
        self.plr.setHand('Silver', 'Estate', 'Duchy', 'Province', 'Copper')
        self.plr.test_input = ['Discard Silver', 'Discard Duchy', 'Discard Province', 'Finish']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.plr.get_actions(), 1)
            self.assertEqual(self.plr.discardpile.size(), 3)
            self.assertEqual(self.plr.hand.size(), 5 + 1 - 3)
            self.plr.end_turn()
            self.plr.start_turn()
            self.assertEqual(self.plr.getCoin(), 3)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
