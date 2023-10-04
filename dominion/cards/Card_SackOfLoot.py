#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Sack_of_Loot"""
import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_SackOfLoot(Card.Card):
    """Sack Of Loot"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """$1; +1 Buy; Gain a Loot."""
        self.name = "Sack Of Loot"
        self.cost = 6
        self.required_cards = ["Loot"]
        self.coin = 1
        self.buys = 1

    def special(self, game, player):
        player.gain_card("Loot")


###############################################################################
class Test_SackOfLoot(unittest.TestCase):
    """Test Sack Of Loot"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sack Of Loot"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Sack Of Loot")

    def test_play(self):
        """Play card"""
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        buys = self.plr.buys.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 1)
        self.assertEqual(self.plr.buys.get(), buys + 1)
        found = any([True for _ in self.plr.piles[Piles.DISCARD] if _.isLoot()])
        self.assertTrue(found)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
