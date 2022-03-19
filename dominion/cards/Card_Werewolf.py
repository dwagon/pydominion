#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Werewolf(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.TYPE_ACTION,
            Card.TYPE_ATTACK,
            Card.TYPE_NIGHT,
            Card.TYPE_DOOM,
        ]
        self.base = Game.NOCTURNE
        self.desc = "If it's your Night phase, each other player receives the next Hex.  Otherwise, +3 Cards."
        self.name = "Werewolf"
        self.cost = 5

    def special(self, game, player):
        for _ in range(3):
            player.pickup_card()

    def night(self, game, player):
        for plr in player.attack_victims():
            plr.output("{}'s werewolf hexed you".format(player.name))
            plr.receive_hex()


###############################################################################
class Test_Werewolf(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Werewolf"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Werewolf"].remove()
        self.plr.add_card(self.card, "hand")
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play_day(self):
        """Play a Werewolf during the day"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 3)
        self.assertFalse(self.vic.has_state("Deluded"))

    def test_play_night(self):
        self.plr.phase = Card.TYPE_NIGHT
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertTrue(self.vic.has_state("Deluded"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
