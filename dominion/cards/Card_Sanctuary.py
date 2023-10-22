#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sanctuary """

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Sanctuary(Card.Card):
    """Sanctuary"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """+1 Card; +1 Action; +1 Buy; You may Exile a card from your hand."""
        self.name = "Sanctuary"
        self.cost = 5
        self.cards = 1
        self.actions = 1
        self.buys = 1

    def special(self, game, player):
        crd = player.card_sel(prompt="Exile a card", verbs=("Exile", "Unexile"))
        if crd:
            player.exile_card(crd[0])


###############################################################################
class Test_Sanctuary(unittest.TestCase):
    """Test Sanctuary"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sanctuary"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Sanctuary")

    def test_playcard(self):
        """Play a card"""
        self.plr.piles[Piles.DECK].set("Estate", "Duchy", "Province")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Exile Copper"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertIn("Copper", self.plr.piles[Piles.EXILE])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
