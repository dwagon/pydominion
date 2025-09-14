#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, OptionKeys, Player


###############################################################################
class Card_Outpost(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """You only draw 3 cards (instead of 5) in this turn's Clean-up phase.
        Take an extra turn after this one.
        This can't cause you to take more than two consecutive turns."""
        self.name = "Outpost"
        self.cost = 5

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        player.newhandsize = 3
        return {}

    def hook_end_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        if player.newhandsize == 3:
            player.output("Having a second turn due to Output")
            game.current_player = game.playerToRight(player)
        else:
            player.output("Already had one extra turn")


###############################################################################
class Test_Outpost(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Outpost"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Outpost")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play Outpost"""
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.g.print_state()
        # TODO - Not sure how to test this


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
