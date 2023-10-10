#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/King%27s_Cache"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_KingCache(Card.Card):
    """King's Cache"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "You may play a Treasure from your hand 3 times."
        self.name = "King's Cache"
        self.cost = 7

    def special(self, game, player):
        treasures = [_ for _ in player.piles[Piles.HAND] if _.isTreasure()]
        if not treasures:
            return
        options = [("Do Nothing", None)]
        for treasure in treasures:
            options.append((f"Play {treasure}?", treasure))
        to_play = player.plr_choose_options("Play a treasure three times", *options)
        if to_play:
            for i in range(3):
                player.play_card(to_play, cost_action=False, discard=False)


###############################################################################
class TestKingCache(unittest.TestCase):
    """Test King's Cache"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["King's Cache"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("King's Cache")

    def test_play(self):
        """Play a card"""
        self.plr.piles[Piles.HAND].set("Copper", "Gold", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.test_input = ["Play Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 3 * 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
