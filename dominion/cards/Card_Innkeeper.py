#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Innkeeper """

import unittest
from dominion import Card, Game, Piles, NoCardException


###############################################################################
class Card_Innkeeper(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALLIES
        self.name = "Innkeeper"
        self.desc = """+1 Action; Choose one: +1 Card;
            or +3 Cards, then discard 3 cards; or +5 Cards, then discard 6 cards."""
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        choice = player.plr_choose_options(
            "Choose one",
            ("+1 Card", "one"),
            ("+3 Cards then discard 3", "three"),
            ("+5 Cards then discard 6", "five"),
        )
        if choice == "one":
            player.pickup_cards(1)
        elif choice == "three":
            player.pickup_cards(3)
            player.plr_discard_cards(3, force=True)
        elif choice == "five":
            player.pickup_cards(5)
            player.plr_discard_cards(6, force=True)


###############################################################################
class Test_Innkeeper(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Innkeeper"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Innkeeper")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_one(self):
        """Play the card to gain one card"""
        hndsize = self.plr.piles[Piles.HAND].size()
        self.plr.test_input = ["+1 Card"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hndsize + 1 - 1)

    def test_play_three(self):
        """Play the card to gain three cards"""
        self.plr.piles[Piles.DECK].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.HAND].set(
            "Copper", "Silver", "Gold", "Estate", "Duchy", "Province"
        )
        self.plr.add_card(self.card, Piles.HAND)
        hndsize = self.plr.piles[Piles.HAND].size()
        self.plr.test_input = [
            "+3 Cards",
            "Discard Estate",
            "Discard Duchy",
            "Discard Province",
            "Finish",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hndsize + 3 - 1 - 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
