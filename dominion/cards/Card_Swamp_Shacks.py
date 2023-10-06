#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Wealthy_Village """
import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_SwampShacks(Card.Card):
    """Swamp Shacks"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+2 Actions; +1 Card per 3 cards you have in play (round down)."""
        self.name = "Swamp Shacks"
        self.cost = 4
        self.actions = 2

    def special(self, game, player):
        """+1 Card per 3 cards you have in play (round down)."""
        in_play = sum([1 for _ in player.piles[Piles.PLAYED]]) + sum(
            [1 for _ in player.piles[Piles.DURATION]]
        )
        num_cards = int(in_play / 3)
        player.pickup_cards(num=num_cards)


###############################################################################
class TestSwampShacks(unittest.TestCase):
    """Test Swamp Shacks"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Swamp Shacks"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Swamp Shacks")

    def test_gain_action(self):
        """Play a Swamp Shacks"""
        self.plr.piles[Piles.PLAYED].set("Copper", "Duchy", "Estate", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        actions = self.plr.actions.get()
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertEqual(
            self.plr.actions.get(), actions + 2 - 1
        )  # One action to play card
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
