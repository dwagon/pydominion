#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Way_of_the_Butterfly """

import unittest
from typing import Optional, Any

from dominion import Card, Game, Way, Piles, Player, OptionKeys


###############################################################################
class Way_Butterfly(Way.Way):
    def __init__(self) -> None:
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "You may return this to its pile to gain a card costing exactly $1 more than it."
        self.name = "Way of the Butterfly"

    def special_way(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> Optional[dict[OptionKeys, Any]]:
        player.move_card(card, Piles.CARDPILE)
        cst = player.card_cost(card)
        player.plr_gain_card(cst + 1, "equal")
        return {OptionKeys.DISCARD: False}


###############################################################################
class TestButterfly(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            ways=["Way of the Butterfly"],
            initcards=["Moat", "Witch"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Moat")
        self.way = self.g.ways["Way of the Butterfly"]

    def test_play(self) -> None:
        """Perform a Butterfly"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Get Witch"]
        self.plr.perform_way(self.way, self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Witch"])
        self.assertEqual(len(self.g.card_piles["Moat"]), 10)
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
