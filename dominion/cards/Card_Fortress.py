#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Fortress(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 Card; +2 Actions. When you trash this, put it into your hand."""
        self.name = "Fortress"
        self.cards = 1
        self.actions = 2
        self.cost = 4

    def hook_trash_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        player.output("Putting Fortress back in hand")
        if not self.location:
            player.add_card(self, Piles.HAND)
        else:
            player.move_card(self, Piles.HAND)
        return {OptionKeys.TRASH: False}


###############################################################################
class TestFortress(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Fortress"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Fortress")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play the card"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_trash(self) -> None:
        self.plr.trash_card(self.card)
        self.assertIn("Fortress", self.plr.piles[Piles.HAND])
        self.assertNotIn("Fortress", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
