#!/usr/bin/env python

import contextlib
import unittest

from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Shepherd(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = (
            "+1 action; Discard any number of victory cards +2 cards per card discarded"
        )
        self.name = "Shepherd"
        self.cost = 4
        self.actions = 1
        self.heirloom = "Pasture"

    def special(self, game: Game.Game, player: Player.Player) -> None:
        num_victories = sum(1 for _ in player.piles[Piles.HAND] if _.isVictory())
        if num_victories == 0:
            return
        to_discard = player.plr_discard_cards(
            num=0, any_number=True, types={Card.CardType.VICTORY: True}
        )
        if not to_discard:
            return
        with contextlib.suppress(NoCardException):
            player.pickup_cards(2 * len(to_discard))


###############################################################################
class TestShepherd(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Shepherd"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Shepherd")

    def test_play(self) -> None:
        """Play a Shepherd"""
        self.plr.piles[Piles.HAND].set("Estate", "Province", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Estate", "Duchy", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
