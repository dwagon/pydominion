#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Astrolabe"""

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Astrolabe(Card.Card):
    """Astrolabe"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.DURATION]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = "Now and at the start of your next turn: $1, +1 Buy"
        self.name = "Astrolabe"
        self.buys = 1
        self.coin = 1
        self.cost = 3

    def duration(self, game, player):
        """+1 coin, +1 buy"""
        player.coins.add(1)
        player.buys.add(1)


###############################################################################
class Test_Astrolabe(unittest.TestCase):
    """Test Astrolabe"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Astrolabe"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Astrolabe"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self):
        """Play an astrolabe"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 0)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 1)
        self.assertEqual(self.plr.piles[Piles.PLAYED][-1].name, "Astrolabe")
        self.assertEqual(self.plr.buys.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
