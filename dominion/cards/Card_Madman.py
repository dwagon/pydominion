#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Madman(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+2 Actions. Return this to the Madman pile. If you do, +1 Card per card in your hand."""
        self.name = "Madman"
        self.insupply = False
        self.actions = 2
        self.cost = 0
        self.purchasable = False

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        hand_size = player.piles[Piles.HAND].size()
        player.output(f"Gaining {hand_size} cards from madman")
        for _ in range(hand_size):
            player.pickup_cards(1)
        game.card_piles["Madman"].add(self)
        if self in player.piles[Piles.PLAYED]:
            player.piles[Piles.PLAYED].remove(self)


###############################################################################
class TestMadman(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Hermit"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Madman")

    def test_play(self) -> None:
        """Play a Madman"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 * 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
