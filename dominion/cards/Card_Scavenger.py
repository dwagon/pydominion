#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Scavenger(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+2 Coin. You may put your deck into your discard pile.
            Look through your discard pile and put one card from it on top of
            your deck."""
        self.name = "Scavenger"
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        dumpdeck = player.plr_choose_options(
            "Put your deck into your discard pile?",
            ("Keep it where it is", False),
            ("Put deck into discard?", True),
        )
        if dumpdeck:
            for card in player.piles[Piles.DECK]:
                player.add_card(card, "discard")
                player.piles[Piles.DECK].remove(card)
        if player.piles[Piles.DISCARD].size():
            cards = []
            cardnames = set()
            for c in player.piles[Piles.DISCARD]:
                if c.name not in cardnames:
                    cards.append(c)
                    cardnames.add(c.name)
            card = player.card_sel(
                force=True,
                cardsrc=cards,
                prompt="Pull card from discard and add to top of your deck",
            )
            player.add_card(card[0], "topdeck")
            player.piles[Piles.DISCARD].remove(card[0])


###############################################################################
class Test_Scavenger(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Scavenger", "Moat", "Witch"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Scavenger"].remove()

    def test_play(self):
        """Play a scheme"""
        self.plr.piles[Piles.DECK].set("Province", "Moat", "Witch", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Put", "Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Moat")
        self.assertIn("Witch", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
