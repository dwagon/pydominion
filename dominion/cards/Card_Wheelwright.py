#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Wheelwright """

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Wheelwright(Card.Card):
    """Wheelwright"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
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
        player.plr_gain_card(cost=disc[0].cost, types={Card.CardType.ACTION: True})


###############################################################################
class Test_Wheelwright(unittest.TestCase):
    """Test Wheelwright"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Wheelwright", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Wheelwright")

    def test_play(self):
        """Play the Wheelwright"""
        self.plr.piles[Piles.DECK].set("Estate", "Duchy")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Discard Silver", "Get Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
