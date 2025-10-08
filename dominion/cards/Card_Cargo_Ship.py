#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Cargo_Ship"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys, PlayArea


###############################################################################
class Card_CargoShip(Card.Card):
    """Cargo Ship"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.RENAISSANCE
        self.name = "Cargo Ship"
        self.desc = """+2 Coin; Once this turn, when you gain a card, you may
            set it aside face up (on this). At the start of your next turn,
            put it into your hand."""
        self.cost = 3
        self.coin = 2

    ###########################################################################
    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if self.location != Piles.DURATION:  # Only works if played this turn
            return {}
        if card.location == Piles.SPECIAL:  # Card already moved
            return {}
        if not player.has_done_once(self.uuid):
            if player.plr_choose_options(
                f"Do you want to set {card} aside to play next turn?", ("No", False), ("Yes", True)
            ):
                player.do_once(self.uuid)
                player.specials[self.uuid] = PlayArea.PlayArea(f"Cargo Ship {self.uuid}", initial=[])
                player.secret_count += 1
                return {OptionKeys.DESTINATION: player.specials[self.uuid]}
        return {}

    ###########################################################################
    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        if self.uuid in player.specials:
            for card in player.specials[self.uuid]:
                player.move_card(card, Piles.HAND)
                player.secret_count -= 1
                player.output(f"Moving {card} out of {self}")
            del player.specials[self.uuid]
        return {}

    ###########################################################################
    def debug_dump(self, player: Player.Player) -> None:  # pragma: no coverage
        if self.uuid in player.specials:
            player.output(f"{self}: {player.specials[self.uuid]}")


###############################################################################
class TestCargoShip(unittest.TestCase):
    """Test Cargo Ship"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Cargo Ship", "Moat"], badcards=["Shaman"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Cargo Ship")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card_yes(self) -> None:
        """Play card and set it aside"""
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)
        self.plr.test_input = ["Yes"]
        self.plr.buy_card("Moat")
        self.assertEqual(self.plr.specials[self.card.uuid][0].name, "Moat")
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Moat", self.plr.piles[Piles.HAND])

    def test_play_card_no(self) -> None:
        """Play card and don't set it aside"""
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)
        self.plr.test_input = ["No"]
        self.plr.buy_card("Moat")
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 5)

    def test_play_cargo_twice(self) -> None:
        """If we have two cargo ships active at the same time we shouldn't be able to set aside a card twice"""
        self.plr.add_actions(2)
        self.plr.test_input = ["Yes", "Yes"]
        self.plr.play_card(self.card)
        card2 = self.g.get_card_from_pile("Cargo Ship")
        self.plr.add_card(card2, Piles.HAND)
        self.assertNotIn(self.card.uuid, self.plr.specials)
        self.assertNotIn(card2.uuid, self.plr.specials)
        self.plr.play_card(card2)
        self.plr.buy_card("Moat")
        # Only one cargo ship should have the moat
        self.assertEqual(len(self.plr.specials[self.card.uuid]) + len(self.plr.specials[card2.uuid]), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
