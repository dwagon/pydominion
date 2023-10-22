#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Sheepdog """

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Sheepdog(Card.Card):
    """Sheepdog"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+2 Cards; When you gain a card, you may play this from your hand."
        self.name = "Sheepdog"
        self.cards = 2
        self.cost = 3

    def hook_gain_card(self, game, player, card):
        if self in player.piles[Piles.HAND]:
            player.play_card(self, cost_action=False)


###############################################################################
class TestSheepdog(unittest.TestCase):
    """Test Sheepdog"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sheepdog"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Sheepdog")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self):
        """Play card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)

    def test_gain(self):
        """Gain a card"""
        self.plr.gain_card("Estate")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertIn("Sheepdog", self.plr.piles[Piles.PLAYED])

    def test_gain_twice(self):
        """Gain a card twice"""
        self.plr.gain_card("Estate")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.plr.gain_card("Estate")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
