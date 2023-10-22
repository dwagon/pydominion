#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Huntingparty(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = """+1 Card +1 Action. Reveal your hand.
            Reveal cards from your deck until you reveal a card that isn't a
            duplicate of one in your hand. Put it into your hand and discard the rest."""
        self.name = "Hunting Party"
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        discards = []
        for card in player.piles[Piles.HAND]:
            player.reveal_card(card)
        while True:
            card = player.next_card()
            player.reveal_card(card)
            if not card:
                player.output("No more cards")
                break
            if player.piles[Piles.HAND][card.name]:
                player.output(f"Discarding {card.name}")
                discards.append(card)
                continue
            player.output(f"Picked up a {card.name}")
            player.add_card(card, Piles.HAND)
            break
        for card in discards:
            player.discard_card(card)


###############################################################################
class Test_Huntingparty(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Hunting Party"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Hunting Party")
        self.plr.piles[Piles.HAND].set("Silver", "Gold")

    def test_playcard(self):
        """Play a hunting party"""
        self.plr.piles[Piles.DECK].set("Copper", "Province", "Silver", "Gold", "Duchy")
        self.plr.piles[Piles.HAND].set("Gold", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Duchy", self.plr.piles[Piles.HAND])
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        # Original Hand of 2 + 1 card and 1 non-dupl picked up
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
