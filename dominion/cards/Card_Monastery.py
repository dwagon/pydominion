#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Monastery(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_NIGHT
        self.base = Game.NOCTURNE
        self.desc = "For each card you've gained this turn, you may trash a card from your hand or a Copper you have in play."
        self.name = "Monastery"
        self.cost = 2

    def night(self, game, player):
        numgained = len(player.stats["gained"])
        if not numgained:
            return
        selectfrom = player.hand + [_ for _ in player.played if _.name == "Copper"]
        player.plr_trash_card(num=numgained, cardsrc=selectfrom)


###############################################################################
class Test_Monastery(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Monastery"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.monastery = self.g["Monastery"].remove()

    def test_play_card(self):
        """Play Monastery"""
        self.plr.phase = Card.TYPE_NIGHT
        self.plr.hand.set("Duchy")
        self.plr.add_card(self.monastery, "hand")
        self.plr.gain_card("Silver")
        self.plr.test_input = ["Duchy"]
        self.plr.play_card(self.monastery)
        self.assertIn("Duchy", self.g.trashpile)

    def test_play_no_gained(self):
        """Play Monastery when you didn't gain a card"""
        self.plr.phase = Card.TYPE_NIGHT
        self.plr.hand.set("Duchy")
        self.plr.add_card(self.monastery, "hand")
        self.plr.play_card(self.monastery)

    def test_play_copper(self):
        """Play Monastery when you have a copper"""
        self.plr.phase = Card.TYPE_NIGHT
        self.plr.hand.set("Duchy")
        self.plr.played.set("Copper")
        self.plr.add_card(self.monastery, "hand")
        self.plr.gain_card("Silver")
        self.plr.test_input = ["Copper"]
        self.plr.play_card(self.monastery)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
