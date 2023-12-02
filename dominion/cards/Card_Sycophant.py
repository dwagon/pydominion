#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Sycophant(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.base = Card.CardExpansion.ALLIES
        self.name = "Sycophant"
        self.actions = 1
        self.desc = """+1 Action; Discard 3 cards. If you discarded at least one, +$3.
When you gain or trash this, +2 Favors."""
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        disc = player.plr_discard_cards(num=3, force=True)
        if disc:
            player.coins.add(3)

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        player.favors.add(2)
        return {}

    def hook_trash_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        player.favors.add(2)
        return {}


###############################################################################
class Test_Sycophant(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Sycophant"],
            ally="Plateau Shepherds",
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Sycophant")

    def test_gain(self) -> None:
        """Gain the card"""
        favs = self.plr.favors.get()
        self.plr.gain_card("Sycophant")
        self.assertEqual(self.plr.favors.get(), favs + 2)

    def test_trash(self) -> None:
        """Test trashing the card"""
        self.plr.add_card(self.card, Piles.HAND)
        favs = self.plr.favors.get()
        self.plr.trash_card(self.card)
        self.assertEqual(self.plr.favors.get(), favs + 2)

    def test_play(self) -> None:
        """Play the card"""
        favs = self.plr.favors.get()
        coin = self.plr.coins.get()
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Province", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = [
            "Discard Estate",
            "Discard Duchy",
            "Discard Province",
            "Finish",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.favors.get(), favs)
        self.assertEqual(self.plr.coins.get(), coin + 3)
        self.assertNotIn("Province", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
