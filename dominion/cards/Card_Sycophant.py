#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Sycophant(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_LIAISON]
        self.base = Game.ALLIES
        self.name = "Sycophant"
        self.actions = 1
        self.desc = """+1 Action; Discard 3 cards. If you discarded at least one, +$3.
When you gain or trash this, +2 Favors."""
        self.cost = 2

    def special(self, game, player):
        disc = player.plrDiscardCards(num=3, force=True)
        if disc:
            player.addCoin(3)

    def hook_gain_this_card(self, game, player):
        player.addFavor(2)

    def hook_trashThisCard(self, game, player):
        player.addFavor(2)


###############################################################################
class Test_Sycophant(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Sycophant"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Sycophant"].remove()

    def test_gain(self):
        """Gain the card"""
        favs = self.plr.getFavor()
        self.plr.gainCard("Sycophant")
        self.assertEqual(self.plr.getFavor(), favs + 2)

    def test_trash(self):
        """Test trashing the card"""
        self.plr.addCard(self.card, "hand")
        favs = self.plr.getFavor()
        self.plr.trashCard(self.card)
        self.assertEqual(self.plr.getFavor(), favs + 2)

    def test_play(self):
        """Play the card"""
        favs = self.plr.getFavor()
        coin = self.plr.getCoin()
        self.plr.setHand("Estate", "Duchy", "Province", "Silver")
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = [
            "Discard Estate",
            "Discard Duchy",
            "Discard Province",
            "Finish",
        ]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getFavor(), favs)
        self.assertEqual(self.plr.getCoin(), coin + 3)
        self.assertIsNone(self.plr.in_hand("Province"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
