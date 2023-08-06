#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Tent(Card.Card):
    """Tent"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.FORT,
        ]  # pylint: disable=no-member
        self.base = Card.CardExpansion.ALLIES
        self.cost = 3
        self.coin = 2
        self.name = "Tent"
        self.desc = """+$2; You may rotate the Forts.
            When you discard this from play, you may put it onto your deck."""

    def special(self, game, player):
        opt = player.plr_choose_options(
            "Do you want to rotate the Forts?",
            ("Don't change", False),
            ("Rotate", True),
        )
        if opt:
            game["Forts"].rotate()

    def hook_discard_this_card(self, game, player, source):
        opt = player.plr_choose_options(
            "How to discard the Tent?",
            ("Discard as normal", False),
            ("Put it on to deck", True),
        )
        if opt:
            player.move_card(self, "topdeck")


###############################################################################
class Test_Tent(unittest.TestCase):
    """Test Tent"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Forts"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        while True:
            self.card = self.g["Forts"].remove()
            if self.card.name == "Tent":
                break
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a tent - don't rotate"""
        self.plr.test_input = ["Discard as normal"]
        self.plr.discard_card(self.card)
        self.assertIn("Tent", self.plr.discardpile)

    def test_play_rotate(self):
        """Play a tent - rotate"""
        self.plr.test_input = ["Rotate"]
        self.plr.play_card(self.card)
        card = self.g["Forts"].remove()
        self.assertEqual(card.name, "Garrison")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
