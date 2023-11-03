#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, NoCardException


###############################################################################
class Card_Cartographer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """+1 Card; +1 Action; Look at the top 4 cards of your deck.
            Discard any number of them. Put the rest back on top in any order."""
        self.name = "Cartographer"
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        cards: list[Card.Card] = []
        for _ in range(4):
            try:
                cards.append(player.next_card())
            except NoCardException:
                break
        to_discard = player.plr_discard_cards(
            prompt="Discard any number and the rest go back on the top of the deck",
            any_number=True,
            cardsrc=cards,
        )
        for card in cards:
            if card not in to_discard:
                player.add_card(card, "topdeck")


###############################################################################
class Test_Cartographer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cartographer"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Cartographer")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.piles[Piles.DECK].set("Silver", "Gold", "Province", "Duchy", "Copper")
        self.plr.test_input = ["Province", "Duchy", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Silver", self.plr.piles[Piles.DECK])
        self.assertIn("Gold", self.plr.piles[Piles.DECK])
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
