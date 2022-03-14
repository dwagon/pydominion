#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


class Card_Marauder(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_LOOTER]
        self.base = Game.DARKAGES
        self.desc = (
            "Gain a Spoils from the Spoils pile. Each other player gains a Ruins."
        )
        self.name = "Marauder"
        self.cost = 4
        self.required_cards = ["Spoils"]

    def special(self, game, player):
        for plr in player.attackVictims():
            plr.output("Gained a ruin from %s's Marauder" % player.name)
            plr.gain_card("Ruins")
        player.gain_card("Spoils")


###############################################################################
class Test_Marauder(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=["Marauder"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Marauder"].remove()

    def test_play(self):
        """Play a marauder"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_discard("Spoils"))
        self.assertTrue(self.victim.discardpile[0].isRuin())


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
