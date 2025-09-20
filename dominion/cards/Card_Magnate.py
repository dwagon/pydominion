#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Magnate"""

import unittest

from dominion import Card, Game, Piles


###############################################################################
class Card_Magnate(Card.Card):
    """Magnate"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "Reveal your hand. +1 Card per Treasure in it."
        self.name = "Magnate"
        self.cost = 5

    def special(self, game, player):
        cards = 0
        for crd in player.piles[Piles.HAND]:
            player.reveal_card(crd)
            if crd.isTreasure():
                cards += 1
        if cards:
            player.output(f"Picking up {cards} cards")
            player.pickup_cards(cards)


###############################################################################
class Test_Magnate(unittest.TestCase):
    """Test Magnate"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Magnate"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Magnate")

    def test_play_card(self):
        """Play Magnate"""
        self.plr.piles[Piles.HAND].set("Copper", "Gold", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        orig = self.plr.piles[Piles.HAND].size()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), orig + 2 - 1)  # 2 for magnate, -1 for played


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
