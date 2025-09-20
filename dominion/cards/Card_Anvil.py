#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Anvil"""

import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_Anvil(Card.Card):
    """Anvil"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "$1; You may discard a Treasure to gain a card costing up to $4."
        self.coin = 1
        self.name = "Anvil"
        self.cost = 3

    def special(self, game, player):
        treasures = [_ for _ in player.piles[Piles.HAND] if _.isTreasure()]
        if not treasures:
            return
        options = [("Do Nothing", None)]
        for treas in treasures:
            options.append((f"Discard {treas.name}?", treas))
        disc = player.plr_choose_options(
            "Discard a treasure to gain a card costing up to 4", *options
        )
        if disc:
            player.discard_card(disc)
            player.plr_gain_card(4)


###############################################################################
class Test_Anvil(unittest.TestCase):
    """Test Anvil"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Anvil", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Anvil")

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
