#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Innkeeper """

import unittest
from dominion import Card, Game


###############################################################################
class Card_Innkeeper(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ALLIES
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
            player.pickup_card()
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
        self.card = self.g["Innkeeper"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_one(self):
        """Play the card to gain one card"""
        hndsize = self.plr.hand.size()
        self.plr.test_input = ["+1 Card"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), hndsize + 1 - 1)

    def test_play_three(self):
        """Play the card to gain three cards"""
        self.plr.deck.set("Copper", "Silver", "Gold")
        self.plr.hand.set("Copper", "Silver", "Gold", "Estate", "Duchy", "Province")
        self.plr.add_card(self.card, "hand")
        hndsize = self.plr.hand.size()
        self.plr.test_input = [
            "+3 Cards",
            "Discard Estate",
            "Discard Duchy",
            "Discard Province",
            "Finish",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), hndsize + 3 - 1 - 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
