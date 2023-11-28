#!/usr/bin/env python

import contextlib
import unittest
from typing import Optional, Any

from dominion import Card, Game, Piles, Player, NoCardException, OptionKeys


###############################################################################
class Card_Rats(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 Card, +1 Action, Gain a Rats.
            Trash a card from your hand other than a Rats (or reveal a hand of all Rats).
            When you trash this, +1 Card."""
        self.name = "Rats"
        self.numcards = 20
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Gain a Rats. Trash a card from your hand other than a Rats."""
        try:
            player.gain_card("Rats")
            player.output("Gained a Rays")
        except NoCardException:
            player.output("No more Rats")
        player.plr_trash_card(force=True, exclude=["Rats"])

    def hook_trash_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> Optional[dict[OptionKeys, Any]]:
        """When you trash this +1 Card"""
        with contextlib.suppress(NoCardException):
            player.pickup_card(verb="Due to trashing Rats picked up")
        return None


###############################################################################
class Test_Rats(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Rats"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.rats = self.g.get_card_from_pile("Rats")
        self.plr.piles[Piles.DECK].set("Estate", "Province", "Duchy")
        self.plr.piles[Piles.HAND].set("Copper", "Gold", "Silver", "Rats")
        self.plr.add_card(self.rats, Piles.HAND)

    def test_play(self) -> None:
        self.plr.test_input = ["trash copper"]
        self.plr.play_card(self.rats)
        self.assertIn("Copper", self.g.trash_pile)

    def test_trash_card(self) -> None:
        tsize = self.g.trash_pile.size()
        self.plr.test_input = ["trash copper"]
        self.plr.play_card(self.rats)
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertNotEqual(self.g.trash_pile[0].name, "Rats")

    def test_gain_rats(self) -> None:
        self.plr.test_input = ["trash copper"]
        self.plr.play_card(self.rats)
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Rats")

    def test_trash_rats(self) -> None:
        """Trashing Rats - gain another card"""
        handsize = self.plr.piles[Piles.HAND].size()
        self.plr.trash_card(self.rats)
        # Lose rats, gain another card
        self.assertEqual(self.plr.piles[Piles.HAND].size(), handsize)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
