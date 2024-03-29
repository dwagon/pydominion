#!/usr/bin/env python

import unittest
from typing import Optional, Any

from dominion import Card, Game, Piles, Player, NoCardException, OptionKeys


###############################################################################
class Card_Deathcart(Card.Card):
    """Death Cart"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LOOTER]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """You may trash this or an Action card from your hand, for +5 Coin.
            When you gain this, gain 2 Ruins."""
        self.name = "Death Cart"
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        action_cards = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        choices = [
            ("Trash this Death Cart for 5 Gold", "trash_dc"),
        ]
        if action_cards:
            choices.append(("Trash an Action card for 5 Gold", "trash_action"))
        else:
            choices.append(("No action cards to trash", "nothing"))
        choices.append(("Do nothing", "nothing"))
        ans = player.plr_choose_options("What to do with Death Cart?", *choices)
        trash: Optional[bool] = None
        if ans == "nothing":
            return
        if ans == "trash_action":
            trash = player.plr_trash_card(cardsrc=action_cards)
        if ans == "trash_dc":
            player.output("Trashing Death Cart")
            player.trash_card(self)
            trash = True
        if trash:
            player.coins.add(5)

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, Any]:
        for _ in range(2):
            try:
                if card := player.gain_card("Ruins"):
                    player.output(f"Gained {card}")
            except NoCardException:
                player.output("No more Ruins")
                break
        return {}


###############################################################################
class Test_Deathcart(unittest.TestCase):
    """Test Death Cart"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Death Cart", "Moat"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Death Cart")

    def test_play(self) -> None:
        """Play a death cart - no actions"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Do nothing"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertNotIn("Death Cart", self.g.trash_pile)

    def test_play_trash_action(self) -> None:
        """Play a death cart - no actions"""
        self.plr.piles[Piles.HAND].set("Copper", "Moat")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash an Action", "Trash Moat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 5)
        self.assertIn("Moat", self.g.trash_pile)
        self.assertNotIn("Death Cart", self.g.trash_pile)

    def test_play_trash_self(self) -> None:
        """Play a death cart - no actions"""
        self.plr.piles[Piles.HAND].set("Copper", "Moat")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash this Death"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 5)
        self.assertNotIn("Moat", self.g.trash_pile)
        self.assertIn("Death Cart", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
