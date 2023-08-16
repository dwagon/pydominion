#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Mandarin(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.name = "Mandarin"
        self.coin = 3
        self.cost = 5

    def desc(self, player):
        if player.phase == "buy":
            return """+3 Coins. Put a card from your hand on top of your deck.
            When you gain this, put all Treasures you have in play on top of your deck in any order."""
        return "+3 Coins. Put a card from your hand on top of your deck."

    def special(self, game, player):
        card = player.card_sel(
            force=True,
            cardsrc=Piles.HAND,
            prompt="Put a card from your hand on top of your deck",
        )
        player.move_card(card[0], "topdeck")

    def hook_gain_this_card(self, game, player):
        for card in player.piles[Piles.PLAYED]:
            if card.isTreasure():
                player.output(f"Putting {card.name} on to deck")
                player.move_card(card, "topdeck")
        return {}


###############################################################################
class Test_Mandarin(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Mandarin"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Mandarin"].remove()

    def test_play(self):
        """Play the card"""
        self.plr.piles[Piles.HAND].set("Gold", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")

    def test_gain(self):
        """Gain the card"""
        self.plr.piles[Piles.PLAYED].set("Gold", "Duchy")
        self.plr.gain_card("Mandarin")
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")
        self.assertIn("Duchy", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
