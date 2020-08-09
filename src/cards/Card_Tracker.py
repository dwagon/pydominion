#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Tracker(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_FATE]
        self.base = Game.NOCTURNE
        self.desc = "+1 Coin, Receive a boon; While this is in play, when you gain a card, you may put that card onto your deck"
        self.name = 'Tracker'
        self.cost = 2
        self.coin = 1
        self.heirloom = 'Pouch'

    def special(self, game, player):
        # Special flag to stop boon interfering with tests
        if not hasattr(player, '_tracker_dont_boon'):
            player.receive_boon()

    def hook_gain_card(self, game, player, card):
        """ While this is in play, when you gain a card, you may
            put that card on top of your deck"""
        mod = {}
        deck = player.plrChooseOptions(
            "Where to put %s?" % card.name,
            ("Put %s on discard" % card.name, False),
            ("Put %s on top of deck" % card.name, True))
        if deck:
            player.output("Putting %s on deck due to Tracker" % card.name)
            mod['destination'] = 'topdeck'
        return mod


###############################################################################
class Test_Tracker(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Tracker'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.plr._tracker_dont_boon = True
        self.card = self.g['Tracker'].remove()

    def test_play(self):
        """ Play a Tracker """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.plr.getCoin(), 1)
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise

    def test_discard(self):
        """ Have a Tracker  - discard the gained card"""
        self.plr.setPlayed('Tracker')
        self.plr.test_input = ['discard']
        self.plr.gainCard('Gold')
        self.assertEqual(self.plr.discard_size(), 1)
        self.assertEqual(self.plr.discardpile[0].name, 'Gold')
        self.assertFalse(self.plr.in_hand('Gold'))

    def test_deck(self):
        """ Have a Tracker  - the gained card on the deck"""
        self.plr.setPlayed('Tracker')
        self.plr.test_input = ['deck']
        self.plr.gainCard('Gold')
        self.assertEqual(self.plr.deck[-1].name, 'Gold')
        self.assertIsNone(self.plr.in_hand('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
