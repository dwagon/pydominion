#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Wheelwright """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Wheelwright(Card.Card):
    """Wheelwright"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.desc = """+1 Card; +1 Action; You may discard a card to gain an
            Action card costing as much as it or less."""
        self.name = "Wheelwright"
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        disc = player.plr_discard_cards(num=1)
        if not disc:
            return
        player.plr_gain_card(cost=disc[0].cost, types={Card.TYPE_ACTION: True})


###############################################################################
class Test_Wheelwright(unittest.TestCase):
    """Test Wheelwright"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Wheelwright", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Wheelwright"].remove()

    def test_play(self):
        """Play the Wheelwright"""
        self.plr.deck.set("Estate", "Duchy")
        self.plr.hand.set("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Discard Silver", "Get Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.discardpile)
        self.assertIn("Silver", self.plr.discardpile)
        self.assertEqual(self.plr.get_actions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
