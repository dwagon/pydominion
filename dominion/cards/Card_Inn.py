#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Inn(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.name = "Inn"
        self.cards = 2
        self.actions = 2
        self.cost = 5

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return """+2 Cards, +2 Actions, Discard 2 cards.
            When you gain this, look through your discard pile
            (including this), reveal any number of Action cards
            from it, and shuffle them into your deck."""
        return "+2 Cards, +2 Actions, Discard 2 cards"

    def special(self, game, player):
        player.plr_discard_cards(num=2, force=True)

    def hook_gain_this_card(self, game, player):
        cards = []
        for card in player.piles[Piles.DISCARD]:
            if card.isAction():
                player.reveal_card(card)
                cards.append(card)
        cards.append(self)
        back = player.card_sel(
            anynum=True,
            prompt="Select cards to shuffle back into your deck",
            cardsrc=cards,
        )
        for card in back:
            if card.name == "Inn":
                return {"destination": "deck", "shuffle": True}
            player.piles[Piles.DISCARD].remove(card)
            player.add_card(card, "deck")
            player.piles[Piles.DECK].shuffle()
        return {}


###############################################################################
class Test_Inn(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Inn", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Inn"].remove()

    def test_play(self):
        """Play the card"""
        self.plr.piles[Piles.HAND].set("Duchy", "Province", "Gold", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Duchy", "Province", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4 + 2 - 2)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_gain(self):
        self.plr.piles[Piles.DISCARD].set("Moat", "Gold")
        self.plr.test_input = ["Moat", "finish"]
        self.plr.gain_card("Inn")
        self.assertIn("Moat", self.plr.piles[Piles.DECK])

    def test_gain_self(self):
        self.plr.piles[Piles.DISCARD].set()
        self.plr.test_input = ["Inn", "finish"]
        self.plr.gain_card("Inn")
        self.assertIn("Inn", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
