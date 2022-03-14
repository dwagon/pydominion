#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Tormentor(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_DOOM]
        self.base = Game.NOCTURNE
        self.desc = """+2 Coin; If you have no other cards in play, gain an Imp
            from its pile. Otherwise, each other player receives the next Hex."""
        self.name = "Tormentor"
        self.required_cards = [("Card", "Imp")]
        self.coin = 2
        self.cost = 5

    def special(self, game, player):
        if player.played.size() == 1:  # Include this card
            player.gainCard("Imp")
            player.output("Gained an Imp")
        else:
            for pl in player.attackVictims():
                player.output("Hexed {}".format(pl.name))
                pl.output("Received a hex from {}'s Tormentor".format(player.name))
                pl.receive_hex()


###############################################################################
class Test_Tormentor(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Tormentor"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Tormentor"].remove()
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play_imp(self):
        """Play tormentor with no other cards being played"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertIsNotNone(self.plr.in_discard("Imp"))

    def test_play_hex(self):
        """Play tormentor with other cards already being played"""
        self.plr.set_played("Tormentor")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertIsNone(self.plr.in_discard("Imp"))
        self.assertTrue(self.vic.has_state("Deluded"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
