#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Silver_Mine"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_SilverMine(Card.Card):
    """Silver Mine"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "Gain a Treasure costing less than this to your hand."
        self.name = "Silver Mine"
        self.cost = 5

    def special(self, game, player):
        cost = player.card_cost(self)
        player.plr_gain_card(cost, destination=Piles.HAND)


###############################################################################
class Test_SilverMine(unittest.TestCase):
    """Test Silver Mine"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Silver Mine", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Silver Mine")

    def test_gaincard(self):
        """Gain a card"""
        self.plr.piles[Piles.HAND].set("Copper", "Gold", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Get Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
