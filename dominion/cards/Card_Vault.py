#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Vault(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """+2 Cards; Discard any number of cards. +1 Coin per card
            discarded. Each other player may discard 2 cards. If he does, he
            draws a card."""
        self.name = "Vault"
        self.cards = 2
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if discards := player.plr_discard_cards(
            any_number=True,
            prompt="Discard any number of cards. +1 Coin per card discarded",
        ):
            player.coins.add(len(discards))
            player.output(f"Gaining {len(discards)} coins")

        for plr in game.player_list():
            if plr != player:
                plr.output(
                    f"Due to {player.name}'s Vault you may discard two cards. If you do, draw one"
                )
                if plr_discards := plr.plr_discard_cards(num=2):
                    if len(plr_discards) == 2:
                        plr.pickup_cards(1)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(2)


###############################################################################
class TestVault(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Vault"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g.get_card_from_pile("Vault")

    def test_play(self) -> None:
        self.other.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.piles[Piles.HAND].set("Duchy", "Province", "Gold", "Silver", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.other.test_input = ["Copper", "Silver", "Finish"]
        self.plr.test_input = ["Duchy", "Province", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2 - 2)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.other.piles[Piles.HAND].size(), 3 - 2 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
