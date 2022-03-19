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
        disc = player.plr_discard_cards(num=3, force=True)
        if disc:
            player.add_coins(3)

    def hook_gain_this_card(self, game, player):
        player.add_favors(2)

    def hook_trashThisCard(self, game, player):
        player.add_favors(2)


###############################################################################
class Test_Sycophant(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sycophant"], use_liaisons=True)
        print(f"{self.g.use_liaisons=}")
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Sycophant"].remove()

    def test_gain(self):
        """Gain the card"""
        favs = self.plr.get_favors()
        self.plr.gain_card("Sycophant")
        self.assertEqual(self.plr.get_favors(), favs + 2)

    def test_trash(self):
        """Test trashing the card"""
        self.plr.add_card(self.card, "hand")
        favs = self.plr.get_favors()
        self.plr.trash_card(self.card)
        self.assertEqual(self.plr.get_favors(), favs + 2)

    def test_play(self):
        """Play the card"""
        favs = self.plr.get_favors()
        coin = self.plr.get_coins()
        self.plr.set_hand("Estate", "Duchy", "Province", "Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = [
            "Discard Estate",
            "Discard Duchy",
            "Discard Province",
            "Finish",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_favors(), favs)
        self.assertEqual(self.plr.get_coins(), coin + 3)
        self.assertIsNone(self.plr.in_hand("Province"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
