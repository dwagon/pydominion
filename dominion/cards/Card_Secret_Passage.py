#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_SecretPassage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """+2 Cards; +1 Action; Take a card from your hand and put it anywhere in your deck."""
        self.name = "Secret Passage"
        self.cost = 4
        self.actions = 1
        self.cards = 2

    def special(self, game, player):
        if card := player.card_sel(prompt="Take a card from your hand and put into your deck", cardsrc=Piles.HAND):
            dest = player.plr_choose_options(
                f"Put {card[0].name} into top or bottom of deck",
                ("Top of deck", "topdeck"),
                ("Bottom of deck", "deck"),
            )
            player.add_card(card[0], dest)
            player.piles[Piles.HAND].remove(card[0])


###############################################################################
class Test_SecretPassage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Secret Passage", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Secret Passage")

    def test_play(self):
        """Play an Secret Passage"""
        self.plr.piles[Piles.HAND].set("Gold", "Province", "Duchy", "Copper", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Select Province", "Bottom"]
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.plr.actions.get(), 1)
            self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2 - 1)  # Hand + SP - back on deck
            self.assertEqual(self.plr.piles[Piles.DECK][0].name, "Province")
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
