#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player, PlayArea


###############################################################################
class Card_Soldier(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.TRAVELLER,
        ]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """+2 Coins; +1 Coin per other Attack you have in play.
        Each other player with 4 or more cards in hand discards a card."""
        self.name = "Soldier"
        self.purchasable = False
        self.coin = 2
        self.cost = 3
        self.numcards = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """+2 Coins; +1 Coin per other Attack you have in play.
        Each other player with 4 or more cards in hand discards a card."""
        count = 0
        for c in player.piles[Piles.PLAYED]:
            if c == self:
                continue
            if c.isAttack():
                count += 1
        player.coins.add(count)
        player.output(f"Gained {count} extra coins")
        for plr in player.attack_victims():
            if plr.piles[Piles.HAND].size() >= 4:
                plr.output(f"{player}'s Soldier: Discard a card")
                plr.plr_discard_cards(force=True)

    def hook_discard_this_card(self, game: Game.Game, player: Player.Player, source: PlayArea.PlayArea) -> None:
        """Replace with Hero"""
        player.replace_traveller(self, "Fugitive")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(1)


###############################################################################
class TestSoldier(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=2, initcards=["Peasant", "Militia"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Soldier")
        self.plr.add_card(self.card, Piles.HAND)

    def test_soldier(self) -> None:
        """Play a soldier with no extra attacks"""
        self.vic.piles[Piles.HAND].set("Copper")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_soldier_more(self) -> None:
        """Play a soldier with no extra attacks"""
        self.vic.piles[Piles.HAND].set("Copper")
        mil = self.g.get_card_from_pile("Militia")
        self.plr.add_card(mil, Piles.PLAYED)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3)

    def test_soldier_attack(self) -> None:
        """Play a soldier with more than 4 cards"""
        self.vic.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate", "Duchy")
        self.vic.test_input = ["Gold"]
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.vic.piles[Piles.DISCARD])
        self.assertNotIn("Gold", self.vic.piles[Piles.HAND])
        self.assertEqual(self.vic.piles[Piles.HAND].size(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
