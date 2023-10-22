#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Navigator(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+2 coin. Look at the top 5 cards of your deck.
            Either discard all of them, or put them back on top of your deck
            in any order"""
        self.name = "Navigator"
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        cards = []
        for _ in range(5):
            cards.append(player.next_card())
        player.output("Top 5 cards on the deck are: %s" % ", ".join([c.name for c in cards]))
        discard = player.plr_choose_options(
            "What do you want to do?",
            ("Discard cards", True),
            ("Return them to the deck", False),
        )
        if discard:
            for c in cards:
                player.discard_card(c)
        else:
            for c in cards:
                player.add_card(c, "topdeck")


###############################################################################
class Test_Navigator(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Navigator"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.navigator = self.g.get_card_from_pile("Navigator")
        self.plr.add_card(self.navigator, Piles.HAND)

    def test_discard(self):
        self.plr.piles[Piles.DECK].set("Copper", "Estate", "Gold", "Province", "Silver", "Duchy")
        self.plr.test_input = ["discard"]
        self.plr.play_card(self.navigator)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 5)
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 1)

    def test_keep(self):
        self.plr.piles[Piles.DECK].set("Copper", "Estate", "Gold", "Province", "Silver", "Duchy")
        self.plr.test_input = ["return"]
        self.plr.play_card(self.navigator)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
