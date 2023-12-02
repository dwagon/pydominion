#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Player, NoCardException, OptionKeys


###############################################################################
class Card_Duchy(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.VICTORY
        self.base = Card.CardExpansion.DOMINION
        self.desc = "3 VP"
        self.playable = False
        self.basecard = True
        self.name = "Duchy"
        self.cost = 5
        self.victory = 3

    @classmethod
    def calc_numcards(cls, game: Game.Game) -> int:
        return 8 if game.numplayers == 2 else 12

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, Any]:
        if "Duchess" in game.card_piles:
            if player.plr_choose_options(
                "Gain a Duchess as well?",
                ("No thanks", False),
                ("Gain Duchess", True),
            ):
                try:
                    player.gain_card("Duchess")
                except NoCardException:
                    player.output("No more Duchess")
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return False  # Don't gain a duchess


###############################################################################
class Test_Duchy(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Duchy")

    def test_have(self) -> None:
        self.plr.add_card(self.card)
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Duchy"], 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
