#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Garrison(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.FORT,  # pylint: disable=no-member
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 4
        self.coin = 2
        self.name = "Garrison"
        self.desc = """+$2; This turn, when you gain a card, add a token here.
            At the start of your next turn, remove them for +1 Card each."""
        self._tokens = 0
        self.pile = "Forts"

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        self._tokens += 1
        return {}

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        if self._tokens:
            player.output(f"Picking up {self._tokens} cards from Garrison")
            player.pickup_cards(self._tokens)
            self._tokens = 0
        return {}


###############################################################################
class Test_arrison(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Forts"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        while True:
            self.card = self.g.get_card_from_pile("Forts")
            if self.card.name == "Garrison":
                break
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a garrison"""
        self.plr.test_input = ["Get Silver -"]
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)
        self.plr.gain_card("Estate")
        self.plr.gain_card("Copper")
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
