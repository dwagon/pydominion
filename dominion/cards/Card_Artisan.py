#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Artisan(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Gain a card to your hand costing up to 5 Coin. Put a card from your hand onto your deck."
        self.name = "Artisan"
        self.cost = 6

    def special(self, game, player):
        player.plr_gain_card(5, destination=Piles.HAND)
        card = player.card_sel(
            force=True,
            cardsrc=Piles.HAND,
            prompt="Put a card from your hand on top of your deck",
        )
        player.move_card(card[0], "topdeck")


###############################################################################
class Test_Artisan(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Artisan", "Festival"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Artisan")

    def test_play(self):
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Silver", "Gold", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Get Festival", "Select Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Gold")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
