#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


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
        player.gainCard("Rats")
        player.plrTrashCard(force=True, exclude=["Rats"])

    def hook_trashThisCard(self, game, player):
        """When you trash this +1 Card"""
        player.pickupCard(verb="Due to trashing Rats picked up")


###############################################################################
class Test_Rats(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Rats"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.rats = self.g["Rats"].remove()
        self.plr.setDeck("Estate", "Province", "Duchy")
        self.plr.setHand("Copper", "Gold", "Silver", "Rats")
        self.plr.addCard(self.rats, "hand")

    def test_play(self):
        self.plr.setDeck("Gold")
        self.plr.test_input = ["trash copper"]
        self.plr.playCard(self.rats)
        self.plr.addActions(1)
        self.assertEqual(self.plr.hand[-1].name, "Gold")

    def test_trashcard(self):
        tsize = self.g.trashSize()
        self.plr.test_input = ["trash copper"]
        self.plr.playCard(self.rats)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertNotEqual(self.g.trashpile[0].name, "Rats")

    def test_gainrats(self):
        self.plr.test_input = ["trash copper"]
        self.plr.playCard(self.rats)
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
