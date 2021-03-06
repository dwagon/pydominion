#!/usr/bin/env python

import unittest
import Card
import Game
from Boon import Boon


###############################################################################
class Boon_Swamps_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = Card.TYPE_BOON
        self.base = Game.NOCTURNE
        self.desc = "Gain a Will-o'-Wisp from its pile."
        self.name = "The Swamp's Gift"
        self.purchasable = False
        self.required_cards = [('Card', "Will-o'-Wisp")]

    def special(self, game, player):
        player.gainCard("Will-o'-Wisp")


###############################################################################
class Test_Swamps_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'], badcards=['Druid'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The Swamp's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g['Bard'].remove()

    def test_winds_gift(self):
        self.plr.addCard(self.card, 'hand')
        self.g.print_state()
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard("Will-o'-Wisp"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
