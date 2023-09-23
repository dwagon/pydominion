#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Chancellor """

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Chancellor(Card.Card):
    """Chancellor"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "+2 Coin; You may immediately put your deck into your discard pile."
        self.name = "Chancellor"
        self.coin = 2
        self.cost = 3

    def special(self, game, player):  # pylint: disable=unused-argument
        """Chancellor Special"""
        disc = player.plr_choose_options(
            "Discard deck?", ("Don't Discard", False), ("Discard Deck", True)
        )
        if disc:
            for card in player.piles[Piles.DECK]:
                player.add_card(card, Piles.DISCARD)
                player.piles[Piles.DECK].remove(card)


###############################################################################
class Test_Chancellor(unittest.TestCase):
    """Test Chancellor"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Chancellor"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.ccard = self.g.get_card_from_pile("Chancellor")
        self.plr.piles[Piles.HAND].set("Estate")
        self.plr.add_card(self.ccard, Piles.HAND)

    def test_nodiscard(self):
        """Play Chancellor and choose not to discard"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.DISCARD].set("Estate", "Duchy", "Province")
        self.plr.test_input = ["Don't discard"]
        self.plr.play_card(self.ccard)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 3)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 3)

    def test_discard(self):
        """Play Chancellor and choose to discard deck"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.DISCARD].set("Estate", "Duchy", "Province")
        self.plr.test_input = ["discard deck"]
        self.plr.play_card(self.ccard)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 0)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
