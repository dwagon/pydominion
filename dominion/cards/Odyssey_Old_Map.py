#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Old_Map"""

import unittest
from dominion import Game, Card


###############################################################################
class Card_Old_Map(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.TYPE_ACTION,
            Card.TYPE_ODYSSEY,  # pylint: disable=no-member
        ]
        self.base = Game.ALLIES
        self.cost = 3
        self.name = "Old Map"
        self.cards = 1
        self.actions = 1
        self.desc = """+1 Card; +1 Action; Discard a card. +1 Card. You may rotate the Odysseys."""

    def special(self, game, player):
        player.plr_discard_cards(num=1)
        player.pickup_card()
        opt = player.plr_choose_options(
            "Do you want to rotate the Odysseys?",
            ("Don't change", False),
            ("Rotate", True),
        )
        if opt:
            game["Odysseys"].rotate()


###############################################################################
class Test_Old_Map(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Odysseys"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

        while True:
            card = self.g["Odysseys"].remove()
            if card.name == "Old Map":
                break
        self.card = card

    def test_play(self):
        """Play the card"""
        self.plr.deck.set("Estate", "Duchy", "Province")
        self.plr.hand.set("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Discard Copper", "Rotate"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.plr.discardpile)
        self.assertNotIn("Copper", self.plr.hand)
        self.assertIn("Province", self.plr.hand)
        self.assertEqual(self.g["Odysseys"].top_card(), "Voyage")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
