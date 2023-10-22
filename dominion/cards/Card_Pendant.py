#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Pendant"""
import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Pendant(Card.Card):
    """Pendant"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+$1 per differently named Treasure you have in play."""
        self.name = "Pendant"
        self.cost = 5

    def special(self, game, player):
        treasures = set([_.name for _ in player.piles[Piles.PLAYED] if _.isTreasure()])
        player.coins += len(treasures)
        player.output(f"Gaining {len(treasures)} coins from Pendant")


###############################################################################
class Test_Pendant(unittest.TestCase):
    """Test Pendant"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Pendant"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Pendant")

    def test_play(self):
        """Play a pendant"""
        coins = self.plr.coins.get()
        self.plr.piles[Piles.PLAYED].set("Copper", "Copper", "Silver", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
