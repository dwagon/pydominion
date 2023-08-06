#!/usr/bin/env python

import unittest
from dominion import Boon
from dominion import Card
from dominion import Game


###############################################################################
class Boon_Swamps_Gift(Boon.Boon):
    def __init__(self):
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Gain a Will-o'-Wisp from its pile."
        self.name = "The Swamp's Gift"
        self.purchasable = False
        self.required_cards = [("Card", "Will-o'-Wisp")]

    def special(self, game, player):
        player.gain_card("Will-o'-Wisp")


###############################################################################
class Test_Swamps_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The Swamp's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g["Bard"].remove()

    def test_winds_gift(self):
        self.plr.add_card(self.card, "hand")
        self.g.print_state()
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.discardpile["Will-o'-Wisp"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
