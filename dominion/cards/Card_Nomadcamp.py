#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_NomadCamp(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.name = "Nomad Camp"
        self.buys = 1
        self.cards = 2
        self.cost = 4

    def desc(self, player):
        if player.phase == "action":
            return "+1 Buy +2 Coins"
        return "+1 Buy +2 Coins; When you gain this, put it on top of your deck."

    def hook_gain_this_card(self, game, player):
        return {"destination": "topdeck"}


###############################################################################
class Test_NomadCamp(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Nomad Camp"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Nomad Camp"].remove()

    def test_play(self):
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 7)
        self.assertEqual(self.plr.get_buys(), 2)

    def test_gain(self):
        self.plr.gain_card("Nomad Camp")
        self.assertEqual(self.plr.deck[-1].name, "Nomad Camp")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
