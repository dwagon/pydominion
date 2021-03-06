#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Leprechaun(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DOOM]
        self.base = Game.NOCTURNE
        self.desc = "Gain a Gold. If you have exactly 7 cards in play, gain a Wish from its pile. Otherwise, receive a Hex."
        self.name = 'Leprechaun'
        self.required_cards = [('Card', 'Wish')]
        self.cost = 5

    def special(self, game, player):
        player.output("Gained a gold")
        player.gainCard('Gold')
        if player.played.size() + player.durationpile.size() == 7:
            player.gainCard('Wish')
        else:
            player.receive_hex()


###############################################################################
class Test_Leprechaun(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Leprechaun', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Leprechaun'].remove()
        self.plr.addCard(self.card, 'hand')
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play_with_not_seven(self):
        """ Play a Leprechaun with not 7 cards """
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard('Gold'))
        self.assertTrue(self.plr.has_state('Deluded'))

    def test_play_with_seven(self):
        """ Play a Leprechaun with 7 cards in play """
        self.plr.setPlayed('Moat', 'Moat', 'Moat', 'Moat', 'Moat', 'Moat')  # + Leprec
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard('Gold'))
        self.assertFalse(self.plr.has_state('Deluded'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
