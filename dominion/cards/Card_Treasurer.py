#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Treasurer(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.name = "Treasurer"
        self.desc = """+3 Coin; Choose one: Trash a Treasure from your hand;
                or gain a Treasure from the trash to your hand; or take the Key."""
        self.cost = 5
        self.coin = 3
        self.needsartifacts = True

    ###########################################################################
    def special(self, game: Game.Game, player: Player.Player) -> None:
        gain_treas = [_ for _ in game.trash_pile if _.isTreasure()]
        choice = player.plr_choose_options(
            "Choose one?",
            ("Trash a treasure from your hand", "trash"),
            (
                f"Gain a treasure from the trash ({len(gain_treas)} available)",
                "gain",
            ),
            ("Take the key", "key"),
        )
        if choice == "trash":
            treas = [_ for _ in player.piles[Piles.HAND] if _.isTreasure()]
            player.plr_trash_card(cardsrc=treas)
        elif choice == "gain":
            if card := player.card_sel(cardsrc=gain_treas, prompt="Select Treasure from the Trash"):
                game.trash_pile.remove(card[0])
                player.add_card(card[0], Piles.HAND)
        elif choice == "key":
            player.assign_artifact("Key")


###############################################################################
class TestTreasurer(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Treasurer"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.plr.piles[Piles.HAND].set("Copper", "Silver")
        self.card = self.g.get_card_from_pile("Treasurer")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_trash(self) -> None:
        self.plr.test_input = ["Trash a treasure", "Silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertIn("Silver", self.g.trash_pile)

    def test_play_recover(self) -> None:
        self.g.trash_pile.set("Gold", "Estate")
        self.plr.test_input = ["Gain a treasure", "Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertNotIn("Gold", self.g.trash_pile)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])

    def test_play_key(self) -> None:
        self.plr.test_input = ["Take the key"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertIsNotNone(self.plr.has_artifact("Key"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
