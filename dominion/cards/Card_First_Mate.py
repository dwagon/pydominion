#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/First_Mate"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_FirstMate(Card.Card):
    """First Mate"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Play any number of Action cards with the same name from your hand, 
        then draw until you have 6 cards in hand."""
        self.name = "First Mate"
        self.cost = 5

    def special(self, game, player):
        actions = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        options = [(f"Play {_.name}", _) for _ in actions]
        if actions:
            options.insert(0, ("Play nothing", None))
        to_play = player.plr_choose_options("Play which action?", *actions)
        if to_play:
            pass

        while len(player.piles[Piles.HAND]) < 6:
            player.pickup_card()


###############################################################################
class Test_FirstMate(unittest.TestCase):
    """Test First Mate"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["First Mate", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("First Mate")

    def test_gaincard(self):
        """Gain a card"""
        self.plr.piles[Piles.HAND].set("Copper", "Gold", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Discard Copper", "Get Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.plr.piles[Piles.DISCARD])
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Copper", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
