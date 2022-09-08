#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Tide_Pools"""

import unittest
from dominion import Card, Game


###############################################################################
class Card_Tide_Pools(Card.Card):
    """Tide_Pools"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.SEASIDE
        self.desc = "+3 Cards; +1 Action; At the start of your next turn, discard 2 cards."
        self.name = "Tide Pools"
        self.cards = 3
        self.actions = 2
        self.cost = 4

    def duration(self, game, player):
        """Discard 2 carps"""
        player.plr_discard_cards(num=2)


###############################################################################
class Test_Tide_Pools(unittest.TestCase):
    """Test Tide_Pools"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Tide Pools"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Tide Pools"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a tide pools"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 3)
        self.assertEqual(self.plr.durationpile.size(), 1)
        self.plr.end_turn()
        self.plr.test_input = ["Discard Copper", "Discard Silver", "Finish"]
        self.plr.hand.set("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.plr.start_turn()
        self.assertEqual(self.plr.durationpile.size(), 0)
        self.assertEqual(self.plr.played[-1].name, "Tide Pools")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
