#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Sibyl(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.AUGUR]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 6
        self.name = "Sibyl"
        self.cards = 4
        self.actions = 1
        self.desc = """+4 Cards; +1 Action;
            Put a card from your hand on top of your deck, and another on the bottom."""
        self.pile = "Augurs"

    def special(self, game, player):
        tcard = player.card_sel(
            prompt="Put a card from your hand on top of your deck",
            cardsrc=player.piles[Piles.HAND],
        )
        player.move_card(tcard[0], "topdeck")

        bcard = player.card_sel(
            prompt="Put a card from your hand on bottom of your deck",
            cardsrc=player.piles[Piles.HAND],
        )
        player.move_card(bcard[0], Piles.DECK)


###############################################################################
class TestSibyl(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Augurs"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

        while True:
            card = self.g.get_card_from_pile("Augurs")
            if card.name == "Sibyl":
                break
        self.card = card

    def test_play(self):
        """Play a Sibyl"""
        self.plr.piles[Piles.HAND].set("Gold", "Silver", "Duchy", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Select Gold", "Select Silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DECK].top_card().name, "Gold")
        self.assertIn("Silver", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
