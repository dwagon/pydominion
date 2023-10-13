#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Pickaxe"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Pickaxe(Card.Card):
    """Pickaxe"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "$1; Trash a card from your hand. If it costs $3 or more, gain a Loot to your hand."
        self.coin = 1
        self.name = "Pickaxe"
        self.cost = 5
        self.required_cards = ["Loot"]

    def special(self, game, player):
        trashed = player.plr_trash_card(num=1, printcost=True)
        if trashed and player.card_cost(trashed[0]) >= 3:
            player.gain_card("Loot")


###############################################################################
class Test_Pickaxe(unittest.TestCase):
    """Test Pickaxe"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Pickaxe"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Pickaxe")

    def test_gain_card(self):
        """Gain a card"""
        self.plr.piles[Piles.HAND].set("Copper", "Gold", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.test_input = ["Trash Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), coins + 1)
        found = any([True for _ in self.plr.piles[Piles.DISCARD] if _.isLoot()])
        self.assertTrue(found)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
