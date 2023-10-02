#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Blacksmith(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.TOWNSFOLK]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 3
        self.name = "Blacksmith"
        self.desc = """Choose one: Draw until you have 6 cards in hand;
            or +2 Cards; or +1 Card and +1 Action."""
        self.pile = "Townsfolk"

    def special(self, game, player):
        opt = player.plr_choose_options(
            "Choose One: ",
            ("Draw until you have 6 cards in your hand", "draw"),
            ("+2 Cards", "cards"),
            ("+1 Card and +1 Action", "action"),
        )
        if opt == "draw":
            while player.piles[Piles.HAND].size() < 6:
                player.pickup_card()
        elif opt == "cards":
            player.pickup_cards(2)
        elif opt == "action":
            player.pickup_card()
            player.add_actions(1)


###############################################################################
class Test_Blacksmith(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Townsfolk"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        while True:
            self.card = self.g.get_card_from_pile("Townsfolk")
            if self.card.name == "Blacksmith":
                break
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_draw(self):
        self.plr.test_input = ["Draw"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)

    def test_play_cards(self):
        self.plr.test_input = ["2 Cards"]
        hndsze = self.plr.piles[Piles.HAND].size()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hndsze + 2 - 1)

    def test_play_action(self):
        self.plr.test_input = ["Action"]
        hndsze = self.plr.piles[Piles.HAND].size()
        acts = self.plr.actions.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), hndsze + 1 - 1)
        self.assertEqual(self.plr.actions.get(), acts + 1 - 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
