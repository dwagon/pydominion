#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Pilgrim"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Pilgrim(Card.Card):
    """Pilgrim"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+4 Cards; Put a card from your hand onto your deck."
        self.cards = 4
        self.name = "Pilgrim"
        self.cost = 5

    def special(self, game, player):
        """Put a card from your hand onto your deck."""
        card = player.card_sel(
            prompt="Put a card from your hand onto your deck.", cardsrc="hand"
        )
        if card:
            player.move_card(card[0], Piles.DECK)


###############################################################################
class Test_Pilgrim(unittest.TestCase):
    """Test Pilgrim"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Pilgrim"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Pilgrim")

    def test_play(self):
        """Play a card"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.plr.piles[Piles.HAND].set("Province")
        self.plr.add_card(self.card, Piles.HAND)
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.test_input = ["Province"]
        self.plr.play_card(self.card)
        self.assertEqual(
            len(self.plr.piles[Piles.HAND]), hand_size + 4 - 1 - 1
        )  # One for playing, one moved to deck
        self.assertIn("Province", self.plr.piles[Piles.DECK])
        self.assertNotIn("Province", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
