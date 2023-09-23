#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Talisman(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+1 coin. Gain copy of non-victory cards you buy"
        self.name = "Talisman"
        self.playable = False
        self.cost = 4
        self.coin = 1

    def hook_buy_card(self, game, player, card):
        """While this is in play, when you buy a card costing 4
        or less that is not a victory card, gain a copy of it."""
        if card.cost <= 4 and not card.isVictory():
            player.output(f"Gained another {card} from Talisman")
            player.add_card(game.get_card_from_pile(card.name))


###############################################################################
class TestTalisman(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, initcards=["Talisman"], oldcards=True, badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Talisman")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_buy(self):
        self.plr.play_card(self.card)
        self.plr.buy_card("Copper")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Copper")

    def test_too_expensive(self):
        self.plr.play_card(self.card)
        self.plr.coins.set(6)
        self.plr.buy_card("Gold")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Gold")

    def test_victory(self):
        self.plr.play_card(self.card)
        self.plr.coins.set(6)
        self.plr.buy_card("Duchy")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Duchy")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
