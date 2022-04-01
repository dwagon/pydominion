#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Rats(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """+1 Card, +1 Action, Gain a Rats.
        Trash a card from your hand other than a Rats (or reveal a hand of all Rats).
        When you trash this, +1 Card."""
        self.name = "Rats"
        self.numcards = 20
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """Gain a Rats. Trash a card from your hand other than a Rats."""
        player.output("Gained a Rays")
        player.gain_card("Rats")
        player.plr_trash_card(force=True, exclude=["Rats"])

    def hook_trashThisCard(self, game, player):
        """When you trash this +1 Card"""
        player.pickup_card(verb="Due to trashing Rats picked up")


###############################################################################
class Test_Rats(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Rats"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.rats = self.g["Rats"].remove()
        self.plr.set_deck("Estate", "Province", "Duchy")
        self.plr.set_hand("Copper", "Gold", "Silver", "Rats")
        self.plr.add_card(self.rats, "hand")

    def test_play(self):
        self.plr.set_deck("Gold")
        self.plr.test_input = ["trash copper"]
        self.plr.play_card(self.rats)
        self.plr.add_actions(1)
        self.assertEqual(self.plr.hand[-1].name, "Gold")

    def test_trashcard(self):
        tsize = self.g.trash_size()
        self.plr.test_input = ["trash copper"]
        self.plr.play_card(self.rats)
        self.assertEqual(self.g.trash_size(), tsize + 1)
        self.assertNotEqual(self.g.trashpile[0].name, "Rats")

    def test_gainrats(self):
        self.plr.test_input = ["trash copper"]
        self.plr.play_card(self.rats)
        self.assertEqual(self.plr.discardpile[0].name, "Rats")

    def test_trashrats(self):
        """Trashing Rats - gain another card"""
        handsize = self.plr.hand.size()
        self.plr.trash_card(self.rats)
        # Lose rats, gain another card
        self.assertEqual(self.plr.hand.size(), handsize)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
