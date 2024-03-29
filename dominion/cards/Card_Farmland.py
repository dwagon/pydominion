#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Farmland(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.VICTORY
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """2VP; When you buy this, trash a card from your hand.
            Gain a card costing exactly 2 more than the trashed card."""
        self.name = "Farmland"
        self.cost = 6
        self.victory = 2

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        if card := player.plr_trash_card(force=True):
            player.plr_gain_card(cost=card[0].cost + 2, modifier="equal")
        return {}


###############################################################################
class TestFarmland(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Farmland", "Militia"],
            badcards=["Death Cart", "Cemetery", "Blessed Village"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Farmland")

    def test_gain(self) -> None:
        """Gain a farmland"""
        try:
            trash_size = self.g.trash_pile.size()
            self.plr.piles[Piles.HAND].set("Estate", "Duchy")
            self.plr.test_input = ["Trash Estate", "Get Militia"]
            self.plr.gain_card("Farmland")
            self.assertEqual(self.g.trash_pile.size(), trash_size + 1)
            self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
            # 1 for farmland, 1 for gained card
            self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        except (AssertionError, IOError):  # pragma: no cover
            self.g.print_state()
            raise

    def test_score(self) -> None:
        self.plr.piles[Piles.DECK].set("Farmland")
        sd = self.plr.get_score_details()
        self.assertEqual(sd["Farmland"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
