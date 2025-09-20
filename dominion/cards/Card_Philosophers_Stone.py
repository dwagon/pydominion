#!/usr/bin/env python

import unittest

from dominion import Game, Piles, Card, Player


###############################################################################
class Card_Philosophers_Stone(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = """When you play this, count your deck and discard pile.
                Worth 1 Coin per 5 cards total between them (rounded down)"""
        self.name = "Philosopher's Stone"
        self.cost = 3
        self.required_cards = ["Potion"]
        self.potcost = True

    def hook_coinvalue(self, game: "Game.Game", player: "Player.Player") -> int:
        """When you play this, count your deck and discard pile.
        Worth 1 per 5 cards total between them (rounded down)"""
        num_cards = player.piles[Piles.DECK].size() + player.piles[Piles.DISCARD].size()
        extra_coin = num_cards / 5
        player.output(f"Gained {extra_coin} coins from Philosopher's Stone")
        return int(extra_coin)


###############################################################################
class Test_Philosophers_Stone(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Philosopher's Stone"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Philosopher's Stone")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a philosophers stone with not much on"""
        self.plr.piles[Piles.DECK].set("Estate")
        self.plr.piles[Piles.DISCARD].set("Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 0)

    def test_play_value(self):
        """Play a philosophers stone with the full Nicholas Flamel"""
        self.plr.piles[Piles.DECK].set("Estate", "Estate", "Estate", "Estate", "Silver")
        self.plr.piles[Piles.DISCARD].set("Estate", "Estate", "Estate", "Estate", "Silver")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
