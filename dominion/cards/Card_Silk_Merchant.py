#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_SilkMerchant(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """+2 Cards; +1 Buy; When you gain or trash this, +1 Coffers and +1 Villager."""
        self.name = "Silk Merchant"
        self.cards = 2
        self.cost = 4

    ###########################################################################
    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        player.villagers.add(1)
        player.coffers.add(1)
        return {}

    ###########################################################################
    def hook_trash_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        player.villagers.add(1)
        player.coffers.add(1)
        return {}


###############################################################################
class Test_SilkMerchant(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Silk Merchant"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Silk Merchant")
        self.plr.piles[Piles.HAND].set()

    def test_gain_card(self) -> None:
        self.plr.coffers.set(0)
        self.plr.gain_card("Silk Merchant")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 0)
        self.assertEqual(self.plr.villagers.get(), 1)
        self.assertEqual(self.plr.coffers.get(), 1)

    def test_trash_card(self) -> None:
        self.plr.coffers.set(0)
        self.plr.trash_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 0)
        self.assertEqual(self.plr.villagers.get(), 1)
        self.assertEqual(self.plr.coffers.get(), 1)

    def test_play_card(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.coffers.set(0)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertEqual(self.plr.villagers.get(), 0)
        self.assertEqual(self.plr.coffers.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
